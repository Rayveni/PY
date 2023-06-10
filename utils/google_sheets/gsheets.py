from httplib2 import Http
import apiclient.discovery as discovery
from oauth2client.service_account import ServiceAccountCredentials
import re


class gsheets:
    """_summary_ 
    https://habr.com/ru/articles/305378/

    Returns:
        _type_: _description_
    """

    def __init__(self, token_path: str) -> None:
        self.scope = ['https://www.googleapis.com/auth/spreadsheets',
                      'https://www.googleapis.com/auth/drive']

        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            token_path, self.scope)
        httpAuth = credentials.authorize(Http())
        self.service = discovery.build('sheets', 'v4', http=httpAuth)

    def extract_sheetid_from_url(self, url: str) -> dict:
        spreadsheet_id = re.search(
            "/spreadsheets/d/([a-zA-Z0-9-_]+)", url).group(1)
        sheet_id = re.search("[#&]gid=([0-9]+)", url).group(1)
        _sheet_info = self.sheet_info(spreadsheet_id)
        for _sheet in _sheet_info['sheets']:
            if str(_sheet['properties']['sheetId']) == sheet_id:
                break
        return {'spreadsheet_id': spreadsheet_id, 'sheet_id': sheet_id, 'range': _sheet['properties']['title']}

    def sheet_info(self, spreadsheet_id: str) -> dict:
        return self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()

    def cell_values(self, spreadsheet_id: str = None, range: str = None, url: str = None) -> dict:
        """
        range=Sheet1!A1:H1  or range=Sheet1
        """
        if url:
            _sheet_info = self.extract_sheetid_from_url(url)
            return self.service.spreadsheets().values().get(spreadsheetId=_sheet_info['spreadsheet_id'],
                                                            range=_sheet_info['range']).execute()

        return self.service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                                        range=range).execute()

        """
        spreadsheet = service.spreadsheets().create(body = {
    'properties': {'title': 'Сие есть название документа', 'locale': 'ru_RU'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': 'Сие есть название листа',
                               'gridProperties': {'rowCount': 8, 'columnCount': 5}}}]
}).execute()

## даем доступ

driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth)
shareRes = driveService.permissions().create(
    fileId = spreadsheet['spreadsheetId'],
    body = {'type': 'anyone', 'role': 'reader'},  # доступ на чтение кому угодно
    fields = 'id'
).execute()
        
        """
