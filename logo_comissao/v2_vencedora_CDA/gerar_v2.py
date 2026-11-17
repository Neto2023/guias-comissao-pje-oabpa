"""v2 da logo vencedora (Squad A, "Folha que atende") com os ajustes do orquestrador e a sigla CDA PJe.

Uso (de qualquer pasta):  python -I gerar_v2.py
Reaproveita as funcoes do gerador do Squad A (competicao_v1/squad-A_tela-processo/gerar.py), sem altera-lo.
Ajustes desta versao:
  1. no fundo marinho, a dobra fica branca (antes: azul, contraste de cerca de 2,9:1);
  2. check com pontas e quina retas, cortadas a 45 graus (antes: pontas redondas);
  3. versao empilhada e centralizada;
  4. sigla CDA PJe em tres arranjos (A: sigla no titulo; B: sigla na regua; C: empilhada).
"""
import html as H
import json
import pathlib
import subprocess
import sys
import tempfile

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parent / "competicao_v1"
sys.path.insert(0, str(RAIZ / "squad-A_tela-processo"))
import gerar as G  # noqa: E402

MARINHO, AZUL, BRANCO, TEXTO = G.MARINHO, G.AZUL, G.BRANCO, G.TEXTO
CLARO = {"doc": MARINHO, "acento": AZUL}
ESCURO = {"doc": BRANCO, "acento": BRANCO}          # ajuste 1: dobra branca no marinho
APOIO = G.APOIO
SIGLA = "CDA"


# ---------------------------------------------------------------- metricas extras (Edge headless)
def medir(amostras):
    js = """(async () => { const am = %s;
  for (const w of ['600','700','800']) await document.fonts.load(w + ' 1000px Barlow');
  const ctx = document.createElement('canvas').getContext('2d'); const out = {};
  for (const [w, t] of am) { ctx.font = w + ' 1000px Barlow'; const m = ctx.measureText(t);
    out[w + '|' + t] = {adv: m.width, l: m.actualBoundingBoxLeft, r: m.actualBoundingBoxRight, n: [...t].length}; }
  document.getElementById('o').textContent = JSON.stringify(out); })();""" % json.dumps(amostras)
    doc = (f'<!doctype html><html><head><meta charset="utf-8"><style>{G.FONTE}</style></head>'
           f'<body><pre id="o">x</pre><script>{js}</script></body></html>')
    tmp = pathlib.Path(tempfile.mkdtemp()) / "m.html"
    tmp.write_text(doc, encoding="utf-8")
    edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    r = subprocess.run([edge, "--headless=new", "--disable-gpu", "--virtual-time-budget=5000", "--dump-dom",
                        tmp.as_uri()], capture_output=True, text=True, encoding="utf-8", timeout=90)
    txt = r.stdout.split('<pre id="o">', 1)[1].split("</pre>", 1)[0]
    return json.loads(H.unescape(txt))


MET = dict(G.MET)
MET.update(medir([("800", SIGLA), ("600", APOIO)]))


def tinta(peso, txt, size):
    m = MET[f"{peso}|{txt}"]
    return (m["r"] + m["l"]) / 1000 * size


def texto(txt, peso, x_tinta, y, size, cor, extra=""):
    m = MET[f"{peso}|{txt}"]
    x0 = x_tinta + m["l"] / 1000 * size
    return (f'<text x="{x0:.2f}" y="{y:.2f}" font-family="Barlow" font-weight="{peso}" font-size="{size:.2f}" '
            f'fill="{cor}" {extra}>{txt}</text>')


def apoio_uma_linha(x_tinta, y, largura, cor):
    """Linha de apoio inteira, com espacejamento calculado para ocupar exatamente a largura dada."""
    m = MET["600|" + APOIO]
    n = m["n"]
    a = largura / ((m["r"] + m["l"]) / 1000 + 0.10 * (n - 1))
    track = 0.10 * a
    return texto(APOIO, 600, x_tinta, y, a, cor, f'letter-spacing="{track:.3f}"'), a


# ---------------------------------------------------------------- simbolo v2 (check reto a 45 graus)
def simbolo(uid, c, check_w=42):
    x0, y0, x1, y1 = 96, 32, 416, 352
    dobra, resp = G.DOBRA, G.RESP
    fx = x1 - dobra
    corpo = G.rpoly([(x0, y0), (fx, y0), (x1, y0 + dobra), (x1, y1), (x0 + G.CAUDA, y1), (x0, y1 + G.CAUDA)],
                    [36, 0, 0, 36, 14, 10])
    dob = G.rpoly([(fx, y0), (x1, y0 + dobra), (fx, y0 + dobra)], [3, 3, 18])
    corte = G.rpoly([(fx - resp, y0 - 64), (x1 + 64, y0 - 64), (x1 + 64, y0 + dobra + resp),
                     (fx - resp, y0 + dobra + resp)], [0, 0, 0, 6])
    # ajuste 2: sem pontas redondas; as pontas retas ficam a 45 graus porque os bracos sao diagonais.
    # Bracos alongados em meia espessura para manter o comprimento visual do check anterior.
    e = check_w / 2 / 2 ** 0.5
    (a, b), (c2, d), (f, g) = G.CHECK
    ck = f"M {a - e:.2f} {b - e:.2f} L {c2} {d} L {f + e:.2f} {g - e:.2f}"
    return f'''<defs><mask id="{uid}m" maskUnits="userSpaceOnUse" x="-512" y="-512" width="1536" height="1536">
<rect x="-512" y="-512" width="1536" height="1536" fill="#fff"/><path d="{corte}" fill="#000"/>
<path d="{ck}" fill="none" stroke="#000" stroke-width="{check_w}" stroke-linecap="butt" stroke-linejoin="miter" stroke-miterlimit="4"/></mask></defs>
<path d="{corpo}" fill="{c['doc']}" mask="url(#{uid}m)"/><path d="{dob}" fill="{c['acento']}"/>'''


def sim_em(uid, c, x, y, altura):
    k = altura / 448
    return (f'<g transform="translate({x - 96 * k:.2f},{y - 32 * k:.2f}) scale({k:.5f})">{simbolo(uid, c)}</g>',
            320 * k)


def favicon32(c):
    corpo = G.rpoly([(2, 1), (11, 1), (14, 4), (14, 12), (5, 12), (2, 15)], [1.6, 0, 0, 1.6, 0.6, 0.4])
    dob = G.rpoly([(11, 1), (14, 4), (11, 4)], [0.2, 0.2, 0.8])
    return f'''<defs><mask id="fvm" maskUnits="userSpaceOnUse" x="-16" y="-16" width="48" height="48">
<rect x="-16" y="-16" width="48" height="48" fill="#fff"/><path d="M 10 0 L 15 5 L 10 5 Z" fill="#000"/>
<path d="M 4.3 7.3 L 7 10 L 10.9 6.1" fill="none" stroke="#000" stroke-width="2" stroke-linecap="butt" stroke-linejoin="miter"/></mask></defs>
<path d="{corpo}" fill="{c['doc']}" mask="url(#fvm)"/><path d="{dob}" fill="{c['acento']}"/>'''


# ---------------------------------------------------------------- pecas comuns
def oab_bloco(x, y, ho, escuro, centro=False):
    if escuro:
        pad = ho * 0.12
        hi = ho - 2 * pad
        wi = hi * G.OAB_W / G.OAB_H
        wt = wi + 2 * pad
        if centro:
            x -= wt / 2
        return (f'<rect x="{x:.2f}" y="{y:.2f}" width="{wt:.2f}" height="{ho:.2f}" rx="{pad:.2f}" fill="{BRANCO}"/>'
                f'<image x="{x + pad:.2f}" y="{y + pad:.2f}" width="{wi:.2f}" height="{hi:.2f}" href="{G.OAB}"/>')
    w = ho * G.OAB_W / G.OAB_H
    if centro:
        x -= w / 2
    return f'<image x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{ho:.2f}" href="{G.OAB}"/>'


def titulo_cda_pje(x, y, S, escuro):
    """'CDA PJe' na mesma linha: sigla em azul (branco no marinho), PJe em marinho (branco)."""
    w_c = tinta(800, SIGLA, S)
    gap = 0.20 * S
    t = texto(SIGLA, 800, x, y, S, BRANCO if escuro else AZUL)
    tp, wp = G.pje(x + w_c + gap, y, S, BRANCO if escuro else MARINHO)
    return t + tp, w_c + gap + wp


def cores(escuro):
    return (ESCURO if escuro else CLARO), (BRANCO if escuro else MARINHO), (BRANCO if escuro else AZUL)


# ---------------------------------------------------------------- arranjos
def arranjo_a(escuro=False):
    """A: sigla no titulo. Apoio em uma linha na largura de 'CDA PJe'; regua e OAB abaixo."""
    c, txt, ac = cores(escuro)
    S = 260.0
    _, wt = titulo_cda_pje(0, 0, S, escuro)
    xt0 = 0
    _, a = apoio_uma_linha(0, 0, wt, txt)
    y_a = G.CAP * a
    y_t = y_a + 0.12 * S + G.CAP * S
    rt = 0.03 * S
    y_r = y_t + 0.11 * S
    ho = 0.56 * S
    y_o = y_r + rt + 0.10 * S                        # OAB sempre abaixo da regua, com respiro
    hb = max((y_r + rt) * 448 / 320, y_o + ho)
    sim, wsim = sim_em("a" + str(escuro), c, 0, 0, hb)
    xt = wsim * 1.25
    ap, _ = apoio_uma_linha(xt, y_a, wt, txt)
    tt, _ = titulo_cda_pje(xt, y_t, S, escuro)
    corpo = sim + ap + tt + G.regua(xt, y_r, wt, rt, ac) + oab_bloco(xt, y_o, ho, escuro)
    return corpo, xt + wt, hb


def arranjo_b(escuro=False):
    """B: PJe continua o destaque (como na vencedora); a sigla CDA abre a regua, abaixo do PJe."""
    c, txt, ac = cores(escuro)
    S = 300.0
    wp = G.largura_pje(S)
    a = 0.095 * S
    m1 = MET["600|" + G.APOIO_1]
    track = (wp - (m1["r"] + m1["l"]) / 1000 * a) / (m1["n"] - 1)
    y_a1 = G.CAP * a
    y_a2 = y_a1 + 1.42 * a
    y_p = y_a2 + 0.10 * S + G.CAP * S
    sc = 0.30 * S                                    # sigla
    y_s = y_p + 0.12 * S + G.CAP * sc
    rt = 0.03 * S
    w_s = tinta(800, SIGLA, sc)
    ho = 0.36 * S
    hb = y_s * 448 / 320
    y_o = hb - ho
    if y_o - y_s < 0.08 * S:                         # garante respiro entre a sigla e a OAB
        hb = (y_s + 0.08 * S + ho)
        y_o = hb - ho
    sim, wsim = sim_em("b" + str(escuro), c, 0, 0, hb)
    xt = wsim * 1.25
    corpo = (sim + G.linha_apoio(G.APOIO_1, xt, y_a1, a, track, txt) + G.linha_apoio(G.APOIO_2, xt, y_a2, a, track, txt)
             + G.pje(xt, y_p, S, txt)[0] + texto(SIGLA, 800, xt, y_s, sc, ac)
             + G.regua(xt + w_s + 0.10 * S, y_s - G.CAP * sc / 2 - rt / 2, wp - w_s - 0.10 * S, rt, ac)
             + oab_bloco(xt, y_o, ho, escuro))
    return corpo, xt + wp, hb


def arranjo_c(escuro=False):
    """C: empilhada e centralizada. Simbolo, 'CDA PJe', apoio, regua e OAB, todos no eixo."""
    c, txt, ac = cores(escuro)
    S = 260.0
    _, wt = titulo_cda_pje(0, 0, S, escuro)
    cx = wt / 2
    hs = 1.15 * S
    wsim = 320 * hs / 448
    sim, _ = sim_em("c" + str(escuro), c, cx - wsim / 2, 0, hs)
    y_t = hs + 0.28 * S + G.CAP * S
    tt, _ = titulo_cda_pje(0, y_t, S, escuro)
    ap, a = apoio_uma_linha(0, 0, wt, txt)
    y_a = y_t + 0.16 * S + G.CAP * a
    ap, _ = apoio_uma_linha(0, y_a, wt, txt)
    rt = 0.03 * S
    y_r = y_a + 0.14 * S
    ho = 0.60 * S
    y_o = y_r + rt + 0.14 * S
    corpo = (sim + tt + ap + f'<rect x="{cx - wt * 0.2:.2f}" y="{y_r:.2f}" width="{wt * 0.4:.2f}" height="{rt:.2f}" fill="{ac}"/>'
             + oab_bloco(cx, y_o, ho, escuro, centro=True))
    return corpo, wt, y_o + ho


def enquadrar(corpo, wc, hc, escuro, W=1600, M=150):
    k = (W - 2 * M) / wc
    H_ = int(round(hc * k + 2 * M))
    g = f'<g transform="translate({M},{(H_ - hc * k) / 2:.2f}) scale({k:.5f})">{corpo}</g>'
    return G.svg_doc(W, H_, g, bg=MARINHO if escuro else BRANCO), W, H_


def avatar():
    W = 1080
    alt = 600
    wsim = 320 * alt / 448
    sim, _ = sim_em("av", ESCURO, (W - wsim) / 2, (W - alt) / 2 - 20, alt)
    return G.svg_doc(W, W, sim, bg=MARINHO)


# ---------------------------------------------------------------- saida
def salvar(nome, svg, w, h, bg=BRANCO):
    (AQUI / f"{nome}.svg").write_text(svg, encoding="utf-8")
    G.render(AQUI / f"{nome}.svg", AQUI / f"{nome}.png", w, h, bg)


def main():
    salvar("simbolo_v2", G.svg_doc(512, 512, simbolo("s", CLARO), fonte=False), 512, 512)
    salvar("simbolo_v2_marinho", G.svg_doc(512, 512, simbolo("se", ESCURO), bg=MARINHO, fonte=False), 512, 512, MARINHO)
    salvar("favicon_v2", G.svg_doc(16, 16, favicon32(CLARO), fonte=False), 32, 32)
    (AQUI / "favicon_v2_16.svg").write_text(G.svg_doc(16, 16, G.favicon16_corpo(CLARO), fonte=False), encoding="utf-8")
    G.render(AQUI / "favicon_v2_16.svg", AQUI / "favicon_v2_16.png", 16, 16)
    salvar("avatar_v2", avatar(), 1080, 1080, MARINHO)
    dims = {}
    for letra, fn in (("A", arranjo_a), ("B", arranjo_b), ("C", arranjo_c)):
        for esc in (False, True):
            corpo, wc, hc = fn(esc)
            W = 1600 if letra != "C" else 1200
            svg, W, H_ = enquadrar(corpo, wc, hc, esc, W=W, M=150 if letra != "C" else 170)
            nome = f"logo_{letra}{'_marinho' if esc else ''}"
            salvar(nome, svg, W, H_, MARINHO if esc else BRANCO)
            dims[nome] = (W, H_)
    prancha(dims)


def prancha(dims):
    W = 2000
    uri = G.png_uri
    c = [f'<text x="50" y="80" font-family="Barlow" font-weight="800" font-size="46" fill="{MARINHO}">'
         f'Logo CDA PJe, versão 2: escolha do arranjo da sigla</text>',
         f'<text x="50" y="124" font-family="Barlow" font-weight="500" font-size="24" fill="{TEXTO}">'
         f'Vencedora da competição (Squad A) com os ajustes do orquestrador: dobra branca no marinho, check reto a 45 graus, versão empilhada.</text>']

    def lab(t, x, y):
        return f'<text x="{x}" y="{y}" font-family="Barlow" font-weight="700" font-size="24" letter-spacing="1.5" fill="#5A6275">{t}</text>'

    y = 190
    col = (W - 150) / 2
    for letra, titulo in (("A", "A  |  SIGLA NO TÍTULO"), ("B", "B  |  PJe EM DESTAQUE, SIGLA NA RÉGUA")):
        w0, h0 = dims[f"logo_{letra}"]
        h = col * h0 / w0
        c += [lab(titulo, 50, y - 14),
              f'<rect x="50" y="{y}" width="{col:.1f}" height="{h:.1f}" fill="#fff" stroke="#D5DAE5" stroke-width="2"/>',
              f'<image x="50" y="{y}" width="{col:.1f}" height="{h:.1f}" href="{uri(AQUI / f"logo_{letra}.png")}"/>',
              f'<image x="{100 + col:.1f}" y="{y}" width="{col:.1f}" height="{h:.1f}" href="{uri(AQUI / f"logo_{letra}_marinho.png")}"/>']
        y += h + 80
    w0, h0 = dims["logo_C"]
    hc = 640
    wc = hc * w0 / h0
    c += [lab("C  |  EMPILHADA E CENTRALIZADA", 50, y - 14),
          f'<rect x="50" y="{y}" width="{wc:.1f}" height="{hc}" fill="#fff" stroke="#D5DAE5" stroke-width="2"/>',
          f'<image x="50" y="{y}" width="{wc:.1f}" height="{hc}" href="{uri(AQUI / "logo_C.png")}"/>',
          f'<image x="{80 + wc:.1f}" y="{y}" width="{wc:.1f}" height="{hc}" href="{uri(AQUI / "logo_C_marinho.png")}"/>']
    y += hc + 80
    x = 50
    c += [lab("SÍMBOLO V2", x, y - 14),
          f'<rect x="{x:.1f}" y="{y}" width="300" height="300" fill="#fff" stroke="#D5DAE5" stroke-width="2"/>',
          f'<image x="{x:.1f}" y="{y}" width="300" height="300" href="{uri(AQUI / "simbolo_v2.png")}"/>',
          f'<image x="{x + 320:.1f}" y="{y}" width="300" height="300" href="{uri(AQUI / "simbolo_v2_marinho.png")}"/>',
          lab("FAVICON 32 E 16", x + 680, y - 14),
          f'<image x="{x + 680:.1f}" y="{y + 40}" width="32" height="32" href="{uri(AQUI / "favicon_v2.png")}"/>',
          f'<image x="{x + 740:.1f}" y="{y}" width="128" height="128" style="image-rendering:pixelated" href="{uri(AQUI / "favicon_v2.png")}"/>',
          f'<image x="{x + 900:.1f}" y="{y + 48}" width="16" height="16" href="{uri(AQUI / "favicon_v2_16.png")}"/>',
          f'<image x="{x + 940:.1f}" y="{y}" width="128" height="128" style="image-rendering:pixelated" href="{uri(AQUI / "favicon_v2_16.png")}"/>',
          lab("AVATAR", x + 1140, y - 14),
          f'<image x="{x + 1140:.1f}" y="{y}" width="300" height="300" href="{uri(AQUI / "avatar_v2.png")}"/>']
    H_ = int(y + 300 + 60)
    (AQUI / "prancha_escolha_v2.svg").write_text(G.svg_doc(W, H_, "".join(c), bg="#F3F5F9"), encoding="utf-8")
    G.render(AQUI / "prancha_escolha_v2.svg", AQUI / "prancha_escolha_v2.png", W, H_, "#F3F5F9")


if __name__ == "__main__":
    main()
