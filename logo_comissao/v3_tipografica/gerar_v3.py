"""v3 da logo da Comissao: a mesma ideia da imagem usada hoje no WhatsApp (PJe | nome por extenso),
redesenhada nas cores da Seccional, com "PJe" em Barlow (e nao a marca do CNJ) e a OAB Para discreta.

Uso:  python -I gerar_v3.py
Reaproveita utilidades do gerador do Squad A (competicao_v1/squad-A_tela-processo/gerar.py), sem altera-lo.
"""
import pathlib
import sys

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parent / "competicao_v1"
sys.path.insert(0, str(RAIZ / "squad-A_tela-processo"))
import gerar as G  # noqa: E402

MARINHO, AZUL, VERMELHO, BRANCO, TEXTO = G.MARINHO, G.AZUL, G.VERMELHO, G.BRANCO, G.TEXTO
MET, CAP = G.MET, G.CAP
LINHAS = ["COMISSÃO", "ESTADUAL", "DE APOIO", "INSTITUCIONAL", "AO PJe"]
CORES_E = {"vermelho": VERMELHO, "azul": AZUL}


def pje(x_tinta, y, S, cor_pj, cor_e):
    """'PJe' em Barlow 800 com o espacejamento optico do Squad A; o 'e' em cor de destaque."""
    kern_pj = MET["800|PJ"]["adv"] - MET["800|P"]["adv"] - MET["800|J"]["adv"]
    oJ = MET["800|P"]["adv"] + kern_pj + G.K_PJ
    oE = oJ + MET["800|J"]["adv"] + G.K_JE
    esq = -MET["800|P"]["l"]
    u = S / 1000
    x0 = x_tinta - esq * u
    t = lambda ch, o, c: (f'<text x="{x0 + o * u:.2f}" y="{y:.2f}" font-family="Barlow" font-weight="800" '
                          f'font-size="{S:.2f}" font-kerning="none" fill="{c}">{ch}</text>')
    return t("P", 0, cor_pj) + t("J", oJ, cor_pj) + t("e", oE, cor_e), (oE + MET["800|e"]["r"] - esq) * u


def lockup(cor_e, com_oab=True):
    """Bloco horizontal: PJe | nome em 5 linhas (+ OAB Para sob o nome). Devolve (svg, largura, altura)."""
    S = 300.0
    capS = CAP * S
    a = 0.205 * S                     # corpo do nome
    lh = 1.13 * a                     # entrelinha
    bloco = 4 * lh + CAP * a          # altura de tinta das 5 linhas
    ho = 1.55 * a if com_oab else 0
    gap_o = 0.55 * a if com_oab else 0
    total = bloco + gap_o + ho
    # PJe centralizado na altura do nome (sem a OAB), como na imagem atual
    y_nome0 = 0.0
    y_pje = y_nome0 + bloco / 2 + capS / 2
    tp, wp = pje(0, y_pje, S, MARINHO, cor_e)
    xb = wp + 0.17 * S                 # barra vertical
    wb = 0.018 * S
    xn = xb + wb + 0.13 * S
    nome = "".join(
        f'<text x="{xn:.2f}" y="{y_nome0 + CAP * a + i * lh:.2f}" font-family="Barlow" font-weight="700" '
        f'font-size="{a:.2f}" letter-spacing="{0.01 * a:.2f}" fill="{MARINHO}">{l}</text>'
        for i, l in enumerate(LINHAS))
    barra = f'<rect x="{xb:.2f}" y="{-0.06 * S:.2f}" width="{wb:.2f}" height="{total + 0.12 * S:.2f}" fill="{MARINHO}"/>'
    oab = ""
    w_oab = 0
    if com_oab:
        w_oab = ho * G.OAB_W / G.OAB_H
        oab = f'<image x="{xn - 0.02 * a:.2f}" y="{bloco + gap_o:.2f}" width="{w_oab:.2f}" height="{ho:.2f}" href="{G.OAB}"/>'
    # largura do nome: a linha mais longa e INSTITUCIONAL (~ 6,4 corpos em Barlow 700)
    w_nome = 7.0 * a
    return tp + barra + nome + oab, xn + max(w_nome, w_oab), total


def horizontal(cor_e, W=1600, M=140):
    corpo, wc, hc = lockup(cor_e)
    k = (W - 2 * M) / wc
    H = int(round(hc * k + 2 * M + 0.12 * 300 * k))
    g = f'<g transform="translate({M},{(H - hc * k) / 2:.2f}) scale({k:.5f})">{corpo}</g>'
    return G.svg_doc(W, H, g, bg=BRANCO), W, H


def avatar_completo(cor_e, W=1080):
    """Para o WhatsApp: o bloco cabe inteiro no circulo de recorte, com folga."""
    corpo, wc, hc = lockup(cor_e)
    raio_util = 0.84 * W / 2
    k = raio_util / ((wc / 2) ** 2 + (hc / 2) ** 2) ** 0.5
    x = (W - wc * k) / 2
    y = (W - hc * k) / 2
    return G.svg_doc(W, W, f'<g transform="translate({x:.2f},{y:.2f}) scale({k:.5f})">{corpo}</g>', bg=BRANCO)


def avatar_pje(cor_e, W=1080):
    """So o PJe, legivel mesmo na lista de conversas (cerca de 50 px)."""
    S = 1000.0
    tp, wp = pje(0, 0, S, MARINHO, cor_e)
    k = 0.66 * W / wp
    capS = CAP * S
    x = (W - wp * k) / 2
    y = W / 2 + capS * k / 2
    corpo = f'<g transform="translate({x:.2f},{y:.2f}) scale({k:.5f})">{tp}</g>'
    return G.svg_doc(W, W, corpo, bg=BRANCO)


def favicon(cor_e):
    return avatar_pje(cor_e, W=64)


def salvar(nome, svg, w, h, bg=BRANCO):
    (AQUI / f"{nome}.svg").write_text(svg, encoding="utf-8")
    G.render(AQUI / f"{nome}.svg", AQUI / f"{nome}.png", w, h, bg)


def prancha(dims):
    uri = G.png_uri
    W = 2000

    def lab(t, x, y):
        return (f'<text x="{x}" y="{y}" font-family="Barlow" font-weight="700" font-size="24" '
                f'letter-spacing="1.5" fill="#5A6275">{t}</text>')

    c = [f'<text x="50" y="80" font-family="Barlow" font-weight="800" font-size="46" fill="{MARINHO}">'
         f'Logo da Comissão, versão 3: a ideia que já está no WhatsApp, nas cores da OAB/PA</text>',
         f'<text x="50" y="124" font-family="Barlow" font-weight="500" font-size="24" fill="{TEXTO}">'
         f'PJe em Barlow (não a marca do CNJ), barra e nome em 5 linhas, OAB Pará discreta. '
         f'Duas opções para a cor do "e": vermelho ou azul.</text>']
    y = 200
    for cor in CORES_E:
        w0, h0 = dims[f"logo_horizontal_{cor}"]
        lw = 1000
        lh = lw * h0 / w0
        c += [lab(f'"e" {cor.upper()}', 50, y - 14),
              f'<rect x="50" y="{y}" width="{lw}" height="{lh:.1f}" fill="#fff" stroke="#D5DAE5" stroke-width="2"/>',
              f'<image x="50" y="{y}" width="{lw}" height="{lh:.1f}" href="{uri(AQUI / f"logo_horizontal_{cor}.png")}"/>']
        # previas do WhatsApp em circulo
        x = 1110
        for nome, d, rot in ((f"avatar_completo_{cor}", 300, "WHATSAPP, PERFIL"),
                             (f"avatar_pje_{cor}", 300, "WHATSAPP, SÓ PJe")):
            cid = f"c{nome}"
            c += [lab(rot, x, y - 14),
                  f'<clipPath id="{cid}"><circle cx="{x + d / 2}" cy="{y + d / 2}" r="{d / 2}"/></clipPath>',
                  f'<circle cx="{x + d / 2}" cy="{y + d / 2}" r="{d / 2 + 1}" fill="none" stroke="#C9D0DE" stroke-width="2"/>',
                  f'<image x="{x}" y="{y}" width="{d}" height="{d}" clip-path="url(#{cid})" href="{uri(AQUI / f"{nome}.png")}"/>']
            # tamanho real da lista de conversas (48 px)
            cid2 = cid + "p"
            c += [f'<clipPath id="{cid2}"><circle cx="{x + 24}" cy="{y + d + 50}" r="24"/></clipPath>',
                  f'<image x="{x}" y="{y + d + 26}" width="48" height="48" clip-path="url(#{cid2})" href="{uri(AQUI / f"{nome}.png")}"/>',
                  f'<text x="{x + 62}" y="{y + d + 58}" font-family="Barlow" font-weight="500" font-size="20" fill="#5A6275">48 px, lista de conversas</text>']
            x += 440
        y += max(lh, 400) + 90
    H = int(y)
    (AQUI / "prancha_v3.svg").write_text(G.svg_doc(W, H, "".join(c), bg="#F3F5F9"), encoding="utf-8")
    G.render(AQUI / "prancha_v3.svg", AQUI / "prancha_v3.png", W, H, "#F3F5F9")


def main():
    dims = {}
    for cor, hexa in CORES_E.items():
        svg, W, H = horizontal(hexa)
        salvar(f"logo_horizontal_{cor}", svg, W, H)
        dims[f"logo_horizontal_{cor}"] = (W, H)
        salvar(f"avatar_completo_{cor}", avatar_completo(hexa), 1080, 1080)
        salvar(f"avatar_pje_{cor}", avatar_pje(hexa), 1080, 1080)
        salvar(f"favicon_{cor}", favicon(hexa), 64, 64)
    prancha(dims)


if __name__ == "__main__":
    main()
