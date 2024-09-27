from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = '%Y/%m/%d %H:%M:%S'
ROWS = 100
COLUMNS = 11
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
TABLE_VALUES_CONST = [
    ['Отчет от', {}],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]
TITLE = 'Отчет от {}'


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    SPREADSHEET_BODY['properties']['title'] = TITLE.format(now_date_time)
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=SPREADSHEET_BODY)
    )
    spreadsheet_id = response['spreadsheetId']
    spreadsheet_url = response['spreadsheetUrl']
    return spreadsheet_id, spreadsheet_url


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
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    TABLE_VALUES_CONST[0][1] = now_date_time
    table_values = [
        *TABLE_VALUES_CONST,
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
    count_columns = len(table_values[2])
    if count_rows > ROWS or count_columns > COLUMNS:
        raise ValueError(
            ('В таблице должно быть не более ' + str(ROWS) + ' строк. '
             if count_rows > ROWS else '') +
            ('В таблице должно быть не более ' + str(COLUMNS) + ' столбцов. '
             if count_columns > COLUMNS else '')
        )
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{count_rows}C{count_columns}',
            valueInputOption='USER_ENTERED',
            json=update_body))
