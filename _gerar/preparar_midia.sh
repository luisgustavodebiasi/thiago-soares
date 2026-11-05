#!/bin/zsh
# Gera as versões de web das fotos, capas, áudios e PDFs a partir da pasta de extração.
# Uso: zsh _gerar/preparar_midia.sh   (rodar de dentro da pasta site/)
set -e
X="../extracao-wix"
A="assets"
mkdir -p $A/img/fotos $A/img/capas $A/img/videos $A/audio $A/pdf

web(){ # origem destino largura qualidade  (nunca amplia)
  local w=$(sips -g pixelWidth "$1" | awk '/pixel/{print $2}')
  local alvo=$3; [ $w -lt $alvo ] && alvo=$w
  sips -s format jpeg -s formatOptions ${4:-72} --resampleWidth $alvo "$1" --out "$2" >/dev/null
}

O="$X/fotos/originais-do-wix"
F="$X/fotos"
web "$O/RON_2579-stf-original-do-hero.jpg"            $A/img/fotos/hero-2400.jpg 2400 68
web "$O/RON_2579-stf-original-do-hero.jpg"            $A/img/fotos/hero-1200.jpg 1200 72
web "$O/RON_2643-planalto-original-da-galeria.jpg"    $A/img/fotos/planalto-2400.jpg 2400 66
web "$O/RON_2643-planalto-original-da-galeria.jpg"    $A/img/fotos/planalto-1200.jpg 1200 70
web "$O/RON_2708_edited-aeroporto-3000-sem-clarear.jpg" $A/img/fotos/aeroporto-2000.jpg 2000 66
web "$O/RON_2708_edited-aeroporto-3000-sem-clarear.jpg" $A/img/fotos/aeroporto-1000.jpg 1000 70
web "$F/home-03-retrato-sobre-mim.jpg"                $A/img/fotos/retrato-800.jpg 800 80

for f in "$F"/trabalhos-0*.jpg; do
  n=$(basename "$f" .jpg | sed 's/^trabalhos-//')
  web "$f" $A/img/fotos/$n-1600.jpg 1600 74
  web "$f" $A/img/fotos/$n-700.jpg 700 74
done

# imagem de compartilhamento (1200x630) a partir do hero
ffmpeg -v error -y -i $A/img/fotos/hero-2400.jpg -vf "scale=1200:-2,crop=1200:630:0:(ih-630)*0.35" -q:v 4 $A/img/og.jpg

# capas: tira as marcas de corte da gráfica (esq dir topo base, em fração da página)
for f in "$X"/impresso/capas/*.jpg; do
  n=$(basename "$f")
  case "$n" in
    *encontro*) m="0.0535 0.0535 0.0535 0.0535" ;;
    *carcere*)  m="0.0125 0.0125 0.065 0.05" ;;
    *pqn*)      m="0.03 0.03 0.04 0.04" ;;
    *)          m="0.025 0.025 0.065 0.05" ;;
  esac
  set -- ${=m}
  ffmpeg -v error -y -i "$f" -vf "crop=iw*(1-$1-$2):ih*(1-$3-$4):iw*$1:ih*$3,scale=560:-2" -q:v 4 $A/img/capas/$n
done
for f in "$X"/miniaturas-youtube/*.jpg; do
  web "$f" $A/img/videos/$(basename "$f") 720 74
done
web "$X/miniaturas-youtube/yQYTJbeJ2N0.jpg" $A/img/videos/destaque-yQYTJbeJ2N0.jpg 1280 78

cp "$X"/audios/*.mp3 $A/audio/
cp "$X"/impresso/pdfs/*.pdf $A/pdf/
echo "mídia pronta"

# cortes verticais (4:5) para o retrato do "Sobre" e para a capa no celular
ffmpeg -v error -y -i "$O/RON_2708-aeroporto-original-do-sobre-mim.jpg" -vf "crop=2892:3615:1861:0,scale=1000:1250" -q:v 4 $A/img/fotos/retrato-vertical.jpg
ffmpeg -v error -y -i "$O/RON_2579-stf-original-do-hero.jpg" -vf "crop=2891:3614:0:0,scale=1080:1350" -q:v 4 $A/img/fotos/hero-celular.jpg
echo "cortes prontos"
