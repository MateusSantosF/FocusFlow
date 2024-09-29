from pydantic_settings import BaseSettings
import streamlit as st

class AppConfig(BaseSettings):
    OPENAI_API_KEY: str = st.secrets["openai_key"]
    DATABASE_URL: str = st.secrets["database_url"]
    SUPABASE_URL: str = st.secrets["supabase_url"]
    SUPABASE_KEY: str = st.secrets["supabase_key"]
    SUPABASE_VECTORS_COLLECTION: str = "embeddings"

appConfig = AppConfig() # type: ignore