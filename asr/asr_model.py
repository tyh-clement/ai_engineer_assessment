import os
from pathlib import Path

import numpy as np
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from transformers.utils import logging
logging.set_verbosity_error()


MODEL_NAME = "facebook/wav2vec2-large-960h"
SAMPLE_RATE = 16000
REPO_ROOT = Path(__file__).resolve().parent.parent


def get_model_dir(base_dir: str | os.PathLike | None = None) -> Path:
    """Local directory holding the model: <base>/<model name>.

    Base defaults to $MODEL_DIR, falling back to <repo root>/models.
    """
    base = base_dir or os.environ.get("MODEL_DIR") or REPO_ROOT / "models"
    return Path(base).expanduser().resolve() / MODEL_NAME.split("/")[-1]


class ASRModel:
    def __init__(self, model_dir: str | os.PathLike | None = None):
        path = Path(model_dir) if model_dir else get_model_dir()
        if not path.is_dir():
            raise FileNotFoundError(
                f"Model not found at {path}. Run `python asr/download_model.py` first."
            )
        self.processor = Wav2Vec2Processor.from_pretrained(path, local_files_only=True)
        self.model = Wav2Vec2ForCTC.from_pretrained(path, local_files_only=True).eval()

    def transcribe(self, audio: np.ndarray) -> str:
        """Transcribe a mono 16 kHz float waveform."""
        inputs = self.processor(audio, sampling_rate=SAMPLE_RATE, return_tensors="pt")
        with torch.no_grad():
            logits = self.model(inputs.input_values).logits
        ids = torch.argmax(logits, dim=-1)
        return self.processor.batch_decode(ids)[0]