const params = new URLSearchParams(window.location.search);
const mode = params.get("mode") === "edit" ? "edit" : "add";
const teacherId = mode === "edit" ? Number(params.get("id")) : null;

class FormValidator {
    static emailPattern = /^[\w.-]+@[\w.-]+\.\w+$/;

    static validate(payload) {
        const required = [
            "first_name",
            "last_name",
            "email",
            "academic_degree",
            "administrative_position",
            "experience_years",
        ];

        const missing = required.filter((field) => !payload[field] || payload[field].trim() === "");
        if (missing.length) {
            return `Заполните поля: ${missing.join(", ")}`;
        }

        if (!FormValidator.emailPattern.test(payload.email)) {
            return "Некорректный email";
        }

        const experience = Number(payload.experience_years);
        if (!Number.isInteger(experience) || experience < 0) {
            return "Стаж должен быть неотрицательным целым числом";
        }

        return null;
    }
}

class TeacherFormView {
    constructor(form, statusEl, titleEl, modeLabel, submitBtn) {
        this.form = form;
        this.statusEl = statusEl;
        this.titleEl = titleEl;
        this.modeLabel = modeLabel;
        this.submitBtn = submitBtn;
        this.successFlag = false;
        this.submitHandler = () => {};

        this.form.addEventListener("submit", (event) => {
            event.preventDefault();
            const payload = this.getPayload();
            this.submitHandler(payload);
        });
    }

    onSubmit(handler) {
        this.submitHandler = handler;
    }

    showForm() {
        this.form.classList.remove("hidden");
    }

    setMode(mode, id) {
        if (mode === "edit") {
            this.modeLabel.textContent = "Редактирование";
            this.titleEl.textContent = "Редактирование преподавателя";
            this.submitBtn.textContent = "Сохранить изменения";
            if (id) {
                this.statusEl.textContent = `ID: ${id}`;
            }
        } else {
            this.modeLabel.textContent = "Создание";
            this.titleEl.textContent = "Новый преподаватель";
            this.submitBtn.textContent = "Сохранить";
            this.statusEl.textContent = "Заполните все поля";
        }
    }

    setStatus(message) {
        this.statusEl.textContent = message;
    }

    fillForm(data) {
        this.form.elements.first_name.value = data.first_name || "";
        this.form.elements.last_name.value = data.last_name || "";
        this.form.elements.email.value = data.email || "";
        this.form.elements.academic_degree.value = data.academic_degree || "";
        this.form.elements.administrative_position.value = data.administrative_position || "";
        this.form.elements.experience_years.value = data.experience_years ?? "";
    }

    getPayload() {
        const formData = new FormData(this.form);
        return Object.fromEntries(formData.entries());
    }

    notifyOpener(type) {
        if (window.opener && typeof window.opener.postMessage === "function") {
            window.opener.postMessage({ type }, "*");
        }
    }
}

class AddFormController {
    constructor(view) {
        this.view = view;
        this.success = false;
    }

    init() {
        this.view.setMode("add");
        this.view.showForm();
        this.view.onSubmit((payload) => this.handleSubmit(payload));
        window.addEventListener("beforeunload", () => {
            this.view.notifyOpener(this.success ? "teacher-added" : "refresh-main");
        });
    }

    async handleSubmit(payload) {
        const error = FormValidator.validate(payload);
        if (error) {
            this.view.setStatus(error);
            return;
        }

        try {
            const response = await fetch("/api/teachers", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    ...payload,
                    experience_years: Number(payload.experience_years),
                }),
            });
            const data = await response.json();
            if (!response.ok || !data.success) {
                throw new Error(data.message || "Не удалось сохранить");
            }
            this.success = true;
            this.view.setStatus(`Сохранено. ID: ${data.id}. Окно закроется.`);
            this.view.notifyOpener("teacher-added");
            setTimeout(() => window.close(), 700);
        } catch (err) {
            this.view.setStatus(err.message);
        }
    }
}

class EditFormController {
    constructor(view, teacherId) {
        this.view = view;
        this.teacherId = teacherId;
        this.success = false;
    }

    init() {
        if (!this.teacherId) {
            this.view.setStatus("Некорректный идентификатор");
            return;
        }
        this.view.setMode("edit", this.teacherId);
        this.loadTeacher();
        this.view.onSubmit((payload) => this.handleSubmit(payload));
        window.addEventListener("beforeunload", () => {
            this.view.notifyOpener(this.success ? "teacher-updated" : "refresh-main");
        });
    }

    async loadTeacher() {
        this.view.setStatus("Загружаем данные...");
        try {
            const response = await fetch(`/api/teachers/${this.teacherId}`);
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.error || "Не удалось загрузить данные");
            }
            this.view.fillForm(data);
            this.view.showForm();
            this.view.setStatus(`ID: ${this.teacherId}`);
        } catch (err) {
            this.view.setStatus(err.message);
        }
    }

    async handleSubmit(payload) {
        const error = FormValidator.validate(payload);
        if (error) {
            this.view.setStatus(error);
            return;
        }

        try {
            const response = await fetch(`/api/teachers/${this.teacherId}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    ...payload,
                    experience_years: Number(payload.experience_years),
                }),
            });
            const data = await response.json();
            if (!response.ok || !data.success) {
                throw new Error(data.message || "Не удалось обновить");
            }
            this.success = true;
            this.view.setStatus("Изменения сохранены. Окно закроется.");
            this.view.notifyOpener("teacher-updated");
            setTimeout(() => window.close(), 700);
        } catch (err) {
            this.view.setStatus(err.message);
        }
    }
}

const formEl = document.getElementById("teacher-form");
const statusEl = document.getElementById("status");
const titleEl = document.getElementById("title");
const modeLabel = document.getElementById("mode-label");
const submitBtn = document.getElementById("submit-btn");
const cancelBtn = document.getElementById("cancel-btn");

const view = new TeacherFormView(formEl, statusEl, titleEl, modeLabel, submitBtn);
cancelBtn.addEventListener("click", () => window.close());

if (mode === "edit") {
    new EditFormController(view, teacherId).init();
} else {
    new AddFormController(view).init();
}
