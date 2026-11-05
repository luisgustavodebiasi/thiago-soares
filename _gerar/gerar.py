#!/usr/bin/env python3
"""Gera as páginas HTML do site a partir de _gerar/dados.json.

Uso (de dentro da pasta site/):  python3 _gerar/gerar.py
Para mudar um texto, um vídeo ou uma matéria: edite dados.json e rode de novo.
"""
import html
import json
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
D = json.loads((RAIZ / "_gerar" / "dados.json").read_text(encoding="utf-8"))
ANO = date.today().year
BASE = "https://luisgustavodebiasi.github.io/thiago-soares/"  # endereço publicado (mude se usar domínio próprio)
e = html.escape

# ---------------------------------------------------------------- ícones (traço, 24x24)
def ic(corpo, preenchido=False):
    if preenchido:
        return f'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">{corpo}</svg>'
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{corpo}</svg>')

I = {
    "linkedin": ic('<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/>'),
    "facebook": ic('<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>'),
    "youtube": ic('<path d="M2.5 17a24.1 24.1 0 0 1 0-10 2 2 0 0 1 1.4-1.4 49.6 49.6 0 0 1 16.2 0A2 2 0 0 1 21.5 7a24.1 24.1 0 0 1 0 10 2 2 0 0 1-1.4 1.4 49.6 49.6 0 0 1-16.2 0A2 2 0 0 1 2.5 17"/><path d="m10 15 5-3-5-3z"/>'),
    "instagram": ic('<rect x="2" y="2" width="20" height="20" rx="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><path d="M17.5 6.5h.01"/>'),
    "email": ic('<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>'),
    "telefone": ic('<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.1 9.9a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>'),
    "whatsapp": ic('<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/><path d="M9 10a.5.5 0 0 0 1 0V9a.5.5 0 0 0-1 0v1a5 5 0 0 0 5 5h1a.5.5 0 0 0 0-1h-1a.5.5 0 0 0 0 1"/>'),
    "menu": ic('<path d="M4 7h16M4 12h16M4 17h16"/>').replace("<svg ", '<svg class="tres" '),
    "x": ic('<path d="M18 6 6 18M6 6l12 12"/>').replace("<svg ", '<svg class="x" '),
    "seta": ic('<path d="M5 12h14M13 6l6 6-6 6"/>'),
    "voltar": ic('<path d="m15 18-6-6 6-6"/>'),
    "baixo": ic('<path d="m6 9 6 6 6-6"/>'),
    "cima": ic('<path d="m18 15-6-6-6 6"/>'),
    "play": ic('<path d="M8 5.5v13a1 1 0 0 0 1.5.86l10.4-6.5a1 1 0 0 0 0-1.72L9.5 4.64A1 1 0 0 0 8 5.5Z"/>', True),
    "play_circulo": ic('<circle cx="12" cy="12" r="10"/><path d="m10 8 6 4-6 4z" fill="currentColor"/>'),
    "ant": ic('<path d="M19 20 9 12l10-8z" fill="currentColor"/><path d="M5 19V5"/>'),
    "prox": ic('<path d="m5 4 10 8-10 8z" fill="currentColor"/><path d="M19 5v14"/>'),
    "pdf": ic('<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M9 13h6M9 17h6"/>'),
}

R = D["redes"]
C = D["contato"]
TEL_DIGITOS = "55" + "".join(ch for ch in C["telefone"] if ch.isdigit())

REDES = [("LinkedIn", R["linkedin"], "linkedin"), ("Facebook", R["facebook"], "facebook"),
         ("YouTube", R["youtube"], "youtube"), ("Instagram", R["instagram"], "instagram")]


def redes_html():
    itens = "".join(
        f'<a href="{e(u)}" target="_blank" rel="noopener" aria-label="{n}">{I[k]}</a>' for n, u, k in REDES)
    return f'<div class="redes">{itens}</div>'


# ---------------------------------------------------------------- moldura da página
MENU = [
    ("index.html", "Início"),
    ("trabalhos.html", "Meus trabalhos", [("video.html", "Vídeo"), ("impresso.html", "Impresso"), ("radio.html", "Rádio")]),
    ("curriculo.html", "Currículo"),
    ("index.html#contato", "Contato"),
]


def menu_html(atual):
    lis = []
    for item in MENU:
        href, rotulo = item[0], item[1]
        cur = ' aria-current="page"' if href == atual else ""
        if len(item) == 3:
            filhos = item[2]
            ativo = any(h == atual for h, _ in filhos)
            marca = ' aria-current="page"'
            sub = "".join(
                f'<li><a href="{h}"{marca if h == atual else ""}>{r}</a></li>' for h, r in filhos)
            lis.append(f'<li class="sub{" ativo" if ativo else ""}"><a href="{href}"{cur}>{rotulo}</a><ul>{sub}</ul></li>')
        else:
            lis.append(f'<li><a href="{href}"{cur}>{rotulo}</a></li>')
    return "".join(lis)


def pagina(arquivo, titulo, descricao, corpo, extra_head=""):
    t = f"{titulo} | Thiago Soares, jornalista" if titulo else "Thiago Soares | Jornalista em Brasília"
    doc = f"""<!doctype html>
<html lang="pt-BR" class="sem-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(t)}</title>
<meta name="description" content="{e(descricao)}">
<meta name="theme-color" content="#326b9a">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:title" content="{e(t)}">
<meta property="og:description" content="{e(descricao)}">
<meta property="og:image" content="{BASE}assets/img/og.jpg">
<meta property="og:url" content="{BASE}{"" if arquivo == "index.html" else arquivo}">
<link rel="canonical" href="{BASE}{"" if arquivo == "index.html" else arquivo}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Nunito+Sans:ital,wght@0,300;0,400;0,600;0,700;1,300&family=Syncopate:wght@400;700&display=swap">
<link rel="stylesheet" href="assets/css/style.css">
{extra_head}</head>
<body>
<a class="pular" href="#conteudo">Pular para o conteúdo</a>
<header class="topo">
  <div class="container">
    <a class="logo" href="index.html" aria-label="Thiago Soares, página inicial"><strong>THIAGO SOARES</strong><span>Jornalista</span></a>
    <button class="botao-menu" type="button" aria-controls="menu" aria-expanded="false" aria-label="Abrir menu">{I["menu"]}{I["x"]}</button>
    <nav id="menu" class="menu" aria-label="Principal">
      <ul>{menu_html(arquivo)}</ul>
      {redes_html()}
    </nav>
  </div>
</header>
<main id="conteudo">
{corpo}
</main>
<footer class="rodape">
  <div class="container">
    <div>
      <p>© {ANO} Thiago Soares</p>
      <p class="direitos">{e(D["site"]["rodape"]["aviso"])}<br>{e(D["site"]["rodape"]["aviso_2"])}</p>
    </div>
    {redes_html()}
    <a class="voltar-topo" href="#conteudo" aria-label="Voltar ao topo">{I["cima"]}</a>
  </div>
</footer>
<script src="assets/js/main.js" defer></script>
</body>
</html>
"""
    (RAIZ / arquivo).write_text(doc, encoding="utf-8")
    print("  ", arquivo)


def topo_interno(titulo, intro=None, voltar=("trabalhos.html", "Meus trabalhos")):
    v = f'<a class="voltar" href="{voltar[0]}">{I["voltar"]}{voltar[1]}</a>' if voltar else ""
    i = f'<p class="intro revela">{e(intro)}</p>' if intro else ""
    return f"""<section class="pagina-topo">
  <div class="container">
    {v}
    <div class="moldura revela"><h1>{e(titulo)}</h1></div>
    {i}
  </div>
</section>"""


def faixas_html(variante=""):
    n_videos = 1 + sum(len(g["videos"]) for g in D["video"]["grupos"])
    n_materias = len(D["impresso"]["materias"])
    n_audios = len(D["radio"]["playlist"]["faixas"])
    itens = [
        ("video", "video.html", "Vídeo", f"{n_videos} vídeos · reportagem e apresentação"),
        ("impresso", "impresso.html", "Impresso", f"{n_materias} matérias · jornal e revista"),
        ("radio", "radio.html", "Rádio", f"{n_audios} áudios · rádio e podcast"),
    ]
    a = "".join(
        f'<a class="faixa {c} revela" href="{h}"><span><strong>{r}</strong><small>{s}</small></span>'
        f'<span class="seta">{I["seta"]}</span></a>' for c, h, r, s in itens)
    return f'<div class="faixas {variante}">{a}</div>'


def contato_html():
    f = C["formulario"]
    return f"""<section class="secao contato" id="contato">
  <div class="container">
    <div class="moldura revela"><h2>Fale comigo!</h2></div>
    <div class="contato-grade">
      <div class="revela">
        <h3>Contato</h3>
        <ul class="canais">
          <li><a href="tel:+{TEL_DIGITOS}"><span class="icone">{I["telefone"]}</span><span>Tel: {e(C["telefone"])}</span></a></li>
          <li><a href="https://wa.me/{TEL_DIGITOS}" target="_blank" rel="noopener"><span class="icone">{I["whatsapp"]}</span><span>WhatsApp</span></a></li>
          <li><a href="mailto:{e(C["email"])}"><span class="icone">{I["email"]}</span><span>{e(C["email"])}</span></a></li>
        </ul>
        {redes_html()}
      </div>
      <form class="formulario revela" data-contato data-para="{e(C["email"])}" data-endpoint="" novalidate>
        <label><span class="visualmente-oculto">Nome</span><input name="nome" type="text" placeholder="{e(f["campos"][0])}" autocomplete="name" required></label>
        <label><span class="visualmente-oculto">E-mail</span><input name="email" type="email" placeholder="E-mail" autocomplete="email" required></label>
        <label><span class="visualmente-oculto">Telefone</span><input name="telefone" type="tel" placeholder="{e(f["campos"][2])}" autocomplete="tel"></label>
        <label><span class="visualmente-oculto">Mensagem</span><textarea name="mensagem" placeholder="{e(f["campos"][3])}" required></textarea></label>
        <div class="rodape-form">
          <p class="status" role="status" aria-live="polite"></p>
          <button class="botao" type="submit">{e(f["botao"])}</button>
        </div>
      </form>
    </div>
  </div>
</section>"""


# ---------------------------------------------------------------- páginas
def gerar_inicio():
    s = D["inicio"]["sobre"]
    passagens = ["Correio Braziliense", "RecordTV Brasília", "OAB Nacional", "MPT · Trabalho Legal",
                 "Ministério da Justiça", "ANTT"]
    pessoa = {
        "@context": "https://schema.org", "@type": "Person", "name": "Thiago Soares",
        "jobTitle": "Jornalista", "email": "mailto:" + C["email"], "telephone": "+" + TEL_DIGITOS,
        "address": {"@type": "PostalAddress", "addressLocality": "Brasília", "addressRegion": "DF", "addressCountry": "BR"},
        "alumniOf": "Pontifícia Universidade Católica de Minas Gerais (PUC-Minas)",
        "sameAs": [u for _, u, _ in REDES],
    }
    head = ('<link rel="preload" as="image" href="assets/img/fotos/hero-1200.jpg" '
            'imagesrcset="assets/img/fotos/hero-1200.jpg 1200w, assets/img/fotos/hero-2400.jpg 2400w" imagesizes="100vw">\n'
            f'<script type="application/ld+json">{json.dumps(pessoa, ensure_ascii=False)}</script>\n')
    corpo = f"""<section class="hero">
  <picture>
    <img src="assets/img/fotos/hero-1200.jpg" srcset="assets/img/fotos/hero-1200.jpg 1200w, assets/img/fotos/hero-2400.jpg 2400w" sizes="100vw"
      alt="Thiago Soares de terno em frente à estátua da Justiça, no Supremo Tribunal Federal" fetchpriority="high">
  </picture>
  <div class="hero-texto">
    <h1><span>Thiago</span> <span>Soares</span></h1>
    <span class="assinatura">• Jornalista •</span>
    <p class="hero-local">Brasília · DF</p>
  </div>
  <a class="rolar" href="#sobre" aria-label="Ir para Sobre mim">{I["baixo"]}</a>
</section>

<section class="secao secao-foto sobre" id="sobre">
  <div class="fundo"><img src="assets/img/fotos/aeroporto-1000.jpg" srcset="assets/img/fotos/aeroporto-1000.jpg 1000w, assets/img/fotos/aeroporto-2000.jpg 2000w" sizes="100vw" alt="" loading="lazy"></div>
  <div class="container sobre-grade">
    <figure class="retrato revela">
      <img src="assets/img/fotos/retrato-800.jpg" alt="Retrato de Thiago Soares, sorrindo, de óculos e camisa xadrez" loading="lazy" width="800" height="809">
      <figcaption>Sobre<br>mim!</figcaption>
    </figure>
    <div class="sobre-texto revela">
      <p class="lead">{e(s["texto"])}</p>
      <a class="botao" href="curriculo.html">{e(s["botao"]["rotulo"])} {I["seta"]}</a>
      <div class="passagens">
        <h3>Passagens por</h3>
        <ul>{"".join(f"<li>{e(p)}</li>" for p in passagens)}</ul>
      </div>
    </div>
  </div>
</section>

<section class="secao secao-foto categorias" id="trabalhos">
  <div class="fundo"><img src="assets/img/fotos/planalto-1200.jpg" srcset="assets/img/fotos/planalto-1200.jpg 1200w, assets/img/fotos/planalto-2400.jpg 2400w" sizes="100vw" alt="" loading="lazy"></div>
  <div class="container">
    <h2 class="titulo-secao marca-titulo revela">Meus trabalhos</h2>
    {faixas_html()}
  </div>
</section>

{contato_html()}"""
    pagina("index.html", "", "Thiago Soares, jornalista em Brasília. Reportagem e apresentação em TV, "
           "texto para jornal e revista, rádio e assessoria de imprensa.", corpo, head)


FOTOS = [
    ("01-esplanada", "Thiago Soares com a Esplanada dos Ministérios ao fundo"),
    ("02-congresso", "Thiago Soares em frente ao Congresso Nacional"),
    ("03-catedral", "Thiago Soares diante da Catedral de Brasília"),
    ("04-oab", "Thiago Soares apresentando em frente à sede da OAB Nacional"),
    ("05-bastidor-gravacao", "Bastidores de uma gravação, com equipe e iluminação"),
    ("06-bastidor-luz", "Thiago Soares nos bastidores de uma gravação, contra a luz do estúdio"),
    ("07-dragoes-planalto", "Thiago Soares entre os Dragões da Independência, no Palácio do Planalto"),
]


def gerar_trabalhos():
    fotos = "".join(
        f'<a href="assets/img/fotos/{n}-1600.jpg"><img src="assets/img/fotos/{n}-700.jpg" alt="{e(a)}" loading="lazy"></a>'
        for n, a in FOTOS)
    corpo = f"""{topo_interno("Meus trabalhos", "Reportagem, apresentação e produção em TV, texto para jornal e revista, rádio e podcast.", ("index.html", "Início"))}
<section class="pagina-corpo">
  <div class="container">
    <div class="galeria revela" data-galeria>{fotos}</div>
    <div class="galeria-faixas">{faixas_html("agua")}</div>
  </div>
</section>"""
    pagina("trabalhos.html", "Meus trabalhos", "Portfólio de Thiago Soares: vídeo, impresso e rádio.", corpo)


def cartao_video(v):
    desc = f'<p>{e(v["descricao"])}</p>' if v.get("descricao") else ""
    return (f'<button class="cartao-video revela" type="button" data-youtube="{v["youtube"]}" data-titulo="{e(v["titulo"])}">'
            f'<span class="miniatura"><img src="assets/img/videos/{v["youtube"]}.jpg" alt="" loading="lazy">'
            f'<span class="play">{I["play"]}</span><span class="duracao">{v["duracao"]}</span></span>'
            f'<h3>{e(v["titulo"])}</h3>{desc}</button>')


def gerar_video():
    V = D["video"]
    d = V["destaque"]
    grupos = "".join(
        f'<section class="grupo"><div class="grupo-cabeca"><h2>{e(g["nome"])}</h2><span>{len(g["videos"])} vídeos</span></div>'
        f'<div class="cartoes">{"".join(cartao_video(v) for v in g["videos"])}</div></section>'
        for g in V["grupos"])
    corpo = f"""{topo_interno("Vídeo", V["texto"])}
<section class="pagina-corpo">
  <div class="container">
    <button class="destaque revela" type="button" data-youtube="{d["youtube"]}" data-titulo="{e(d["titulo"])}">
      <img src="assets/img/videos/destaque-{d["youtube"]}.jpg" alt="" loading="lazy">
      <span class="destaque-texto"><strong>Compilado de reportagens</strong><span>{I["play_circulo"]}Reproduzir vídeo</span></span>
    </button>
    {grupos}
  </div>
</section>"""
    pagina("video.html", "Vídeo", "Reportagens e programas apresentados por Thiago Soares: Trabalho Legal (MPT), "
           "OAB Nacional e produções para a RecordTV.", corpo)


MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro",
         "outubro", "novembro", "dezembro"]


def data_br(s):
    p = s.split("-")
    if len(p) == 3:
        return f"{int(p[2])} de {MESES[int(p[1]) - 1]} de {p[0]}"
    if len(p) == 2:
        return f"{MESES[int(p[1]) - 1]} de {p[0]}"
    return s


def gerar_impresso():
    M = D["impresso"]["materias"]
    cards = []
    for m in M:
        tipo = "jornal" if m["veiculo"].startswith("Correio") else "revista"
        nome = Path(m["pdf"]).name
        pags = f'{m["paginas"]} página' + ("s" if m["paginas"] > 1 else "")
        veic = m["veiculo"].replace("Revista PQN - Pão de Queijo Notícias", "Revista PQN")
        foco = f' style="object-position:{m["capa_foco"]}"' if m.get("capa_foco") else ""
        cards.append(
            f'<a class="materia revela" data-tipo="{tipo}" href="assets/pdf/{nome}" target="_blank" rel="noopener" '
            f'aria-label="{e(m["titulo"])}, {e(veic)}, {data_br(m["data"])}. Abrir PDF, {pags}">'
            f'<span class="folha"><img src="assets/img/capas/{Path(m["capa"]).name}" alt="" loading="lazy"{foco}>'
            f'<span class="ler">{I["pdf"]}Ler matéria</span></span>'
            f'<span class="veiculo">{e(veic)}</span><h3>{e(m["titulo"])}</h3>'
            f'<span class="meta">{data_br(m["data"])} · {pags}</span></a>')
    n_j = sum(1 for m in M if m["veiculo"].startswith("Correio"))
    corpo = f"""{topo_interno("Impresso", D["impresso"]["texto"])}
<section class="pagina-corpo">
  <div class="container">
    <div class="filtros" role="group" aria-label="Filtrar matérias">
      <button type="button" data-filtro="todos" aria-pressed="true">Todas ({len(M)})</button>
      <button type="button" data-filtro="jornal" aria-pressed="false">Correio Braziliense ({n_j})</button>
      <button type="button" data-filtro="revista" aria-pressed="false">Revistas ({len(M) - n_j})</button>
    </div>
    <div class="materias">{"".join(cards)}</div>
  </div>
</section>"""
    pagina("impresso.html", "Impresso", "Matérias de Thiago Soares no Correio Braziliense e nas revistas Encontro e PQN.", corpo)


def gerar_radio():
    P = D["radio"]["playlist"]
    faixas = "".join(
        f'<li data-src="assets/audio/{Path(f["arquivo"]).name}" data-titulo="{e(f["titulo"])}" data-duracao="{f["duracao"]}">'
        f'<button type="button"><span class="num">{i:02d}</span><span>{e(f["titulo"])}</span><span class="dur">{f["duracao"]}</span></button></li>'
        for i, f in enumerate(P["faixas"], 1))
    corpo = f"""{topo_interno("Rádio", D["radio"]["texto"])}
<section class="pagina-corpo">
  <div class="container">
    <div class="player revela" data-player>
      <figure class="player-capa"><img src="assets/img/fotos/01-esplanada-1600.jpg" alt="Thiago Soares com a Esplanada dos Ministérios ao fundo" loading="lazy"></figure>
      <div class="player-corpo">
        <span class="sobretitulo">Playlist</span>
        <h2>{e(P["nome"])}</h2>
        <p>{e(P["descricao"])}</p>
        <div class="tocando">
          <div class="tocando-titulo" aria-live="polite"></div>
          <div class="tocando-autor">Thiago Soares</div>
          <div class="barra">
            <span data-tempo="atual">00:00</span>
            <input type="range" min="0" max="1000" value="0" step="1" aria-label="Posição do áudio">
            <span data-tempo="total">00:00</span>
          </div>
          <div class="controles">
            <button type="button" data-acao="anterior" aria-label="Faixa anterior">{I["ant"]}</button>
            <button type="button" class="principal" data-acao="tocar" aria-label="Tocar"></button>
            <button type="button" data-acao="proxima" aria-label="Próxima faixa">{I["prox"]}</button>
          </div>
        </div>
        <ol class="faixas-audio">{faixas}</ol>
        <audio preload="none"></audio>
      </div>
    </div>
  </div>
</section>"""
    pagina("radio.html", "Rádio", "Trabalhos de Thiago Soares em rádio e podcast: Rádio Globo e OAB Cast.", corpo)


def gerar_curriculo():
    cv = D["curriculo"]
    exp = "".join(
        f'<li class="revela"><span class="cargo">{e(x["cargo"])}</span><div><h3>{e(x["empresa"])}</h3>'
        f'<span class="periodo">{e(x["periodo"])}</span><p>{e(x["descricao"])}</p></div></li>'
        for x in cv["experiencias"])
    paras = "".join(f"<p>{e(p)}</p>" for p in cv["paragrafos"])
    corpo = f"""{topo_interno("Currículo", None, ("index.html", "Início"))}
<section class="pagina-corpo">
  <div class="container estreito">
    <div class="cv-cabeca revela"><h2>Thiago Soares</h2><span class="assinatura">• Jornalista •</span></div>
    <div class="cv-texto revela"><p class="lead">{e(cv["abertura"])}</p>{paras}</div>
    <h2 class="cv-titulo revela">{e(cv["experiencia_titulo"])}</h2>
    <ol class="linha-tempo">{exp}</ol>
  </div>
</section>
{contato_html()}"""
    pagina("curriculo.html", "Currículo", "Currículo de Thiago Soares: Correio Braziliense, RecordTV Brasília, "
           "OAB Nacional, MPT, Ministério da Justiça e ANTT.", corpo)


def gerar_404():
    corpo = f"""<section class="erro"><div class="container">
  <div class="moldura"><h1>Página não encontrada</h1></div>
  <p>O endereço pode ter mudado com o site novo.</p>
  <a class="botao" href="index.html">Ir para o início</a>
</div></section>"""
    pagina("404.html", "Página não encontrada", "Página não encontrada.", corpo)


if __name__ == "__main__":
    print("Gerando páginas:")
    gerar_inicio(); gerar_trabalhos(); gerar_video(); gerar_impresso(); gerar_radio(); gerar_curriculo(); gerar_404()
