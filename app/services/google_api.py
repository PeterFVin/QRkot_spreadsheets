from copy import deepcopy
from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = '%Y/%m/%d %H:%M:%S'
ROWS = 100
COLUMNS = 11
TITLE = 'Отчет от {}'
SPREADSHEET_BODY = dict(
    properties=dict(
        title='',
        locale='ru_RU',
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Лист1',
        gridProperties=dict(
            rowCount=ROWS,
            columnCount=COLUMNS,
        )))])
TABLE_HEAD = [
    ['Отчет от', ''],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = deepcopy(SPREADSHEET_BODY)
    spreadsheet_body['properties']['title'] = TITLE.format(
        datetime.now().strftime(FORMAT)
    )
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=SPREADSHEET_BODY)
    )
    return response['spreadsheetId'], response['spreadsheetUrl']


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        charity_projects: list,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    table_head = deepcopy(TABLE_HEAD)
    table_head[0][1] = datetime.now().strftime(FORMAT)
    table_values = [
        *table_head,
        *[list(map(str, [
            charity_project.name,
            charity_project.close_date - charity_project.create_date,
            charity_project.description
        ]
        )) for charity_project in charity_projects],
    ]
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    count_rows = len(table_values)
    count_columns = max(len(row) for row in table_values)
    if count_rows > ROWS or count_columns > COLUMNS:
        raise ValueError(
            f'В таблице должно быть не более {ROWS} строк. '
            f'В таблице должно быть не более {COLUMNS} столбцов. '
        )
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{count_rows}C{count_columns}',
            valueInputOption='USER_ENTERED',
            json=update_body))
