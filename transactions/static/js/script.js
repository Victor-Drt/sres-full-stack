// script.js
document.querySelector('.login-form').addEventListener('submit', function(e) {
    e.preventDefault();
    // Simulação de login
    window.location.href = "dashboard.html";
  });
  

  // script.js
document.addEventListener("DOMContentLoaded", () => {
    const logoutBtn = document.getElementById("logout");
    if (logoutBtn) {
      logoutBtn.addEventListener("click", () => {
        alert("Sessão encerrada.");
        window.location.href = "index.html";
      });
    }
  });

  document.addEventListener("DOMContentLoaded", () => {
    const logoutBtn = document.getElementById("logout");
    if (logoutBtn) {
      logoutBtn.addEventListener("click", () => {
        alert("Sessão encerrada.");
        window.location.href = "index.html";
      });
    }
  
    const tipoSelect = document.getElementById("tipo");
    const campoDizimista = document.getElementById("campo-dizimista");
    const listaEntradas = document.getElementById("lista-entradas");
    const form = document.getElementById("form-entrada");
  
    if (tipoSelect) {
      tipoSelect.addEventListener("change", () => {
        campoDizimista.style.display = tipoSelect.value === "dizimo" ? "block" : "none";
      });
    }
  
    const carregarEntradas = () => {
      const entradas = JSON.parse(localStorage.getItem("entradas") || "[]");
      listaEntradas.innerHTML = "";
  
      entradas.forEach((entrada) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${entrada.tipo}</td>
          <td>${entrada.dizimista || '-'}</td>
          <td>R$ ${parseFloat(entrada.valor).toFixed(2)}</td>
          <td>${entrada.data}</td>
        `;
        listaEntradas.appendChild(tr);
      });
    };
  
    if (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
  
        const tipo = document.getElementById("tipo").value;
        const valor = document.getElementById("valor").value;
        const data = document.getElementById("data").value;
        const dizimista = document.getElementById("dizimista").value;
  
        const novaEntrada = { tipo, valor, data };
        if (tipo === "dizimo") novaEntrada.dizimista = dizimista;
  
        const entradas = JSON.parse(localStorage.getItem("entradas") || "[]");
        entradas.push(novaEntrada);
        localStorage.setItem("entradas", JSON.stringify(entradas));
  
        form.reset();
        campoDizimista.style.display = "none";
        carregarEntradas();
      });
    }
  
    carregarEntradas();
  });  

  
  // === Saídas ===
const formSaida = document.getElementById("form-saida");
const listaSaidas = document.getElementById("lista-saidas");

const carregarSaidas = () => {
  if (!listaSaidas) return;
  const saidas = JSON.parse(localStorage.getItem("saidas") || "[]");
  listaSaidas.innerHTML = "";

  saidas.forEach((saida) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${saida.descricao}</td>
      <td>R$ ${parseFloat(saida.valor).toFixed(2)}</td>
      <td>${saida.data}</td>
    `;
    listaSaidas.appendChild(tr);
  });
};

if (formSaida) {
  formSaida.addEventListener("submit", (e) => {
    e.preventDefault();

    const descricao = document.getElementById("descricao").value;
    const valor = document.getElementById("valor-saida").value;
    const data = document.getElementById("data-saida").value;

    const novaSaida = { descricao, valor, data };
    const saidas = JSON.parse(localStorage.getItem("saidas") || "[]");
    saidas.push(novaSaida);
    localStorage.setItem("saidas", JSON.stringify(saidas));

    formSaida.reset();
    carregarSaidas();
  });

  carregarSaidas();
}


// === Relatórios ===
const formRelatorio = document.getElementById("form-relatorio");
if (formRelatorio) {
  formRelatorio.addEventListener("submit", (e) => {
    e.preventDefault();

    const inicio = document.getElementById("data-inicio").value;
    const fim = document.getElementById("data-fim").value;
    const resultado = document.getElementById("resultado-relatorio");

    const entradas = JSON.parse(localStorage.getItem("entradas") || "[]");
    const saidas = JSON.parse(localStorage.getItem("saidas") || "[]");

    let totalDizimos = 0;
    let totalOfertas = 0;
    let totalSaidas = 0;

    entradas.forEach(e => {
      if (e.data >= inicio && e.data <= fim) {
        if (e.tipo === "dizimo") {
          totalDizimos += parseFloat(e.valor);
        } else {
          totalOfertas += parseFloat(e.valor);
        }
      }
    });

    saidas.forEach(s => {
      if (s.data >= inicio && s.data <= fim) {
        totalSaidas += parseFloat(s.valor);
      }
    });

    const saldo = totalDizimos + totalOfertas - totalSaidas;

    document.getElementById("total-dizimos").textContent = totalDizimos.toFixed(2);
    document.getElementById("total-ofertas").textContent = totalOfertas.toFixed(2);
    document.getElementById("total-saidas").textContent = totalSaidas.toFixed(2);
    document.getElementById("saldo-final").textContent = saldo.toFixed(2);

    resultado.style.display = "block";
  });
}
