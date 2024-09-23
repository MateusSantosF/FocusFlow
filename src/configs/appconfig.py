from pydantic_settings import BaseSettings
import streamlit as st

class AppConfig(BaseSettings):
    OPENAI_API_KEY: str = st.secrets["openai_key"]
    VECTOR_STORAGE_DIR: str = "./vector_storage/"
    TRAINING_DATA_DIR: str = "./training_data/"

appConfig = AppConfig() # type: ignore