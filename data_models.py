from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import inspect
import pandas as pd

class DataField(BaseModel):
    """Class representing a single data field"""
    name: str
    description: str
    type: str
    available_types: List[str] = Field(default_factory=list)
    options: Dict[str, Any] = Field(default_factory=dict)
    
    def copy(self, **kwargs):
        """Create a copy of the field with updates"""
        return self.__class__(**{**self.dict(), **kwargs})

class DataModel(BaseModel):
    """Class representing a complete data model"""
    name: str
    description: str
    category: str
    fields: List[DataField]
    schema: Dict[str, Any] = Field(default_factory=dict)
    
    @property
    def field_names(self) -> List[str]:
        return [field.name for field in self.fields]

def get_available_models(search_term: str = "") -> List[DataModel]:
    """Get available data models filtered by search term"""
    # نماذج افتراضية (يمكن استبدالها بقاعدة بيانات حقيقية)
    models = [
        DataModel(
            name="Customer Data",
            description="Complete customer information with demographics",
            category="Business",
            fields=[
                DataField(
                    name="customer_id",
                    description="Unique customer identifier",
                    type="uuid",
                    available_types=["uuid", "integer", "string"]
                ),
                DataField(
                    name="name",
                    description="Customer full name",
                    type="name",
                    available_types=["name", "string"]
                ),
                # يمكن إضافة المزيد من الحقول
            ]
        ),
        # يمكن إضافة المزيد من النماذج
    ]
    
    if search_term:
        search_term = search_term.lower()
        models = [
            m for m in models
            if (search_term in m.name.lower() or 
                search_term in m.description.lower() or 
                search_term in m.category.lower())
        ]
    
    return models
