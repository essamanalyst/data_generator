import pandas as pd
import numpy as np
from typing import Dict, Any
from data_models import DataModel
import random
from faker import Faker
import uuid

fake = Faker()

def generate_data(model: DataModel, rows: int, batch_size: int = 1000, seed: int = None) -> pd.DataFrame:
    """Generate data based on the specified model"""
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
        Faker.seed(seed)
    
    data = {}
    for field in model.fields:
        data[field.name] = []
    
    for _ in range(rows):
        for field in model.fields:
            if field.type == "uuid":
                data[field.name].append(str(uuid.uuid4()))
            elif field.type == "name":
                data[field.name].append(fake.name())
            elif field.type == "email":
                data[field.name].append(fake.email())
            # يمكن إضافة المزيد من أنواع الحقول
            
    return pd.DataFrame(data)
