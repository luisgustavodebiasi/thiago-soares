#!/usr/bin/env python3
"""Gera as páginas HTML do site a partir de _gerar/dados.json.

Uso (de dentro da pasta site/):  python3 _gerar/gerar.py
Para mudar um texto, um vídeo ou uma matéria: edite dados.json e rode de novo.
"""
import html
import json
import re
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
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{corpo}</svg>')


I = {
    "linkedin": ic('<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/>'),
    "facebook": ic('<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>'),
    "youtube": ic('<path d="M2.5 17a24.1 24.1 0 0 1 0-10 2 2 0 0 1 1.4-1.4 49.6 49.6 0 0 1 16.2 0A2 2 0 0 1 21.5 7a24.1 24.1 0 0 1 0 10 2 2 0 0 1-1.4 1.4 49.6 49.6 0 0 1-16.2 0A2 2 0 0 1 2.5 17"/><path d="m10 15 5-3-5-3z"/>'),
    "instagram": ic('<rect x="2" y="2" width="20" height="20" rx="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><path d="M17.5 6.5h.01"/>'),
    "email": ic('<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>'),
    "telefone": ic('<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.1 9.9a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>'),
    "whatsapp": ic('<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>'),
    "menu": ic('<path d="M4 8h16M4 16h16"/>').replace("<svg ", '<svg class="tres" '),
    "x": ic('<path d="M18 6 6 18M6 6l12 12"/>').replace("<svg ", '<svg class="x" '),
    "seta": ic('<path d="M5 12h14M13 6l6 6-6 6"/>'),
    "seta_diag": ic('<path d="M7 17 17 7M8 7h9v9"/>'),
    "cima": ic('<path d="M12 19V5M6 11l6-6 6 6"/>'),
    "play": ic('<path d="M8 5.5v13a1 1 0 0 0 1.5.86l10.4-6.5a1 1 0 0 0 0-1.72L9.5 4.64A1 1 0 0 0 8 5.5Z"/>', True),
    "ant": ic('<path d="M19 20 9 12l10-8z" fill="currentColor"/><path d="M5 19V5"/>'),
    "prox": ic('<path d="m5 4 10 8-10 8z" fill="currentColor"/><path d="M19 5v14"/>'),
    "pdf": ic('<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M9 13h6M9 17h6"/>'),
}

R = D["redes"]
C = D["contato"]
TEL_DIGITOS = "55" + "".join(ch for ch in C["telefone"] if ch.isdigit())
REDES = [("LinkedIn", R["linkedin"], "linkedin"), ("Instagram", R["instagram"], "instagram"),
         ("YouTube", R["youtube"], "youtube"), ("Facebook", R["facebook"], "facebook")]

N_VIDEOS = 1 + sum(len(g["videos"]) for g in D["video"]["grupos"])
N_MATERIAS = len(D["impresso"]["materias"])
N_AUDIOS = len(D["radio"]["playlist"]["faixas"])


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
    marca = ' aria-current="page"'
    lis = []
    for item in MENU:
        href, rotulo = item[0], item[1]
        cur = marca if href == atual else ""
        if len(item) == 3:
            filhos = item[2]
            ativo = " ativo" if any(h == atual for h, _ in filhos) else ""
            sub = "".join(f'<li><a href="{h}"{marca if h == atual else ""}>{r}</a></li>' for h, r in filhos)
            lis.append(f'<li class="sub{ativo}"><a href="{href}"{cur}>{rotulo}</a><ul>{sub}</ul></li>')
        else:
            lis.append(f'<li><a href="{href}"{cur}>{rotulo}</a></li>')
    return "".join(lis)


def rodape_html():
    nav = "".join(f'<li><a href="{h}">{r}</a></li>' for h, r in [
        ("index.html", "Início"), ("trabalhos.html", "Meus trabalhos"), ("video.html", "Vídeo"),
        ("impresso.html", "Impresso"), ("radio.html", "Rádio"), ("curriculo.html", "Currículo")])
    redes = "".join(f'<li><a href="{e(u)}" target="_blank" rel="noopener">{n}</a></li>' for n, u, _ in REDES)
    r = D["site"]["rodape"]
    return f"""<footer class="rodape">
  <div class="container">
    <div class="rodape-topo">
      <div>
        <p class="rodape-nome">Thiago <em>Soares</em></p>
        <p>Jornalista em Brasília. TV, impresso, rádio e assessoria de imprensa.</p>
      </div>
      <div><h2>Navegação</h2><ul>{nav}</ul></div>
      <div><h2>Contato</h2><ul><li><a href="https://wa.me/{TEL_DIGITOS}" target="_blank" rel="noopener">WhatsApp</a></li><li><a href="tel:+{TEL_DIGITOS}">{e(C["telefone"])}</a></li>{redes}</ul></div>
    </div>
    <div class="rodape-base">
      <p>© {ANO} Thiago Soares</p>
      <p class="direitos">{e(r["aviso"])} {e(r["aviso_2"])}</p>
      <a class="voltar-topo" href="#conteudo">Topo <span>{I["cima"]}</span></a>
    </div>
  </div>
</footer>"""


def pagina(arquivo, titulo, descricao, corpo, extra_head="", classe=""):
    t = f"{titulo} | Thiago Soares, jornalista" if titulo else "Thiago Soares | Jornalista em Brasília"
    url = BASE + ("" if arquivo == "index.html" else arquivo)
    doc = f"""<!doctype html>
<html lang="pt-BR" class="sem-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(t)}</title>
<meta name="description" content="{e(descricao)}">
<meta name="theme-color" content="#0a2740">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:title" content="{e(t)}">
<meta property="og:description" content="{e(descricao)}">
<meta property="og:site_name" content="Thiago Soares · Jornalista">
<meta property="og:image" content="{BASE}assets/img/og-thiago-soares.jpg">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Thiago Soares, jornalista em Brasília, de terno, ao lado do nome e das áreas Vídeo, Impresso e Rádio">
<meta name="twitter:image" content="{BASE}assets/img/og-thiago-soares.jpg">
<meta property="og:url" content="{url}">
<link rel="canonical" href="{url}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,300..600;1,6..72,300..500&display=swap">
<link rel="stylesheet" href="assets/css/style.css">
{extra_head}</head>
<body class="{classe}">
<a class="pular" href="#conteudo">Pular para o conteúdo</a>
<header class="topo">
  <div class="container">
    <a class="logo" href="index.html" aria-label="Thiago Soares, página inicial"><strong>Thiago <em>Soares</em></strong><span>Jornalista</span></a>
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
{rodape_html()}
<script src="assets/js/main.js" defer></script>
</body>
</html>
"""
    (RAIZ / arquivo).write_text(doc, encoding="utf-8")
    print("  ", arquivo)


def topo_interno(titulo_html, intro, trilha, contagem="", numero=""):
    passos = [("index.html", "Início")] + trilha
    t = "".join(f'<li><a href="{h}">{r}</a></li>' if h else f'<li aria-current="page">{r}</li>' for h, r in passos)
    n = f'<span class="numero-fundo" aria-hidden="true">{numero}</span>' if numero else ""
    c = f'<span class="contagem">{contagem}</span>' if contagem else ""
    return f"""<section class="pagina-topo">
  {n}
  <div class="container">
    <ol class="trilha">{t}</ol>
    <div class="grade">
      <h1 class="revela">{titulo_html}</h1>
      <div class="revela"><p class="intro">{e(intro)}</p>{c}</div>
    </div>
  </div>
</section>"""


def areas_html():
    capas = [m for m in D["impresso"]["materias"] if any(k in m["pdf"] for k in ("temer", "infancia", "gastos"))]
    pilha = "".join(f'<img src="assets/img/capas/{Path(m["capa"]).name}" alt="" loading="lazy">' for m in capas[:3])
    return f"""<div class="areas" data-escalonar>
  <a class="area video revela" href="video.html">
    <img src="assets/img/fotos/04-oab-1600.jpg" alt="" loading="lazy">
    <span class="num">01</span>
    <h3>Vídeo</h3>
    <p>{N_VIDEOS} vídeos de reportagem e apresentação, da TV Justiça à RecordTV.</p>
    <span class="ir"><span>{I["seta"]}</span>Assistir</span>
  </a>
  <a class="area impresso revela" href="impresso.html">
    <div class="pilha">{pilha}</div>
    <span class="num">02</span>
    <h3>Impresso</h3>
    <p>{N_MATERIAS} matérias assinadas no Correio Braziliense e nas revistas Encontro e PQN.</p>
    <span class="ir"><span>{I["seta"]}</span>Ler</span>
  </a>
  <a class="area radio revela" href="radio.html">
    <img src="assets/img/fotos/06-bastidor-luz-1600.jpg" alt="" loading="lazy">
    <span class="num">03</span>
    <h3>Rádio</h3>
    <p>{N_AUDIOS} áudios entre o noticiário de rádio e o podcast OAB Cast.</p>
    <span class="ir"><span>{I["seta"]}</span>Ouvir</span>
  </a>
</div>"""


def contato_html():
    return f"""<section class="secao contato" id="contato">
  <div class="container contato-grade">
    <div class="revela">
      <span class="rotulo">Contato</span>
      <h2 class="titulo">Fale <em>comigo.</em></h2>
      <p class="texto-contato">Para trabalhos, pautas e parcerias, chame no WhatsApp ou ligue.</p>
      {redes_html()}
    </div>
    <div class="contato-opcoes revela">
      <a class="opcao destaque" href="https://wa.me/{TEL_DIGITOS}" target="_blank" rel="noopener">
        <span class="opcao-icone">{I["whatsapp"]}</span>
        <span class="opcao-texto"><small>WhatsApp</small><strong>Mandar mensagem</strong></span>
        <span class="opcao-seta">{I["seta_diag"]}</span>
      </a>
      <a class="opcao" href="tel:+{TEL_DIGITOS}">
        <span class="opcao-icone">{I["telefone"]}</span>
        <span class="opcao-texto"><small>Telefone</small><strong>{e(C["telefone"])}</strong></span>
        <span class="opcao-seta">{I["seta_diag"]}</span>
      </a>
    </div>
  </div>
</section>"""


# ---------------------------------------------------------------- páginas
def gerar_inicio():
    s = D["inicio"]["sobre"]
    d = D["video"]["destaque"]
    passagens = ["Correio Braziliense", "RecordTV Brasília", "OAB Nacional", "MPT · Trabalho Legal",
                 "Ministério da Justiça", "ANTT"]
    pessoa = {
        "@context": "https://schema.org", "@type": "Person", "name": "Thiago Soares",
        "jobTitle": "Jornalista", "url": BASE, "telephone": "+" + TEL_DIGITOS,
        "image": BASE + "assets/img/fotos/retrato-vertical.jpg",
        "address": {"@type": "PostalAddress", "addressLocality": "Brasília", "addressRegion": "DF", "addressCountry": "BR"},
        "alumniOf": "Pontifícia Universidade Católica de Minas Gerais (PUC-Minas)",
        "sameAs": [u for _, u, _ in REDES],
    }
    head = ('<link rel="preload" as="image" href="assets/img/fotos/hero-1200.jpg" media="(min-width: 901px)" '
            'imagesrcset="assets/img/fotos/hero-1200.jpg 1200w, assets/img/fotos/hero-2400.jpg 2400w" imagesizes="100vw">\n'
            '<link rel="preload" as="image" href="assets/img/fotos/hero-celular.jpg" media="(max-width: 900px)">\n'
            f'<script type="application/ld+json">{json.dumps(pessoa, ensure_ascii=False)}</script>\n')
    corpo = f"""<section class="hero">
  <picture>
    <source media="(max-width: 900px)" srcset="assets/img/fotos/hero-celular.jpg">
    <img src="assets/img/fotos/hero-1200.jpg" srcset="assets/img/fotos/hero-1200.jpg 1200w, assets/img/fotos/hero-2400.jpg 2400w" sizes="100vw"
      alt="Thiago Soares de terno em frente à estátua da Justiça, no Supremo Tribunal Federal" fetchpriority="high">
  </picture>
  <div class="container">
    <div class="hero-texto">
      <span class="rotulo">Jornalista · Brasília</span>
      <h1>Thiago <br class="quebra"><em>Soares</em></h1>
      <p class="hero-sub">Reportagem, apresentação e texto para TV, jornal, revista e rádio. Hoje, assessor de imprensa da ANTT.</p>
      <div class="hero-acoes">
        <a class="botao claro" href="trabalhos.html">Ver trabalhos {I["seta"]}</a>
        <a class="link-seta" href="#contato">Fale comigo</a>
      </div>
    </div>
  </div>
  <a class="rolar" href="#sobre">Role</a>
</section>

<section class="secao papel" id="sobre">
  <div class="container sobre-grade">
    <figure class="retrato revela">
      <img src="assets/img/fotos/retrato-vertical.jpg" alt="Retrato de Thiago Soares, sorrindo, de óculos e camisa xadrez" loading="lazy" width="1000" height="1250">
      <figcaption>Brasília · DF</figcaption>
    </figure>
    <div class="sobre-texto revela">
      <span class="rotulo">Sobre mim</span>
      <h2 class="titulo">Do rádio à TV, <em>do papel à web.</em></h2>
      <p class="lead">{e(s["texto"])}</p>
      <dl class="fatos">
        <div><dt>2009</dt><dd>no jornalismo, desde a redação da Revista Viver Brasil</dd></div>
        <div><dt>2012</dt><dd>em Brasília, onde vive e trabalha</dd></div>
        <div><dt>4</dt><dd>formatos: TV, impresso, rádio e web</dd></div>
      </dl>
      <a class="botao" href="curriculo.html">{e(s["botao"]["rotulo"])} {I["seta"]}</a>
    </div>
  </div>
</section>

<section class="passagens" aria-label="Passagens profissionais">
  <div class="container">
    <h2>Passagens por</h2>
    <ul>{"".join(f"<li>{e(p)}</li>" for p in passagens)}</ul>
  </div>
</section>

<section class="secao escuro" id="trabalhos">
  <div class="container">
    <div class="cabeca-secao lado revela">
      <div><span class="rotulo">Portfólio</span><h2 class="titulo" style="margin-top:18px">Meus <em>trabalhos</em></h2></div>
      <p>Reportagens e programas em vídeo, matérias assinadas em jornal e revista e trabalhos em rádio e podcast.</p>
    </div>
    {areas_html()}
  </div>
</section>

<section class="secao papel destaque-secao">
  <div class="container destaque-grade">
    <div class="revela">
      <span class="rotulo">Em destaque</span>
      <h2 class="titulo">Compilado de <em>reportagens</em></h2>
      <p>Um recorte do trabalho em vídeo: reportagens e apresentações para o MPT, a OAB Nacional e a RecordTV.</p>
      <a class="link-seta" href="video.html">Todos os vídeos {I["seta"]}</a>
    </div>
    <button class="tela-video revela" type="button" data-youtube="{d["youtube"]}" data-titulo="{e(d["titulo"])}">
      <img src="assets/img/videos/destaque-{d["youtube"]}.jpg" alt="" loading="lazy">
      <span class="botao-play" aria-hidden="true">{I["play"]}</span>
      <span class="legenda-tela"><strong>Compilado de reportagens</strong><span>Assistir</span></span>
      <span class="visualmente-oculto">Assistir: {e(d["titulo"])}</span>
    </button>
  </div>
</section>

{contato_html()}"""
    pagina("index.html", "", "Thiago Soares, jornalista em Brasília. Reportagem e apresentação em TV, "
           "texto para jornal e revista, rádio e assessoria de imprensa.", corpo, head, "inicio")


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
        f'<a class="revela" href="assets/img/fotos/{n}-1600.jpg"><img src="assets/img/fotos/{n}-700.jpg" alt="{e(a)}" loading="lazy"></a>'
        for n, a in FOTOS)
    corpo = f"""{topo_interno("Meus <em>trabalhos</em>", "Reportagem, apresentação e produção em TV, texto para jornal e revista, rádio e podcast.",
                 [(None, "Meus trabalhos")], f"{len(FOTOS)} fotos · 3 áreas")}
<section class="pagina-corpo escuro">
  <div class="container">
    <div class="galeria" data-galeria data-escalonar>{fotos}</div>
    <div class="galeria-areas">
      <div class="cabeca-secao revela"><span class="rotulo">Escolha uma área</span></div>
      {areas_html()}
    </div>
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
        f'<section class="grupo"><div class="grupo-cabeca revela"><h2>{e(g["nome"])}</h2><span>{len(g["videos"])} vídeos</span></div>'
        f'<div class="cartoes" data-escalonar>{"".join(cartao_video(v) for v in g["videos"])}</div></section>'
        for g in V["grupos"])
    corpo = f"""{topo_interno("Vídeo", V["texto"], [("trabalhos.html", "Meus trabalhos"), (None, "Vídeo")],
                 f"{N_VIDEOS} vídeos · {len(V['grupos'])} programas", "01")}
<section class="pagina-corpo escuro">
  <div class="container">
    <button class="tela-video revela" type="button" data-youtube="{d["youtube"]}" data-titulo="{e(d["titulo"])}">
      <img src="assets/img/videos/destaque-{d["youtube"]}.jpg" alt="" loading="lazy">
      <span class="botao-play" aria-hidden="true">{I["play"]}</span>
      <span class="legenda-tela"><strong>Compilado de reportagens</strong><span>Destaque</span></span>
      <span class="visualmente-oculto">Assistir: {e(d["titulo"])}</span>
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
    anos = sorted(int(m["data"][:4]) for m in M)
    corpo = f"""{topo_interno("Impresso", D["impresso"]["texto"], [("trabalhos.html", "Meus trabalhos"), (None, "Impresso")],
                 f"{N_MATERIAS} matérias · {anos[0]} a {anos[-1]}", "02")}
<section class="pagina-corpo papel">
  <div class="container">
    <div class="filtros revela" role="group" aria-label="Filtrar matérias">
      <button type="button" data-filtro="todos" aria-pressed="true">Todas ({len(M)})</button>
      <button type="button" data-filtro="jornal" aria-pressed="false">Correio Braziliense ({n_j})</button>
      <button type="button" data-filtro="revista" aria-pressed="false">Revistas ({len(M) - n_j})</button>
    </div>
    <div class="materias" data-escalonar>{"".join(cards)}</div>
  </div>
</section>"""
    pagina("impresso.html", "Impresso", "Matérias de Thiago Soares no Correio Braziliense e nas revistas Encontro e PQN.", corpo)


def gerar_radio():
    P = D["radio"]["playlist"]
    seg = sum(int(f["duracao"].split(":")[0]) * 60 + int(f["duracao"].split(":")[1]) for f in P["faixas"])
    faixas = "".join(
        f'<li data-src="assets/audio/{Path(f["arquivo"]).name}" data-titulo="{e(f["titulo"])}" data-duracao="{f["duracao"]}">'
        f'<button type="button"><span class="num">{i:02d}</span><span>{e(f["titulo"])}</span><span class="dur">{f["duracao"]}</span></button></li>'
        for i, f in enumerate(P["faixas"], 1))
    corpo = f"""{topo_interno("Rádio", D["radio"]["texto"], [("trabalhos.html", "Meus trabalhos"), (None, "Rádio")],
                 f"{N_AUDIOS} áudios · {round(seg / 60)} minutos", "03")}
<section class="pagina-corpo escuro">
  <div class="container">
    <div class="player revela" data-player>
      <figure class="player-capa"><img src="assets/img/fotos/06-bastidor-luz-1600.jpg" alt="Thiago Soares nos bastidores de uma gravação, com microfone e luz de estúdio" loading="lazy"></figure>
      <div class="player-corpo">
        <span class="rotulo">Playlist</span>
        <h2>{e(P["nome"])}</h2>
        <p>{e(P["descricao"])}</p>
        <div class="tocando">
          <div class="tocando-linha">
            <div><div class="tocando-titulo" aria-live="polite"></div><div class="tocando-autor">Thiago Soares</div></div>
            <span class="ondas" aria-hidden="true"><i></i><i></i><i></i><i></i></span>
          </div>
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
    pagina("radio.html", "Rádio", "Trabalhos de Thiago Soares em rádio e podcast: noticiário de rádio e OAB Cast.", corpo)


def gerar_curriculo():
    cv = D["curriculo"]
    itens = []
    for x in cv["experiencias"]:
        anos = re.findall(r"(?:19|20)\d{2}", x["periodo"])
        inicio = anos[0] if anos else ""
        itens.append(
            f'<li class="revela"><div class="anos">{inicio}<small>{e(x["periodo"])}</small></div>'
            f'<div><span class="cargo">{e(x["cargo"])}</span><h3>{e(x["empresa"])}</h3><p>{e(x["descricao"])}</p></div></li>')
    paras = "".join(f"<p>{e(p)}</p>" for p in cv["paragrafos"])
    primeiro = min(int(a) for x in cv["experiencias"] for a in re.findall(r"(?:19|20)\d{2}", x["periodo"]))
    corpo = f"""{topo_interno("Currículo", "Jornalista formado pela PUC Minas, com passagens por redação de jornal, TV, rádio e assessoria de imprensa.",
                 [(None, "Currículo")], f"{len(cv['experiencias'])} experiências · desde {primeiro}")}
<section class="pagina-corpo papel">
  <div class="container">
    <div class="cv-abertura">
      <aside class="revela"><img src="assets/img/fotos/02-congresso-1600.jpg" alt="Thiago Soares em frente ao Congresso Nacional" loading="lazy"></aside>
      <div class="revela"><span class="rotulo">Perfil</span><p class="lead" style="margin-top:20px">{e(cv["abertura"])}</p>{paras}</div>
    </div>
    <div class="cv-titulo revela"><span class="rotulo">Trajetória</span><h2 class="titulo">Experiência <em>profissional</em></h2></div>
    <ol class="linha-tempo">{"".join(itens)}</ol>
  </div>
</section>
{contato_html()}"""
    pagina("curriculo.html", "Currículo", "Currículo de Thiago Soares: Correio Braziliense, RecordTV Brasília, "
           "OAB Nacional, MPT, Ministério da Justiça e ANTT.", corpo)


def gerar_404():
    corpo = f"""<section class="pagina-topo erro"><div class="container">
  <span class="rotulo">Erro 404</span>
  <h1 style="margin-top:20px">Página não <em>encontrada</em></h1>
  <p>O endereço pode ter mudado com o site novo.</p>
  <a class="botao claro" href="index.html">Ir para o início {I["seta"]}</a>
</div></section>"""
    pagina("404.html", "Página não encontrada", "Página não encontrada.", corpo)


if __name__ == "__main__":
    print("Gerando páginas:")
    gerar_inicio(); gerar_trabalhos(); gerar_video(); gerar_impresso(); gerar_radio(); gerar_curriculo(); gerar_404()
