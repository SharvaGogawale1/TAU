def transform(_extracted_dict: dict, _db_name: str, _table_name: str, _start_time: int, _end_time: int) -> dict:
    try:
        _extracted_dict[_db_name][_table_name]=[_start_time, _end_time]
        return _extracted_dict
    except KeyError:
        _extracted_dict[_db_name]={}
        _extracted_dict[_db_name][_table_name]=[_start_time, _end_time]
        return _extracted_dict
    except:
        raise Exception("Issue in handling labeling transform.")