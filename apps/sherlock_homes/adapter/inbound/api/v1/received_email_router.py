from fastapi import APIRouter, Depends

from sherlock_homes.adapter.inbound.api.schemas.received_email_schema import (
    ReceiveEmailRequest,
    ReceivedEmailListSchema,
    ReceivedEmailSchema,
)
from sherlock_homes.app.dtos.received_email_dto import ReceivedEmailCommand
from sherlock_homes.app.ports.input.received_email_use_case import ReceivedEmailUseCase
from sherlock_homes.dependencies.received_email_provider import get_received_email_interactor

received_email_router = APIRouter(prefix="/watson", tags=["watson"])


@received_email_router.post("/emails/receive", response_model=ReceivedEmailSchema, summary="Gmail 수신 메일 저장")
async def receive_email(
    body: ReceiveEmailRequest,
    use_case: ReceivedEmailUseCase = Depends(get_received_email_interactor),
) -> ReceivedEmailSchema:
    command = ReceivedEmailCommand(
        gmail_id=body.gmail_id,
        thread_id=body.thread_id,
        from_=body.from_,
        to=body.to,
        subject=body.subject,
        snippet=body.snippet,
    )
    result = await use_case.receive(command)
    return ReceivedEmailSchema(
        id=result.id,
        gmail_id=result.gmail_id,
        thread_id=result.thread_id,
        from_=result.from_,
        to=result.to,
        subject=result.subject,
        snippet=result.snippet,
    )


@received_email_router.get("/emails", response_model=ReceivedEmailListSchema, summary="수신 메일 목록 조회")
async def list_emails(
    use_case: ReceivedEmailUseCase = Depends(get_received_email_interactor),
) -> ReceivedEmailListSchema:
    result = await use_case.list_all()
    return ReceivedEmailListSchema(
        total=result.total,
        emails=[
            ReceivedEmailSchema(
                id=e.id,
                gmail_id=e.gmail_id,
                thread_id=e.thread_id,
                from_=e.from_,
                to=e.to,
                subject=e.subject,
                snippet=e.snippet,
            )
            for e in result.emails
        ],
    )
