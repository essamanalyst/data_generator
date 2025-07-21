from pydantic import BaseModel, Field
from typing import List, Dict, Any
from functools import lru_cache
import pandas as pd
import streamlit as st

class DataField(BaseModel):
    name: str
    description: str
    type: str
    available_types: List[str] = Field(default_factory=list)
    options: Dict[str, Any] = Field(default_factory=dict)
    
    def copy(self, **kwargs):
        return self.__class__(**{**self.dict(), **kwargs})

class DataModel(BaseModel):
    name: str
    description: str
    category: str
    fields: List[DataField]
    schema: Dict[str, Any] = Field(default_factory=dict)
    
    @property
    def field_names(self) -> List[str]:
        return [field.name for field in self.fields]

@st.cache_data
def _load_sample_models() -> List[DataModel]:
    """Load sample data models with caching"""
    return [
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
                DataField(
                    name="email",
                    description="Customer email",
                    type="email",
                    available_types=["email", "string"]
                ),
                DataField(
                    name="age",
                    description="Customer age",
                    type="integer",
                    available_types=["integer", "range"],
                    options={"min": 18, "max": 100}
                )
            ]
        ),
        DataModel(
            name="Product Data",
            description="Product inventory information",
            category="E-commerce",
            fields=[
                DataField(
                    name="product_id",
                    description="Product identifier",
                    type="integer",
                    available_types=["integer", "string"]
                ),
                DataField(
                    name="product_name",
                    description="Product name",
                    type="string",
                    available_types=["string"]
                ),
                DataField(
                    name="price",
                    description="Product price",
                    type="float",
                    available_types=["float", "integer"],
                    options={"min": 0, "max": 10000}
                )
            ]
        )
    ]

@st.cache_data
def get_available_models(search_term: str = "") -> List[DataModel]:
    """Get available data models with search functionality"""
    all_models = _load_sample_models()
    
    if not search_term:
        return all_models
    
    search_term = search_term.lower()
    return [
        m for m in all_models
        if (search_term in m.name.lower() or 
            search_term in m.description.lower() or 
            search_term in m.category.lower())
    ]
