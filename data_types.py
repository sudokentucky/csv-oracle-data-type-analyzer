import datetime
from collections import Counter

def detect_data_type(value):
    v = value.strip()
    if v == "":
        return "empty"

    try:
        int(v)
        return "int"
    except:
        pass

    try:
        float(v)
        return "float"
    except:
        pass

    if any(sep in v for sep in ('-', '/', ':')):
        formatos_fecha = [
            '%Y-%m-%d',
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d %H:%M:%S.%f',
            '%d/%m/%Y',
            '%d/%m/%Y %H:%M:%S'
        ]
        for fmt in formatos_fecha:
            try:
                dt = datetime.datetime.strptime(v, fmt)
                if "H" in fmt:
                    return "datetime"
                else:
                    return "date"
            except:
                pass
    
    return "string"


def most_frequent_type(type_list):

    counts = Counter(t for t in type_list if t != "empty")
    if not counts:
        return "string"
    
    priority = ["int", "float", "date", "datetime", "string"]
    return max(counts, key=lambda k: (counts[k], -priority.index(k)))


def is_boolean_column(unique_values):
    bool_set = {"true", "false", "t", "f", "1", "0"}
    return all(v.lower() in bool_set for v in unique_values if v != "")