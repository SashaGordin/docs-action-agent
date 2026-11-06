import json
from hashlib import sha256
from pathlib import PurePosixPath
from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator


class LicenseRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")
    spdx_id: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=8000)
    ]
    license_url: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=8000)
    ]
    attribution: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=8000)
    ]


class CorpusFile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_path: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=8000)
    ]
    content_sha256: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=64,
            max_length=64,
            pattern=r"^[0-9a-f]{64}$",
        ),
    ]
    byte_size: Annotated[int, Field(ge=0)]


class CorpusManifest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["1"]
    corpus_name: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=8000)
    ]
    repository_url: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=8000)
    ]
    release_tag: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=8000)
    ]
    source_commit: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=40,
            max_length=40,
            pattern=r"^[0-9a-f]{40}$",
        ),
    ]
    license: LicenseRecord
    included_paths: Annotated[
        list[
            Annotated[
                str,
                StringConstraints(strip_whitespace=True, min_length=1, max_length=8000),
            ]
        ],
        Field(min_length=1),
    ]
    excluded_paths: list[
        Annotated[
            str, StringConstraints(strip_whitespace=True, min_length=1, max_length=8000)
        ]
    ]
    fetch_method: Literal["github_raw_at_commit", "checked_in_fixture"]
    source_url_template: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=8000)
    ]
    identity_scheme: Literal["sha256-v1"]
    files: Annotated[list[CorpusFile], Field(min_length=1)]

    @model_validator(mode="after")
    def validate_file_paths(self) -> Self:
        for corpus_file in self.files:
            path = PurePosixPath(corpus_file.source_path)

            if path.is_absolute() or ".." in path.parts:
                raise ValueError("source path must be a safe repository-relative path")

            if not any(path.match(pattern) for pattern in self.included_paths):
                raise ValueError("source path is outside the corpus allowlist")

            if any(path.match(pattern) for pattern in self.excluded_paths):
                raise ValueError("source path is explicitly excluded")

        return self


def _sha256_parts(*parts: str) -> str:
    canonical_input = json.dumps(
        parts,
        ensure_ascii=True,
        separators=(",", ":"),
    ).encode("utf-8")

    return sha256(canonical_input).hexdigest()


def content_matches_manifest(corpus_file: CorpusFile, content: bytes) -> bool:
    return (
        len(content) == corpus_file.byte_size
        and sha256(content).hexdigest() == corpus_file.content_sha256
    )


def logical_document_id(
    manifest: CorpusManifest,
    corpus_file: CorpusFile,
) -> str:
    return _sha256_parts(
        manifest.identity_scheme,
        manifest.corpus_name,
        manifest.repository_url,
        corpus_file.source_path,
    )


def document_version_id(
    manifest: CorpusManifest,
    corpus_file: CorpusFile,
) -> str:
    return _sha256_parts(
        manifest.identity_scheme,
        logical_document_id(manifest, corpus_file),
        manifest.source_commit,
        corpus_file.content_sha256,
    )


def source_url(manifest: CorpusManifest, corpus_file: CorpusFile) -> str:
    return manifest.source_url_template.format(
        commit=manifest.source_commit,
        path=corpus_file.source_path,
    )
