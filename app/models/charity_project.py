from sqlalchemy import Column, String, Text

from app.models.base_model import BaseTranscationModel


class CharityProject(BaseTranscationModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        base_repr = super().__repr__()
        return (f'Проект {self.name}: {self.description[:20]}... '
                f'{base_repr}')
