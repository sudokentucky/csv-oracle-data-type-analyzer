import csv
from tkinter import messagebox
from data_types import detect_data_type, most_frequent_type
from suggester import custom_suggest_oracle_data_type

def analyze_csv_column(file_path, column_name):
    max_length = 0
    type_list = []
    unique_values = set()
    total_values = 0
    non_empty_values = 0

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            value = row.get(column_name, "")
            total_values += 1
            if value.strip() != "":
                non_empty_values += 1
            unique_values.add(value.strip())
            l = len(value)
            if l > max_length:
                max_length = l
            t = detect_data_type(value)
            type_list.append(t)

    final_type = most_frequent_type(type_list)
    oracle_type = custom_suggest_oracle_data_type(final_type, max_length, column_name, unique_values)

    if total_values > 0:
        non_empty_ratio = non_empty_values / total_values
        empty_ratio = 1 - non_empty_ratio
    else:
        non_empty_ratio = 0
        empty_ratio = 1

    sugerir_not_null = non_empty_ratio >= 0.95

    return {
        "column_name": column_name,
        "max_length": max_length,
        "final_type": final_type,
        "oracle_type": oracle_type,
        "total_values": total_values,
        "non_empty_values": non_empty_values,
        "non_empty_ratio": round(non_empty_ratio * 100, 2),  
        "empty_ratio": round(empty_ratio * 100, 2),         
        "sugerir_not_null": sugerir_not_null
    }


def analyze_all_columns(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        columns = reader.fieldnames
        if not columns:
            return {}

        data_cols = {
            col: {
                "max_length": 0,
                "type_list": [],
                "unique_values": set(),
                "total_values": 0,
                "non_empty_values": 0
            }
            for col in columns
        }

        for row in reader:
            for col in columns:
                value = row.get(col, "")
                data_cols[col]["total_values"] += 1
                if value.strip() != "":
                    data_cols[col]["non_empty_values"] += 1
                data_cols[col]["unique_values"].add(value.strip())
                l = len(value)
                if l > data_cols[col]["max_length"]:
                    data_cols[col]["max_length"] = l
                t = detect_data_type(value)
                data_cols[col]["type_list"].append(t)

    final_results = {}
    for col, info in data_cols.items():
        final_type = most_frequent_type(info["type_list"])
        oracle_type = custom_suggest_oracle_data_type(
            final_type,
            info["max_length"],
            col,
            info["unique_values"]
        )

        if info["total_values"] > 0:
            non_empty_ratio = info["non_empty_values"] / info["total_values"]
            empty_ratio = 1 - non_empty_ratio
        else:
            non_empty_ratio = 0
            empty_ratio = 1

        sugerir_not_null = non_empty_ratio >= 0.95

        final_results[col] = {
            "column_name": col,
            "max_length": info["max_length"],
            "final_type": final_type,
            "oracle_type": oracle_type,
            "total_values": info["total_values"],
            "non_empty_values": info["non_empty_values"],
            "non_empty_ratio": round(non_empty_ratio * 100, 2),  # porcentaje de no vacíos
            "empty_ratio": round(empty_ratio * 100, 2),          # porcentaje de vacíos
            "sugerir_not_null": sugerir_not_null
        }

    return final_results
