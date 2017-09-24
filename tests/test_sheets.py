import gspread

from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name("sheet-creds.json", scope)

gc = gspread.authorize(credentials)

sheet = gc.open_by_key('1ISRlnLwsYKaKMeTHUIUUUWlH2XucBTkgFUV44e14OlA')
ws = sheet.get_worksheet(0)
print(ws.update_acell('A42', "Test!"))
