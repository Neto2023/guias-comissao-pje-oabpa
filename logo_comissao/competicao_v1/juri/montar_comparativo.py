"""Monta juri/comparativo.svg (prancha do orquestrador) e renderiza em PNG.
Uso, a partir de competicao_v1:  python -I juri/montar_comparativo.py
Nao altera nenhum arquivo dos squads: apenas le as PNGs e as embute em data URI.
"""
import base64, pathlib, subprocess, sys, struct

BASE = pathlib.Path(__file__).resolve().parent.parent
JURI = BASE / "juri"
MAR, AZUL, VERM, TXT = "#003399", "#008BD2", "#D2091E", "#1B1B1B"
W, H = 2400, 1720

SQUADS = [
    ("A", "squad-A_tela-processo", "Folha que atende", (8.0, 8.5, 7.0)),
    ("B", "squad-B_monograma", "Monograma PJe", (6.5, 5.5, 6.0)),
    ("C", "squad-C_balanca", "Balança digital", (5.5, 8.0, 4.0)),
]


def uri(p):
    return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()


def dim(p):
    d = p.read_bytes()[16:24]
    return struct.unpack(">II", d)


def br(x):
    return f"{x:.2f}".replace(".", ",")


medias = {s[0]: sum(s[3]) / 3 for s in SQUADS}
ordem = sorted(medias, key=lambda k: -medias[k])
fonte = (BASE / "_kit" / "barlow_fontface.css").read_text(encoding="utf-8")

o = []
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
o.append(f"<style>{fonte} text{{font-family:'Barlow',sans-serif}} .px{{image-rendering:pixelated}}</style>")
o.append(f'<rect width="{W}" height="{H}" fill="#EEF1F6"/>')
o.append(f'<text x="80" y="112" font-size="50" font-weight="800" fill="{MAR}">Competição da logo | Comparativo final do júri</text>')
o.append(f'<text x="80" y="162" font-size="27" font-weight="500" fill="{TXT}">Comissão Estadual de Apoio Institucional ao PJe, OAB/PA. '
         f'Notas por lente: identidade | técnica | originalidade. Média simples.</text>')

colw, gap, x0 = 720, 40, 80
for i, (sq, pasta, nome, notas) in enumerate(SQUADS):
    x = x0 + i * (colw + gap)
    d = BASE / pasta
    venc = sq == ordem[0]
    pos = ordem.index(sq) + 1
    # cabecalho
    if venc:
        o.append(f'<rect x="{x-14}" y="196" width="{colw+28}" height="1448" rx="18" fill="none" stroke="{AZUL}" stroke-width="6"/>')
    o.append(f'<rect x="{x}" y="214" width="80" height="80" rx="14" fill="{MAR}"/>')
    o.append(f'<text x="{x+40}" y="273" font-size="56" font-weight="800" fill="#FFFFFF" text-anchor="middle">{sq}</text>')
    o.append(f'<text x="{x+104}" y="248" font-size="34" font-weight="700" fill="{MAR}">{nome}</text>')
    n = " | ".join(f"{v:.1f}".replace(".", ",") for v in notas)
    o.append(f'<text x="{x+104}" y="286" font-size="24" font-weight="500" fill="{TXT}">Notas {n}<tspan dx="22">Média </tspan><tspan font-weight="800">{br(medias[sq])}</tspan><tspan dx="22">{pos}º lugar</tspan></text>')
    if venc:
        o.append(f'<rect x="{x+colw-170}" y="216" width="170" height="40" rx="20" fill="{AZUL}"/>')
        o.append(f'<text x="{x+colw-85}" y="244" font-size="21" font-weight="800" fill="#FFFFFF" text-anchor="middle" letter-spacing="2">VENCEDORA</text>')

    def rotulo(y, t):
        o.append(f'<text x="{x}" y="{y}" font-size="19" font-weight="600" fill="#5A6475" letter-spacing="2.5">{t}</text>')

    def card(y, h):
        o.append(f'<rect x="{x}" y="{y}" width="{colw}" height="{h}" fill="#FFFFFF" stroke="#D5DBE5" stroke-width="2"/>')

    # simbolo
    rotulo(345, "SÍMBOLO")
    card(360, 420)
    o.append(f'<image x="{x+(colw-360)/2}" y="390" width="360" height="360" href="{uri(d/"simbolo.png")}"/>')
    # logo horizontal
    rotulo(825, "LOGO HORIZONTAL")
    card(840, 470)
    lw, lh = dim(d / "logo_horizontal.png")
    iw = 680
    ih = iw * lh / lw
    o.append(f'<image x="{x+20}" y="{840+(470-ih)/2:.1f}" width="{iw}" height="{ih:.1f}" href="{uri(d/"logo_horizontal.png")}"/>')
    # favicons
    rotulo(1355, "FAVICON: 32 PX REAL E A 4X | 16 PX REAL E A 8X")
    card(1370, 250)
    f32, f16 = uri(d / "favicon_32.png"), uri(d / "favicon_16.png")
    yb = 1410
    o.append(f'<image x="{x+40}" y="{yb+48}" width="32" height="32" href="{f32}"/>')
    o.append(f'<image class="px" x="{x+110}" y="{yb}" width="128" height="128" href="{f32}" style="image-rendering:pixelated"/>')
    o.append(f'<image x="{x+330}" y="{yb+56}" width="16" height="16" href="{f16}"/>')
    o.append(f'<image class="px" x="{x+390}" y="{yb}" width="128" height="128" href="{f16}" style="image-rendering:pixelated"/>')
    for cx, t in ((x + 56, "32"), (x + 174, "32 a 4x"), (x + 338, "16"), (x + 454, "16 a 8x")):
        o.append(f'<text x="{cx}" y="{yb+168}" font-size="19" font-weight="600" fill="#5A6475" text-anchor="middle">{t}</text>')
    # aba de navegador simulada com 16 px
    o.append(f'<rect x="{x+560}" y="{yb+46}" width="140" height="36" rx="8" fill="#EEF1F6" stroke="#D5DBE5"/>')
    o.append(f'<image x="{x+572}" y="{yb+56}" width="16" height="16" href="{f16}"/>')
    o.append(f'<text x="{x+596}" y="{yb+70}" font-size="15" font-weight="500" fill="{TXT}">Apoio ao PJe</text>')
    o.append(f'<text x="{x+630}" y="{yb+168}" font-size="19" font-weight="600" fill="#5A6475" text-anchor="middle">aba</text>')

o.append(f'<text x="80" y="{H-24}" font-size="21" font-weight="500" fill="#5A6475">Arquivos originais de cada squad, sem alteração, '
         f'embutidos nesta prancha. Detalhes e ajustes em RESULTADO.md.</text>')
o.append("</svg>")

svg = JURI / "comparativo.svg"
svg.write_text("\n".join(o), encoding="utf-8")
subprocess.run([sys.executable, "-I", str(BASE / "_kit" / "render.py"), str(svg), str(JURI / "comparativo.png"), str(W), str(H)],
               check=True, cwd=str(BASE))
print("medias", {k: round(v, 3) for k, v in medias.items()}, "ordem", ordem)
