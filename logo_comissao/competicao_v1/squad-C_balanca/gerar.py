"""Squad C (Balanca digital): gera rascunhos e entregaveis.
Rodar a partir de competicao_v1:  python -I squad-C_balanca/gerar.py [rascunhos|final]
"""
import sys, pathlib, subprocess, base64

BASE = pathlib.Path(__file__).resolve().parent.parent
SQ = BASE / "squad-C_balanca"
KIT = BASE / "_kit"
FONT = (KIT / "barlow_fontface.css").read_text(encoding="utf-8").strip()
OAB = (KIT / "oab_para_datauri.txt").read_text(encoding="utf-8").strip()
OAB_W, OAB_H = 347, 202

MAR, AZU, VER, TXT, BRA = "#003399", "#008BD2", "#D2091E", "#1B1B1B", "#FFFFFF"


def render(svg_path, png_path, w, h, bg=None):
    args = [sys.executable, "-I", str(KIT / "render.py"), str(svg_path), str(png_path), str(w), str(h)]
    if bg:
        args.append(bg)
    r = subprocess.run(args, cwd=str(BASE), capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(r.stderr)
    print(r.stdout.strip())


def svg_doc(w, h, body, font=False, extra_style=""):
    style = ""
    if font or extra_style:
        style = "<style>" + (FONT if font else "") + extra_style + "</style>"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'{style}{body}</svg>')


# ---------------------------------------------------------------------------
# Rascunho A / final: balanca em pixels numa grade 16x16
# M = marinho, A = azul, R = vermelho
PIXEL_GRID_V1 = [  # rascunho A: pendurais retos
    "................",
    "................",
    ".......RR.......",
    ".......RR.......",
    ".MMMMMMMMMMMMMM.",
    "..A....MM....A..",
    "..A....MM....A..",
    "..A....MM....A..",
    "AAAAA..MM..AAAAA",
    ".AAA...MM...AAA.",
    ".......MM.......",
    ".......MM.......",
    ".......MM.......",
    ".....MMMMMM.....",
    "...MMMMMMMMMM...",
    "................",
]

PIXEL_GRID = [  # versao final: cordas em V, leitura classica
    "................",
    ".......RR.......",
    ".......RR.......",
    ".MMMMMMMMMMMMMM.",
    "..A....MM....A..",
    ".A.A...MM...A.A.",
    "A...A..MM..A...A",
    "AAAAA..MM..AAAAA",
    ".AAA...MM...AAA.",
    ".......MM.......",
    ".......MM.......",
    ".......MM.......",
    ".....MMMMMM.....",
    "...MMMMMMMMMM...",
    "................",
    "................",
]


def pixel_symbol(grid=PIXEL_GRID, gap=0.0, radius=0.0, colors=None, x0=0, y0=0, size=16):
    """Desenha a grade como quadrados. gap e radius em fracao do modulo."""
    colors = colors or {"M": MAR, "A": AZU, "R": VER}
    n = len(grid)
    m = size / n
    g = gap * m
    out = []
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == ".":
                continue
            x = x0 + c * m + g / 2
            y = y0 + r * m + g / 2
            s = m - g
            rx = f' rx="{radius * m:.3f}"' if radius else ""
            out.append(f'<rect x="{x:.3f}" y="{y:.3f}" width="{s:.3f}" height="{s:.3f}"{rx} fill="{colors[ch]}"/>')
    return "".join(out)


def pixel_symbol_merged(grid=PIXEL_GRID, colors=None, x0=0, y0=0, size=16):
    """Sem vaos: junta corridas horizontais (favicon nitido)."""
    colors = colors or {"M": MAR, "A": AZU, "R": VER}
    n = len(grid)
    m = size / n
    out = []
    for r, row in enumerate(grid):
        c = 0
        while c < n:
            ch = row[c]
            if ch == ".":
                c += 1
                continue
            e = c
            while e < n and row[e] == ch:
                e += 1
            out.append(f'<rect x="{x0 + c * m:g}" y="{y0 + r * m:g}" width="{(e - c) * m:g}" height="{m:g}" fill="{colors[ch]}"/>')
            c = e
    return "".join(out)


# Rascunho B: coluna em forma de cursor de texto (I-beam)
def cursor_symbol():
    return (
        # cursor I-beam (coluna)
        f'<rect x="46" y="22" width="8" height="58" fill="{AZU}"/>'
        f'<rect x="37" y="16" width="26" height="7" fill="{AZU}"/>'
        f'<rect x="37" y="79" width="26" height="7" fill="{AZU}"/>'
        # travessao da balanca (barra horizontal)
        f'<rect x="8" y="30" width="84" height="7" fill="{MAR}"/>'
        # pendurais
        f'<rect x="15" y="37" width="4" height="16" fill="{MAR}"/>'
        f'<rect x="81" y="37" width="4" height="16" fill="{MAR}"/>'
        # pratos planos com ponto de dado quadrado
        f'<rect x="4" y="53" width="26" height="6" fill="{MAR}"/>'
        f'<rect x="70" y="53" width="26" height="6" fill="{MAR}"/>'
        f'<rect x="12" y="44" width="10" height="9" fill="{VER}"/>'
        f'<rect x="78" y="44" width="10" height="9" fill="{VER}"/>'
    )


# Rascunho C: balanca classica dentro de uma moldura de selecao (alcas)
def selecao_symbol():
    h = 7
    corners = [(8, 8), (92, 8), (8, 92), (92, 92)]
    frame = (f'<rect x="8" y="8" width="84" height="84" fill="none" stroke="{AZU}" stroke-width="1.6"/>')
    handles = "".join(
        f'<rect x="{x - h / 2}" y="{y - h / 2}" width="{h}" height="{h}" fill="{BRA}" stroke="{AZU}" stroke-width="1.6"/>'
        for x, y in corners)
    bal = (
        f'<rect x="47" y="26" width="6" height="46" fill="{MAR}"/>'
        f'<rect x="20" y="30" width="60" height="5" fill="{MAR}"/>'
        f'<path d="M24 35 L16 54 M24 35 L32 54 M76 35 L68 54 M76 35 L84 54" stroke="{MAR}" stroke-width="2"/>'
        f'<path d="M13 54 H35 A11 9 0 0 1 13 54 Z" fill="{MAR}"/>'
        f'<path d="M65 54 H87 A11 9 0 0 1 65 54 Z" fill="{MAR}"/>'
        f'<path d="M36 76 H64 L58 70 H42 Z" fill="{MAR}"/>'
        f'<rect x="46" y="19" width="8" height="8" fill="{VER}"/>'
    )
    return frame + handles + bal


def rascunhos():
    out = SQ / "rascunhos"
    out.mkdir(exist_ok=True)
    va = svg_doc(16, 16, pixel_symbol(PIXEL_GRID_V1, gap=0.14, radius=0.08))
    va_m = svg_doc(16, 16, pixel_symbol_merged(PIXEL_GRID_V1))
    vd = svg_doc(16, 16, pixel_symbol(PIXEL_GRID, gap=0.14, radius=0.08))
    vd_m = svg_doc(16, 16, pixel_symbol_merged(PIXEL_GRID))
    vb = svg_doc(100, 100, cursor_symbol())
    vc = svg_doc(100, 100, selecao_symbol())
    items = [("A_pixel", va, va_m), ("B_cursor", vb, vb), ("C_selecao", vc, vc), ("D_pixel_refinado", vd, vd_m)]
    for name, big, small in items:
        p = out / f"{name}.svg"
        p.write_text(big, encoding="utf-8")
        ps = out / f"{name}_pequeno.svg"
        ps.write_text(small, encoding="utf-8")
        render(p, out / f"{name}_512.png", 512, 512)
        render(ps, out / f"{name}_32.png", 32, 32)
        render(ps, out / f"{name}_16.png", 16, 16)
    # prancha de comparacao dos rascunhos
    cells = []
    for i, (name, _, _) in enumerate(items):
        x = 20 + i * 420
        b = lambda f: "data:image/png;base64," + base64.b64encode((out / f).read_bytes()).decode()
        cells.append(
            f'<image href="{b(name + "_512.png")}" x="{x}" y="20" width="380" height="380"/>'
            f'<image href="{b(name + "_32.png")}" x="{x}" y="420" width="32" height="32" style="image-rendering:pixelated"/>'
            f'<image href="{b(name + "_16.png")}" x="{x + 50}" y="420" width="16" height="16" style="image-rendering:pixelated"/>'
            f'<image href="{b(name + "_32.png")}" x="{x + 90}" y="420" width="96" height="96" style="image-rendering:pixelated"/>'
            f'<image href="{b(name + "_16.png")}" x="{x + 200}" y="420" width="96" height="96" style="image-rendering:pixelated"/>'
            f'<text x="{x}" y="560" font-family="Barlow" font-weight="700" font-size="28" fill="{MAR}">{name.replace("_", " ")}</text>')
    comp = svg_doc(1700, 600, "".join(cells), font=True)
    (out / "comparacao.svg").write_text(comp, encoding="utf-8")
    render(out / "comparacao.svg", out / "comparacao.png", 1700, 600)



# ---------------------------------------------------------------------------
# Entregaveis finais (simbolo escolhido: D, balanca em pixels com cordas em V)
# Revisao da direcao de arte (ver PARECER_DIRECAO.md):
#  - modulos fundidos em TODOS os tamanhos (o desenho grande e o mesmo do favicon),
#    um unico path por cor para nao haver emenda de antisserrilhado entre linhas;
#  - horizontal refeita: modulo = altura de versal do "PJe" / 11; o travessao alinha
#    com o topo do P, a base da balanca pousa na linha de base do "PJe", o remate
#    vermelho ocupa a faixa da linha de apoio; linha de apoio com a largura de tinta
#    do "PJe"; regua corre do pe do simbolo ate a marca OAB, que assina a direita;
#  - versao negativa: estrutura e pratos em branco, so o remate em vermelho.
APOIO = "COMISSÃO ESTADUAL DE APOIO INSTITUCIONAL AO"
# Metricas de tinta do Barlow medidas no Edge (em em)
PJE_ESQ, PJE_TINTA = 0.046, 1.627     # "PJe" 800: recuo do P e largura de tinta
APOIO_ESQ = 0.05                      # "C" 600: recuo lateral
APOIO_DIR = 0.035                     # ajuste medido: sobra a direita do "O" com textLength
CAP = 0.70                            # altura de versal
# Marca OAB (caixa 347 x 202): tinta encosta a esquerda; recuos medidos nas outras bordas
OAB_DIR, OAB_TOPO, OAB_BAIXO = 0.033, 0.010, 0.047
COLS, ROW0, ROWS = 16, 1, 13          # conteudo da grade: 16 colunas, linhas 1 a 13
CORES_CLARO = {"M": MAR, "A": AZU, "R": VER}
CORES_MARINHO = {"M": BRA, "A": BRA, "R": VER}


def pixel_paths(grid, colors, x0, y0, m):
    """Um unico path por cor, com corridas horizontais: modulos fundidos, sem emendas."""
    d = {}
    for r, row in enumerate(grid):
        c = 0
        while c < len(row):
            ch = row[c]
            if ch == ".":
                c += 1
                continue
            e = c
            while e < len(row) and row[e] == ch:
                e += 1
            x, y, w = x0 + c * m, y0 + r * m, (e - c) * m
            d.setdefault(ch, []).append(f"M{x:.3f} {y:.3f}h{w:.3f}v{m:.3f}h{-w:.3f}z")
            c = e
    ordem = [k for k in ("A", "M", "R") if k in d]
    return "".join(f'<path fill="{colors[k]}" d="{"".join(d[k])}"/>' for k in ordem)


def simbolo_em(x, y, w, cores=CORES_CLARO):
    """Simbolo com o canto superior esquerdo do CONTEUDO em (x, y) e largura w."""
    m = w / COLS
    return pixel_paths(PIXEL_GRID, cores, x, y - ROW0 * m, m)


# --- logo horizontal ---------------------------------------------------------
FP, FA = 400, 24                      # corpo do "PJe" e da linha de apoio
MOD = CAP * FP / 11                   # modulo: versal do PJe = 11 modulos (travessao a base)
X_TXT = COLS * MOD + 2 * MOD          # inicio da tinta do texto
LARG_TXT = PJE_TINTA * FP             # largura de tinta do PJe = largura da linha de apoio
X_DIR = X_TXT + LARG_TXT              # borda direita do conjunto
Y_BASE = ROWS * MOD                   # linha de base do PJe = pe da balanca
ALT_REGUA = 0.25 * MOD
Y_OAB = Y_BASE + 1.75 * MOD           # topo da tinta da marca OAB
OAB_ALT = 4.5 * MOD                   # altura da caixa da marca OAB
OAB_CENTRO = 0.365                    # centro do selo OAB (sem a palavra Para), em fracao da altura
MARGEM = 3 * MOD


def bloco_texto(cor_txt, cor_regua, fundo_marinho=False):
    s = []
    larg_apoio = LARG_TXT + (APOIO_ESQ + APOIO_DIR) * FA
    s.append(f'<text x="{X_TXT - APOIO_ESQ * FA:.2f}" y="{CAP * FA:.2f}" font-family="Barlow" font-weight="600" '
             f'font-size="{FA}" textLength="{larg_apoio:.2f}" lengthAdjust="spacing" fill="{cor_txt}">{APOIO}</text>')
    s.append(f'<text x="{X_TXT - PJE_ESQ * FP:.2f}" y="{Y_BASE:.2f}" font-family="Barlow" font-weight="800" '
             f'font-size="{FP}" fill="{cor_txt}">PJe</text>')
    # regua e marca OAB na mesma faixa: a regua corre ate a marca, que assina a direita
    if not fundo_marinho:
        h = OAB_ALT
        w = h * OAB_W / OAB_H
        ox = X_DIR - w * (1 - OAB_DIR)
        oy = Y_OAB - OAB_TOPO * h
        s.append(f'<image href="{OAB}" x="{ox:.2f}" y="{oy:.2f}" width="{w:.2f}" height="{h:.2f}"/>')
        y_reg = oy + OAB_CENTRO * h
        fim_reg = ox - 1.0 * MOD
        base = oy + h * (1 - OAB_BAIXO)
    else:
        pad = 0.45 * MOD                  # a placa ocupa o lugar da tinta da marca na versao clara
        ph = OAB_ALT * (1 - OAB_TOPO - OAB_BAIXO)   # mesma altura da tinta da marca na versao clara
        h = ph - 2 * pad
        w = h * OAB_W / OAB_H
        pw = w + 2 * pad
        px, py = X_DIR - pw, Y_OAB
        s.append(f'<rect x="{px:.2f}" y="{py:.2f}" width="{pw:.2f}" height="{ph:.2f}" rx="{0.4 * MOD:.2f}" fill="{BRA}"/>')
        s.append(f'<image href="{OAB}" x="{px + pad:.2f}" y="{py + pad:.2f}" width="{w:.2f}" height="{h:.2f}"/>')
        y_reg = py + pad + OAB_CENTRO * h
        fim_reg = px - 0.75 * MOD
        base = py + ph
    s.append(f'<rect x="0" y="{y_reg - ALT_REGUA / 2:.2f}" width="{fim_reg:.2f}" height="{ALT_REGUA:.2f}" fill="{cor_regua}"/>')
    return "".join(s), base


def logo_horizontal(marinho=False):
    W = 1600
    txt, base = bloco_texto(BRA if marinho else MAR, BRA if marinho else AZU, marinho)
    vx, vy = -MARGEM, -MARGEM
    vw, vh = X_DIR + 2 * MARGEM, base + 2 * MARGEM
    H = round(W * vh / vw)
    corp = []
    if marinho:
        corp.append(f'<rect x="{vx:.2f}" y="{vy:.2f}" width="{vw:.2f}" height="{vh:.2f}" fill="{MAR}"/>')
    corp.append(simbolo_em(0, 0, COLS * MOD, CORES_MARINHO if marinho else CORES_CLARO))
    corp.append(txt)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vx:.2f} {vy:.2f} {vw:.2f} {vh:.2f}" '
           f'width="{W}" height="{H}"><style>{FONT}</style>{"".join(corp)}</svg>')
    return svg, W, H


def simbolo_svg():
    S, pad = 512, 48
    w = S - 2 * pad
    h = w / COLS * ROWS
    return svg_doc(S, S, simbolo_em(pad, (S - h) / 2, w))


def avatar_svg():
    S, w = 1080, 620
    m = w / COLS
    fs = 10 * m / PJE_TINTA            # tinta do "PJe" = largura do degrau inferior da base (10 modulos)
    gap = 2 * m
    total = ROWS * m + gap + CAP * fs
    y = (S - total) / 2
    x = (S - w) / 2
    corp = [f'<rect width="{S}" height="{S}" fill="{MAR}"/>',
            simbolo_em(x, y, w, CORES_MARINHO),
            f'<text x="{x + 3 * m - PJE_ESQ * fs:.2f}" y="{y + total:.2f}" font-family="Barlow" font-weight="800" '
            f'font-size="{fs:.2f}" fill="{BRA}">PJe</text>']
    return svg_doc(S, S, "".join(corp), font=True)


def favicon_svg():
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16" shape-rendering="crispEdges">'
            + pixel_symbol_merged(PIXEL_GRID) + '</svg>')


def b64png(path):
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()


def prancha():
    import struct
    lw = 1100
    pw, ph = struct.unpack(">II", (SQ / "logo_horizontal.png").read_bytes()[16:24])
    lh = lw * ph / pw
    g = 40
    W = round(g + lw + g + lh + g)
    band = 330
    H = round(150 + 2 * (lh + g) + band + g)
    c = []
    c.append(f'<rect width="{W}" height="{H}" fill="#EEF1F6"/>')
    c.append(f'<text x="{g}" y="78" font-family="Barlow" font-weight="800" font-size="44" fill="{MAR}">Squad C | Balança digital</text>')
    c.append(f'<text x="{g}" y="118" font-family="Barlow" font-weight="500" font-size="24" fill="{TXT}">'
             f'Comissão Estadual de Apoio Institucional ao PJe | OAB/PA | todas as versões</text>')
    y1 = 150
    c.append(f'<image href="{b64png(SQ / "logo_horizontal.png")}" x="{g}" y="{y1}" width="{lw}" height="{lh:.1f}"/>')
    c.append(f'<image href="{b64png(SQ / "simbolo.png")}" x="{g + lw + g}" y="{y1}" width="{lh:.1f}" height="{lh:.1f}"/>')
    y2 = y1 + lh + g
    c.append(f'<image href="{b64png(SQ / "logo_horizontal_marinho.png")}" x="{g}" y="{y2:.1f}" width="{lw}" height="{lh:.1f}"/>')
    c.append(f'<image href="{b64png(SQ / "avatar.png")}" x="{g + lw + g}" y="{y2:.1f}" width="{lh:.1f}" height="{lh:.1f}"/>')
    y3 = y2 + lh + g
    c.append(f'<rect x="{g}" y="{y3:.1f}" width="{W - 2 * g}" height="{band}" fill="{BRA}"/>')
    f32, f16 = b64png(SQ / "favicon_32.png"), b64png(SQ / "favicon_16.png")
    px = 'style="image-rendering:pixelated"'
    t = f'font-family="Barlow" font-weight="600" font-size="20" fill="{TXT}"'
    yy = y3 + 40
    # 1) tamanho real
    c.append(f'<image href="{f32}" x="{g + 40}" y="{yy:.1f}" width="32" height="32" {px}/>')
    c.append(f'<image href="{f16}" x="{g + 100}" y="{yy + 8:.1f}" width="16" height="16" {px}/>')
    c.append(f'<text x="{g + 40}" y="{yy + 72:.1f}" {t}>32 px e 16 px,</text>')
    c.append(f'<text x="{g + 40}" y="{yy + 98:.1f}" {t}>tamanho real</text>')
    # 2) ampliados
    c.append(f'<image href="{f32}" x="{g + 260}" y="{yy:.1f}" width="192" height="192" {px}/>')
    c.append(f'<image href="{f16}" x="{g + 480}" y="{yy:.1f}" width="192" height="192" {px}/>')
    c.append(f'<text x="{g + 260}" y="{yy + 232:.1f}" {t}>favicon 32 e 16 ampliados:</text>')
    c.append(f'<text x="{g + 260}" y="{yy + 258:.1f}" {t}>um pixel por módulo da grade</text>')
    # 3) aba de navegador
    tx, ty = g + 740, yy + 10
    c.append(f'<rect x="{tx}" y="{ty:.1f}" width="420" height="44" rx="8" fill="#DDE3EC"/>')
    c.append(f'<rect x="{tx + 8}" y="{ty + 6:.1f}" width="300" height="38" rx="6" fill="{BRA}"/>')
    c.append(f'<image href="{f16}" x="{tx + 22}" y="{ty + 17:.1f}" width="16" height="16" {px}/>')
    c.append(f'<text x="{tx + 48}" y="{ty + 31:.1f}" font-family="Barlow" font-weight="500" font-size="17" fill="{TXT}">Comissão do PJe | OAB/PA</text>')
    c.append(f'<text x="{tx}" y="{ty + 90:.1f}" {t}>favicon 16 px numa aba</text>')
    c.append(f'<text x="{tx}" y="{ty + 116:.1f}" {t}>de navegador</text>')
    # 4) avatar no recorte circular das redes
    av = b64png(SQ / "avatar.png")
    cx = g + 1260
    c.append(f'<clipPath id="circ1"><circle cx="{cx + 80}" cy="{yy + 80:.1f}" r="80"/></clipPath>')
    c.append(f'<image href="{av}" x="{cx}" y="{yy:.1f}" width="160" height="160" clip-path="url(#circ1)"/>')
    c.append(f'<clipPath id="circ2"><circle cx="{cx + 220}" cy="{yy + 120:.1f}" r="20"/></clipPath>')
    c.append(f'<image href="{av}" x="{cx + 200}" y="{yy + 100:.1f}" width="40" height="40" clip-path="url(#circ2)"/>')
    c.append(f'<text x="{cx}" y="{yy + 200:.1f}" {t}>avatar no recorte circular</text>')
    c.append(f'<text x="{cx}" y="{yy + 226:.1f}" {t}>das redes, 160 e 40 px</text>')
    return svg_doc(W, H, "".join(c), font=True), W, H


def final():
    (SQ / "simbolo.svg").write_text(simbolo_svg(), encoding="utf-8")
    render(SQ / "simbolo.svg", SQ / "simbolo.png", 512, 512)
    for nome, mar in (("logo_horizontal", False), ("logo_horizontal_marinho", True)):
        svg, W, H = logo_horizontal(mar)
        (SQ / f"{nome}.svg").write_text(svg, encoding="utf-8")
        render(SQ / f"{nome}.svg", SQ / f"{nome}.png", W, H, MAR if mar else None)
    (SQ / "avatar.svg").write_text(avatar_svg(), encoding="utf-8")
    render(SQ / "avatar.svg", SQ / "avatar.png", 1080, 1080, MAR)
    (SQ / "favicon.svg").write_text(favicon_svg(), encoding="utf-8")
    render(SQ / "favicon.svg", SQ / "favicon_32.png", 32, 32)
    render(SQ / "favicon.svg", SQ / "favicon_16.png", 16, 16)
    svg, W, H = prancha()
    (SQ / "prancha.svg").write_text(svg, encoding="utf-8")
    render(SQ / "prancha.svg", SQ / "prancha.png", W, H, "#EEF1F6")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "final"
    if mode == "rascunhos":
        rascunhos()
    else:
        final()
