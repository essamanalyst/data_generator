import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Callable
from data_models import DataModel
import random
from faker import Faker
import uuid
import time
from concurrent.futures import ThreadPoolExecutor

fake = Faker()

def generate_field_data(field: DataField, batch_size: int) -> list:
    """Generate data for a single field efficiently"""
    if field.type == "uuid":
        return [str(uuid.uuid4()) for _ in range(batch_size)]
    elif field.type == "name":
        return [fake.name() for _ in range(batch_size)]
    elif field.type == "email":
        return [fake.email() for _ in range(batch_size)]
    elif field.type == "integer":
        if 'min' in field.options and 'max' in field.options:
            return np.random.randint(field.options['min'], field.options['max'], batch_size).tolist()
        return np.random.randint(0, 100, batch_size).tolist()
    elif field.type == "float":
        if 'min' in field.options and 'max' in field.options:
            return np.round(np.random.uniform(field.options['min'], field.options['max'], batch_size), 2).tolist()
        return np.round(np.random.uniform(0, 100, batch_size), 2).tolist()
    return ["" for _ in range(batch_size)]

def generate_data(
    model: DataModel,
    rows: int,
    batch_size: int = 10000,  # Increased default batch size
    seed: int = None,
    progress_callback: Optional[Callable[[float], None]] = None,
    max_workers: int = 4
) -> pd.DataFrame:
    """Generate data based on the specified model with progress reporting"""
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
        Faker.seed(seed)
    
    data = {}
    total_batches = (rows + batch_size - 1) // batch_size
    
    for batch_num in range(total_batches):
        current_batch_size = min(batch_size, rows - batch_num * batch_size)
        
        # Use threading for parallel field generation
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = {
                field.name: executor.submit(generate_field_data, field, current_batch_size)
                for field in model.fields
            }
            
            for field_name, future in results.items():
                if field_name not in data:
                    data[field_name] = []
                data[field_name].extend(future.result())
        
        if progress_callback:
            progress = (batch_num + 1) / total_batches
            progress_callback(progress)
    
    return pd.DataFrame(data)
