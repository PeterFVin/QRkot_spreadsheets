from datetime import datetime

from app.models.base_model import BaseTranscationModel


def func_donation(
        target: BaseTranscationModel,
        sources: list[BaseTranscationModel]) -> list[BaseTranscationModel]:
    modified = []
    for source in sources:
        if target.fully_invested:
            break
        rest_amount = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount
        )
        modified.append(source)
        for operation in [target, source]:
            operation.invested_amount += rest_amount
            operation.fully_invested = (
                operation.invested_amount == operation.full_amount
            )
            if operation.fully_invested:
                operation.close_date = datetime.now()

    return modified
