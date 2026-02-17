const searchInput = document.getElementById("search");
const cards = document.querySelectorAll(".horizontal-card");

function normalizeText(text) {
  return text
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .trim();
}

if (searchInput) {
  searchInput.addEventListener("input", function () {
    const filter = normalizeText(searchInput.value);

    cards.forEach((card) => {
      const nameEl = card.querySelector(".name");
      const cursosEl = card.querySelector(".cursos");

      if (!nameEl || !cursosEl) return;

      const name = normalizeText(nameEl.textContent);
      const cursos = normalizeText(cursosEl.textContent);

      if (name.includes(filter) || cursos.includes(filter)) {
        card.style.display = "";
      } else {
        card.style.display = "none";
      }
    });
  });
}
