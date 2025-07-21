import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Callable
from data_models import DataModel
import random
from faker import Faker
import uuid
import time

fake = Faker()

def generate_data(
    model: DataModel,
    rows: int,
    batch_size: int = 1000,
    seed: int = None,
    progress_callback: Optional[Callable[[float], None]] = None
) -> pd.DataFrame:
    """Generate data based on the specified model with progress reporting"""
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
        Faker.seed(seed)
    
    data = {field.name: [] for field in model.fields}
    total_batches = (rows + batch_size - 1) // batch_size
    
    for batch_num in range(total_batches):
        current_batch_size = min(batch_size, rows - batch_num * batch_size)
        
        for field in model.fields:
            if field.type == "uuid":
                data[field.name].extend([str(uuid.uuid4()) for _ in range(current_batch_size)])
            elif field.type == "name":
                data[field.name].extend([fake.name() for _ in range(current_batch_size)])
            elif field.type == "email":
                data[field.name].extend([fake.email() for _ in range(current_batch_size)])
            elif field.type == "integer":
                data[field.name].extend([random.randint(0, 100) for _ in range(current_batch_size)])
            elif field.type == "float":
                data[field.name].extend([round(random.uniform(0, 100), 2) for _ in range(current_batch_size)])
            else:
                data[field.name].extend(["" for _ in range(current_batch_size)])
        
        if progress_callback:
            progress = (batch_num + 1) / total_batches
            progress_callback(progress)
    
    return pd.DataFrame(data)
