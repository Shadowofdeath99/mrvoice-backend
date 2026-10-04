import numpy as np
import librosa
from app.core.config import settings

class PitchService:
    def __init__(self, sample_rate: int = settings.SAMPLE_RATE):
        self.sr = sample_rate

    def analyze_chunk(self, audio_data: np.ndarray) -> dict:
        if len(audio_data) < settings.N_FFT:
            return {"status": "insufficient_data", "f0": 0.0}

        rms = librosa.feature.rms(y=audio_data)[0]
        mean_energy = float(np.mean(rms))
        
        if mean_energy < 0.01:
            return {
                "status": "silence",
                "f0": 0.0,
                "energy": mean_energy,
                "in_target_zone": False
            }

        f0, voiced_flag, _ = librosa.pyin(
            audio_data,
            fmin=60,
            fmax=200,
            sr=self.sr,
            frame_length=settings.N_FFT,
            hop_length=settings.HOP_LENGTH
        )

        valid_f0 = f0[voiced_flag & ~np.isnan(f0)] if f0 is not None else []
        
        if len(valid_f0) == 0:
            return {
                "status": "unvoiced",
                "f0": 0.0,
                "energy": mean_energy,
                "in_target_zone": False
            }

        current_f0 = float(np.mean(valid_f0))
        in_zone = settings.TARGET_F0_MIN <= current_f0 <= settings.TARGET_F0_MAX

        return {
            "status": "voiced",
            "f0": round(current_f0, 2),
            "energy": round(mean_energy, 4),
            "in_target_zone": in_zone,
            "target_min": settings.TARGET_F0_MIN,
            "target_max": settings.TARGET_F0_MAX
        }

pitch_service = PitchService()
