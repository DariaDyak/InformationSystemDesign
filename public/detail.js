const titleElement = document.getElementById("detail-title");
const statusElement = document.getElementById("detail-status");
const detailRoot = document.getElementById("detail-root");

const params = new URLSearchParams(window.location.search);
const teacherId = Number(params.get("id"));

if (!teacherId) {
    statusElement.textContent = "Не указан идентификатор преподавателя";
} else {
    loadTeacher(teacherId);
}

async function loadTeacher(id) {
    statusElement.textContent = `Получаем данные по ID ${id}...`;
    detailRoot.innerHTML = "";

    try {
        const response = await fetch(`/api/teachers/${id}`);
        if (!response.ok) {
            const payload = await response.json().catch(() => ({}));
            throw new Error(payload.error || "Не удалось загрузить карточку");
        }
        const teacher = await response.json();
        renderTeacher(teacher);
    } catch (error) {
        statusElement.textContent = error.message;
    }
}

function renderTeacher(teacher) {
    titleElement.textContent = `${teacher.last_name} ${teacher.first_name}`;
    statusElement.textContent = `ID: ${teacher.id_teacher}`;

    detailRoot.innerHTML = `
        ${detailBlock("Фамилия", teacher.last_name)}
        ${detailBlock("Имя", teacher.first_name)}
        ${detailBlock("Email", teacher.email)}
        ${detailBlock("Ученая степень", teacher.academic_degree)}
        ${detailBlock("Должность", teacher.administrative_position)}
        ${detailBlock("Стаж", `${teacher.experience_years} лет`)}
        ${detailBlock("ID", teacher.id_teacher)}
    `;
}

function detailBlock(label, value) {
    return `
        <div class="detail__item">
            <p class="detail__label">${label}</p>
            <p class="detail__value">${value ?? "—"}</p>
        </div>
    `;
}
