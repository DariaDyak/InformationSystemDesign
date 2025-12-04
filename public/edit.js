const params = new URLSearchParams(window.location.search);
const teacherId = Number(params.get("id"));

const titleEl = document.getElementById("title");
const statusEl = document.getElementById("status");
const form = document.getElementById("edit-form");
const cancelBtn = document.getElementById("cancel-btn");
const emailPattern = /^[\w.-]+@[\w.-]+\.\w+$/;
let successUpdated = false;

if (!teacherId) {
    statusEl.textContent = "Некорректный идентификатор преподавателя";
} else {
    loadTeacher(teacherId);
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    const payload = Object.fromEntries(formData.entries());

    const error = validatePayload(payload);
    if (error) {
        statusEl.textContent = error;
        return;
    }

    try {
        const response = await fetch(`/api/teachers/${teacherId}`, {
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
        successUpdated = true;
        statusEl.textContent = "Изменения сохранены. Окно закроется.";
        notifyOpener("teacher-updated");
        setTimeout(() => window.close(), 700);
    } catch (err) {
        statusEl.textContent = err.message;
    }
});

cancelBtn.addEventListener("click", () => window.close());

window.addEventListener("beforeunload", () => {
    notifyOpener(successUpdated ? "teacher-updated" : "refresh-main");
});

async function loadTeacher(id) {
    statusEl.textContent = "Загружаем данные...";
    try {
        const response = await fetch(`/api/teachers/${id}`);
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "Не удалось загрузить данные");
        }
        fillForm(data);
    } catch (err) {
        statusEl.textContent = err.message;
    }
}

function fillForm(teacher) {
    titleEl.textContent = `Редактирование: ${teacher.last_name} ${teacher.first_name}`;
    statusEl.textContent = `ID: ${teacher.id_teacher}`;
    form.classList.remove("hidden");

    form.elements.first_name.value = teacher.first_name || "";
    form.elements.last_name.value = teacher.last_name || "";
    form.elements.email.value = teacher.email || "";
    form.elements.academic_degree.value = teacher.academic_degree || "";
    form.elements.administrative_position.value = teacher.administrative_position || "";
    form.elements.experience_years.value = teacher.experience_years ?? "";
}

function validatePayload(payload) {
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

    if (!emailPattern.test(payload.email)) {
        return "Некорректный email";
    }

    const experience = Number(payload.experience_years);
    if (!Number.isInteger(experience) || experience < 0) {
        return "Стаж должен быть неотрицательным целым числом";
    }

    return null;
}

function notifyOpener(type) {
    if (window.opener && typeof window.opener.postMessage === "function") {
        window.opener.postMessage({ type }, "*");
    }
}
