from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from docs_action_agent.corpus import (
    CorpusFile,
    CorpusManifest,
    content_matches_manifest,
    document_version_id,
    logical_document_id,
    source_url,
)

PROJECT_ROOT = Path(__file__).parents[1]
FIXTURE_ROOT = Path(__file__).parent / "fixtures" / "corpus"


def _manifest_data(**overrides: Any) -> dict[str, Any]:
    data: dict[str, Any] = {
        "schema_version": "1",
        "corpus_name": "offline-contract-fixture",
        "repository_url": "https://example.invalid/offline-corpus-fixture",
        "release_tag": "fixture-v1",
        "source_commit": "a" * 40,
        "license": {
            "spdx_id": "LicenseRef-Test-Fixture",
            "license_url": "https://example.invalid/license",
            "attribution": "Synthetic test fixture authored for this project",
        },
        "included_paths": [
            "docs/en/docs/tutorial/*.md",
            "docs/en/docs/tutorial/**/*.md",
        ],
        "excluded_paths": [],
        "fetch_method": "checked_in_fixture",
        "source_url_template": "https://example.invalid/blob/{commit}/{path}",
        "identity_scheme": "sha256-v1",
        "files": [
            {
                "source_path": "docs/en/docs/tutorial/body.md",
                "content_sha256": "b" * 64,
                "byte_size": 6611,
            }
        ],
    }
    data.update(overrides)
    return data


def _manifest(**overrides: Any) -> CorpusManifest:
    return CorpusManifest.model_validate(_manifest_data(**overrides))


def test_valid_manifest_accepted() -> None:
    manifest = _manifest()

    assert manifest.corpus_name == "offline-contract-fixture"
    assert manifest.files[0].byte_size == 6611


def test_unexpected_manifest_field_rejected() -> None:
    with pytest.raises(ValidationError):
        _manifest(unexpected_field="not allowed")


@pytest.mark.parametrize("source_commit", ["a" * 41, "g" * 40, "A" * 40])
def test_invalid_source_commit_rejected(source_commit: str) -> None:
    with pytest.raises(ValidationError):
        _manifest(source_commit=source_commit)


@pytest.mark.parametrize("content_sha256", ["b" * 65, "g" * 64, "B" * 64])
def test_invalid_content_sha256_rejected(content_sha256: str) -> None:
    files = [
        {
            "source_path": "docs/en/docs/tutorial/body.md",
            "content_sha256": content_sha256,
            "byte_size": 6611,
        }
    ]

    with pytest.raises(ValidationError):
        _manifest(files=files)


def test_out_of_scope_path_rejected() -> None:
    files = [
        {
            "source_path": "docs/de/docs/tutorial/body.md",
            "content_sha256": "b" * 64,
            "byte_size": 6611,
        }
    ]

    with pytest.raises(ValidationError, match="outside the corpus allowlist"):
        _manifest(files=files)


def test_explicitly_excluded_path_rejected() -> None:
    with pytest.raises(ValidationError, match="explicitly excluded"):
        _manifest(excluded_paths=["docs/en/docs/tutorial/body.md"])


def test_unsafe_relative_path_rejected() -> None:
    files = [
        {
            "source_path": "docs/en/docs/tutorial/../body.md",
            "content_sha256": "b" * 64,
            "byte_size": 6611,
        }
    ]

    with pytest.raises(ValidationError, match="safe repository-relative path"):
        _manifest(files=files)


def test_identical_inputs_produce_identical_ids() -> None:
    manifest = _manifest()
    corpus_file = manifest.files[0]

    first_logical_id = logical_document_id(manifest, corpus_file)
    second_logical_id = logical_document_id(manifest, corpus_file)
    first_version_id = document_version_id(manifest, corpus_file)
    second_version_id = document_version_id(manifest, corpus_file)

    assert first_logical_id == second_logical_id
    assert first_version_id == second_version_id
    assert len(first_logical_id) == 64
    assert len(first_version_id) == 64


def test_changed_commit_changes_only_document_version_id() -> None:
    first_manifest = _manifest(source_commit="a" * 40)
    second_manifest = _manifest(source_commit="c" * 40)
    corpus_file = first_manifest.files[0]

    assert logical_document_id(first_manifest, corpus_file) == logical_document_id(
        second_manifest, corpus_file
    )
    assert document_version_id(
        first_manifest, corpus_file
    ) != document_version_id(second_manifest, corpus_file)


def test_changed_content_changes_only_document_version_id() -> None:
    manifest = _manifest()
    original_file = manifest.files[0]
    changed_file = CorpusFile(
        source_path=original_file.source_path,
        content_sha256="c" * 64,
        byte_size=original_file.byte_size,
    )

    assert logical_document_id(manifest, original_file) == logical_document_id(
        manifest, changed_file
    )
    assert document_version_id(manifest, original_file) != document_version_id(
        manifest, changed_file
    )


def test_production_manifest_is_pinned_and_bounded() -> None:
    manifest_path = PROJECT_ROOT / "corpus" / "fastapi-0.162.0.json"
    manifest = CorpusManifest.model_validate_json(
        manifest_path.read_text(encoding="utf-8")
    )

    assert manifest.source_commit == "7a0a3f0b286c6c865cf4398ea0e957a87b8bffa4"
    assert manifest.license.spdx_id == "MIT"
    assert len(manifest.files) == 5
    assert set(manifest.included_paths) == {
        corpus_file.source_path for corpus_file in manifest.files
    }


def test_source_url_uses_immutable_commit() -> None:
    manifest_path = PROJECT_ROOT / "corpus" / "fastapi-0.162.0.json"
    manifest = CorpusManifest.model_validate_json(
        manifest_path.read_text(encoding="utf-8")
    )

    assert source_url(manifest, manifest.files[0]) == (
        "https://github.com/fastapi/fastapi/blob/"
        "7a0a3f0b286c6c865cf4398ea0e957a87b8bffa4/"
        "docs/en/docs/tutorial/first-steps.md"
    )


def test_checked_in_fixture_matches_manifest_hash_and_size() -> None:
    manifest_path = FIXTURE_ROOT / "manifest.json"
    manifest = CorpusManifest.model_validate_json(
        manifest_path.read_text(encoding="utf-8")
    )
    corpus_file = manifest.files[0]
    content = (FIXTURE_ROOT / corpus_file.source_path).read_bytes()

    assert content_matches_manifest(corpus_file, content)


def test_changed_fixture_content_fails_verification() -> None:
    manifest_path = FIXTURE_ROOT / "manifest.json"
    manifest = CorpusManifest.model_validate_json(
        manifest_path.read_text(encoding="utf-8")
    )
    corpus_file = manifest.files[0]
    content = (FIXTURE_ROOT / corpus_file.source_path).read_bytes()

    assert not content_matches_manifest(corpus_file, content + b"changed")
