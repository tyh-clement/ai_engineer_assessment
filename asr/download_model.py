import argparse

from dotenv import load_dotenv
from huggingface_hub import snapshot_download

from asr_model import MODEL_NAME, get_model_dir

load_dotenv()  # picks up HF_TOKEN / MODEL_DIR from .env


def main() -> None:
    parser = argparse.ArgumentParser(description=f"Download {MODEL_NAME} locally.")
    parser.add_argument(
        "--model-dir",
        help="Base directory for models (default: $MODEL_DIR or <repo root>/models). "
        f"The model is stored in <model-dir>/{MODEL_NAME.split('/')[-1]}.",
    )
    args = parser.parse_args()

    target = get_model_dir(args.model_dir)
    snapshot_download(
        repo_id=MODEL_NAME,
        local_dir=target,
        allow_patterns=["*.json", "*.txt", "pytorch_model.bin"],
    )
    print(f"Model downloaded to {target}")


if __name__ == "__main__":
    main()
