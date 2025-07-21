from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional
from enum import Enum
import pandas as pd
import streamlit as st

class FieldType(str, Enum):
    UUID = "uuid"
    NAME = "name"
    EMAIL = "email"
    INTEGER = "integer"
    FLOAT = "float"
    STRING = "string"
    BOOLEAN = "boolean"
    DATE = "date"
    DATETIME = "datetime"
    CATEGORY = "category"

class DataField(BaseModel):
    name: str
    description: str
    type: FieldType = FieldType.STRING
    required: bool = True
    unique: bool = False
    available_types: List[FieldType] = Field(default_factory=list)
    options: Dict[str, Any] = Field(default_factory=dict)
    
    @validator('available_types', pre=True, always=True)
    def set_available_types(cls, v, values):
        if not v:
            return [values.get('type', FieldType.STRING)]
        return v
    
    def copy(self, **kwargs):
        return self.__class__(**{**self.dict(), **kwargs})

class DataModel(BaseModel):
    name: str
    description: str
    category: str
    fields: List[DataField]
    schema: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)
    
    @property
    def field_names(self) -> List[str]:
        return [field.name for field in self.fields]
    
    def add_field(self, field: DataField):
        self.fields.append(field)
        return self
    
    def remove_field(self, field_name: str):
        self.fields = [f for f in self.fields if f.name != field_name]
        return self

@st.cache_data
def suggest_fields(search_term: str) -> List[DataField]:
    """Suggest relevant fields based on search terms"""
    suggestions = {
        "customer": [
            DataField(name="customer_id", description="Unique customer identifier", type=FieldType.UUID),
            DataField(name="name", description="Customer full name", type=FieldType.NAME),
            DataField(name="email", description="Customer email", type=FieldType.EMAIL),
            DataField(name="age", description="Customer age", type=FieldType.INTEGER, options={"min": 18, "max": 100}),
            DataField(name="is_active", description="Customer active status", type=FieldType.BOOLEAN)
        ],
        "product": [
            DataField(name="product_id", description="Product identifier", type=FieldType.INTEGER),
            DataField(name="product_name", description="Product name", type=FieldType.STRING),
            DataField(name="price", description="Product price", type=FieldType.FLOAT, options={"min": 0}),
            DataField(name="category", description="Product category", type=FieldType.CATEGORY)
        ],
        "transaction": [
            DataField(name="transaction_id", description="Transaction identifier", type=FieldType.UUID),
            DataField(name="amount", description="Transaction amount", type=FieldType.FLOAT),
            DataField(name="date", description="Transaction date", type=FieldType.DATE),
            DataField(name="status", description="Transaction status", type=FieldType.CATEGORY)
        ]
    }
    
    search_term = search_term.lower()
    suggested_fields = []
    
    for key, fields in suggestions.items():
        if key in search_term:
            suggested_fields.extend(fields)
    
    # Add some general fields if no specific matches
    if not suggested_fields:
        suggested_fields.extend([
            DataField(name="id", description="Unique identifier", type=FieldType.UUID),
            DataField(name="created_at", description="Creation timestamp", type=FieldType.DATETIME),
            DataField(name="updated_at", description="Last update timestamp", type=FieldType.DATETIME)
        ])
    
    return suggested_fields

@st.cache_data
def _load_sample_models() -> List[DataModel]:
    """Load sample data models with enhanced examples"""
    models = [
        DataModel(
            name="Customer Data",
            description="Complete customer information with demographics",
            category="Business",
            tags=["customer", "user", "profile"],
            fields=[
                DataField(
                    name="customer_id",
                    description="Unique customer identifier",
                    type=FieldType.UUID,
                    available_types=[FieldType.UUID, FieldType.INTEGER, FieldType.STRING]
                ),
                DataField(
                    name="name",
                    description="Customer full name",
                    type=FieldType.NAME,
                    available_types=[FieldType.NAME, FieldType.STRING]
                ),
                DataField(
                    name="email",
                    description="Customer email",
                    type=FieldType.EMAIL,
                    available_types=[FieldType.EMAIL, FieldType.STRING]
                ),
                DataField(
                    name="age",
                    description="Customer age",
                    type=FieldType.INTEGER,
                    available_types=[FieldType.INTEGER, FieldType.FLOAT],
                    options={"min": 18, "max": 100}
                )
            ]
        ),
        DataModel(
            name="Product Data",
            description="Product inventory information",
            category="E-commerce",
            tags=["product", "inventory", "items"],
            fields=[
                DataField(
                    name="product_id",
                    description="Product identifier",
                    type=FieldType.INTEGER,
                    available_types=[FieldType.INTEGER, FieldType.STRING]
                ),
                DataField(
                    name="product_name",
                    description="Product name",
                    type=FieldType.STRING,
                    available_types=[FieldType.STRING]
                ),
                DataField(
                    name="price",
                    description="Product price",
                    type=FieldType.FLOAT,
                    available_types=[FieldType.FLOAT, FieldType.INTEGER],
                    options={"min": 0, "max": 10000}
                )
            ]
        )
    ]
    return models

@st.cache_data
def get_available_models(search_term: str = "") -> List[DataModel]:
    """Get available data models with enhanced search functionality"""
    all_models = _load_sample_models()
    
    if not search_term:
        return all_models
    
    search_term = search_term.lower()
    results = []
    
    for model in all_models:
        # Search in name, description, category
        if (search_term in model.name.lower() or 
            search_term in model.description.lower() or 
            search_term in model.category.lower()):
            results.append(model)
            continue
        
        # Search in tags
        if any(search_term in tag.lower() for tag in model.tags):
            results.append(model)
            continue
        
        # Search in field names and descriptions
        if any(search_term in field.name.lower() or 
               search_term in field.description.lower() 
               for field in model.fields):
            results.append(model)
    
    return results
