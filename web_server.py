import json
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from typing import Any, Dict
from urllib.parse import parse_qs, urlparse

from TeacherController import TeacherController
from TeacherCreateController import TeacherCreateController
from TeacherUpdateController import TeacherUpdateController
from TeacherDeleteController import TeacherDeleteController

BASE_DIR = Path(__file__).parent
PUBLIC_DIR = BASE_DIR / "public"


class TeacherRequestHandler(SimpleHTTPRequestHandler):
    """HTTP обработчик: отдает статику и API на основе контроллера."""

    controller = TeacherController()
    create_controller = TeacherCreateController()
    update_controller = TeacherUpdateController()
    delete_controller = TeacherDeleteController()

    def __init__(self, *args, directory: str | None = None, **kwargs) -> None:
        directory = directory or str(PUBLIC_DIR)
        super().__init__(*args, directory=directory, **kwargs)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)

        if parsed.path == "/api/teachers":
            self._handle_teachers_list(parsed)
            return

        if parsed.path.startswith("/api/teachers/"):
            self._handle_teacher_detail(parsed)
            return

        if parsed.path == "/":
            self.path = "/index.html"

        super().do_GET()

    def do_POST(self) -> None:
        parsed = urlparse(self.path)

        if parsed.path == "/api/teachers":
            self._handle_teacher_create()
            return

        self.send_error(404, "Not Found")

    def do_PUT(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/teachers/"):
            self._handle_teacher_update(parsed)
            return
        self.send_error(404, "Not Found")

    def do_DELETE(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/teachers/"):
            self._handle_teacher_delete(parsed)
            return
        self.send_error(404, "Not Found")

    def _handle_teachers_list(self, parsed) -> None:
        query = parse_qs(parsed.query)
        page = self._safe_int(query.get("page", [1])[0], default=1)
        page_size_raw = query.get("page_size", [None])[0]
        page_size = self._safe_int(page_size_raw) if page_size_raw is not None else None

        payload = self.controller.get_short_teachers(page_size=page_size, page=page)
        self._send_json(payload)

    def _handle_teacher_detail(self, parsed) -> None:
        try:
            teacher_id = int(parsed.path.rstrip("/").split("/")[-1])
        except ValueError:
            self._send_json({"error": "Некорректный идентификатор"}, status=400)
            return

        teacher = self.controller.get_teacher(teacher_id)
        if teacher is None:
            self._send_json({"error": "Преподаватель не найден"}, status=404)
            return

        self._send_json(teacher)

    def _handle_teacher_create(self) -> None:
        payload = self._read_json_body()
        if payload is None:
            self._send_json({"error": "Некорректный JSON"}, status=400)
            return

        result = self.create_controller.create_teacher(payload)
        status = 200 if result.get("success") else 400
        self._send_json(result, status=status)

    def _handle_teacher_update(self, parsed) -> None:
        try:
            teacher_id = int(parsed.path.rstrip("/").split("/")[-1])
        except ValueError:
            self._send_json({"error": "Некорректный идентификатор"}, status=400)
            return

        payload = self._read_json_body()
        if payload is None:
            self._send_json({"error": "Некорректный JSON"}, status=400)
            return

        result = self.update_controller.update_teacher(teacher_id, payload)
        status = 200 if result.get("success") else 400
        self._send_json(result, status=status)

    def _handle_teacher_delete(self, parsed) -> None:
        try:
            teacher_id = int(parsed.path.rstrip("/").split("/")[-1])
        except ValueError:
            self._send_json({"error": "Некорректный идентификатор"}, status=400)
            return

        result = self.delete_controller.delete_teacher(teacher_id)
        status = 200 if result.get("success") else 400
        self._send_json(result, status=status)

    def _safe_int(self, value: Any, default: int | None = None) -> int | None:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def _send_json(self, payload: Dict[str, Any], status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self) -> Dict[str, Any] | None:
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length)
            if not raw_body:
                return {}
            return json.loads(raw_body.decode("utf-8"))
        except Exception:
            return None

    def log_message(self, format: str, *args) -> None:
        """Тише лог, чтобы не захламлять вывод."""
        return


def run_server(host: str = "127.0.0.1", port: int = 8000) -> None:
    handler = partial(TeacherRequestHandler, directory=str(PUBLIC_DIR))
    with HTTPServer((host, port), handler) as httpd:
        print(f"Сервер запущен: http://{host}:{port}")
        print("Ctrl+C для остановки")
        httpd.serve_forever()


if __name__ == "__main__":
    run_server()
