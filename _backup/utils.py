# utils.py
import json
from openai import OpenAI
import streamlit as st
from pydantic import BaseModel

# --- Schema ---
class NutritionSchema(BaseModel):
    energy: float
    protein: float
    fat: float
    sugar: float
    sugar_type: float
    fiber: float
    salt: float

class RecipeResponseSchema(BaseModel):
    title: str
    cook_time: str
    ingredients: str
    seasonings: str
    instructions: str
    point: str
    nutrition: NutritionSchema

# --- 🚀 高速化関数 ---
@st.cache_data
def load_json_cached(filepath, default):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return default

def save_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    st.cache_data.clear()

@st.cache_resource
def get_openai_client():
    api_key = st.secrets["OPENAI_API_KEY"]
    return OpenAI(api_key=api_key)
