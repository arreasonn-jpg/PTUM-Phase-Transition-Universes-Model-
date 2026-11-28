#!/usr/bin/env python3
"""Inventory a bundled CLASS/Cobaya archive without extracting untrusted paths.

This is a provenance and completeness audit only. It does not apply a patch,
build CLASS, run Cobaya, or independently reproduce any posterior.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any


MAX_MEMBERS = 10000
MAX_MEMBER_BYTES = 32 * 1024 * 1024
MAX_TOTAL_READ_BYTES = 256 * 1024 * 1024
MAX_NESTED_DEPTH = 2
COMMIT_RE = re.compile(r"\b[0-9a-f]{40}\b", re.IGNORECASE)
DATA_SUFFIXES = {".fits", ".fit", ".dat", ".txt", ".gz", ".h5", ".hdf5", ".clik", ".npy", ".npz", ".csv"}
CHAIN_SUFFIXES = {".txt", ".dat", ".chain", ".chains", ".h5", ".hdf5", ".fits", ".csv", ".gz"}
LOCK_NAMES = {
    "requirements.txt", "environment.yml", "environment.yaml",
    "conda-lock.yml", "conda-lock.yaml", "poetry.lock", "uv.lock",
    "pipfile.lock", "pyproject.toml",
}
LIKELIHOOD_TOKENS = (
    "planck", "plik", "clik", "bao", "pantheon", "supernova",
    "likelihood", "boss", "des", "sn_data", "highl", "lowl",
)
CHAIN_TOKENS = ("chain", "mcmc", "posterior", "samples", "getdist", "paramnames", "covmat")
CLASS_SOURCE_NAMES = {
    "background.c", "thermodynamics.c", "perturbations.c", "primordial.c",
    "transfer.c", "spectra.c", "nonlinear.c", "input.c", "parser.c",
}


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _normal_name(name: str) -> str:
    return name.replace("\\", "/").lstrip("./")


def _decode(data: bytes, limit: int = 1_000_000) -> str:
    return data[:limit].decode("utf-8", errors="replace")


def _is_patch(name: str, data: bytes) -> tuple[bool, bool]:
    lower = name.lower()
    suffix = PurePosixPath(lower).suffix
    text = _decode(data, 128_000)
    signature = "diff --git " in text or ("--- " in text and "+++ " in text)
    candidate = suffix in {".patch", ".diff"} or "patch" in PurePosixPath(lower).name
    return candidate, bool(candidate and signature)


def _is_cobaya_config(name: str, data: bytes) -> tuple[bool, bool]:
    lower = name.lower()
    if PurePosixPath(lower).suffix not in {".yaml", ".yml"}:
        return False, False
    text = _decode(data, 128_000).lower()
    candidate = (
        "cobaya" in lower
        or ("theory:" in text and "likelihood:" in text and "sampler:" in text)
    )
    return bool(candidate), bool(candidate and "theory:" in text and "likelihood:" in text and "sampler:" in text)


def _is_pinned_lock(name: str, data: bytes) -> tuple[bool, bool]:
    base = PurePosixPath(name.lower()).name
    if base not in LOCK_NAMES and not base.startswith("requirements-"):
        return False, False
    text = _decode(data, 256_000)
    non_comment = [
        line.strip() for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith(("#", ";"))
    ]
    if base in {"requirements.txt"} or base.startswith("requirements-"):
        pinned = bool(non_comment) and all(
            "==" in line or "@ " in line or "--hash=sha256:" in line
            for line in non_comment
        )
    else:
        pinned = any(
            token in text.lower()
            for token in ("lock-version", "content-hash", "sha256", "==")
        )
    return True, bool(pinned)


def _entry_record(name: str, data: bytes) -> dict[str, Any]:
    lower = name.lower()
    base = PurePosixPath(lower).name
    suffix = PurePosixPath(lower).suffix
    patch_candidate, patch_signature = _is_patch(name, data)
    config_candidate, config_complete = _is_cobaya_config(name, data)
    lock_candidate, lock_pinned = _is_pinned_lock(name, data)
    text = _decode(data, 1_000_000)
    commit_hashes = sorted(set(COMMIT_RE.findall(text)))
    chain_candidate = (
        any(token in lower for token in CHAIN_TOKENS)
        and suffix in CHAIN_SUFFIXES
    )
    likelihood_candidate = (
        any(token in lower for token in LIKELIHOOD_TOKENS)
        and suffix in DATA_SUFFIXES
    )
    raw_data_candidate = (
        any(part in {"data", "datasets", "likelihood_data"} for part in PurePosixPath(lower).parts[:-1])
        and suffix in DATA_SUFFIXES
    )
    class_source_candidate = (
        "class" in lower
        and (suffix in {".c", ".h", ".cpp", ".hpp", ".f90", ".py"} or base in CLASS_SOURCE_NAMES)
    )
    commit_metadata_candidate = (
        ("class" in lower or "commit" in lower or base in {"readme", "readme.md", "manifest.txt"})
        and bool(commit_hashes)
    )
    nested_archive_candidate = suffix in {".zip", ".tgz", ".gz", ".bz2", ".xz", ".tar"}
    return {
        "path": name,
        "size_bytes": len(data),
        "sha256": _sha256(data),
        "patch_candidate": patch_candidate,
        "patch_signature_valid": patch_signature,
        "patch_targets_class": bool(patch_candidate and ("class" in lower or "class" in text.lower())),
        "cobaya_yaml_candidate": config_candidate,
        "cobaya_yaml_has_required_sections": config_complete,
        "dependency_lock_candidate": lock_candidate,
        "dependency_lock_pinned": lock_pinned,
        "chain_candidate": chain_candidate,
        "likelihood_data_candidate": likelihood_candidate,
        "raw_data_candidate": raw_data_candidate,
        "class_source_candidate": class_source_candidate,
        "class_commit_metadata_candidate": commit_metadata_candidate,
        "commit_hashes": commit_hashes,
        "nested_archive_candidate": nested_archive_candidate,
    }


def _read_zip_members(
    archive: zipfile.ZipFile,
    prefix: str,
    depth: int,
    budget: dict[str, int],
    records: list[dict[str, Any]],
    nested: list[dict[str, Any]],
) -> None:
    infos = archive.infolist()
    if len(infos) + len(records) > MAX_MEMBERS:
        raise ValueError(f"archive member limit exceeded ({MAX_MEMBERS})")
    for info in infos:
        if info.is_dir():
            continue
        name = _normal_name(prefix + info.filename)
        if info.file_size > MAX_MEMBER_BYTES:
            records.append({
                "path": name,
                "size_bytes": int(info.file_size),
                "sha256": None,
                "inspection_skipped": "member exceeds size limit",
            })
            continue
        if budget["read_bytes"] + info.file_size > MAX_TOTAL_READ_BYTES:
            records.append({
                "path": name,
                "size_bytes": int(info.file_size),
                "sha256": None,
                "inspection_skipped": "archive read budget exceeded",
            })
            continue
        data = archive.read(info)
        budget["read_bytes"] += len(data)
        record = _entry_record(name, data)
        records.append(record)

        if depth >= MAX_NESTED_DEPTH or not record["nested_archive_candidate"]:
            continue
        nested_record = {"path": name, "kind": "uninspected", "member_count": 0, "members": []}
        if zipfile.is_zipfile(io.BytesIO(data)):
            try:
                with zipfile.ZipFile(io.BytesIO(data)) as nested_zip:
                    nested_record["kind"] = "zip"
                    nested_record["member_count"] = len(nested_zip.infolist())
                    nested_record["members"] = [
                        _normal_name(f"{name}!{item.filename}")
                        for item in nested_zip.infolist()
                        if not item.is_dir()
                    ][:MAX_MEMBERS]
                    _read_zip_members(
                        nested_zip,
                        prefix=f"{name}!",
                        depth=depth + 1,
                        budget=budget,
                        records=records,
                        nested=nested,
                    )
            except (OSError, zipfile.BadZipFile, RuntimeError) as exc:
                nested_record["error"] = str(exc)
        else:
            nested_record["kind"] = "non-zip archive or opaque compressed file"
        nested.append(nested_record)


def audit_archive(path: str | Path) -> dict[str, Any]:
    archive_path = Path(path)
    raw = archive_path.read_bytes()
    report: dict[str, Any] = {
        "archive": archive_path.name,
        "archive_size_bytes": len(raw),
        "archive_sha256": _sha256(raw),
        "archive_valid": False,
        "crc_test_passed": False,
        "entry_count": 0,
        "entries": [],
        "nested_archives": [],
        "candidate_groups": {},
        "commit_hash_evidence": [],
        "reproduction_checklist": {},
        "scope": {
            "inventory_only": True,
            "patch_applied": False,
            "class_built": False,
            "cobaya_executed": False,
            "posterior_independently_reproduced": False,
        },
    }
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            bad_member = archive.testzip()
            report["archive_valid"] = True
            report["crc_test_passed"] = bad_member is None
            report["crc_bad_member"] = bad_member
            budget = {"read_bytes": 0}
            _read_zip_members(
                archive, prefix="", depth=0, budget=budget,
                records=report["entries"], nested=report["nested_archives"],
            )
    except (OSError, zipfile.BadZipFile, ValueError, RuntimeError) as exc:
        report["errors"] = [str(exc)]
        report["archive_valid"] = False
        report["crc_test_passed"] = False

    entries = report["entries"]
    report["entry_count"] = len(entries)
    groups = {
        "class_patch_candidates": [x for x in entries if x.get("patch_candidate")],
        "valid_class_patch_candidates": [
            x for x in entries
            if x.get("patch_candidate") and x.get("patch_signature_valid")
            and x.get("patch_targets_class")
        ],
        "cobaya_yaml_candidates": [x for x in entries if x.get("cobaya_yaml_candidate")],
        "complete_cobaya_yaml_candidates": [
            x for x in entries if x.get("cobaya_yaml_has_required_sections")
        ],
        "dependency_lock_candidates": [x for x in entries if x.get("dependency_lock_candidate")],
        "pinned_dependency_locks": [x for x in entries if x.get("dependency_lock_pinned")],
        "chain_candidates": [x for x in entries if x.get("chain_candidate")],
        "likelihood_data_candidates": [x for x in entries if x.get("likelihood_data_candidate")],
        "raw_data_candidates": [x for x in entries if x.get("raw_data_candidate")],
        "class_source_candidates": [x for x in entries if x.get("class_source_candidate")],
    }
    report["candidate_groups"] = {
        key: [
            {
                "path": item["path"],
                "size_bytes": item["size_bytes"],
                "sha256": item.get("sha256"),
                "commit_hashes": item.get("commit_hashes", []),
            }
            for item in values
        ]
        for key, values in groups.items()
    }
    report["commit_hash_evidence"] = [
        {"path": item["path"], "hashes": item["commit_hashes"]}
        for item in entries
        if item.get("class_commit_metadata_candidate")
    ]

    checklist = {
        "valid_zip_and_crc": bool(report["archive_valid"] and report["crc_test_passed"]),
        "reviewable_class_patch_candidate": bool(groups["valid_class_patch_candidates"]),
        "class_commit_hash_metadata_candidate": bool(report["commit_hash_evidence"]),
        "cobaya_yaml_candidate_with_required_sections": bool(groups["complete_cobaya_yaml_candidates"]),
        "pinned_dependency_lock_candidate": bool(groups["pinned_dependency_locks"]),
        "chain_or_posterior_candidate": bool(groups["chain_candidates"]),
        "likelihood_data_candidate": bool(groups["likelihood_data_candidates"]),
        "raw_data_candidate": bool(groups["raw_data_candidates"]),
    }
    report["reproduction_checklist"] = {
        **checklist,
        "missing_candidate_categories": [name for name, present in checklist.items() if not present],
        "candidate_input_categories_present": all(checklist.values()),
        "independent_reproduction_verified": False,
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventory the PTUM CLASS/Cobaya source archive.")
    parser.add_argument("--archive", default="PTUM.zip")
    parser.add_argument("--output", default="ptum_class_cobaya_archive_audit.json")
    args = parser.parse_args()
    report = audit_archive(args.archive)
    Path(args.output).write_text(
        json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    checklist = report["reproduction_checklist"]
    print(f"Archive valid: {report['archive_valid']}; entries inspected: {report['entry_count']}")
    print(f"Candidate input categories present: {checklist['candidate_input_categories_present']}")
    print(f"Missing candidate categories: {checklist['missing_candidate_categories']}")
    print(f"Output: {args.output}")
    return 0 if report["archive_valid"] and report["crc_test_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
