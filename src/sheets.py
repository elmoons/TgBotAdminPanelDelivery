import gspread
from gspread import Client, Spreadsheet, Worksheet

from src.config import settings


def initial():
    gc: Client = gspread.service_account(".././credentials.json")
    sh: Spreadsheet = gc.open_by_url(settings.SPREADSHEET_URL)
    return sh


def add_data_to_sheet(sh: Spreadsheet):
    ...


add_data_to_sheet(initial())
