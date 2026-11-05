/* Thiago Soares · interações do site (sem dependências) */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.remove("sem-js");

  var ICONES = {
    fechar: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12"/></svg>',
    ant: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m15 18-6-6 6-6"/></svg>',
    prox: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 18 6-6-6-6"/></svg>',
    play: '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.5v13a1 1 0 0 0 1.5.86l10.4-6.5a1 1 0 0 0 0-1.72L9.5 4.64A1 1 0 0 0 8 5.5Z"/></svg>',
    pausa: '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg>'
  };

  /* ---------- cabeçalho ---------- */
  var topo = document.querySelector(".topo");
  function aoRolar() { if (topo) topo.classList.toggle("rolou", window.scrollY > 8); }
  window.addEventListener("scroll", aoRolar, { passive: true });
  aoRolar();

  /* ---------- menu do celular ---------- */
  var botaoMenu = document.querySelector(".botao-menu");
  var menu = document.getElementById("menu");
  function fecharMenu() {
    if (!menu) return;
    menu.classList.remove("aberto");
    document.body.classList.remove("menu-aberto");
    if (botaoMenu) botaoMenu.setAttribute("aria-expanded", "false");
  }
  if (botaoMenu && menu) {
    botaoMenu.addEventListener("click", function () {
      var abrir = !menu.classList.contains("aberto");
      menu.classList.toggle("aberto", abrir);
      document.body.classList.toggle("menu-aberto", abrir);
      botaoMenu.setAttribute("aria-expanded", String(abrir));
    });
    menu.addEventListener("click", function (e) { if (e.target.closest("a")) fecharMenu(); });
    window.addEventListener("resize", function () { if (window.innerWidth > 880) fecharMenu(); });
  }

  /* ---------- aparecer ao rolar ---------- */
  document.querySelectorAll("[data-escalonar]").forEach(function (g) {
    Array.prototype.forEach.call(g.children, function (c, i) { c.style.setProperty("--atraso", (i % 6) * 90 + "ms"); });
  });
  var revelar = document.querySelectorAll(".revela");
  if ("IntersectionObserver" in window) {
    var obs = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("visivel"); obs.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    revelar.forEach(function (el) { obs.observe(el); });
  } else {
    revelar.forEach(function (el) { el.classList.add("visivel"); });
  }

  /* ---------- janela (galeria e vídeo) ---------- */
  var janela, conteudo, ultimoFoco, aoFechar = null, navegar = null;
  function criarJanela() {
    if (janela) return;
    janela = document.createElement("div");
    janela.className = "janela";
    janela.setAttribute("role", "dialog");
    janela.setAttribute("aria-modal", "true");
    janela.setAttribute("aria-label", "Visualização");
    janela.innerHTML =
      '<div class="janela-conteudo"></div>' +
      '<button class="janela-nav ant" type="button" aria-label="Anterior">' + ICONES.ant + "</button>" +
      '<button class="janela-nav prox" type="button" aria-label="Próxima">' + ICONES.prox + "</button>" +
      '<button class="janela-fechar" type="button" aria-label="Fechar">' + ICONES.fechar + "</button>";
    document.body.appendChild(janela);
    conteudo = janela.querySelector(".janela-conteudo");
    janela.querySelector(".janela-fechar").addEventListener("click", fecharJanela);
    janela.querySelector(".ant").addEventListener("click", function () { if (navegar) navegar(-1); });
    janela.querySelector(".prox").addEventListener("click", function () { if (navegar) navegar(1); });
    janela.addEventListener("click", function (e) { if (e.target === janela) fecharJanela(); });
    var x0 = null;
    janela.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    janela.addEventListener("touchend", function (e) {
      if (x0 === null || !navegar) return;
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 50) navegar(dx < 0 ? 1 : -1);
      x0 = null;
    });
  }
  function abrirJanela(html, opcoes) {
    criarJanela();
    ultimoFoco = document.activeElement;
    conteudo.innerHTML = html;
    navegar = opcoes && opcoes.navegar ? opcoes.navegar : null;
    aoFechar = opcoes && opcoes.aoFechar ? opcoes.aoFechar : null;
    janela.querySelectorAll(".janela-nav").forEach(function (b) { b.hidden = !navegar; });
    janela.classList.add("aberta");
    document.body.style.overflow = "hidden";
    janela.querySelector(".janela-fechar").focus();
  }
  function fecharJanela() {
    if (!janela || !janela.classList.contains("aberta")) return;
    janela.classList.remove("aberta");
    document.body.style.overflow = "";
    if (aoFechar) aoFechar();
    setTimeout(function () { if (!janela.classList.contains("aberta")) conteudo.innerHTML = ""; }, 250);
    if (ultimoFoco) ultimoFoco.focus();
  }
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { fecharJanela(); fecharMenu(); }
    if (janela && janela.classList.contains("aberta") && navegar) {
      if (e.key === "ArrowLeft") navegar(-1);
      if (e.key === "ArrowRight") navegar(1);
    }
  });

  /* galeria de fotos */
  var fotos = Array.prototype.slice.call(document.querySelectorAll("[data-galeria] a"));
  if (fotos.length) {
    var atual = 0;
    var mostrar = function (i) {
      atual = (i + fotos.length) % fotos.length;
      var a = fotos[atual];
      var alt = a.querySelector("img").getAttribute("alt") || "";
      var html = '<img src="' + a.getAttribute("href") + '" alt="' + alt.replace(/"/g, "&quot;") + '">' +
        '<p class="legenda">' + (atual + 1) + " / " + fotos.length + "</p>";
      if (janela && janela.classList.contains("aberta")) conteudo.innerHTML = html;
      else abrirJanela(html, { navegar: function (d) { mostrar(atual + d); } });
    };
    fotos.forEach(function (a, i) {
      a.addEventListener("click", function (e) { e.preventDefault(); mostrar(i); });
    });
  }

  /* vídeos do YouTube: só carregam ao clicar */
  document.querySelectorAll("[data-youtube]").forEach(function (b) {
    b.addEventListener("click", function () {
      var id = b.getAttribute("data-youtube");
      var titulo = b.getAttribute("data-titulo") || "";
      abrirJanela(
        '<div class="tela"><iframe src="https://www.youtube-nocookie.com/embed/' + id +
        '?autoplay=1&rel=0&modestbranding=1" title="' + titulo.replace(/"/g, "&quot;") +
        '" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe></div>' +
        '<p class="legenda">' + titulo + "</p>"
      );
    });
  });

  /* ---------- filtro do impresso ---------- */
  var filtros = document.querySelectorAll("[data-filtro]");
  var materias = document.querySelectorAll(".materia[data-tipo]");
  filtros.forEach(function (b) {
    b.addEventListener("click", function () {
      var f = b.getAttribute("data-filtro");
      filtros.forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
      materias.forEach(function (m) { m.hidden = !(f === "todos" || m.getAttribute("data-tipo") === f); });
    });
  });

  /* ---------- player de rádio ---------- */
  var player = document.querySelector("[data-player]");
  if (player) {
    var audio = player.querySelector("audio");
    var itens = Array.prototype.slice.call(player.querySelectorAll(".faixas-audio li"));
    var botaoTocar = player.querySelector("[data-acao='tocar']");
    var barra = player.querySelector("input[type='range']");
    var tAtual = player.querySelector("[data-tempo='atual']");
    var tTotal = player.querySelector("[data-tempo='total']");
    var titulo = player.querySelector(".tocando-titulo");
    var faixa = 0, arrastando = false;

    var tocar = function () { var p = audio.play(); if (p && p.catch) p.catch(function () {}); };
    var fmt = function (s) {
      if (!isFinite(s)) return "00:00";
      s = Math.floor(s);
      return String(Math.floor(s / 60)).padStart(2, "0") + ":" + String(s % 60).padStart(2, "0");
    };
    var carregar = function (i, deveTocar) {
      faixa = (i + itens.length) % itens.length;
      var li = itens[faixa];
      itens.forEach(function (x) { x.classList.toggle("atual", x === li); });
      itens.forEach(function (x) { x.querySelector("button").removeAttribute("aria-current"); });
      li.querySelector("button").setAttribute("aria-current", "true");
      audio.src = li.getAttribute("data-src");
      titulo.textContent = li.getAttribute("data-titulo");
      tTotal.textContent = li.getAttribute("data-duracao");
      barra.value = 0; tAtual.textContent = "00:00";
      if (deveTocar) tocar();
    };
    var atualizarBotao = function () {
      var tocando = !audio.paused;
      player.classList.toggle("ativo", tocando);
      botaoTocar.innerHTML = tocando ? ICONES.pausa : ICONES.play;
      botaoTocar.setAttribute("aria-label", tocando ? "Pausar" : "Tocar");
    };
    botaoTocar.addEventListener("click", function () {
      if (!audio.getAttribute("src")) carregar(faixa, true);
      else if (audio.paused) tocar(); else audio.pause();
    });
    player.querySelector("[data-acao='anterior']").addEventListener("click", function () {
      if (audio.currentTime > 3) { audio.currentTime = 0; return; }
      carregar(faixa - 1, true);
    });
    player.querySelector("[data-acao='proxima']").addEventListener("click", function () { carregar(faixa + 1, true); });
    itens.forEach(function (li, i) {
      li.querySelector("button").addEventListener("click", function () {
        if (i === faixa && audio.getAttribute("src")) { if (audio.paused) tocar(); else audio.pause(); }
        else carregar(i, true);
      });
    });
    audio.addEventListener("play", atualizarBotao);
    audio.addEventListener("pause", atualizarBotao);
    audio.addEventListener("loadedmetadata", function () { tTotal.textContent = fmt(audio.duration); });
    audio.addEventListener("timeupdate", function () {
      if (arrastando || !audio.duration) return;
      barra.value = (audio.currentTime / audio.duration) * 1000;
      tAtual.textContent = fmt(audio.currentTime);
    });
    audio.addEventListener("ended", function () { if (faixa < itens.length - 1) carregar(faixa + 1, true); });
    barra.addEventListener("input", function () {
      arrastando = true;
      if (audio.duration) tAtual.textContent = fmt((barra.value / 1000) * audio.duration);
    });
    barra.addEventListener("change", function () {
      if (!audio.getAttribute("src")) carregar(faixa, false);
      if (audio.duration) audio.currentTime = (barra.value / 1000) * audio.duration;
      arrastando = false;
    });
    carregar(0, false);
    audio.removeAttribute("src"); /* não baixa nada até o visitante apertar o play */
    atualizarBotao();
  }

})();
