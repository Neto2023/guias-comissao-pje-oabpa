"""Rascunhos do Squad B: variacoes do monograma PJe (grade 100x100)."""
import pathlib, subprocess, sys
AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parent.parent
NAV, AZ, VM = "#003399", "#008BD2", "#D2091E"

def e_letra(cx, cy, r, sw, cor, cor_barra):
    # e geometrico: arco aberto no quadrante inferior direito + barra horizontal
    import math
    a0 = math.radians(40)  # abertura
    x1, y1 = cx + r*math.cos(a0), cy + r*math.sin(a0)
    arco = f'<path d="M{cx+r:.2f} {cy} A{r} {r} 0 1 0 {x1:.2f} {y1:.2f}" fill="none" stroke="{cor}" stroke-width="{sw}"/>'
    barra = f'<path d="M{cx-r-sw/2+0.5:.2f} {cy} H{cx+r+sw/2:.2f}" stroke="{cor_barra}" stroke-width="{sw*0.75:.2f}"/>'
    return arco + barra

def var_a():
    # Ligadura: haste do P desce e vira o gancho do J; e a direita com barra vermelha
    s = 13
    pj = f'<path d="M38 8 V66 A14 14 0 0 1 10 66" fill="none" stroke="{NAV}" stroke-width="{s}"/>'
    bojo = f'<path d="M38 14.5 H58 A16.5 16.5 0 0 1 58 47.5 H38" fill="none" stroke="{NAV}" stroke-width="{s}"/>'
    return pj + bojo + e_letra(72, 76, 14, 10, NAV, VM)

def var_b():
    # Tres letras em placa marinho, brancas, barra do e vermelha
    s = 10
    g = f'<rect x="2" y="2" width="96" height="96" rx="20" fill="{NAV}"/>'
    p = f'<path d="M17 76 V27 H29 A11.5 11.5 0 0 1 29 50 H17" fill="none" stroke="#fff" stroke-width="{s}" stroke-linejoin="miter"/>'
    j = f'<path d="M52 22 V62 A9 9 0 0 1 34 62" fill="none" stroke="#fff" stroke-width="{s}"/>'
    return g + p + j + e_letra(73, 62, 12, s, "#fff", VM)

def var_c():
    # Ligadura PJ branca em placa marinho; e vermelho integral
    s = 14
    g = f'<rect x="2" y="2" width="96" height="96" rx="22" fill="{NAV}"/>'
    pj = f'<path d="M36 18 V64 A12 12 0 0 1 12 64" fill="none" stroke="#fff" stroke-width="{s}"/>'
    bojo = f'<path d="M36 25 H54 A14 14 0 0 1 54 53 H36" fill="none" stroke="#fff" stroke-width="{s}"/>'
    return g + pj + bojo + e_letra(72, 75, 11.5, 9, VM, VM)

def var_d():
    # P e J compartilham a haste em contraforma; e ocupa o bojo do P (contraforma vermelha)
    s = 13
    pj = f'<path d="M30 8 V68 A13 13 0 0 1 4 68" fill="none" stroke="{NAV}" stroke-width="{s}"/>'
    bojo = f'<path d="M30 14.5 H62 A27 27 0 0 1 62 68.5 H30" fill="none" stroke="{NAV}" stroke-width="{s}"/>'
    return pj + bojo + e_letra(60, 41.5, 12, 8, NAV, VM)


def letras(cor, barra, s=11, extend=False):
    # grade: altura de caixa 60, haste 11, curvas de raio externo 17 (P e J) e 21 (e)
    P = (f'<path d="M5.5 0 V60" stroke="{cor}" stroke-width="{s}"/>'
         f'<path d="M5.5 5.5 H17 A11.5 11.5 0 0 1 17 28.5 H5.5" fill="none" stroke="{cor}" stroke-width="{s}"/>')
    J = f'<path d="M45.5 0 V43 A11.5 11.5 0 0 1 22.5 43" fill="none" stroke="{cor}" stroke-width="{s}"/>'
    import math
    cx, cy, Ro, t, tb = 78, 39, 21, 10, 7.5
    rc = Ro - t/2; a = math.radians(40)
    e = (f'<path d="M{cx+rc} {cy} A{rc} {rc} 0 1 0 {cx+rc*math.cos(a):.2f} {cy+rc*math.sin(a):.2f}" fill="none" stroke="{cor}" stroke-width="{t}"/>'
         f'<rect x="{(51 if extend else cx-Ro+1):.2f}" y="{cy-tb/2}" width="{(cx+Ro-(51 if extend else cx-Ro+1)):.2f}" height="{tb}" fill="{barra}"/>')
    return P + J + e

def var_e():
    return f'<g transform="translate(0.5 20) scale(1)">{letras(NAV, VM)}</g>'

def var_f():
    return f'<rect x="2" y="2" width="96" height="96" rx="22" fill="{NAV}"/><g transform="translate(13.4 27.8) scale(0.74)">{letras("#fff", VM)}</g>'

def var_g():
    return f'<g transform="translate(0.5 20)">{letras(NAV, VM, extend=True)}</g>'

def var_h():
    # E + ligadura: a barra superior do P segue ate a haste do J (um so traco)
    liga = f'<path d="M5.5 5.5 H51" stroke="{NAV}" stroke-width="11"/>'
    return f'<g transform="translate(0.5 20)">{letras(NAV, VM)}{liga}</g>'

def var_i():
    liga = '<path d="M5.5 5.5 H51" stroke="#fff" stroke-width="11"/>'
    return f'<rect x="2" y="2" width="96" height="96" rx="22" fill="{NAV}"/><g transform="translate(10.4 25.8) scale(0.8)">{letras("#fff", VM)}{liga}</g>'

VARS = {"H_ligadura_topo": var_h, "I_ligadura_topo_placa": var_i, "E_monograma_grade": var_e, "F_monograma_placa": var_f, "G_barra_conexao": var_g, "A_ligadura": var_a, "B_placa_tres_letras": var_b, "C_placa_ligadura_e_vermelho": var_c, "D_e_no_bojo": var_d}
for nome, f in VARS.items():
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">{f()}</svg>'
    sp = AQUI / f"{nome}.svg"; sp.write_text(svg, encoding="utf-8")
    for tam in (256, 32, 16):
        subprocess.run([sys.executable, "-I", str(RAIZ / "_kit/render.py"), str(sp), str(AQUI / f"{nome}_{tam}.png"), str(tam), str(tam)], check=True, cwd=RAIZ, capture_output=True)
print("ok")
