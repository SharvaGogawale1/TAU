import pyodbc

def get_connection(db_file: str) -> pyodbc.Cursor:
    try:
        return pyodbc.connect(
            r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+db_file+';')
        )