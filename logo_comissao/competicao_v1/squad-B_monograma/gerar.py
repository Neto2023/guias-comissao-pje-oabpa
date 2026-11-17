"""Squad B (Monograma PJe): gera todos os SVGs e PNGs da proposta.

Rodar a partir de competicao_v1:  python -I squad-B_monograma/gerar.py

Construcao do monograma numa grade de modulo m (haste = 3m):
  - altura de caixa 17m; largura total 30m (desenho mestre)
  - P: haste 3m, barra superior que segue ate a haste do J (ligadura), bojo com raio externo 5m
  - J: haste 3m, gancho de raio externo 5m encaixado sob o bojo do P
  - e: diametro 12m, traco 3m, braco superior fechado ate a barra, abertura de 40 graus;
       barra de 2m em vermelho, encerrada entre os dois lados do anel
  - compensacao optica: as curvas do J e do e passam 0,35m da linha de base (so no mestre)

Revisao da direcao de arte (v2):
  - barra do e deixou de vazar para fora do anel: o braco direito do e desce ate a base da barra
  - versao compacta (largura 28m) para o favicon de 32 px: margem de 2 px e tudo em pixel inteiro
  - favicon de 16 px redesenhado: bojo do P com vao de 2x2 px e barra vermelha de 2x2 px
  - linha de apoio com espacejamento menor e em marinho; PJe maior; regua com a largura da linha de apoio
"""
import math, pathlib, subprocess, sys, base64

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parent
KIT = RAIZ / "_kit"
FONTE = (KIT / "barlow_fontface.css").read_text(encoding="utf-8").strip()
OAB = (KIT / "oab_para_datauri.txt").read_text(encoding="utf-8").strip()
OAB_W, OAB_H = 347, 202  # dimensoes reais do JPEG (sem distorcer)

NAV, AZ, VM, TX, BR = "#003399", "#008BD2", "#D2091E", "#1B1B1B", "#FFFFFF"
APOIO = "COMISSÃO ESTADUAL DE APOIO INSTITUCIONAL AO"
ALT = 17

# bx: fim reto do bojo do P; jx: borda esquerda da haste do J; ecx: centro do e; os: compensacao optica
MESTRE = dict(bx=6, jx=13, ecx=24, W=30, os=0.35)
COMPACTO = dict(bx=5, jx=12, ecx=22, W=28, os=0.0)   # favicon de 32 px
LARG = MESTRE["W"]


def e_path(cx, cy, ro, ri, yb, ang=40):
    """Anel do e com o braco superior fechado ate y = yb (base da barra) e terminal inferior a `ang` graus."""
    dy = yb - cy
    a = math.radians(ang)
    xo, xi = cx + math.sqrt(ro * ro - dy * dy), cx + math.sqrt(ri * ri - dy * dy)
    return (f'M{xo:.3f} {yb:.3f} A{ro:.3f} {ro:.3f} 0 1 0 {cx + ro * math.cos(a):.3f} {cy + ro * math.sin(a):.3f} '
            f'L{cx + ri * math.cos(a):.3f} {cy + ri * math.sin(a):.3f} '
            f'A{ri:.3f} {ri:.3f} 0 1 1 {xi:.3f} {yb:.3f} Z')


def monograma(cor, barra, x=0, y=0, m=1.0, g=MESTRE):
    """Letras P J e desenhadas (sem fonte). Ocupa g['W'] x ALT modulos a partir de (x, y)."""
    bx, jx, cx, os = g["bx"], g["jx"], g["ecx"], g["os"]
    cy, t, tb = 11, 3, 2
    ro = 6 + os
    ri = ro - t
    xs = jx + 1.5  # eixo da haste do J
    el = [
        f'<rect x="0" y="0" width="3" height="{ALT}" fill="{cor}"/>',                       # haste do P
        f'<rect x="0" y="0" width="{jx + 3}" height="3" fill="{cor}"/>',                     # barra superior P+J
        f'<path d="M3 1.5 H{bx} A3.5 3.5 0 0 1 {bx} 8.5 H3" fill="none" stroke="{cor}" stroke-width="3"/>',  # bojo
        f'<path d="M{xs} 0 V{12 + os} A3.5 3.5 0 0 1 {xs - 7} {12 + os}" fill="none" stroke="{cor}" stroke-width="3"/>',  # J
        f'<rect x="{cx - ri - 0.3:.3f}" y="{cy - tb / 2}" width="{2 * ri + 0.6:.3f}" height="{tb}" fill="{barra}"/>',  # barra do e
        f'<path d="{e_path(cx, cy, ro, ri, cy + tb / 2)}" fill="{cor}"/>',                   # anel do e (por cima da barra)
    ]
    return f'<g transform="translate({x:.3f} {y:.3f}) scale({m})">{"".join(el)}</g>'


def svg(w, h, corpo, fonte=False, fundo=None):
    estilo = f"<style>{FONTE}</style>" if fonte else ""
    bg = f'<rect width="{w}" height="{h}" fill="{fundo}"/>' if fundo else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'{estilo}{bg}{corpo}</svg>')


def placa(T, rx, mfrac=0.74, cor_letra=BR, fundo=NAV):
    """Simbolo em placa quadrada: letras ocupam mfrac da largura, centradas na caixa."""
    m = T * mfrac / LARG
    x = (T - LARG * m) / 2
    y = (T - ALT * m) / 2
    return f'<rect width="{T}" height="{T}" rx="{rx}" fill="{fundo}"/>' + monograma(cor_letra, VM, x, y, m)


def oab(x, y, h, placa_branca=False):
    w = h * OAB_W / OAB_H
    s = ""
    if placa_branca:
        p = h * 0.16
        s += f'<rect x="{x - p:.1f}" y="{y - p:.1f}" width="{w + 2 * p:.1f}" height="{h + 2 * p:.1f}" rx="{h * 0.14:.1f}" fill="#FFFFFF"/>'
    s += f'<image x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" href="{OAB}"/>'
    return s, w


def logo_horizontal(marinho=False):
    W, H = 1600, 900
    cor = BR if marinho else NAV
    larg_txt = 1100          # linha de apoio e regua com a mesma largura
    fs = 36                  # Barlow 600; altura de versal ~ 0,7 fs
    m = 24
    pje_w, pje_h = LARG * m, ALT * m
    gap = 54                 # mesmo respiro entre apoio, PJe, regua e OAB
    oab_h = 122
    pad = oab_h * 0.16 if marinho else 0
    altura = 0.7 * fs + gap + pje_h + gap + 3 + gap + pad + oab_h + pad
    topo = (H - altura) / 2
    y_apoio = topo + 0.7 * fs
    y_pje = y_apoio + gap
    y_regua = y_pje + pje_h + gap
    y_oab = y_regua + 3 + gap + pad
    corpo = (
        f'<text x="{W / 2}" y="{y_apoio:.1f}" text-anchor="middle" font-family="Barlow" font-weight="600" '
        f'font-size="{fs}" fill="{cor}" textLength="{larg_txt}" lengthAdjust="spacing">{APOIO}</text>'
        + monograma(cor, VM, (W - pje_w) / 2, y_pje, m)
        + f'<rect x="{(W - larg_txt) / 2}" y="{y_regua:.1f}" width="{larg_txt}" height="3" fill="{cor}"/>'
    )
    w = oab_h * OAB_W / OAB_H
    o, _ = oab((W - w) / 2, y_oab, oab_h, placa_branca=marinho)
    corpo += o
    return svg(W, H, corpo, fonte=True, fundo=NAV if marinho else BR), W, H


# Favicon de 16 px desenhado pixel a pixel.
# '.' fundo marinho, '#' branco, 'r' vermelho, '1'..'9' branco com opacidade 0,1..0,9 (suavizacao manual)
GRADE16 = [
    "................",
    "................",
    "................",
    ".########.......",
    ".########.......",
    ".##..#.##.2###2.",
    ".##..#.##.6#..#.",
    ".####5.##.##..#.",
    ".##....##.##rr#.",
    ".##.##.##.##rr#.",
    ".##.##.##.##....",
    ".##.##.##.6#..4.",
    ".##.4###4.2###..",
    "................",
    "................",
    "................",
]


def favicon16():
    rects = []
    for yy, linha in enumerate(GRADE16):
        assert len(linha) == 16, linha
        for xx, ch in enumerate(linha):
            if ch == ".":
                continue
            if ch == "r":
                rects.append(f'<rect x="{xx}" y="{yy}" width="1" height="1" fill="{VM}"/>')
            else:
                op = "" if ch == "#" else f' fill-opacity="{int(ch) / 10}"'
                rects.append(f'<rect x="{xx}" y="{yy}" width="1" height="1" fill="{BR}"{op}/>')
    return svg(16, 16, f'<rect width="16" height="16" rx="3" fill="{NAV}"/>' + "".join(rects))


def render(nome_svg, nome_png, w, h, bg="#FFFFFF"):
    subprocess.run([sys.executable, "-I", str(KIT / "render.py"), str(AQUI / nome_svg), str(AQUI / nome_png), str(w), str(h), bg],
                   check=True, cwd=RAIZ, capture_output=True)


def grava(nome, conteudo):
    (AQUI / nome).write_text(conteudo, encoding="utf-8")


def main():
    # 1. simbolo
    grava("simbolo.svg", svg(512, 512, placa(512, 112)))
    render("simbolo.svg", "simbolo.png", 512, 512)
    # 2 e 3. logos horizontais
    s, W, H = logo_horizontal(False); grava("logo_horizontal.svg", s); render("logo_horizontal.svg", "logo_horizontal.png", W, H)
    s, W, H = logo_horizontal(True); grava("logo_horizontal_marinho.svg", s); render("logo_horizontal_marinho.svg", "logo_horizontal_marinho.png", W, H, NAV)
    # 4. avatar (fundo marinho cheio; letras dentro da area segura do recorte circular)
    grava("avatar.svg", svg(1080, 1080, placa(1080, 0, mfrac=0.62)))
    render("avatar.svg", "avatar.png", 1080, 1080, NAV)
    # 5. favicon: SVG em grade de 32 (desenho compacto, modulo = 1 px, margem de 2 px) e versao propria de 16 px
    fav = f'<rect width="32" height="32" rx="6" fill="{NAV}"/>' + monograma(BR, VM, 2, 7, 1, COMPACTO)
    grava("favicon.svg", svg(32, 32, fav))
    render("favicon.svg", "favicon_32.png", 32, 32)
    grava("favicon_16.svg", favicon16())
    render("favicon_16.svg", "favicon_16.png", 16, 16)
    prancha()


def uri(nome):
    return "data:image/png;base64," + base64.b64encode((AQUI / nome).read_bytes()).decode()


def prancha():
    W, H = 2400, 1440
    def rot(x, y, t, cor=TX):
        return f'<text x="{x}" y="{y}" font-family="Barlow" font-weight="600" font-size="22" letter-spacing="2" fill="{cor}">{t}</text>'
    c = [f'<rect width="{W}" height="{H}" fill="#F3F5F9"/>',
         f'<text x="80" y="110" font-family="Barlow" font-weight="800" font-size="54" fill="{NAV}">Squad B · Monograma PJe</text>',
         f'<text x="80" y="160" font-family="Barlow" font-weight="500" font-size="28" fill="{TX}">Comissão Estadual de Apoio Institucional ao PJe · OAB/PA · proposta para o júri</text>']
    # linha 1: logo horizontal branco e marinho
    lw, lh = 1080, 1080 * 900 / 1600
    c.append(rot(80, 230, "LOGO HORIZONTAL"))
    c.append(f'<rect x="80" y="250" width="{lw}" height="{lh}" fill="#fff" stroke="#D5DAE3"/>')
    c.append(f'<image x="80" y="250" width="{lw}" height="{lh}" href="{uri("logo_horizontal.png")}"/>')
    c.append(rot(1240, 230, "LOGO HORIZONTAL EM FUNDO MARINHO"))
    c.append(f'<image x="1240" y="250" width="{lw}" height="{lh}" href="{uri("logo_horizontal_marinho.png")}"/>')
    # linha 2: simbolo, avatar, favicons
    y2 = 250 + lh + 90
    c.append(rot(80, y2 - 20, "SÍMBOLO"))
    # recorte nos cantos arredondados (o PNG tem fundo branco fora da placa)
    c.append(f'<clipPath id="placa"><rect x="80" y="{y2}" width="440" height="440" rx="{112 * 440 / 512:.2f}"/></clipPath>')
    c.append(f'<image x="80" y="{y2}" width="440" height="440" clip-path="url(#placa)" href="{uri("simbolo.png")}"/>')
    c.append(rot(580, y2 - 20, "AVATAR (RECORTE CIRCULAR)"))
    c.append(f'<clipPath id="circ"><circle cx="{580 + 220}" cy="{y2 + 220}" r="220"/></clipPath>')
    c.append(f'<image x="580" y="{y2}" width="440" height="440" clip-path="url(#circ)" href="{uri("avatar.png")}"/>')
    c.append(rot(1080, y2 - 20, "AVATAR (QUADRADO)"))
    c.append(f'<image x="1080" y="{y2}" width="300" height="300" href="{uri("avatar.png")}"/>')
    c.append(rot(1440, y2 - 20, "FAVICON 32 E 16 (AMPLIADOS 8X)"))
    c.append(f'<clipPath id="f32"><rect x="1440" y="{y2}" width="256" height="256" rx="48"/></clipPath>')
    c.append(f'<image x="1440" y="{y2}" width="256" height="256" clip-path="url(#f32)" style="image-rendering:pixelated" href="{uri("favicon_32.png")}"/>')
    c.append(f'<clipPath id="f16"><rect x="1730" y="{y2}" width="128" height="128" rx="24"/></clipPath>')
    c.append(f'<image x="1730" y="{y2}" width="128" height="128" clip-path="url(#f16)" style="image-rendering:pixelated" href="{uri("favicon_16.png")}"/>')
    c.append(rot(1440, y2 + 320, "TAMANHO REAL"))
    c.append(f'<image x="1440" y="{y2 + 340}" width="32" height="32" href="{uri("favicon_32.png")}"/>')
    c.append(f'<image x="1500" y="{y2 + 348}" width="16" height="16" href="{uri("favicon_16.png")}"/>')
    # aba de navegador simulada
    ty = y2 + 400
    c.append(f'<rect x="1440" y="{ty}" width="560" height="44" rx="10" fill="#DEE3EC"/>')
    c.append(f'<rect x="1452" y="{ty + 6}" width="300" height="38" rx="8" fill="#fff"/>')
    c.append(f'<image x="1466" y="{ty + 17}" width="16" height="16" href="{uri("favicon_16.png")}"/>')
    c.append(f'<text x="1494" y="{ty + 31}" font-family="Barlow" font-weight="500" font-size="17" fill="{TX}">Apoio ao PJe · OAB/PA</text>')
    c.append(f'<rect x="1764" y="{ty + 6}" width="230" height="38" rx="8" fill="#1B1B1B"/>')
    c.append(f'<image x="1778" y="{ty + 17}" width="16" height="16" href="{uri("favicon_16.png")}"/>')
    c.append(f'<text x="1804" y="{ty + 31}" font-family="Barlow" font-weight="500" font-size="17" fill="#fff">Modo escuro</text>')
    # construcao (desenho mestre sem a compensacao optica, para a grade ficar legivel)
    gx, gy, gm = 2060, y2, 9.5
    c.append(rot(gx, y2 - 20, "GRADE (MÓDULO M)"))
    grade = "".join(f'<line x1="{gx + i * gm}" y1="{gy}" x2="{gx + i * gm}" y2="{gy + ALT * gm}" stroke="#C9D2E3" stroke-width="1"/>' for i in range(LARG + 1))
    grade += "".join(f'<line x1="{gx}" y1="{gy + j * gm}" x2="{gx + LARG * gm}" y2="{gy + j * gm}" stroke="#C9D2E3" stroke-width="1"/>' for j in range(ALT + 1))
    c.append(f'<rect x="{gx}" y="{gy}" width="{LARG * gm}" height="{ALT * gm}" fill="#fff"/>' + grade)
    c.append(f'<g opacity="0.85">{monograma(NAV, VM, gx, gy, gm, dict(MESTRE, os=0))}</g>')
    for i, t in enumerate(["haste 3m · altura 17m", "bojo e gancho: raio 5m", "e: diâmetro 12m, barra 2m",
                           "curvas passam 0,35m da base"]):
        c.append(f'<text x="{gx}" y="{gy + ALT * gm + 40 + i * 30}" font-family="Barlow" font-weight="500" font-size="20" fill="{TX}">{t}</text>')
    grava("prancha.svg", svg(W, H, "".join(c), fonte=True))
    render("prancha.svg", "prancha.png", W, H, "#F3F5F9")


if __name__ == "__main__":
    main()
