from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from airtraffic import __version__
from airtraffic.config import PROJECT_ROOT, SOURCE_FILES
from airtraffic.scoring import MODEL_VERSION


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def build_source_manifest() -> dict:
    sources = {}

    for name, path in sorted(SOURCE_FILES.items()):
        sources[name] = {
            "path": str(path.relative_to(PROJECT_ROOT)),
            "size_bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        }

    return {
        "sources": sources,
    }


def source_manifest_sha256(manifest: dict) -> str:
    canonical = json.dumps(
        manifest["sources"],
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    return hashlib.sha256(canonical).hexdigest()


def create_run_context() -> dict:
    generated = datetime.now(timezone.utc)
    source_manifest = build_source_manifest()
    manifest_sha256 = source_manifest_sha256(
        source_manifest
    )

    run_id = (
        f"{generated:%Y%m%dT%H%M%SZ}_"
        f"{manifest_sha256[:12]}"
    )

    return {
        "run_id": run_id,
        "generated_at_utc": generated.isoformat(),
        "pipeline_version": __version__,
        "model_version": MODEL_VERSION,
        "source_manifest": source_manifest,
        "source_manifest_sha256": manifest_sha256,
    }
