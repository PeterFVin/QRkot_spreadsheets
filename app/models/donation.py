from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base_model import BaseTranscationModel


class Donation(BaseTranscationModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
