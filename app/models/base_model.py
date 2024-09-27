from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base


class BaseTranscationModel(Base):
    """Базовая абстрактная модель для моделей CharityProject и Donation."""
    __abstract__ = True

    full_amount = Column(Integer,
                         CheckConstraint('full_amount > 0'),
                         nullable=False)
    invested_amount = Column(Integer,
                             default=0,
                             nullable=False)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    __table_args__ = (
        CheckConstraint('0 <= invested_amount <= full_amount',
                        name='invested_ge_zero_le_full_amount'),
    )

    def __repr__(self):
        return (
            f'создан {self.create_date}, общая сумма {self.full_amount}, '
            f'внесено {self.invested_amount}, ' +
            (('закрыт ' + self.close_date) if self.fully_invested
             else 'не закрыт')
        )
