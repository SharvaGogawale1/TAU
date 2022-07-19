# Standard Library
import os
import sys
import time
from typing import Union

# PIP installed library
import pexpect
import inquirer

# Global Vars
INITIAL_PARTITION = "Loaded Tables:\r\n"
END_PARTITION = "\r\n"
DATABASE_DIR = os.path.join(
    os.getcwd(),
    "database")
DATA_DIR = os.path.join(
    os.getcwd(),
    "data")


#.DDDDDDDDDDDD..........AAAAA..........SSSSSSSSS.....HHHH......HHHHH..
#.DDDDDDDDDDDDD.........AAAAAA........SSSSSSSSSSS....HHHH......HHHHH..
#.DDDDDDDDDDDDDD.......AAAAAAA.......SSSSSSSSSSSSS...HHHH......HHHHH..
#.DDDDD..DDDDDDDD......AAAAAAAA......SSSSSS.SSSSSS...HHHH......HHHHH..
#.DDDDD.....DDDDD......AAAAAAAA......SSSS.....SSSSS..HHHH......HHHHH..
#.DDDDD.....DDDDD.....AAAAAAAAA......SSSSS....SSSSS..HHHH......HHHHH..
#.DDDDD......DDDD.....AAAAAAAAAA.....SSSSSSSS........HHHH......HHHHH..
#.DDDDD......DDDDD....AAAA.AAAAA.....SSSSSSSSSSS.....HHHHHHHHHHHHHHH..
#.DDDDD......DDDDD...AAAAA..AAAA......SSSSSSSSSSSS...HHHHHHHHHHHHHHH..
#.DDDDD......DDDDD...AAAAA..AAAAA......SSSSSSSSSSS...HHHHHHHHHHHHHHH..
#.DDDDD......DDDDD..AAAAA...AAAAA.........SSSSSSSSS..HHHH......HHHHH..
#.DDDDD......DDDD...AAAAAAAAAAAAAA...SSSS.....SSSSS..HHHH......HHHHH..
#.DDDDD.....DDDDD...AAAAAAAAAAAAAA..ASSSS......SSSS..HHHH......HHHHH..
#.DDDDD.....DDDDD..DAAAAAAAAAAAAAA..ASSSS.....SSSSS..HHHH......HHHHH..
#.DDDDD...DDDDDDD..DAAAA......AAAAA..SSSSSSSSSSSSSS..HHHH......HHHHH..
#.DDDDDDDDDDDDDD...DAAA.......AAAAA..SSSSSSSSSSSSS...HHHH......HHHHH..
#.DDDDDDDDDDDDD...DDAAA........AAAAA..SSSSSSSSSSSS...HHHH......HHHHH..
#.DDDDDDDDDDDD....DDAAA........AAAAA...SSSSSSSSS.....HHHH......HHHHH..


def get_db(_path: str=DATABASE_DIR) -> list:
    return os.listdir(_path)

def get_tables(_db: str) -> list:
    process = pexpect.spawn("sh", ["/opt/UCanAccess-5.0.1.bin/console.sh"], encoding='utf-8')
    child = sys.stdout
    process.sendline(os.path.join(DATABASE_DIR, _db))
    time.sleep(2)
    process.expect(INITIAL_PARTITION)
    stdout = process.buffer

    return stdout[:stdout.find(END_PARTITION)]

def get_file(_db: str, _table: str) -> str:
    process = pexpect.spawn("sh", ["/opt/UCanAccess-5.0.1.bin/console.sh"], encoding='utf-8')
    sys.stdout
    process.sendline(os.path.join(DATABASE_DIR, _db))
    time.sleep(2)
    process.expect(INITIAL_PARTITION)
    process.buffer
    file_to_save_path = os.path.join(
        os.getcwd(),
        "data",
        _table.replace(" ", "_")+".csv"
        )
    EXPORT_STRING = f"""export -t \"{_table}\" {file_to_save_path};"""
    process.sendline(EXPORT_STRING)
    time.sleep(2)
    process.expect("UCanAccess")
    return file_to_save_path

def get_csv_path(_filename: str) -> str:
    return os.path.join(os.getcwd(), "data", _filename)

# def dash_extract(db: str = None, table: str = None, req: str = None, csv_filename: str = None) -> Union[str, None]:
#     match req:
#         case "DB":
#             return get_db(DATABASE_DIR)
#         case "TABLES":
#             return get_tables(_db=db)
#         case "FILE":
#             return get_file(_db=db, _table=table)
#         case "CSV":
#             return get_csv_path(_filename=csv_filename)








#.....CCCCCCCC......LLLL...............AAAAA..........SSSSSSSSS.......SSSSSSSSS....SIIII......CCCCCCCC......
#...CCCCCCCCCCCC....LLLL..............AAAAAAA.......SSSSSSSSSSSS....SSSSSSSSSSSS...SIIII....CCCCCCCCCCCC....
#..CCCCCCCCCCCCCC...LLLL..............AAAAAAA.......SSSSSSSSSSSS....SSSSSSSSSSSS...SIIII...CCCCCCCCCCCCCC...
#..CCCCCCCCCCCCCC...LLLL..............AAAAAAA......ASSSSSSSSSSSSS..SSSSSSSSSSSSSS..SIIII...CCCCCCCCCCCCCC...
#.CCCCCC....CCCCC...LLLL.............AAAAAAAAA.....ASSSS....SSSSS..SSSSS....SSSSS..SIIII..ICCCCC....CCCCC...
#.CCCCC......CCCCC..LLLL.............AAAAAAAAA.....ASSSS.....SSSS..SSSSS.....SSSS..SIIII..ICCCC......CCCCC..
#.CCCCC.............LLLL.............AAAA.AAAA.....ASSSSSSSS.......SSSSSSSSS.......SIIII..ICCCC.............
#.CCCC..............LLLL............AAAAA.AAAAA.....SSSSSSSSSSS.....SSSSSSSSSSS....SIIII..ICCC..............
#.CCCC..............LLLL............AAAAA.AAAAA......SSSSSSSSSSS.....SSSSSSSSSSS...SIIII..ICCC..............
#.CCCC..............LLLL............AAAA...AAAAA......SSSSSSSSSSS.....SSSSSSSSSSS..SIIII..ICCC..............
#.CCCC..............LLLL...........AAAAA...AAAAA.........SSSSSSSS........SSSSSSSS..SIIII..ICCC..............
#.CCCCC......CCC....LLLL...........AAAAAAAAAAAAA...ASSS.....SSSSS..SSSS.....SSSSS..SIIII..ICCCC......CCC....
#.CCCCC......CCCCC..LLLL..........AAAAAAAAAAAAAAA..ASSS......SSSSS.SSSS......SSSSS.SIIII..ICCCC......CCCCC..
#.CCCCCC....CCCCC...LLLL..........AAAAAAAAAAAAAAA..ASSSS.....SSSSS.SSSSS.....SSSSS.SIIII..ICCCCC....CCCCC...
#..CCCCCCCCCCCCCC...LLLL..........AAAAA......AAAAA.ASSSSSSSSSSSSS..SSSSSSSSSSSSSS..SIIII...CCCCCCCCCCCCCC...
#..CCCCCCCCCCCCC....LLLLLLLLLLLLLLAAAA.......AAAAA..SSSSSSSSSSSSS...SSSSSSSSSSSSS..SIIII...CCCCCCCCCCCCC....
#...CCCCCCCCCCCC....LLLLLLLLLLLLLLAAAA.......AAAAA..SSSSSSSSSSSS....SSSSSSSSSSSS...SIIII....CCCCCCCCCCCC....
#.....CCCCCCCC......LLLLLLLLLLLLLLAAA.........AAAAA...SSSSSSSSS.......SSSSSSSSS....SIIII......CCCCCCCC......

def make_inquire(available_tables: str) -> str:
    choices_list = available_tables.split(", ")
    questions = [
        inquirer.List('tables',
                    message="What Tables you want to extract to csv file?",
                    choices=choices_list,
                    carousel=True
                ),
    ]

    return inquirer.prompt(questions)

def run_ucanaccess_bin(database: str) -> str:
    process = pexpect.spawn("sh", ["/opt/UCanAccess-5.0.1.bin/console.sh"], encoding='utf-8')
    child = sys.stdout
    process.sendline(os.path.join(DATABASE_DIR, database))
    time.sleep(2)
    process.expect(INITIAL_PARTITION)
    stdout = process.buffer

    stdout = stdout[:
        stdout.find(END_PARTITION)]

    answers = make_inquire(stdout)

    file_to_save_path = os.path.join(
        os.getcwd(),
        "data",
        str(answers.get("tables")).replace(" ","_")+
        ".csv"
        )

    EXPORT_STRING = f"""export -t \"{answers.get("tables")}\" {file_to_save_path};"""
    process.sendline(EXPORT_STRING)
    time.sleep(2)
    process.expect("UCanAccess")
    return file_to_save_path

def extract_data() -> Union[str, None]:
    questions = [
        inquirer.List('run_method',
                    message="What extraction method you want to run?",
                    choices=["Microsoft Database", "Extracted CSV file"],
                    carousel=True
                ),
    ]
    answer = inquirer.prompt(questions).get("run_method")
    if answer == "Microsoft Database":
        databases = [
        inquirer.List('database',
                    message="Select a database:",
                    choices=os.listdir("database"),
                    carousel=True
                ),
        ]
        file = run_ucanaccess_bin(inquirer.prompt(databases).get("database"))
        return file
    else:
        csv_file = [
        inquirer.List('csv_file',
                    message="Select a csv file:",
                    choices=os.listdir("data"),
                    carousel=True
                ),
        ]
        return os.path.join(os.getcwd(), "data", inquirer.prompt(csv_file).get("csv_file"))