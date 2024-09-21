from pydantic_settings import BaseSettings

class AppConfig(BaseSettings):
    OPENAI_API_KEY: str
    VECTOR_STORAGE_DIR: str = "./vector_storage"
    TRAINING_DATA_DIR: str = "./training_data"

appConfig = AppConfig() # type: ignore