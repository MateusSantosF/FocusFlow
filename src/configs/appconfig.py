from pydantic_settings import BaseSettings
import streamlit as st

class AppConfig(BaseSettings):
    OPENAI_API_KEY: str = st.secrets["openai_key"]
    VECTOR_STORAGE_DIR: str = "./vector_storage/"
    TRAINING_DATA_DIR: str = "./training_data/"
    DATABASE_FILE_NAME: str = "vector_store.duckdb"

appConfig = AppConfig() # type: ignore