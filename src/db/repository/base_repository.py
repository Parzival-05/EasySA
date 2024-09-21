from abc import abstractmethod, ABC
from typing import List, Type

from sqlalchemy import and_, not_, or_
from sqlalchemy.orm import Session

from src.db.models import BaseIDModel, BaseModel


class Repository(ABC):
    @property
    @abstractmethod
    def MODEL(self) -> Type[BaseIDModel]:
        pass

    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_one(self, **filters) -> MODEL:
        return self.db_session.query(self.MODEL).filter_by(**filters).one_or_none()

    async def list(self, **filters) -> List[MODEL]:
        return self.db_session.query(self.MODEL).filter_by(**filters).all()

    async def add(self, obj: MODEL):
        self.db_session.add(obj)

    async def add_all(self, objs: List[BaseModel]):
        self.db_session.add_all(objs)

    # noinspection PyMethodMayBeStatic
    async def update_one(self, obj, **kwargs):
        for key, value in kwargs.items():
            setattr(obj, key, value)

    async def update(self, filters: dict, **kwargs) -> List[BaseModel]:
        objs = await self.list(**filters)
        if objs:
            for key, value in kwargs.items():
                for obj in objs:
                    setattr(obj, key, value)
        return objs

    async def delete(self, **filters) -> int:
        return self.db_session.query(self.MODEL).filter_by(**filters).delete()

    async def commit(self):
        self.db_session.commit()

    async def list_where_attr_contains_obj(self, **kwargs):  # ⚰️💀
        return (
            self.db_session.query(self.MODEL)
            .filter(
                and_(
                    *[
                        getattr(self.MODEL, attr).contains(obj)
                        for attr, obj in kwargs.items()
                    ]
                )
            )
            .all()
        )

    async def list_where_attr_not_contains_obj(self, **kwargs):  # ⚰️💀
        return (
            self.db_session.query(self.MODEL)
            .filter(
                not_(
                    and_(
                        *[
                            getattr(self.MODEL, attr).contains(obj)
                            for attr, obj in kwargs.items()
                        ]
                    )
                )
            )
            .all()
        )

    async def list_or_equality(self, filters: dict):
        return self.db_session.query(self.MODEL).filter(
            or_(*[getattr(self.MODEL, attr) == obj for attr, obj in filters.items()])
        )
