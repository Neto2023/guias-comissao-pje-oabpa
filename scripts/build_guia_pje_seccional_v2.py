"""Guia Prático do PJe, versão Seccional v2: aplica a logo oficial da Comissão Estadual de Apoio
Institucional ao PJe sobre a v1 (guia-pje_seccional_v1.html), sem alterar a v1.

Mudanças:
  - capa: logo da Comissão acima da etiqueta "Guia de consulta";
  - rodapé e cartão: logo da Comissão (que já contém a OAB Pará) no lugar da marca OAB Pará sozinha;
  - barra superior: continua com a marca OAB Pará (a logo de 5 linhas não se lê em 38 px);
  - favicon com o "PJe" da logo;
  - versão 1.1 (Seccional).
O Guia de Honorários não muda: ele é da OAB/PA, não da Comissão.

Uso (na pasta GUIAS SECCIONAL OAB-PA):
  python -I scripts/build_guia_pje_seccional_v2.py guia-pje_seccional_v1.html logo_comissao/OFICIAL guia-pje_seccional_v2.html
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
ALT = "Comissão Estadual de Apoio Institucional ao PJe, OAB Pará"


def rep(t, old, new, n=1):
    c = t.count(old)
    if c != n:
        raise SystemExit(f"ERRO: esperado {n} ocorrência(s), achei {c}: {old[:90]!r}")
    return t.replace(old, new)


t = entrada.read_text(encoding="utf-8")

t = rep(t, "const MARCAS = { seccional: '", "const MARCAS = { comissao: '" + LOGO + "', seccional: '")
t = rep(t, "<title>Guia Prático do PJe | OAB/PA</title>",
        f'<title>Guia Prático do PJe | OAB/PA</title>\n<link rel="icon" type="image/png" href="{ICONE}">')
t = rep(t, '"versao": "1.0 (Seccional)",', '"versao": "1.1 (Seccional)",')

t = rep(t, '      <span class="tag-guia">Guia de consulta</span>',
        f'      <img class="marca-capa marca-comissao" src="${{MARCAS.comissao}}" alt="{ALT}">\n'
        '      <span class="tag-guia">Guia de consulta</span>')
t = rep(t, '<img class="marca-rodape" src="${MARCAS.seccional}" alt="OAB Pará">',
        f'<img class="marca-rodape" src="${{MARCAS.comissao}}" alt="{ALT}">')
t = rep(t, '<img class="marca-card" src="${MARCAS.seccional}" alt="OAB Pará">',
        f'<img class="marca-card" src="${{MARCAS.comissao}}" alt="{ALT}">')

CSS = """
/* v2: logo oficial da Comissão (PJe | nome em 5 linhas, com OAB Pará) */
.marca-comissao{display:block;width:auto;height:clamp(96px,17vw,150px);margin:0 0 1.2rem}
.rodape .marca-rodape{height:104px;padding:10px 14px}
.marca-card{height:84px}
@media print{.marca-comissao{height:28mm}.rodape .marca-rodape{height:24mm}}
"""
i = t.rfind("</style>", 0, t.find("</head>"))
t = t[:i] + CSS + t[i:]

for proibido in ("—", "cddClaro", "escudoClaro"):
    if proibido in t:
        raise SystemExit(f"ERRO: sobrou {proibido!r}")
saida.write_text(t, encoding="utf-8")
print("ok", saida, len(t.encode("utf-8")), "bytes")
