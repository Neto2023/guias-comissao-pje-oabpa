"""Logo do grupo "Comitê Gestor, grupo de interação OAB-SETIC", na mesma família da logo da Comissão
(destaque grande | barra | nome em linhas | marcas embaixo).

Decisões de 17/11/2026: texto COMITÊ GESTOR / GRUPO DE INTERAÇÃO / OAB-SETIC; destaque "OAB" (marinho)
sobre "SETIC" (vermelho); marcas OAB Pará + TJPA (a do TJPA entra quando houver o arquivo oficial).

Uso:  python -I gerar.py [caminho_da_marca_tjpa.png|jpg]
Sem o arquivo do TJPA, gera a prévia só com a OAB Pará (arquivos *_previa_sem_tjpa).
Reaproveita o kit da logo da Comissão (fonte Barlow, OAB Pará, render no Edge), sem alterá-lo.
"""
import base64
import html as H
import json
import pathlib
import subprocess
import sys
import tempfile

AQUI = pathlib.Path(__file__).resolve().parent
LOGO = AQUI.parents[1] / "logo_comissao" / "competicao_v1"
sys.path.insert(0, str(LOGO / "squad-A_tela-processo"))
import gerar as G  # noqa: E402

MARINHO, VERMELHO, BRANCO = G.MARINHO, G.VERMELHO, G.BRANCO
CAP = G.CAP
LINHAS = ["COMITÊ GESTOR", "GRUPO DE INTERAÇÃO", "OAB-SETIC"]
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def medir(amostras):
    """Avanço e tinta reais da Barlow a 1000 px, medidos no Edge (canvas.measureText)."""
    js = """(async () => {
      const am = %s;
      for (const w of ['700','800']) await document.fonts.load(w + ' 1000px Barlow');
      const ctx = document.createElement('canvas').getContext('2d'); const out = {};
      for (const [w, t] of am) { ctx.font = w + ' 1000px Barlow'; const m = ctx.measureText(t);
        out[w + '|' + t] = {adv: m.width, l: m.actualBoundingBoxLeft, r: m.actualBoundingBoxRight}; }
      document.getElementById('o').textContent = JSON.stringify(out); })();""" % json.dumps(amostras)
    doc = (f'<!doctype html><html><head><meta charset="utf-8"><style>{G.FONTE}</style></head>'
           f'<body><pre id="o">x</pre><script>{js}</script></body></html>')
    tmp = pathlib.Path(tempfile.mkdtemp()) / "m.html"
    tmp.write_text(doc, encoding="utf-8")
    r = subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--virtual-time-budget=5000", "--dump-dom",
                        tmp.as_uri()], capture_output=True, text=True, encoding="utf-8", timeout=90)
    return json.loads(H.unescape(r.stdout.split('<pre id="o">', 1)[1].split("</pre>", 1)[0]))


MET = medir([["800", "OAB"], ["800", "SETIC"]] + [["700", l] for l in LINHAS])


def tinta(peso, txt, tam):
    m = MET[f"{peso}|{txt}"]
    return -m["l"] * tam / 1000, (m["r"] + m["l"]) * tam / 1000   # deslocamento da tinta, largura da tinta


def destaque(x, y_topo, W_alvo):
    """'OAB' sobre 'SETIC', as duas palavras com a mesma largura de tinta. Devolve (svg, altura)."""
    out, y, alturas = "", y_topo, []
    for txt, cor in (("OAB", MARINHO), ("SETIC", VERMELHO)):
        _, w1 = tinta("800", txt, 1000)
        tam = 1000 * W_alvo / w1
        dx, _ = tinta("800", txt, tam)
        y += CAP * tam
        out += (f'<text x="{x - dx:.2f}" y="{y:.2f}" font-family="Barlow" font-weight="800" font-size="{tam:.2f}" '
                f'font-kerning="normal" fill="{cor}">{txt}</text>')
        alturas.append(CAP * tam)
        y += 0.20 * alturas[-1]                     # respiro entre as palavras
    return out, y - 0.20 * alturas[-1] - y_topo


def marcas(x, y, h, tjpa):
    """OAB Pará e, se houver, a marca do TJPA ao lado, na mesma altura."""
    w_o = h * G.OAB_W / G.OAB_H
    s = f'<image x="{x:.2f}" y="{y:.2f}" width="{w_o:.2f}" height="{h:.2f}" href="{G.OAB}"/>'
    w = w_o
    if tjpa:
        uri, tw, th = tjpa
        sep = 0.30 * h
        xf = x + w_o + sep
        s += f'<rect x="{xf:.2f}" y="{y + 0.12 * h:.2f}" width="{0.012 * h + 1:.2f}" height="{0.76 * h:.2f}" fill="#C9D0DE"/>'
        xt = xf + sep
        wt = h * tw / th
        s += f'<image x="{xt:.2f}" y="{y:.2f}" width="{wt:.2f}" height="{h:.2f}" href="{uri}"/>'
        w = xt + wt - x
    return s, w


def lockup(tjpa=None):
    a = 0.205 * 300                     # corpo do nome (mesma escala da logo da Comissão)
    lh = 1.13 * a
    bloco = (len(LINHAS) - 1) * lh + CAP * a
    ho = 1.55 * a
    gap_o = 0.55 * a
    total = bloco + gap_o + ho
    W_dest = 2.75 * a * 1.0 * 1.6       # largura do destaque
    d_svg, d_h = destaque(0, 0, W_dest)
    y_d = (bloco - d_h) / 2             # destaque centralizado na altura do nome, como na logo da Comissão
    d_svg, _ = destaque(0, y_d, W_dest)
    xb = W_dest + 0.17 * 300
    wb = 0.018 * 300
    xn = xb + wb + 0.13 * 300
    nome = "".join(
        f'<text x="{xn - tinta("700", l, a)[0]:.2f}" y="{CAP * a + i * lh:.2f}" font-family="Barlow" '
        f'font-weight="700" font-size="{a:.2f}" letter-spacing="{0.01 * a:.2f}" fill="{MARINHO}">{l}</text>'
        for i, l in enumerate(LINHAS))
    w_nome = max(tinta("700", l, a)[1] + 0.01 * a * len(l) for l in LINHAS)
    barra = f'<rect x="{xb:.2f}" y="{-0.06 * 300:.2f}" width="{wb:.2f}" height="{total + 0.12 * 300:.2f}" fill="{MARINHO}"/>'
    m_svg, w_m = marcas(xn, bloco + gap_o, ho, tjpa)
    y0 = min(0, y_d)
    return d_svg + barra + nome + m_svg, xn + max(w_nome, w_m), total, y0


def horizontal(tjpa, W=1600, M=140):
    corpo, wc, hc, y0 = lockup(tjpa)
    hc2 = hc - y0
    k = (W - 2 * M) / wc
    H_ = int(round(hc2 * k + 2 * M + 0.12 * 300 * k))
    g = f'<g transform="translate({M},{(H_ - hc2 * k) / 2 - y0 * k:.2f}) scale({k:.5f})">{corpo}</g>'
    return G.svg_doc(W, H_, g, bg=BRANCO), W, H_


def avatar_completo(tjpa, W=1080):
    corpo, wc, hc, y0 = lockup(tjpa)
    hc2 = hc - y0
    k = 0.84 * W / 2 / ((wc / 2) ** 2 + (hc2 / 2) ** 2) ** 0.5
    x = (W - wc * k) / 2
    y = (W - hc2 * k) / 2 - y0 * k
    return G.svg_doc(W, W, f'<g transform="translate({x:.2f},{y:.2f}) scale({k:.5f})">{corpo}</g>', bg=BRANCO)


def avatar_curto(W=1080):
    """Só OAB / SETIC, legível na lista de conversas (cerca de 48 px)."""
    Wd = 0.62 * W
    _, h = destaque(0, 0, Wd)
    s, _ = destaque((W - Wd) / 2, (W - h) / 2, Wd)
    return G.svg_doc(W, W, s, bg=BRANCO)


def salvar(nome, svg, w, h):
    (AQUI / f"{nome}.svg").write_text(svg, encoding="utf-8")
    G.render(AQUI / f"{nome}.svg", AQUI / f"{nome}.png", w, h, BRANCO)


def main():
    tjpa, suf = None, "_previa_sem_tjpa"
    if len(sys.argv) > 1:
        p = pathlib.Path(sys.argv[1])
        tipo = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
        uri = f"data:{tipo};base64," + base64.b64encode(p.read_bytes()).decode()
        dims = [int(v) for v in sys.argv[2:4]] if len(sys.argv) > 3 else None
        if not dims:
            raise SystemExit("Informe largura e altura da marca do TJPA: gerar.py arquivo LARGURA ALTURA")
        tjpa, suf = (uri, *dims), ""
    for nome in (f"logo_comite_oab_setic_horizontal{suf}", f"logo_comite_oab_setic_whatsapp_perfil{suf}"):
        if (AQUI / f"{nome}.png").exists():
            raise SystemExit(f"ERRO: {nome}.png já existe; não sobrescrevo.")
    svg, W, H_ = horizontal(tjpa)
    salvar(f"logo_comite_oab_setic_horizontal{suf}", svg, W, H_)
    salvar(f"logo_comite_oab_setic_whatsapp_perfil{suf}", avatar_completo(tjpa), 1080, 1080)
    if not (AQUI / "logo_comite_oab_setic_whatsapp_curto.png").exists():
        salvar("logo_comite_oab_setic_whatsapp_curto", avatar_curto(), 1080, 1080)


if __name__ == "__main__":
    main()
