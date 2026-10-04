import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "MrVoice AI Coach & Singing Engine"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Target Voice Profile (Low Baritone / Bass)
    TARGET_F0_MIN: float = 80.0   # Hz (E2)
    TARGET_F0_MAX: float = 120.0  # Hz (B2)
    OPTIMAL_F0: float = 95.0      # Hz
    
    # Audio Processing Settings
    SAMPLE_RATE: int = 22050
    CHUNK_SIZE: int = 1024
    HOP_LENGTH: int = 512
    N_FFT: int = 2048
    
    # Paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    MODELS_DIR: str = os.path.join(BASE_DIR, "..", "models")
    DATASET_DIR: str = os.path.join(BASE_DIR, "..", "dataset")
    
    class Config:
        case_sensitive = True

settings = Settings()
