# Thiago Soares · site de portfólio

Site estático (HTML, CSS e JS puros) feito para o GitHub Pages. Recria o antigo site Wix
(https://5z6zc9wr4q.wixsite.com/jornthiagosoares) com as mesmas seções e a mesma família de azuis.

## Páginas

| Arquivo | Conteúdo |
|---|---|
| `index.html` | Capa, Sobre mim, Passagens, cartões de Vídeo/Impresso/Rádio, vídeo em destaque e Fale comigo |
| `trabalhos.html` | Galeria de fotos (amplia ao clicar) e os três atalhos |
| `video.html` | Vídeo em destaque e 14 vídeos em três grupos (abrem numa janela, sem sair do site) |
| `impresso.html` | 12 matérias em PDF, com filtro por veículo |
| `radio.html` | Player com as 3 faixas |
| `curriculo.html` | Currículo com linha do tempo e contato (também sai bem impresso) |
| `404.html` | Página de erro |

## Como editar

Os textos, os vídeos, as matérias e o currículo ficam em `_gerar/dados.json`. Depois de mudar, rode:

```
python3 _gerar/gerar.py
```

Isso reescreve os `.html`. O visual fica em `assets/css/style.css` e as interações em `assets/js/main.js`.

Fotos, capas, áudios e PDFs saem da pasta `../extracao-wix`. Para gerar tudo de novo: `zsh _gerar/preparar_midia.sh`.

Para ver no computador: `python3 -m http.server 8000` e depois abrir http://localhost:8000.

## Publicar no GitHub Pages

1. O repositório é https://github.com/luisgustavodebiasi/thiago-soares (branch `main`).
2. No repositório, vá em **Settings > Pages**, escolha **Deploy from a branch**, branch `main` e pasta `/ (root)`.
3. O site fica em https://luisgustavodebiasi.github.io/thiago-soares/. Para usar um domínio próprio, preencha **Custom domain** no mesmo lugar e troque `BASE` em `_gerar/gerar.py`.

A pasta `_gerar` não é publicada, porque o GitHub Pages ignora pastas que começam com `_`.

## Contato

O site não tem formulário: o contato é pelo WhatsApp e pelo telefone, que vêm de `contato.telefone` no `dados.json`.
O botão de WhatsApp abre uma conversa com esse mesmo número (wa.me).

## Para confirmar com o Thiago

- "36 anos" no Sobre mim e no Currículo (texto do site antigo).
- Se o (61) 98270-8730 é WhatsApp. O site já tem um botão de WhatsApp para esse número.
- No currículo, o texto fala em "Conselho Nacional" da OAB e a experiência fala em "Conselho Federal". O nome oficial é Conselho Federal.
