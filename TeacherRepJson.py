import json
import os

from BaseTeacherRepository import BaseTeacherRepository


class TeacherRepJson(BaseTeacherRepository):
    def __init__(self, json_file="teachers.json"):
        super().__init__(json_file)

    def _ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def read_all(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def write_all(self, data):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return "ок"
