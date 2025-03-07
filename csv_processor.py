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
    return max_length, final_type, oracle_type, total_values, non_empty_values

def analyze_all_columns(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        columns = reader.fieldnames
        if not columns:
            messagebox.showerror("Error", "El archivo CSV no tiene encabezados.")
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
        final_results[col] = (
            info["max_length"], 
            final_type, 
            oracle_type, 
            info["total_values"], 
            info["non_empty_values"]
        )
    return final_results