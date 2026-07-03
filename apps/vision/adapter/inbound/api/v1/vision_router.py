import logging

from fastapi import APIRouter, File, HTTPException, UploadFile

from vision.adapter.inbound.api.schemas.vision_schema import VisionUploadResponseSchema

logger = logging.getLogger(__name__)

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png"}

vision_upload_router = APIRouter(tags=["vision"])


@vision_upload_router.post(
    "/upload",
    response_model=VisionUploadResponseSchema,
    summary="비전 처리용 이미지(jpg, png) 업로드",
)
async def upload_vision_image(file: UploadFile = File(...)) -> VisionUploadResponseSchema:
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="jpg, png 파일만 업로드할 수 있습니다.")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="빈 파일입니다.")

    logger.info(
        "[VisionRouter] received %s (%s, %d bytes)",
        file.filename,
        file.content_type,
        len(content),
    )

    return VisionUploadResponseSchema(
        filename=file.filename or "",
        content_type=file.content_type or "",
        size_bytes=len(content),
        message="이미지가 서버에 정상적으로 전달되었습니다.",
    )
