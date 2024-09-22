from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

CELL_A1_TEXT = 'Отчет от'
CELL_A2_TEXT = 'Топ проектов по скорости закрытия'
CELL_A3_TEXT = 'Название проекта'
CELL_B3_TEXT = 'Время сбора'
CELL_C3_TEXT = 'Описание'
FORMAT = '%Y/%m/%d %H:%M:%S'


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {'title': f'Отчет от {now_date_time}',
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': 'Лист1',
                                   'gridProperties': {'rowCount': 100,
                                                      'columnCount': 11}}}]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response['spreadsheetId']
    return spreadsheetid


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields='id'
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        charity_projects: list,
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        [CELL_A1_TEXT, now_date_time],
        [CELL_A2_TEXT],
        [CELL_A3_TEXT, CELL_B3_TEXT, CELL_C3_TEXT]
    ]
    for charity_project in charity_projects:
        new_row = [str(charity_project.name),
                   str(charity_project.close_date -
                       charity_project.create_date),
                   str(charity_project.description)]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:C100',
            valueInputOption='USER_ENTERED',
            json=update_body))
