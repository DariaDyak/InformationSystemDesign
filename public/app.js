class TeacherRepositoryClient {
    constructor(baseUrl = "/api") {
        this.baseUrl = baseUrl;
        this.subscribers = { list: [], detail: [], error: [] };
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
    constructor(overlayElement, contentElement, closeButton, openTabButton, titleElement) {
        this.overlayElement = overlayElement;
        this.contentElement = contentElement;
        this.closeButton = closeButton;
        this.openTabButton = openTabButton;
        this.titleElement = titleElement;
        this.currentId = null;

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
    constructor(repository, tableView, detailView) {
        this.repository = repository;
        this.tableView = tableView;
        this.detailView = detailView;
    }

    init() {
        this.tableView.bindSelect((id) => {
            this.detailView.showLoading(id);
            this.repository.loadTeacher(id);
        });

        this.tableView.bindRefresh(() => this.repository.loadList());

        this.repository.subscribe("list", (payload) => this.tableView.render(payload));
        this.repository.subscribe("detail", (teacher) => this.detailView.show(teacher));
        this.repository.subscribe("error", ({ message, scope }) => {
            if (scope === "list") {
                this.tableView.showStatus(message);
            } else {
                this.detailView.showError(message);
            }
        });

        this.repository.loadList();
    }
}

const tableBody = document.getElementById("teacher-table-body");
const statusElement = document.getElementById("table-status");
const refreshButton = document.getElementById("refresh-btn");
const overlayElement = document.getElementById("detail-overlay");
const detailContent = document.getElementById("detail-content");
const closeOverlay = document.getElementById("close-overlay");
const openTabButton = document.getElementById("open-tab-btn");
const overlayTitle = document.getElementById("overlay-title");

const repository = new TeacherRepositoryClient("/api");
const tableView = new TeacherTableView(tableBody, statusElement, refreshButton);
const detailView = new TeacherDetailView(
    overlayElement,
    detailContent,
    closeOverlay,
    openTabButton,
    overlayTitle
);
const controller = new UiController(repository, tableView, detailView);
controller.init();
