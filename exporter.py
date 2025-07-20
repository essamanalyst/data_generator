import pandas as pd
import os
from typing import Union
import tempfile
import sqlalchemy

def export_data(
    data: pd.DataFrame,
    format_type: str,
    file_name: str,
    db_type: str = None,
    connection_string: str = None
) -> Union[str, None]:
    """Export data to the specified format"""
    if format_type == "csv":
        output_path = f"{file_name}.csv"
        data.to_csv(output_path, index=False)
        return output_path
    
    elif format_type == "excel":
        output_path = f"{file_name}.xlsx"
        data.to_excel(output_path, index=False)
        return output_path
    
    elif format_type == "json":
        output_path = f"{file_name}.json"
        data.to_json(output_path, orient="records")
        return output_path
    
    elif format_type == "parquet":
        output_path = f"{file_name}.parquet"
        data.to_parquet(output_path, index=False)
        return output_path
    
    elif format_type == "sql":
        if not db_type or not connection_string:
            raise ValueError("Database type and connection string are required for SQL export")
        
        engine = sqlalchemy.create_engine(connection_string)
        data.to_sql(file_name, engine, if_exists="replace", index=False)
        return None
    
    elif format_type == "cloud":
        # يحتاج إلى تنفيذ حسب مزود السحابة
        raise NotImplementedError("Cloud export not implemented yet")
    
    else:
        raise ValueError(f"Unsupported export format: {format_type}")
