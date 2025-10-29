from pydantic_settings import Basesettings 

class APPConfig(Basesettings): 
    APP_NAME: str = "FAQ-Bill-Saver-ai" 
    VERSION: str = "0.0.1" 

    ## apis keys 
    GEMINAI_API_KEY: str 
    NOMIC_KEY: str 
    TAVILY_KEY: str
        

    class Config: 
        env_file = ".env" 
        env_file_encoding = "utf-8"
        extra= "ignore"

settings= APPConfig() 
