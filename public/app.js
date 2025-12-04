class TeacherRepositoryClient {
    constructor(baseUrl = "/api") {
        this.baseUrl = baseUrl;
        this.subscribers = { list: [], detail: [], deleted: [], error: [] };
    }

    subscribe(event, handler) {
        if (!this.subscribers[event]) {
            this.subscribers[event] = [];
        }
        this.subscribers[event].push(handler);
    }

    _notify(event, payload) {
        (this.subscribers[event] || []).forEach((handler) => handler(payload));
    }

    async loadList(page = 1) {
        try {
            const response = await fetch(`${this.baseUrl}/teachers?page=${page}`);
            if (!response.ok) {
                const payload = await response.json().catch(() => ({}));
                throw new Error(payload.error || "Не удалось загрузить список преподавателей");
            }
            const data = await response.json();
            this._notify("list", data);
        } catch (err) {
            this._notify("error", { message: err.message, scope: "list" });
        }
    }

    async loadTeacher(id) {
        try {
            const response = await fetch(`${this.baseUrl}/teachers/${id}`);
            if (!response.ok) {
                const payload = await response.json().catch(() => ({}));
                throw new Error(payload.error || "Не удалось получить карточку");
            }
            const data = await response.json();
            this._notify("detail", data);
        } catch (err) {
            this._notify("error", { message: err.message, scope: "detail" });
        }
    }

    async deleteTeacher(id) {
        try {
            const response = await fetch(`${this.baseUrl}/teachers/${id}`, {
                method: "DELETE",
            });
            const data = await response.json();
            if (!response.ok || !data.success) {
                throw new Error(data.message || "Не удалось удалить");
            }
            this._notify("deleted", { id });
        } catch (err) {
            this._notify("error", { message: err.message, scope: "delete" });
        }
    }
}

class TeacherTableView {
    constructor(bodyElement, statusElement, refreshButton) {
        this.bodyElement = bodyElement;
        this.statusElement = statusElement;
        this.refreshButton = refreshButton;
        this.onSelect = () => {};
    }

    bindSelect(handler) {
        this.onSelect = handler;
    }

    bindRefresh(handler) {
        if (this.refreshButton) {
            this.refreshButton.addEventListener("click", () => handler());
        }
    }

    render(payload) {
        const { items = [], total = 0, page = 1, page_size: pageSize = items.length } = payload;
        this.bodyElement.innerHTML = "";

        if (items.length === 0) {
            const row = document.createElement("tr");
            const cell = document.createElement("td");
            cell.colSpan = 7;
            cell.textContent = "Данные не найдены";
            cell.classList.add("muted");
            row.appendChild(cell);
            this.bodyElement.appendChild(row);
        } else {
            items.forEach((item) => {
                const row = document.createElement("tr");
                row.dataset.id = item.id;
                row.innerHTML = `
                    <td>${item.id}</td>
                    <td>${item.last_name || "—"}</td>
                    <td>${item.first_initial || "—"}</td>
                    <td><span class="pill">${item.academic_degree || "—"}</span></td>
                    <td>${item.administrative_position || "—"}</td>
                    <td>${item.email || "—"}</td>
                    <td>${item.experience_years ?? "—"} лет</td>
                `;
                row.addEventListener("click", () => this.onSelect(item.id));
                this.bodyElement.appendChild(row);
            });
        }

        this.statusElement.textContent = `Всего: ${total} · Страница ${page} · Элементов на странице: ${pageSize}`;
    }

    showStatus(message) {
        this.statusElement.textContent = message;
    }
}

class TeacherDetailView {
    constructor(overlayElement, contentElement, closeButton, openTabButton, editButton, deleteButton, titleElement) {
        this.overlayElement = overlayElement;
        this.contentElement = contentElement;
        this.closeButton = closeButton;
        this.openTabButton = openTabButton;
        this.editButton = editButton;
        this.deleteButton = deleteButton;
        this.titleElement = titleElement;
        this.currentId = null;
        this.onEdit = () => {};
        this.onDelete = () => {};

        this.closeButton.addEventListener("click", () => this.hide());
        this.overlayElement.addEventListener("click", (event) => {
            if (event.target === this.overlayElement) {
                this.hide();
            }
        });
        this.openTabButton.addEventListener("click", () => {
            if (this.currentId) {
                window.open(`detail.html?id=${this.currentId}`, "_blank");
            }
        });
        if (this.editButton) {
            this.editButton.addEventListener("click", () => {
                if (this.currentId) {
                    this.onEdit(this.currentId);
                }
            });
        }
        if (this.deleteButton) {
            this.deleteButton.addEventListener("click", () => {
                if (this.currentId) {
                    this.onDelete(this.currentId);
                }
            });
        }
    }

    showLoading(id) {
        this.currentId = id;
        this.titleElement.textContent = "Загружаем карточку…";
        this.contentElement.innerHTML = `<p class="muted">Получаем данные для ID ${id}</p>`;
        this.overlayElement.classList.remove("hidden");
    }

    show(teacher) {
        this.currentId = teacher.id_teacher;
        this.titleElement.textContent = `${teacher.last_name} ${teacher.first_name}`;
        this.contentElement.innerHTML = `
            ${this._detailBlock("Фамилия", teacher.last_name)}
            ${this._detailBlock("Имя", teacher.first_name)}
            ${this._detailBlock("Email", teacher.email)}
            ${this._detailBlock("Ученая степень", teacher.academic_degree)}
            ${this._detailBlock("Должность", teacher.administrative_position)}
            ${this._detailBlock("Стаж", `${teacher.experience_years} лет`)}
            ${this._detailBlock("ID", teacher.id_teacher)}
        `;
        this.overlayElement.classList.remove("hidden");
    }

    showError(message) {
        this.titleElement.textContent = "Ошибка";
        this.contentElement.innerHTML = `<p class="muted">${message}</p>`;
        this.overlayElement.classList.remove("hidden");
    }

    hide() {
        this.overlayElement.classList.add("hidden");
    }

    _detailBlock(label, value) {
        return `
            <div class="detail__item">
                <p class="detail__label">${label}</p>
                <p class="detail__value">${value ?? "—"}</p>
            </div>
        `;
    }
}

class UiController {
    constructor(repository, tableView, detailView, addButton) {
        this.repository = repository;
        this.tableView = tableView;
        this.detailView = detailView;
        this.addButton = addButton;
        this.addWindow = null;
        this.refreshRequested = false;
    }

    init() {
        this.tableView.bindSelect((id) => {
            this.detailView.showLoading(id);
            this.repository.loadTeacher(id);
        });

        this.tableView.bindRefresh(() => this.repository.loadList());

        if (this.addButton) {
            this.addButton.addEventListener("click", () => this.openAddWindow());
        }

        this.detailView.onEdit = (id) => this.openEditWindow(id);
        this.detailView.onDelete = (id) => this.deleteTeacher(id);

        this.repository.subscribe("list", (payload) => this.tableView.render(payload));
        this.repository.subscribe("detail", (teacher) => this.detailView.show(teacher));
        this.repository.subscribe("deleted", () => {
            this.detailView.hide();
            this.repository.loadList();
            window.location.reload();
        });
        this.repository.subscribe("error", ({ message, scope }) => {
            if (scope === "list") {
                this.tableView.showStatus(message);
            } else if (scope === "delete") {
                this.detailView.showError(message);
            } else {
                this.detailView.showError(message);
            }
        });

        window.addEventListener("message", (event) => {
            if (
                !event.data ||
                (event.data.type !== "teacher-added" &&
                    event.data.type !== "refresh-main" &&
                    event.data.type !== "teacher-updated")
            ) {
                return;
            }
            // Обновляем список и страхуемся полной перезагрузкой, если сообщения прилетело при закрытии
            this.refreshRequested = false;
            this.repository.loadList();
            window.location.reload();
        });

        window.addEventListener("focus", () => {
            if (this.refreshRequested) {
                this.refreshRequested = false;
                this.repository.loadList();
            }
        });

        this.repository.loadList();
    }

    deleteTeacher(id) {
        if (!id) return;
        const confirmed = window.confirm("Удалить преподавателя?");
        if (!confirmed) return;
        this.repository.deleteTeacher(id);
    }

    openAddWindow() {
        const features = "width=720,height=720";
        this.addWindow = window.open("form.html?mode=add", "teacher-form-add", features);
        if (this.addWindow && typeof this.addWindow.focus === "function") {
            this.addWindow.focus();
        }
        // Фолбэк: если окно закрыто без postMessage, всё равно обновим данные
        const checker = setInterval(() => {
            if (!this.addWindow || this.addWindow.closed) {
                clearInterval(checker);
                this.refreshRequested = false;
                this.repository.loadList();
                window.location.reload();
            }
        }, 1000);
        // Если пользователь вернется в главное окно, а форма еще открыта, отметим необходимость обновления
        this.refreshRequested = true;
    }

    openEditWindow(id) {
        if (!id) return;
        const features = "width=760,height=760";
        this.editWindow = window.open(`form.html?mode=edit&id=${id}`, `edit-teacher-${id}`, features);
        if (this.editWindow && typeof this.editWindow.focus === "function") {
            this.editWindow.focus();
        }

        const checker = setInterval(() => {
            if (!this.editWindow || this.editWindow.closed) {
                clearInterval(checker);
                this.refreshRequested = false;
                this.repository.loadList();
                window.location.reload();
            }
        }, 1000);
        this.refreshRequested = true;
    }
}

const tableBody = document.getElementById("teacher-table-body");
const statusElement = document.getElementById("table-status");
const refreshButton = document.getElementById("refresh-btn");
const addButton = document.getElementById("add-btn");
const overlayElement = document.getElementById("detail-overlay");
const detailContent = document.getElementById("detail-content");
const closeOverlay = document.getElementById("close-overlay");
const openTabButton = document.getElementById("open-tab-btn");
const editButton = document.getElementById("edit-btn");
const deleteButton = document.getElementById("delete-btn");
const overlayTitle = document.getElementById("overlay-title");

const repository = new TeacherRepositoryClient("/api");
const tableView = new TeacherTableView(tableBody, statusElement, refreshButton);
const detailView = new TeacherDetailView(
    overlayElement,
    detailContent,
    closeOverlay,
    openTabButton,
    editButton,
    deleteButton,
    overlayTitle
);
const controller = new UiController(repository, tableView, detailView, addButton);
controller.init();
