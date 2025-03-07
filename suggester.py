def custom_suggest_oracle_data_type(detected_type, max_length, column_name, unique_values):
    from data_types import is_boolean_column
    
    col = column_name.lower()
    
    if is_boolean_column(unique_values):
        return "CHAR(1)"
    
    id_keywords = ["document", "passport", "dni", "nif", "nie", "ssn", "license", "certificate"]
    if any(kw in col for kw in id_keywords):
        return f"VARCHAR2({max_length} BYTE)"
    
    is_primary_id = (col == "id" or col.endswith("_id"))
    if is_primary_id and detected_type in ("int", "float"):
        return "NUMBER"
    
    if any(keyword in col for keyword in ["created", "updated", "at"]):
        if detected_type in ("date", "string"):
            if any(":" in v for v in unique_values if v != ""):
                detected_type = "datetime"
            else:
                detected_type = "date"
    
    if detected_type in ("int", "float"):
        return "NUMBER"
    elif detected_type == "date":
        return "DATE"
    elif detected_type == "datetime":
        return "TIMESTAMP"
    else:
        # Asumimos string
        if max_length <= 4000:
            return f"VARCHAR2({max_length} BYTE)"
        elif max_length <= 32767:
            return f"VARCHAR2({max_length})"
        else:
            return "CLOB"