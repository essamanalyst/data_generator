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
                raise ValueError("Database type and connection string are required")
            
            engine = sqlalchemy.create_engine(connection_string)
            data.to_sql(file_name, engine, if_exists="replace", index=False, chunksize=10000)
            return None
        
        elif format_type == "cloud":
            # Implementation for cloud storage would go here
            raise NotImplementedError("Cloud export not implemented yet")
        
        else:
            raise ValueError(f"Unsupported export format: {format_type}")
    
    except Exception as e:
        st.error(f"Export failed: {str(e)}")
        raise
