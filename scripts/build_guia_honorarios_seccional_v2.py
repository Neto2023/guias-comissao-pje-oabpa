"""Guia de Honorários, versão Seccional v2: aplica a logo oficial da Comissão Estadual de Apoio
Institucional ao PJe sobre a v1 (guia-honorarios_seccional_v1.html), sem alterar a v1.

Mudanças (decisão de 16/11/2026: o guia passa a sair pela Comissão, como o Guia do PJe):
  - faixa azul: a pílula vira o nome da Comissão, com "Ordem dos Advogados do Brasil, Seção do Pará" ao lado;
  - capa: logo da Comissão acima da etiqueta "Guia de consulta";
  - rodapé: logo da Comissão (que já contém a OAB Pará);
  - barra superior: continua com a marca OAB Pará;
  - favicon com o "PJe" da logo; versão 1.1 (Seccional).

Uso (na pasta GUIAS SECCIONAL OAB-PA):
  python -I scripts/build_guia_honorarios_seccional_v2.py guia-honorarios_seccional_v1.html logo_comissao/OFICIAL guia-honorarios_seccional_v2.html
"""
import base64
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8")
entrada, pasta_logo, saida = map(pathlib.Path, sys.argv[1:4])
if saida.exists():
    raise SystemExit(f"ERRO: {saida} já existe; não sobrescrevo.")


def uri(p, tipo):
    return f"data:{tipo};base64," + base64.b64encode(p.read_bytes()).decode()


LOGO = uri(pasta_logo / "logo_comissao_pje_horizontal_web.png", "image/png")
ICONE = uri(pasta_logo / "favicon_pje_64.png", "image/png")
COMISSAO = "Comissão Estadual de Apoio Institucional ao PJe"
ALT = COMISSAO + ", OAB Pará"


def rep(t, old, new, n=1):
    c = t.count(old)
    if c != n:
        raise SystemExit(f"ERRO: esperado {n} ocorrência(s), achei {c}: {old[:90]!r}")
    return t.replace(old, new)


t = entrada.read_text(encoding="utf-8")

t = rep(t, "const MARCAS = { seccional: '", "const MARCAS = { comissao: '" + LOGO + "', seccional: '")
t = rep(t, "<title>Guia de Honorários | OAB/PA</title>",
        f'<title>Guia de Honorários | OAB/PA</title>\n<link rel="icon" type="image/png" href="{ICONE}">')
t = rep(t, '<meta name="description" content="Guia de Honorários da Ordem dos Advogados do Brasil, Seção do Pará (OAB/PA):',
        f'<meta name="description" content="Guia de Honorários da {COMISSAO} da Ordem dos Advogados do Brasil, Seção do Pará (OAB/PA):')
t = rep(t, '  "comissao": "Ordem dos Advogados do Brasil, Seção do Pará",', f'  "comissao": "{COMISSAO}",')
t = rep(t, '  "versao": "1.0 (Seccional)",', '  "versao": "1.1 (Seccional)",')
t = rep(t, '"Guia de Honorários · versão 1.0 (Seccional) · 16/11/2026 · Ordem dos Advogados do Brasil, Seção do Pará (OAB/PA)."',
        f'"Guia de Honorários · versão 1.1 (Seccional) · 16/11/2026 · {COMISSAO} · Ordem dos Advogados do Brasil, Seção do Pará (OAB/PA)."')
t = rep(t, '<div class="faixa-orgao"><div class="wrap"><span class="pill">Ordem dos Advogados do Brasil, Seção do Pará</span></div></div>',
        f'<div class="faixa-orgao"><div class="wrap"><span class="pill">{COMISSAO}</span>'
        '<small>Ordem dos Advogados do Brasil, Seção do Pará</small></div></div>')
t = rep(t, '      <span class="tag-guia">Guia de consulta</span>',
        f'      <img class="marca-capa marca-comissao" id="marca-comissao" alt="{ALT}">\n'
        '      <span class="tag-guia">Guia de consulta</span>')
t = rep(t, '<img class="marca-rodape" id="marca-rodape" alt="OAB Pará">',
        f'<img class="marca-rodape" id="marca-rodape" alt="{ALT}">')
t = rep(t, '  $("marca-rodape").src = MARCAS.seccional;',
        '  $("marca-rodape").src = MARCAS.comissao;\n  $("marca-comissao").src = MARCAS.comissao;')

CSS = """
/* v2: logo oficial da Comissão (PJe | nome em 5 linhas, com OAB Pará) */
.marca-comissao{display:block;width:auto;height:clamp(96px,17vw,150px);margin:0 0 1.2rem}
.rodape .marca-rodape{height:104px;padding:10px 14px}
@media print{.marca-comissao{height:28mm}.rodape .marca-rodape{height:24mm}}
"""
i = t.rfind("</style>", 0, t.find("</head>"))
t = t[:i] + CSS + t[i:]

if "—" in t:
    raise SystemExit("ERRO: sobrou travessão")
saida.write_text(t, encoding="utf-8")
print("ok", saida, len(t.encode("utf-8")), "bytes")
