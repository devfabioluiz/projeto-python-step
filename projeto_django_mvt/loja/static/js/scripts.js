// static/js/scripts.js
document.addEventListener("DOMContentLoaded", function () {
  // Confirmação antes de excluir produto
  const botoesExcluir = document.querySelectorAll(".btn-danger");
  botoesExcluir.forEach(function (botao) {
    botao.addEventListener("click", function (event) {
      if (!confirm("Tem certeza que deseja excluir este produto?")) {
        event.preventDefault();
      }
    });
  });
});
