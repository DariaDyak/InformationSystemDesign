const form = document.getElementById("add-form");
const statusEl = document.getElementById("status");
const cancelBtn = document.getElementById("cancel-btn");
let successAdded = false;

const emailPattern = /^[\w.-]+@[\w.-]+\.\w+$/;

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    statusEl.textContent = "";

    const formData = new FormData(form);
    const payload = Object.fromEntries(formData.entries());

    const validationError = validatePayload(payload);
    if (validationError) {
        statusEl.textContent = validationError;
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

        successAdded = true;
        statusEl.textContent = `Сохранено. ID: ${data.id}. Окно закроется автоматически.`;
        notifyOpener("teacher-added");
        setTimeout(() => window.close(), 600);
    } catch (error) {
        statusEl.textContent = error.message;
    }
});

cancelBtn.addEventListener("click", () => {
    window.close();
});

window.addEventListener("beforeunload", () => {
    notifyOpener(successAdded ? "teacher-added" : "refresh-main");
});

function notifyOpener(type) {
    if (window.opener && typeof window.opener.postMessage === "function") {
        window.opener.postMessage({ type }, "*");
    }
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
