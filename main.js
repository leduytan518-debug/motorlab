const menuButton = document.querySelector('.menu-toggle');
const nav = document.querySelector('.main-nav');

if (menuButton && nav) {
  menuButton.addEventListener('click', () => {
    const expanded = menuButton.getAttribute('aria-expanded') === 'true';
    menuButton.setAttribute('aria-expanded', String(!expanded));
    nav.classList.toggle('is-open', !expanded);
  });
}
document.addEventListener("DOMContentLoaded", () => {
  const htmlEl = document.documentElement;
  const themeBtn = document.getElementById("theme-toggle");

  // Lấy chế độ đã lưu (mặc định là 'dark' giống giao diện bạn thích)
  const savedTheme = localStorage.getItem("motorlab_theme") || "dark";
  htmlEl.setAttribute("data-theme", savedTheme);

  const updateBtnText = (theme) => {
    if (!themeBtn) return;
    themeBtn.innerHTML = theme === "dark"
      ? "☀️ Chuyển sang Chế độ Sáng"
      : "🌙 Chuyển sang Chế độ Tối";
  };

  updateBtnText(savedTheme);

  if (themeBtn) {
    themeBtn.addEventListener("click", () => {
      const current = htmlEl.getAttribute("data-theme");
      const nextTheme = current === "dark" ? "light" : "dark";
      htmlEl.setAttribute("data-theme", nextTheme);
      localStorage.setItem("motorlab_theme", nextTheme);
      updateBtnText(nextTheme);
    });
  }
});
