from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base_model import BaseTranscationModel


class Donation(BaseTranscationModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        base_repr = super().__repr__()
        return (f'Пожертвование, {base_repr}')
