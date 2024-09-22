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
        CheckConstraint('invested_amount >= 0',
                        name='invested_ge_zero'),
        CheckConstraint('invested_amount <= full_amount',
                        name='invested_le_full_amount'),
    )
