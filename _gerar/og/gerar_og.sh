#!/bin/zsh
# Gera assets/img/og-thiago-soares.jpg (1200x630) a partir de _gerar/og/og.html.
# Uso (de dentro da pasta site/): zsh _gerar/og/gerar_og.sh
set -e
AQUI="${0:A:h}"
TMP=$(mktemp -d)
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=1 --window-size=1200,630 --virtual-time-budget=8000 \
  --screenshot="$TMP/og.png" "file://$AQUI/og.html" >/dev/null 2>&1
ffmpeg -v error -y -i "$TMP/og.png" -q:v 2 "$AQUI/../../assets/img/og-thiago-soares.jpg"
rm -rf "$TMP"
echo "og pronta: $(du -h "$AQUI/../../assets/img/og-thiago-soares.jpg" | cut -f1)"
