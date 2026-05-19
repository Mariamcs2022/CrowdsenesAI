document.querySelectorAll(".action-tab").forEach(button => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".action-tab").forEach(btn => btn.classList.remove("active"));
    document.querySelectorAll(".action-content").forEach(box => box.classList.remove("active"));

    button.classList.add("active");
    document.getElementById(button.dataset.target).classList.add("active");
  });
});
