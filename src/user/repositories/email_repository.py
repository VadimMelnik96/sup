from sqlalchemy import select

from ..dependencies.session import ISession
from ..dtos.email__dto import CreateEmailCodeDTO
from ..models.email_model import VerifyEmailModel


class EmailRepository:

    def __init__(self, session: ISession):
        self.session = session

    async def create(self, dto: CreateEmailCodeDTO):
        instance = VerifyEmailModel(**dto.model_dump())
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def get_code(self, code: str):
        stmt = select(VerifyEmailModel).filter_by(code=code)
        raw = await self.session.execute(stmt)
        return raw.scalar_one_or_none()
