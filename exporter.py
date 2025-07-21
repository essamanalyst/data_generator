import pandas as pd
import os
from typing import Union, Optional
import tempfile
import sqlalchemy
import pyarrow.parquet as pq
import json
from io import StringIO, BytesIO
import streamlit as st

@st.cache_data
def export_data(
    data: pd.DataFrame,
    format_type: str,
    file_name: str,
    db_type: Optional[str] = None,
    connection_string: Optional[str] = None,
    bucket_name: Optional[str] = None
) -> Union[str, bytes, None]:
    """Export data to various formats with caching"""
    try:
        if format_type in ["csv", "excel", "json", "parquet"]:
            buffer = BytesIO()
            
            if format_type == "csv":
                data.to_csv(buffer, index=False, encoding='utf-8')
                extension = "csv"
            elif format_type == "excel":
                data.to_excel(buffer, index=False)
                extension = "xlsx"
            elif format_type == "json":
                data.to_json(buffer, orient="records", force_ascii=False)
                extension = "json"
            elif format_type == "parquet":
                data.to_parquet(buffer, index=False)
                extension = "parquet"
            
            buffer.seek(0)
            return buffer.getvalue(), f"{file_name}.{extension}"
        
        elif format_type == "sql":
            if not db_type or not connection_string:
                raise ValueError("Database type and connection string are required")
            
            engine = sqlalchemy.create_engine(connection_string)
            data.to_sql(
                file_name, 
                engine, 
                if_exists="replace", 
                index=False, 
                chunksize=10000,
                method='multi'  # Faster insertion for some databases
            )
            return None, None
        
        else:
            raise ValueError(f"Unsupported export format: {format_type}")
    
    except Exception as e:
        st.error(f"Export failed: {str(e)}")
        raise
