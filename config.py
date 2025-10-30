from pydantic_settings import BaseSettings ,SettingsConfigDict

class APPConfig(BaseSettings): 
    APP_NAME: str = "FAQ-Bill-Saver-ai" 
    VERSION: str = "0.0.1" 

    ## apis keys 
    GEMINAI_API_KEY: str 
    NOMIC_KEY: str 
    TAVILY_KEY: str


    ### chroma configs
    CHROMA_PERSIST_DIR:str = "/chroma_db"
    COLLECTION_NAME: str = "semantic_cache"


    model_config= SettingsConfigDict(
        env_file = ".env" ,
        env_file_encoding = "utf-8",
        extra= "ignore"
    )

try:
    settings = APPConfig()
except Exception as e:
    print(f"Failed to load configuration: {e}")