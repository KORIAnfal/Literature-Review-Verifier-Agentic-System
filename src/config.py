import pathlib
import yaml
from dotenv import load_dotenv

load_dotenv()

ROOT = pathlib.Path(__file__).resolve().parent.parent
with open(ROOT / "config.yaml", encoding="utf-8") as f:
    CFG = yaml.safe_load(f)