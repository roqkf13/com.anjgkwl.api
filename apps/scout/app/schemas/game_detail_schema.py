from pydantic import BaseModel, Field


class PatchNoteSchema(BaseModel):
    id: str
    title: str
    published_at: str = Field(..., serialization_alias="publishedAt")
    summary: str
    body_ko: str = Field(..., serialization_alias="bodyKo")
    source_url: str | None = Field(default=None, serialization_alias="sourceUrl")

    model_config = {"populate_by_name": True}


class ModSchema(BaseModel):
    id: str
    name: str
    author: str
    summary: str
    source_url: str | None = Field(default=None, serialization_alias="sourceUrl")

    model_config = {"populate_by_name": True}


class RelatedVideoSchema(BaseModel):
    id: str
    title: str
    channel: str
    published_at: str = Field(..., serialization_alias="publishedAt")
    watch_url: str = Field(..., serialization_alias="watchUrl")

    model_config = {"populate_by_name": True}


class GameDetailSchema(BaseModel):
    steam_app_id: int = Field(..., serialization_alias="steamAppId")
    title: str
    steam_store_url: str = Field(..., serialization_alias="steamStoreUrl")
    official_site_url: str = Field(..., serialization_alias="officialSiteUrl")
    patch_notes: list[PatchNoteSchema] = Field(
        default_factory=list, serialization_alias="patchNotes"
    )
    mods: list[ModSchema] = Field(default_factory=list)
    videos: list[RelatedVideoSchema] = Field(default_factory=list)

    model_config = {"populate_by_name": True}
