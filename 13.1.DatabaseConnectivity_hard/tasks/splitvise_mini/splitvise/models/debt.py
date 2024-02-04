from sqlalchemy import Column, Integer, ForeignKey, Numeric

from .base import Base


class Debt(Base):  # type: ignore
    __tablename__ = 'debts'

    debt_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.event_id'))
    debtor_id = Column(Integer, ForeignKey('users.user_id'))
    value = Column(Numeric)

    def __repr__(self) -> str:
        return f'<Debt debt={self.debt_id}, event_id={self.event_id}, debtor_id={self.debtor_id}, value={self.value}>'
