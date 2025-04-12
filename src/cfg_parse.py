import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent 

model_base_path = (BASE_DIR / ".." / "models" / "RENE").resolve()
data_base_path = (BASE_DIR / ".." / "data").resolve()

cfg = yaml.safe_load(open(model_base_path / 'cfg.yaml'))
class_file = [line.split('|')[0] for line in open(model_base_path / 'class-id.txt').read().splitlines()]
models_folder_path = model_base_path