from typing import Literal

from pydantic import BaseModel, Field


class PatchContentBlockDto(BaseModel):
    """Steam 원문 순서대로 이어지는 텍스트·이미지 블록."""

    type: Literal["text", "image"]
    text: str | None = None
    url: str | None = None


class PatchNoteDto(BaseModel):
    id: str
    title: str
    published_at: str = Field(..., serialization_alias="publishedAt")
    summary: str
    body_ko: str = Field(..., serialization_alias="bodyKo")
    image_urls: list[str] = Field(default_factory=list, serialization_alias="imageUrls")
    content_blocks: list[PatchContentBlockDto] = Field(
        default_factory=list, serialization_alias="contentBlocks"
    )
    source_url: str | None = Field(default=None, serialization_alias="sourceUrl")

    model_config = {"populate_by_name": True}


class ModDto(BaseModel):
    id: str
    name: str
    author: str
    summary: str
    source_url: str | None = Field(default=None, serialization_alias="sourceUrl")

    model_config = {"populate_by_name": True}


class RelatedVideoDto(BaseModel):
    id: str
    title: str
    channel: str
    published_at: str = Field(..., serialization_alias="publishedAt")
    watch_url: str = Field(..., serialization_alias="watchUrl")

    model_config = {"populate_by_name": True}


class GameDetailDto(BaseModel):
    steam_app_id: int = Field(..., serialization_alias="steamAppId")
    title: str
    steam_store_url: str = Field(..., serialization_alias="steamStoreUrl")
    official_site_url: str = Field(..., serialization_alias="officialSiteUrl")
    patch_notes: list[PatchNoteDto] = Field(
        default_factory=list, serialization_alias="patchNotes"
    )
    mods: list[ModDto] = Field(default_factory=list)
    videos: list[RelatedVideoDto] = Field(default_factory=list)

    model_config = {"populate_by_name": True}
