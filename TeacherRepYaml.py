import os

import yaml

from BaseTeacherRepository import BaseTeacherRepository


class TeacherRepYaml(BaseTeacherRepository):
    def __init__(self, yaml_file="teachers.yaml"):
        super().__init__(yaml_file)

    def _ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                yaml.dump([], f, allow_unicode=True, default_flow_style=False, indent=2)

    def read_all(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or []
        return []

    def write_all(self, data):
        with open(self.file_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False, indent=2)
        return "ок"
