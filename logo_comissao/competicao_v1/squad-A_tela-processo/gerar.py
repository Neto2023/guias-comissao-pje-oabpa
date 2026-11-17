"""Squad A (tela + processo): gera rascunhos e entregaveis da logo da Comissao do PJe.

Uso (a partir de competicao_v1):
    python -I squad-A_tela-processo/gerar.py rascunhos
    python -I squad-A_tela-processo/gerar.py final

Le _kit/barlow_fontface.css e _kit/oab_para_datauri.txt e injeta o conteudo nos SVGs.
"""
import json
import math
import pathlib
import subprocess
import sys
import base64

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parent
KIT = RAIZ / "_kit"
RASC = AQUI / "rascunhos"

MARINHO = "#003399"
AZUL = "#008BD2"
VERMELHO = "#D2091E"
TEXTO = "#1B1B1B"
BRANCO = "#FFFFFF"

FONTE = (KIT / "barlow_fontface.css").read_text(encoding="utf-8").strip()
OAB = (KIT / "oab_para_datauri.txt").read_text(encoding="utf-8").strip()
OAB_W, OAB_H = 347, 202  # dimensoes reais do JPEG


# ---------------------------------------------------------------- utilidades
def rpoly(pts, r):
    """Poligono com cantos arredondados (r pode ser numero ou lista por vertice)."""
    n = len(pts)
    rs = r if isinstance(r, (list, tuple)) else [r] * n
    seg = []
    for i in range(n):
        A, P, B = pts[i - 1], pts[i], pts[(i + 1) % n]
        ri = rs[i]
        if ri <= 0:
            seg.append(("L", P, P, 0, 0))
            continue
        ux, uy = A[0] - P[0], A[1] - P[1]
        vx, vy = B[0] - P[0], B[1] - P[1]
        lu, lv = math.hypot(ux, uy), math.hypot(vx, vy)
        ux, uy, vx, vy = ux / lu, uy / lu, vx / lv, vy / lv
        th = math.acos(max(-1, min(1, ux * vx + uy * vy)))
        d = ri / math.tan(th / 2)
        t1 = (P[0] + ux * d, P[1] + uy * d)
        t2 = (P[0] + vx * d, P[1] + vy * d)
        cross = (P[0] - A[0]) * (B[1] - P[1]) - (P[1] - A[1]) * (B[0] - P[0])
        seg.append(("A", t1, t2, ri, 1 if cross > 0 else 0))
    f = lambda p: f"{p[0]:.2f} {p[1]:.2f}"
    out = []
    for k, (tp, t1, t2, ri, sw) in enumerate(seg):
        out.append(("M " if k == 0 else "L ") + f(t1))
        if tp == "A":
            out.append(f"A {ri} {ri} 0 0 {sw} {f(t2)}")
    return " ".join(out) + " Z"


def svg_doc(w, h, corpo, bg=None, fonte=True):
    estilo = f"<style>{FONTE}</style>" if fonte else ""
    fundo = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'viewBox="0 0 {w} {h}" width="{w}" height="{h}">{estilo}{fundo}{corpo}</svg>')


def render(svg_path, png_path, w, h, bg="#FFFFFF"):
    r = subprocess.run([sys.executable, "-I", str(KIT / "render.py"), str(svg_path), str(png_path),
                        str(w), str(h), bg], cwd=RAIZ, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr)
    print(r.stdout.strip())


def png_uri(p):
    return "data:image/png;base64," + base64.b64encode(pathlib.Path(p).read_bytes()).decode()


# ---------------------------------------------------------------- rascunhos
# Todos desenhados numa grade de 512 (modulo 32 = 1 px no favicon de 16).
def r1_folha_selo(uid, c):
    """Folha de processo com dobra + selo circular com check, separado por respiro."""
    doc = rpoly([(96, 48), (256, 48), (352, 144), (352, 432), (96, 432)], [28, 0, 0, 28, 28])
    fold = rpoly([(256, 48), (352, 144), (256, 144)], [0, 0, 20])
    cx, cy, r = 352, 384, 96
    return f'''<defs><mask id="{uid}m" maskUnits="userSpaceOnUse" x="-512" y="-512" width="1536" height="1536">
<rect x="-512" y="-512" width="1536" height="1536" fill="#fff"/><circle cx="{cx}" cy="{cy}" r="{r+28}" fill="#000"/>
<path d="M 220 48 L 256 48 L 352 144 L 352 180 Z" fill="#000"/></mask></defs>
<g transform="translate(-16,8)"><g mask="url(#{uid}m)"><path d="{doc}" fill="{c['doc']}"/>
<rect x="144" y="208" width="160" height="32" rx="16" fill="{c['neg']}"/>
<rect x="144" y="272" width="160" height="32" rx="16" fill="{c['neg']}"/>
<rect x="144" y="336" width="96" height="32" rx="16" fill="{c['neg']}"/></g>
<path d="{fold}" fill="{c['acento']}"/>
<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c['acento']}"/>
<path d="M {cx-42} {cy+2} L {cx-12} {cy+32} L {cx+44} {cy-28}" fill="none" stroke="{c['check']}" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/></g>'''


def r2_janela(uid, c):
    """Janela de sistema (tela) com barra de titulo e folha dentro; selo no canto."""
    cx, cy, r = 400, 376, 88
    return f'''<defs><mask id="{uid}m" maskUnits="userSpaceOnUse" x="-512" y="-512" width="1536" height="1536">
<rect x="-512" y="-512" width="1536" height="1536" fill="#fff"/><circle cx="{cx}" cy="{cy}" r="{r+26}" fill="#000"/></mask></defs>
<g transform="translate(0,-24)"><g mask="url(#{uid}m)">
<path fill-rule="evenodd" fill="{c['doc']}" d="{rpoly([(48,112),(448,112),(448,416),(48,416)],40)} {rpoly([(84,180),(412,180),(412,380),(84,380)],12)}"/>
<rect x="128" y="220" width="200" height="28" rx="14" fill="{c['doc']}"/>
<rect x="128" y="276" width="200" height="28" rx="14" fill="{c['doc']}"/>
<rect x="128" y="332" width="120" height="28" rx="14" fill="{c['doc']}"/></g>
<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c['acento']}"/>
<path d="M {cx-38} {cy+2} L {cx-10} {cy+30} L {cx+40} {cy-26}" fill="none" stroke="{c['check']}" stroke-width="28" stroke-linecap="round" stroke-linejoin="round"/></g>'''


def r3_autos(uid, c):
    """Autos empilhados: folha de tras em azul, folha da frente com check vazado."""
    back = rpoly([(176, 48), (432, 48), (432, 368), (176, 368)], 28)
    front_pts = [(80, 144), (240, 144), (336, 240), (336, 464), (80, 464)]
    front = rpoly(front_pts, [28, 0, 0, 28, 28])
    gap = rpoly([(52, 116), (252, 116), (364, 228), (364, 492), (52, 492)], [48, 0, 0, 48, 48])
    fold = rpoly([(240, 144), (336, 240), (240, 240)], [0, 0, 20])
    return f'''<defs><mask id="{uid}m" maskUnits="userSpaceOnUse" x="-512" y="-512" width="1536" height="1536">
<rect x="-512" y="-512" width="1536" height="1536" fill="#fff"/><path d="{gap}" fill="#000"/></mask>
<mask id="{uid}f" maskUnits="userSpaceOnUse" x="-512" y="-512" width="1536" height="1536">
<rect x="-512" y="-512" width="1536" height="1536" fill="#fff"/><path d="M 200 144 L 240 144 L 336 240 L 336 280 Z" fill="#000"/></mask></defs>
<g transform="translate(0,-8)"><path d="{back}" fill="{c['acento']}" mask="url(#{uid}m)"/>
<path d="{front}" fill="{c['doc']}" mask="url(#{uid}f)"/><path d="{fold}" fill="{c['acento']}"/>
<path d="M 136 320 L 184 368 L 280 272" fill="none" stroke="{c['neg']}" stroke-width="40" stroke-linecap="round" stroke-linejoin="round"/></g>'''


def r4_folha_fala(uid, c):
    """Folha de processo cuja base vira balao de atendimento; check vazado."""
    doc = rpoly([(96, 40), (288, 40), (416, 168), (416, 400), (208, 400), (96, 480), (96, 400)],
                [32, 0, 0, 32, 0, 6, 0])
    fold = rpoly([(288, 40), (416, 168), (288, 168)], [0, 0, 24])
    return f'''<defs><mask id="{uid}m" maskUnits="userSpaceOnUse" x="-512" y="-512" width="1536" height="1536">
<rect x="-512" y="-512" width="1536" height="1536" fill="#fff"/><path d="M 248 40 L 288 40 L 416 168 L 416 208 Z" fill="#000"/></mask></defs>
<g><path d="{doc}" fill="{c['doc']}" mask="url(#{uid}m)"/><path d="{fold}" fill="{c['acento']}"/>
<path d="M 168 268 L 224 324 L 336 212" fill="none" stroke="{c['neg']}" stroke-width="44" stroke-linecap="round" stroke-linejoin="round"/></g>'''


CLARO = {"doc": MARINHO, "acento": AZUL, "check": BRANCO, "neg": BRANCO}


def rascunhos():
    RASC.mkdir(exist_ok=True)
    fns = [("r1_folha_selo", r1_folha_selo), ("r2_janela", r2_janela),
           ("r3_autos", r3_autos), ("r4_folha_fala", r4_folha_fala)]
    cells = []
    for i, (nome, fn) in enumerate(fns):
        p = RASC / f"{nome}.svg"
        p.write_text(svg_doc(512, 512, fn(nome, CLARO), fonte=False), encoding="utf-8")
        render(p, RASC / f"{nome}.png", 512, 512)
        y = i * 300 + 20
        cells.append(f'<text x="20" y="{y+14}" font-family="Barlow" font-weight="700" font-size="18" fill="{TEXTO}">{nome}</text>')
        for sz, x in ((256, 20), (64, 320), (32, 420), (16, 490)):
            cells.append(f'<svg x="{x}" y="{y+30}" width="{sz}" height="{sz}" viewBox="0 0 512 512">{fn(nome+str(sz), CLARO)}</svg>')
        # versao marinho pequena
        cells.append(f'<rect x="560" y="{y+30}" width="256" height="256" fill="{MARINHO}"/>')
        esc = {"doc": BRANCO, "acento": AZUL, "check": BRANCO, "neg": MARINHO}
        cells.append(f'<svg x="560" y="{y+30}" width="256" height="256" viewBox="0 0 512 512">{fn(nome+"esc", esc)}</svg>')
    comp = RASC / "comparativo.svg"
    comp.write_text(svg_doc(840, 1220, "".join(cells), bg=BRANCO), encoding="utf-8")
    render(comp, RASC / "comparativo.png", 840, 1220)


# ---------------------------------------------------------------- simbolo final (r4 refinado)
# Grade de 512 com modulo de 32. Corpo: quadrado de 10 x 10 modulos (96..416 x 32..352).
# Dobra no canto superior direito e cauda no inferior esquerdo, ambas a 45 graus,
# simetricas em relacao ao centro do quadrado. Check vazado no corpo.
DOBRA = 96       # cateto da dobra (3 modulos)
CAUDA = 128      # cateto da cauda (4 modulos)
RESP = 20        # respiro entre dobra e corpo
CHECK = ((160, 232), (212, 284), (308, 188))


def simbolo(uid, c, check_w=42, dobra=None, chk=None, resp=None):
    dobra = dobra or DOBRA
    resp = RESP if resp is None else resp
    chk = chk or CHECK
    x0, y0, x1, y1 = 96, 32, 416, 352
    fx = x1 - dobra
    corpo = rpoly([(x0, y0), (fx, y0), (x1, y0 + dobra), (x1, y1), (x0 + CAUDA, y1), (x0, y1 + CAUDA)],
                  [36, 0, 0, 36, 14, 10])
    dob = rpoly([(fx, y0), (x1, y0 + dobra), (fx, y0 + dobra)], [3, 3, 18])
    # corte em L: respiro uniforme ao longo dos catetos da dobra (o retangulo cobre tambem a
    # diagonal, para nao sobrar filete de antisserrilhado do corpo ao longo dela)
    corte = rpoly([(fx - resp, y0 - 64), (x1 + 64, y0 - 64), (x1 + 64, y0 + dobra + resp),
                   (fx - resp, y0 + dobra + resp)], [0, 0, 0, 6])
    (a, b), (c2, d), (e, f) = chk
    ck = f"M {a} {b} L {c2} {d} L {e} {f}"
    return f'''<defs><mask id="{uid}m" maskUnits="userSpaceOnUse" x="-512" y="-512" width="1536" height="1536">
<rect x="-512" y="-512" width="1536" height="1536" fill="#fff"/><path d="{corte}" fill="#000"/>
<path d="{ck}" fill="none" stroke="#000" stroke-width="{check_w}" stroke-linecap="round" stroke-linejoin="round"/></mask></defs>
<path d="{corpo}" fill="{c['doc']}" mask="url(#{uid}m)"/><path d="{dob}" fill="{c['acento']}"/>'''


ESCURO = {"doc": BRANCO, "acento": AZUL, "check": MARINHO, "neg": MARINHO}

VARIANTES = {
    "a_d96": dict(dobra=96, chk=((160, 232), (212, 284), (308, 188))),
    "b_d96_centro": dict(dobra=96, chk=((152, 200), (208, 256), (296, 168)), check_w=44),
    "c_d112_baixo": dict(dobra=112, chk=((168, 248), (216, 296), (312, 200))),
}


def teste_simbolo():
    cells = []
    for i, (nome, kw) in enumerate(VARIANTES.items()):
        y = 20 + i * 330
        cells.append(f'<text x="20" y="{y+12}" font-size="16" font-family="sans-serif" fill="#000">{nome}</text>')
        for sz, x in ((288, 20), (64, 330), (32, 410), (16, 460)):
            cells.append(f'<svg x="{x}" y="{y+20}" width="{sz}" height="{sz}" viewBox="0 0 512 512">{simbolo(nome+str(sz), CLARO, **kw)}</svg>')
        cells.append(f'<rect x="500" y="{y+20}" width="288" height="288" fill="{MARINHO}"/>')
        cells.append(f'<svg x="500" y="{y+20}" width="288" height="288" viewBox="0 0 512 512">{simbolo(nome+"e", ESCURO, **kw)}</svg>')
        cells.append(f'<rect x="800" y="{y+20}" width="40" height="40" fill="{MARINHO}"/>')
        cells.append(f'<svg x="812" y="{y+32}" width="16" height="16" viewBox="0 0 512 512">{simbolo(nome+"e16", ESCURO, **kw)}</svg>')
    p = RASC / "teste_simbolo.svg"
    p.write_text(svg_doc(860, 1010, "".join(cells), bg=BRANCO, fonte=False), encoding="utf-8")
    render(p, RASC / "teste_simbolo.png", 860, 1010)


# ---------------------------------------------------------------- favicon (desenhado na grade de 16 px)
def favicon_corpo(c):
    corpo = rpoly([(2, 1), (11, 1), (14, 4), (14, 12), (5, 12), (2, 15)], [1.6, 0, 0, 1.6, 0.6, 0.4])
    dob = rpoly([(11, 1), (14, 4), (11, 4)], [0.2, 0.2, 0.8])
    corte = "M 10 0 L 15 5 L 10 5 Z"
    return f'''<defs><mask id="fvm" maskUnits="userSpaceOnUse" x="-16" y="-16" width="48" height="48">
<rect x="-16" y="-16" width="48" height="48" fill="#fff"/><path d="{corte}" fill="#000"/>
<path d="M 5 8 L 7 10 L 10.2 6.8" fill="none" stroke="#000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></mask></defs>
<path d="{corpo}" fill="{c['doc']}" mask="url(#fvm)"/><path d="{dob}" fill="{c['acento']}"/>'''


# Favicon de 16 px desenhado pixel a pixel (M = corpo, A = dobra, . = vazio).
# Check com tracos de 2 px a 45 graus (bracos 2 + 3 linhas), separado do recorte da dobra
# por uma linha cheia de corpo; dobra de 3 px com respiro de 1 px; cauda de 3 px.
FAV16 = [
    "................",
    "...MMMMMMM.A....",
    "..MMMMMMMM.AA...",
    "..MMMMMMMM.AAA..",
    "..MMMMMMMM......",
    "..MMMMMMMMMMMM..",
    "..MMMMMMM..MMM..",
    "..MM..MM..MMMM..",
    "..MMM....MMMMM..",
    "..MMMM..MMMMMM..",
    "..MMMMMMMMMMMM..",
    "..MMMMMMMMMMM...",
    "..MMM...........",
    "..MM............",
    "..M.............",
    "................",
]


def favicon16_corpo(c):
    """Pixel art exata (crispEdges): nada de antisserrilhado no tamanho de 16 px."""
    cor = {"M": c["doc"], "A": c["acento"]}
    out = []
    for y, linha in enumerate(FAV16):
        x = 0
        while x < 16:
            ch = linha[x]
            if ch in cor:
                x2 = x
                while x2 < 16 and linha[x2] == ch:
                    x2 += 1
                out.append(f'<rect x="{x}" y="{y}" width="{x2 - x}" height="1" fill="{cor[ch]}"/>')
                x = x2
            else:
                x += 1
    return f'<g shape-rendering="crispEdges">{"".join(out)}</g>'


# ---------------------------------------------------------------- composicoes
APOIO = "COMISSÃO ESTADUAL DE APOIO INSTITUCIONAL AO"


def oab(x, y, h, placa=False):
    w = h * OAB_W / OAB_H
    s = ""
    if placa:
        pad = h * 0.14
        s += (f'<rect x="{x-pad:.1f}" y="{y-pad:.1f}" width="{w+2*pad:.1f}" height="{h+2*pad:.1f}" '
              f'rx="{pad:.1f}" fill="{BRANCO}"/>')
    s += f'<image x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" href="{OAB}"/>'
    return s, w


def sim_em(uid, c, x, y, altura):
    """Posiciona o simbolo pela caixa visivel (96..416 x 32..480) com a altura dada."""
    k = altura / 448
    return (f'<g transform="translate({x - 96*k:.2f},{y - 32*k:.2f}) scale({k:.5f})">{simbolo(uid, c)}</g>',
            320 * k)


# Metricas reais da Barlow (por 1000 unidades de em), medidas no Edge por medir.py.
MET = json.loads((AQUI / "metricas.json").read_text(encoding="utf-8"))
CAP = MET["800|H"]["asc"] / 1000            # altura de versal (0,703 em)
APOIO_1 = "COMISSÃO ESTADUAL DE APOIO"
APOIO_2 = "INSTITUCIONAL AO"
# Espacejamento optico de "PJe" (em milesimos de em, alem do kerning da fonte):
# o vao P|J abre muito por causa do gancho do J; o J|e fica levemente fechado.
K_PJ, K_JE = -40, -12


def pje(x_tinta, y, S, cor):
    """Escreve "PJe" com posicoes absolutas por letra. x_tinta = borda esquerda da haste do P."""
    kern_pj = MET["800|PJ"]["adv"] - MET["800|P"]["adv"] - MET["800|J"]["adv"]
    oP = 0
    oJ = MET["800|P"]["adv"] + kern_pj + K_PJ
    oE = oJ + MET["800|J"]["adv"] + K_JE
    esq = -MET["800|P"]["l"]
    dir_ = oE + MET["800|e"]["r"]
    u = S / 1000
    x0 = x_tinta - esq * u
    xs = " ".join(f"{x0 + o * u:.2f}" for o in (oP, oJ, oE))
    svg = (f'<text x="{xs}" y="{y:.2f}" font-family="Barlow" font-weight="800" font-size="{S:.2f}" '
           f'font-kerning="none" fill="{cor}">PJe</text>')
    return svg, (dir_ - esq) * u


def largura_pje(S):
    return pje(0, 0, S, "#000")[1]


def linha_apoio(texto, x_tinta, y, a, track, cor):
    m = MET["600|" + texto]
    x0 = x_tinta + m["l"] / 1000 * a
    return (f'<text x="{x0:.2f}" y="{y:.2f}" font-family="Barlow" font-weight="600" font-size="{a:.2f}" '
            f'letter-spacing="{track:.3f}" fill="{cor}">{texto}</text>')


def regua(x, y, w, t, cor):
    """Regua de cor unica com a ponta direita cortada a 45 graus (eco da dobra e da cauda)."""
    return (f'<path d="M {x:.2f} {y:.2f} L {x + w:.2f} {y:.2f} L {x + w - t:.2f} {y + t:.2f} '
            f'L {x:.2f} {y + t:.2f} Z" fill="{cor}"/>')


def lockup(escuro=False):
    """Bloco compacto: linha de apoio em 2 linhas justificada a largura de "PJe"; regua e OAB abaixo.
    Devolve (svg, largura, altura) em coordenadas proprias, com origem no canto do bloco."""
    c = ESCURO if escuro else CLARO
    txt = BRANCO if escuro else MARINHO
    S = 300.0
    wp = largura_pje(S)
    a = 0.095 * S
    m1 = MET["600|" + APOIO_1]
    n1 = m1["n"]
    tinta1 = (m1["r"] + m1["l"]) / 1000 * a
    track = (wp - tinta1) / (n1 - 1)       # linha 1 com a mesma largura de "PJe"
    cap_a = CAP * a
    y_a1 = cap_a
    y_a2 = y_a1 + 1.42 * a
    y_p = y_a2 + 0.10 * S + CAP * S
    rt = 0.03 * S
    y_r = y_p + 0.105 * S
    ho = 0.36 * S
    # Grade do bloco: a base do corpo do simbolo (y 352 de 32..480) coincide com a base da regua,
    # e a cauda ocupa a faixa da marca OAB.
    hb = (y_r + rt) * 448 / 320
    y_o = hb - ho
    assert y_o - (y_r + rt) > 0.08 * S, "respiro entre regua e OAB pequeno demais"
    sim, wsim = sim_em("h" + ("e" if escuro else "c"), c, 0, 0, hb)
    xt = wsim + 0.25 * wsim
    if escuro:
        pad = ho * 0.12
        hi = ho - 2 * pad
        wi = hi * OAB_W / OAB_H
        o = (f'<rect x="{xt:.2f}" y="{y_o:.2f}" width="{wi + 2 * pad:.2f}" height="{ho:.2f}" '
             f'rx="{pad:.2f}" fill="{BRANCO}"/>'
             f'<image x="{xt + pad:.2f}" y="{y_o + pad:.2f}" width="{wi:.2f}" height="{hi:.2f}" href="{OAB}"/>')
    else:
        o, _ = oab(xt, y_o, ho)
    t_pje, _ = pje(xt, y_p, S, txt)
    corpo = (sim + linha_apoio(APOIO_1, xt, y_a1, a, track, txt) + linha_apoio(APOIO_2, xt, y_a2, a, track, txt)
             + t_pje + regua(xt, y_r, wp, rt, BRANCO if escuro else AZUL) + o)
    return corpo, xt + wp, hb, track / a


def horizontal_g(escuro=False):
    corpo, wc, hc, _ = lockup(escuro)
    W, M = 1600, 150
    k = (W - 2 * M) / wc
    H = int(round(hc * k + 2 * M))
    g = f'<g transform="translate({M},{(H - hc * k) / 2:.2f}) scale({k:.5f})">{corpo}</g>'
    return g, W, H


def horizontal(escuro=False):
    g, W, H = horizontal_g(escuro)
    return svg_doc(W, H, g, bg=MARINHO if escuro else BRANCO), W, H


def avatar():
    W = 1080
    alt_s = 470
    wsim = 320 * alt_s / 448
    S = 1000 * wsim / largura_pje(1000)    # "PJe" com a mesma largura do corpo do simbolo
    gap = 0.20 * S
    total = alt_s + gap + CAP * S
    top = (W - total) / 2
    xs = (W - wsim) / 2
    sim, _ = sim_em("av", ESCURO, xs, top, alt_s)
    t, _ = pje(xs, top + total, S, BRANCO)
    return svg_doc(W, W, sim + t, bg=MARINHO)


def final():
    o = AQUI
    (o / "simbolo.svg").write_text(svg_doc(512, 512, simbolo("s", CLARO), fonte=False), encoding="utf-8")
    render(o / "simbolo.svg", o / "simbolo.png", 512, 512)
    assert all(len(l) == 16 for l in FAV16) and len(FAV16) == 16
    print("espacejamento da linha de apoio: %.3f em" % lockup()[3])
    for nome, esc in (("logo_horizontal", False), ("logo_horizontal_marinho", True)):
        svg, W, H = horizontal(esc)
        (o / f"{nome}.svg").write_text(svg, encoding="utf-8")
        render(o / f"{nome}.svg", o / f"{nome}.png", W, H, MARINHO if esc else BRANCO)
        print(nome, W, H)
    (o / "avatar.svg").write_text(avatar(), encoding="utf-8")
    render(o / "avatar.svg", o / "avatar.png", 1080, 1080, MARINHO)
    (o / "favicon.svg").write_text(svg_doc(16, 16, favicon_corpo(CLARO), fonte=False), encoding="utf-8")
    render(o / "favicon.svg", o / "favicon_32.png", 32, 32)
    (o / "favicon_16.svg").write_text(svg_doc(16, 16, favicon16_corpo(CLARO), fonte=False), encoding="utf-8")
    render(o / "favicon_16.svg", o / "favicon_16.png", 16, 16)
    prancha()


def prancha():
    o = AQUI
    _, LW, LH = horizontal(False)
    W = 1800
    hw = (W - 120) / (1 + LH / LW)      # logo horizontal + quadrado do simbolo ocupam a largura
    hh = hw * LH / LW
    q = hh
    x2 = 40 + hw + 40
    y1 = 170
    y2 = y1 + hh + 60
    y3 = y2 + hh + 70
    y4 = y3 + 260 + 70
    H = int(y4 + 280 + 40)

    def img(p, x, y, w, h, px=False):
        st = 'style="image-rendering:pixelated" ' if px else ''
        return f'<image x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" {st}href="{png_uri(o / p)}"/>'

    def lab(t, x, y):
        return (f'<text x="{x}" y="{y}" font-family="Barlow" font-weight="600" font-size="18" '
                f'letter-spacing="2" fill="#5A6275">{t}</text>')

    c = [f'<text x="40" y="72" font-family="Barlow" font-weight="800" font-size="44" fill="{MARINHO}">'
         f'Squad A  |  Folha que atende</text>',
         f'<text x="40" y="112" font-family="Barlow" font-weight="500" font-size="24" fill="{TEXTO}">'
         f'Comissão Estadual de Apoio Institucional ao PJe, OAB/PA. Conceito: tela e processo, '
         f'com selo de apoio que resolve.</text>',
         f'<rect x="40" y="{y1}" width="{hw}" height="{hh:.1f}" fill="#fff" stroke="#D5DAE5" stroke-width="2"/>',
         img("logo_horizontal.png", 40, y1, hw, hh),
         f'<rect x="{x2}" y="{y1}" width="{q:.1f}" height="{q:.1f}" fill="#fff" stroke="#D5DAE5" stroke-width="2"/>',
         img("simbolo.png", x2 + 1, y1 + 1, q - 2, q - 2),
         img("logo_horizontal_marinho.png", 40, y2, hw, hh),
         img("avatar.png", x2, y2, q, q),
         lab("LOGO HORIZONTAL", 40, y1 - 14), lab("SÍMBOLO", x2, y1 - 14),
         lab("LOGO HORIZONTAL, FUNDO MARINHO", 40, y2 - 14), lab("AVATAR 1080", x2, y2 - 14),
         lab("FAVICON E TAMANHOS PEQUENOS", 40, y3 - 14),
         f'<rect x="40" y="{y3}" width="{W-80}" height="260" fill="#F3F5F9" stroke="#D5DAE5" stroke-width="2"/>']
    yb = y3 + 36
    c += [img("favicon_16.png", 84, yb + 56, 16, 16), lab("16 px", 70, yb + 170),
          img("favicon_32.png", 168, yb + 48, 32, 32), lab("32 px", 160, yb + 170),
          img("favicon_16.png", 270, yb, 128, 128, px=True), lab("16 px a 8x", 270, yb + 170),
          img("favicon_32.png", 450, yb, 128, 128, px=True), lab("32 px a 4x", 450, yb + 170)]
    tx = 650
    c += [f'<rect x="{tx}" y="{yb+36}" width="340" height="56" rx="10" fill="#fff" stroke="#C9D0DE" stroke-width="2"/>',
          img("favicon_16.png", tx + 20, yb + 56, 16, 16),
          f'<text x="{tx+48}" y="{yb+70}" font-family="Barlow" font-weight="500" font-size="18" fill="{TEXTO}">'
          f'Apoio ao PJe | OAB/PA</text>',
          lab("ABA DO NAVEGADOR", tx, yb + 170)]
    sx = 1050
    for t in (24, 48, 96):   # vetor no tamanho real, sem reamostrar PNG
        c += [f'<svg x="{sx}" y="{yb + 128 - t}" width="{t}" height="{t}" viewBox="0 0 512 512">'
              f'{simbolo("pr" + str(t), CLARO)}</svg>', lab(f"{t} px", sx, yb + 170)]
        sx += t + 56
    av = 1520
    c += [f'<clipPath id="circ"><circle cx="{av+64}" cy="{yb+64}" r="64"/></clipPath>',
          f'<image x="{av}" y="{yb}" width="128" height="128" clip-path="url(#circ)" href="{png_uri(o / "avatar.png")}"/>',
          lab("AVATAR EM CÍRCULO", av - 20, yb + 170)]
    # reducao: o bloco compacto continua legivel em larguras de cabecalho e assinatura
    gc, _, _ = horizontal_g(False)
    ge, _, _ = horizontal_g(True)
    c += [lab("REDUÇÃO: LOGO A 400, 300 E 200 PX DE LARGURA (MÍNIMO EM TELA: 400 PX; ABAIXO DISSO, SÍMBOLO OU AVATAR)", 40, y4 - 14),
          f'<rect x="40" y="{y4}" width="{W-80}" height="280" fill="#FFFFFF" stroke="#D5DAE5" stroke-width="2"/>']
    rx = 80
    for wl in (400, 300, 200):
        hl = wl * LH / LW
        c.append(f'<svg x="{rx}" y="{y4 + (280 - hl) / 2:.1f}" width="{wl}" height="{hl:.1f}" '
                 f'viewBox="0 0 {LW} {LH}">{gc}</svg>')
        rx += wl + 50
    wl = 400
    hl = wl * LH / LW
    c.append(f'<svg x="{W - 80 - wl}" y="{y4 + (280 - hl) / 2:.1f}" width="{wl}" height="{hl:.1f}" '
             f'viewBox="0 0 {LW} {LH}"><rect width="{LW}" height="{LH}" fill="{MARINHO}"/>{ge}</svg>')
    (o / "prancha.svg").write_text(svg_doc(W, H, "".join(c), bg="#FFFFFF"), encoding="utf-8")
    render(o / "prancha.svg", o / "prancha.png", W, H)


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "final"
    if modo == "rascunhos":
        rascunhos()
    elif modo == "teste":
        teste_simbolo()
    else:
        final()
