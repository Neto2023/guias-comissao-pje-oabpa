"""Gera as versões da Seccional (OAB/PA) do Guia do PJe e do Guia de Honorários.

Entrada: os originais da Comissão de Direito Digital (Subseção Marabá), sem alteração.
Saída:   guia-pje_seccional_v1.html e guia-honorarios_seccional_v1.html.

Decisões aprovadas pelo Dr. Abrahão em 16/11/2026:
- Guia do PJe: Comissão Estadual de Apoio Institucional ao PJe, com nota de origem (Guia CDD 001/2026).
- Guia de Honorários: identidade da OAB/PA (Seccional), sem comissão.
- Grupo Crimes Cibernéticos: mantido como está (proposta CDD com selo).
- Layout: Opção A (moldura do Painel de Jurimetria da Comissão).
- Canal do Guia do PJe: apoio_pje@oabpa.org.br (sem WhatsApp).

Uso: python -I build_guias_seccional_v1.py <pasta_originais> <logo_oab_para.jpeg> <pasta_fontes_barlow> <pasta_saida>
"""
import base64
import pathlib
import re
import sys

orig, logo, fontes_dir, saida = (pathlib.Path(a) for a in sys.argv[1:5])

LOGO_URI = "data:image/jpeg;base64," + base64.b64encode(logo.read_bytes()).decode()
ATUALIZADO = "2026-11-16"


def rep(t, old, new, n=1):
    c = t.count(old)
    if c != n:
        raise SystemExit(f"ERRO: esperado {n}x, achado {c}x: {old[:90]!r}")
    return t.replace(old, new)


def fontes_barlow():
    faces = []
    for w in (400, 500, 600, 700, 800):
        b64 = base64.b64encode((fontes_dir / f"barlow-latin-{w}.woff2").read_bytes()).decode()
        faces.append("@font-face{font-family:'Barlow';font-style:normal;font-weight:%d;font-display:swap;"
                     "src:url(data:font/woff2;base64,%s) format('woff2')}" % (w, b64))
    return "\n".join(faces)


def trocar_fontes(t):
    # retira Archivo e IBM Plex Sans (substituídas pela Barlow); mantém IBM Plex Mono
    linhas = t.split("\n")
    out, removidas = [], 0
    for l in linhas:
        if re.match(r"^(<style id=\"fontes-embutidas\">)?@font-face\{font-family:'(Archivo|IBM Plex Sans)'", l):
            removidas += 1
            if l.startswith('<style id="fontes-embutidas">'):
                out.append('<style id="fontes-embutidas">' + fontes_barlow())
            continue
        out.append(l)
    if removidas != 4:
        raise SystemExit(f"ERRO: esperava remover 4 @font-face, removi {removidas}")
    t = "\n".join(out)
    t = rep(t, '--sans:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;',
            '--sans:Barlow,system-ui,-apple-system,"Segoe UI",sans-serif;')
    t = rep(t, '--display:Archivo,"Segoe UI",system-ui,sans-serif;',
            '--display:Barlow,"Segoe UI",system-ui,sans-serif;')
    return t


def tokens(t):
    t = rep(t, '<meta name="theme-color" content="#001333">', '<meta name="theme-color" content="#008BD2">')
    t = rep(t, "--azul:#0095D9;", "--azul:#008BD2;")
    t = rep(t, "--azul-esc:#0077AE;", "--azul-esc:#0072B5;")
    t = rep(t, "--vermelho:#D1232D;", "--vermelho:#D2091E;--marinho:#003399;--texto:#1B1B1B;")
    t = t.replace("rgba(0,149,217,", "rgba(0,139,210,")
    # só a marca da OAB Pará fica embutida; as marcas da CDD saem do arquivo
    t, n = re.subn(r"const MARCAS = \{ oabClaro: '[^']*', escudoClaro: '[^']*', cddClaro: '[^']*', cdd: '[^']*', oab: '[^']*' \};",
                   "const MARCAS = { seccional: '" + LOGO_URI + "' };", t)
    if n != 1:
        raise SystemExit("ERRO: bloco MARCAS não encontrado")
    return t


# moldura comum (Opção A): faixa azul, barra branca, capa branca, rodapé marinho
CSS_COMUM = """
/* ============================================================
   IDENTIDADE DA SECCIONAL (OAB/PA)
   Moldura do Painel de Jurimetria da Comissão Estadual de Apoio
   Institucional ao PJe: faixa azul, barra branca com a marca da
   OAB Pará, capa branca com sublinhado vermelho, rodapé marinho.
   ============================================================ */
.faixa-orgao{background:var(--azul);color:#fff}
.faixa-orgao .wrap{display:flex;flex-wrap:wrap;gap:.5rem 1rem;align-items:center;justify-content:space-between;padding-top:.55rem;padding-bottom:.55rem}
.faixa-orgao .pill{background:#0072B5;border-radius:6px;padding:.35rem .9rem;font-weight:600;font-size:.9rem;line-height:1.3}
.faixa-orgao small{font-size:.85rem;font-weight:500}
.barra{background:#fff;color:var(--texto);border-bottom:0;box-shadow:0 2px 6px rgba(0,0,0,.08);backdrop-filter:none}
.barra-marca,.barra-marca b{color:var(--marinho)}
.barra-marca b{font-weight:700;letter-spacing:0}
.barra-marca b em{color:var(--azul)}
.selo{height:38px;width:auto}
.selo-oab{display:none!important}
.busca-barra .busca{background:#fff;border-color:#CFD8DF;color:var(--texto)}
.busca-barra .busca::placeholder{color:#6B7785}
.busca-barra .busca:focus{background:#fff;border-color:var(--azul)}
.busca-barra .busca-ico{color:#6B7785}
.busca-tecla{color:#6B7785;border-color:#CFD8DF}
.capa{background:#fff;color:var(--texto);padding:2.4rem 0 2.3rem;border-bottom:1px solid var(--linha)}
.capa::before{display:none}
.capa h1{color:var(--texto);font-weight:700;letter-spacing:-.01em}
.capa h1 em{color:var(--marinho)}
.lede{color:#4A4A4A}
.tag-guia{display:inline-block;font-size:1rem;font-weight:500;color:var(--texto);padding:2px 8px 4px;border-bottom:2px solid var(--vermelho);border-radius:0 0 10px 10px;margin:0 0 1rem}
.inicio{border-top-color:var(--linha)}
.inicio-tit{color:var(--slate)}
.bt-inicio{background:#fff;border-color:var(--linha);color:var(--texto)}
.bt-inicio:hover{background:var(--tint);border-color:var(--azul)}
.bt-inicio b{color:var(--marinho)}
.bt-inicio small{color:var(--slate)}
.bt-inicio .ico{color:var(--azul)}
.bt-inicio.destaque-inicio{background:#fff;border-color:var(--azul);box-shadow:inset 3px 0 0 var(--azul)}
.bt-inicio.destaque-inicio:hover{background:var(--tint)}
.rodape{background:var(--marinho);color:#E6EEFA}
.rodape::before{display:none}
.rodape h3{color:#fff}
.rodape a{color:#BFE3FF}
.marca-rodape{background:#fff;border-radius:10px;padding:8px;height:64px;width:auto}
.fontes,.fontes a{color:#C9D6EE}
.fontes{border-top-color:rgba(255,255,255,.2)}
.origem{font-size:.85rem;color:#C9D6EE;margin-top:1rem}
"""

CSS_PJE = CSS_COMUM + """
.bt{background:#fff;border-color:#CFD8DF;color:var(--texto)}
.bt:hover{background:var(--tint);border-color:var(--azul);color:var(--marinho)}
.bt[aria-pressed="true"],.bt-p{background:var(--azul);border-color:var(--azul);color:#fff}
.bt-p:hover{background:var(--azul-esc);border-color:var(--azul-esc);color:#fff}
.grupo-disp{border-color:#CFD8DF;background:#fff}
.grupo-disp .bt+.bt{border-left-color:#CFD8DF}
.grupo-disp .bt[aria-pressed="true"]{background:var(--azul);color:#fff}
.barra-trilha{background:var(--tint);border-color:var(--linha)}
.trilha-estado u{color:var(--slate)}
.trilha-estado i{color:var(--texto)}
.trilha-estado s .ico{color:var(--verde)}
.mini-barra{background:var(--linha)}
.mini-barra i.completo{background:var(--verde)}
.barra-progresso span{color:var(--slate)}
@media (max-width:820px){.busca-barra:focus-within .busca{background:#fff}}
.portas{border-top-color:var(--linha)}
.portas-tit{color:var(--texto)}
.portas-sub{color:#4A4A4A}
.porta{background:#fff;border-color:var(--linha);color:var(--texto)}
.porta::before{background:var(--azul)}
.porta:last-child::before{background:var(--vermelho)}
.porta:hover{background:var(--tint);border-color:var(--azul)}
.porta:last-child:hover{background:#FFF5F5;border-color:var(--vermelho)}
.porta b{color:var(--marinho)}
.porta span{color:var(--texto)}
.porta small{color:var(--slate)}
.ico-porta{color:var(--azul)}
.porta:last-child .ico-porta{color:var(--vermelho)}
.card-cab{border-bottom-color:var(--azul)}
.marca-card{height:56px}
"""

CSS_HON = CSS_COMUM + """
.bt-disp{background:#fff;border-color:#CFD8DF;color:var(--texto)}
.bt-disp:hover{background:var(--tint);border-color:var(--azul);color:var(--marinho)}
.bt-disp[aria-pressed="true"]{background:var(--azul);border-color:var(--azul);color:#fff}
.grupo-disp{border-color:#CFD8DF;background:#fff}
.resultado{background:var(--marinho)}
.resultado h3 i{background:var(--vermelho)}
.linha-res.grande b{color:#BFE3FF}
.marca-rodape{height:64px}
"""


def css_final(t, css):
    # a última </style> do <head> fecha a folha principal
    i = t.rfind("</style>", 0, t.find("</head>"))
    return t[:i] + css + t[i:]


# ------------------------------------------------------------------ Guia do PJe
def guia_pje():
    t = (orig / "guia-pje.html").read_text(encoding="utf-8")
    t = trocar_fontes(t)
    t = tokens(t)
    t = css_final(t, CSS_PJE)

    t = rep(t, "<title>Guia PJe | CDD OAB Marabá</title>",
            "<title>Guia Prático do PJe | OAB/PA</title>")
    t = rep(t, 'content="Guia PJe da Comissão de Direito Digital da OAB/PA, Subseção Marabá. Primeiro acesso e resolução de problemas recorrentes,',
            'content="Guia Prático do Processo Judicial Eletrônico (PJe) da Comissão Estadual de Apoio Institucional ao PJe da Ordem dos Advogados do Brasil, Seção do Pará (OAB/PA). Primeiro acesso e resolução de problemas recorrentes,')
    t = rep(t, "   GUIA CDD 001/2026 — PRIMEIRO ACESSO AOS SISTEMAS PROCESSUAIS\n   Comissão de Direito Digital · OAB/PA · Subseção Marabá",
            "   GUIA PRÁTICO DO PJE, PRIMEIRO ACESSO AOS SISTEMAS PROCESSUAIS\n   Comissão Estadual de Apoio Institucional ao PJe · OAB/PA (Seccional)\n   1ª edição: Guia CDD 001/2026, Comissão de Direito Digital, Subseção Marabá")

    # dados institucionais
    t = rep(t, '"guia": "CDD 001/2026",', '"guia": "Guia Prático do PJe",')
    t = rep(t, '"versao": "3.1",', '"versao": "1.0 (Seccional)",')
    t = rep(t, '"atualizado_em": "2026-08-16",', f'"atualizado_em": "{ATUALIZADO}",')
    t = rep(t, '"local": "Marabá/PA",', '"local": "[Cidade]/PA",')
    t = rep(t, '"comissao": "Comissão de Direito Digital",', '"comissao": "Comissão Estadual de Apoio Institucional ao PJe",')
    t = rep(t, '"orgao": "Ordem dos Advogados do Brasil, Seccional Pará, Subseção Marabá",',
            '"orgao": "Ordem dos Advogados do Brasil, Seção do Pará (OAB/PA)",\n    "origem": "1ª edição: Guia CDD 001/2026, elaborado pela Comissão de Direito Digital da Subseção Marabá da OAB/PA.",')
    t = re.sub(r'\n\s*"presidente": "[^"]*",\n\s*"inscricao": "[^"]*",', "", t, count=1)
    t = rep(t, '"email": "direitodigitaloabmaraba@gmail.com",', '"email": "apoio_pje@oabpa.org.br",')
    t = rep(t, '"whatsapp": "(94) 98449-3079",', '"whatsapp": "",')
    t = rep(t, '"whatsappNum": "5594984493079",', '"whatsappNum": "",')
    t = rep(t, '"lede": "Primeiro acesso e resolução de problemas recorrentes."',
            '"lede": "Primeiro acesso ao Processo Judicial Eletrônico (PJe) e resolução de problemas recorrentes."')
    t = rep(t, "Ou seja: procurar a Subseção é caminho previsto, não atalho.",
            "Ou seja: procurar a OAB é caminho previsto, não atalho.")
    t = rep(t, '"intro": "Procure a Comissão de Direito Digital quando o suporte do tribunal',
            '"intro": "Procure a Comissão Estadual de Apoio Institucional ao PJe da OAB/PA quando o suporte do tribunal')
    t = rep(t, '"rotulo": "Canais da Comissão",\n        "detalhe": "Havendo prazo correndo, use o WhatsApp. O e-mail serve para registro formal e para casos sem urgência. O botão abaixo monta o texto com os dados que a Comissão precisa para escalar ao Tribunal."',
            '"rotulo": "Canal da Comissão",\n        "detalhe": "Escreva para o e-mail da Comissão. Havendo prazo correndo, abra também o chamado no Tribunal, que é a prova datada da falha. O botão abaixo monta o texto com os dados que a Comissão precisa para analisar e encaminhar o caso."')

    # capa, barra, rodapé e card
    t = rep(t, '  <header class="capa">\n    <div class="wrap">\n      <img class="marca-capa" src="${MARCAS.cddClaro}"\n           alt="${esc(D.meta.comissao)} — Ordem dos Advogados do Brasil, Subseção Marabá">',
            '  <div class="faixa-orgao"><div class="wrap"><span class="pill">${esc(D.meta.comissao)}</span><small>Ordem dos Advogados do Brasil, Seção do Pará</small></div></div>\n  <header class="capa">\n    <div class="wrap">\n      <span class="tag-guia">Guia de consulta</span>')
    t = rep(t, '<img class="selo" src="${MARCAS.escudoClaro}" alt="" aria-hidden="true">',
            '<img class="selo" src="${MARCAS.seccional}" alt="OAB Pará">')
    t = rep(t, '    <img class="selo-oab" src="${MARCAS.oab}" alt="OAB Pará">\n', '')
    t = rep(t, '        <img class="marca-rodape" src="${MARCAS.cddClaro}" alt="${esc(D.meta.comissao)}">\n        <img class="marca-rodape marca-rodape-oab" src="${MARCAS.oabClaro}" alt="OAB Pará">',
            '        <img class="marca-rodape" src="${MARCAS.seccional}" alt="OAB Pará">')
    t = rep(t, '      <p class="assina">${esc(D.meta.presidente)}</p>\n      <p style="margin:0">${esc(D.meta.inscricao)}<br>Presidente da ${esc(D.meta.comissao)}</p>\n',
            '      <p class="origem">${esc(D.meta.origem)}</p>\n')
    t = rep(t, '<img class="marca-card" src="${MARCAS.cdd}" alt="${esc(D.meta.comissao)} — OAB, Subseção Marabá">',
            '<img class="marca-card" src="${MARCAS.seccional}" alt="OAB Pará">')
    t = rep(t, "${esc(D.meta.comissao)} · ${esc(D.meta.orgao)} · ${esc(D.meta.presidente)}, ${esc(D.meta.inscricao)}, Presidente",
            "${esc(D.meta.comissao)} · ${esc(D.meta.orgao)}")
    t = rep(t, "${esc(D.meta.guia)} · ${esc(D.meta.comissao)} · OAB/PA · Subseção Marabá · atualizado em",
            "${esc(D.meta.guia)} · ${esc(D.meta.comissao)} · OAB/PA · atualizado em")
    t = rep(t, '      <a class="canal-zap" href="https://wa.me/${esc(D.meta.whatsappNum)}" target="_blank" rel="noopener">\n        ${ico(\'telefone\')} WhatsApp ${esc(D.meta.whatsapp)}\n      </a>\n',
            '      ${D.meta.whatsappNum ? `<a class="canal-zap" href="https://wa.me/${esc(D.meta.whatsappNum)}" target="_blank" rel="noopener">\n        ${ico(\'telefone\')} WhatsApp ${esc(D.meta.whatsapp)}\n      </a>` : \'\'}\n')

    # gerador de ocorrência: sem WhatsApp, cabeçalho da Comissão
    t = rep(t, "de modo que um preenchimento serve às duas finalidades. Havendo prazo correndo, envie pelo WhatsApp.`",
            "de modo que um preenchimento serve às duas finalidades. Envie pelo e-mail da Comissão.`")
    t = rep(t, "`COMISSÃO DE DIREITO DIGITAL — OAB/PA, SUBSEÇÃO MARABÁ`",
            "`COMISSÃO ESTADUAL DE APOIO INSTITUCIONAL AO PJE, OAB/PA`")
    t = rep(t, "const CHAVE = 'cdd.guia.pje.v3'", "const CHAVE = 'oabpa.guia.pje.v1'")
    t = rep(t, "precisa para escalar, e sai por WhatsApp.", "precisa para analisar o caso, e sai por e-mail.")
    t = rep(t, '<input id="g-oab" placeholder="35.865">', '<input id="g-oab" placeholder="00.000">')

    # travessões em texto visível
    for old, new, n in [
        ("protocolo — abra sempre", "protocolo: abra sempre", 1),
        ("mesmo usuário — o erro piora", "mesmo usuário, e o erro piora", 1),
        ("na ordem — seguir a ordem", "na ordem: seguir a ordem", 1),
        ("do sistema — a jurisprudência", "do sistema: a jurisprudência", 1),
        ("troque de navegador — muitos", "troque de navegador: muitos", 1),
        ("</b> — na sua máquina", "</b>: na sua máquina", 1),
        ("em jus.br — e não no PJe", "em jus.br, e não no PJe", 1),
        ("185/2013 — peticionamento", "185/2013: peticionamento", 1),
        ("455/2022 — intimação", "455/2022: intimação", 1),
        ("adquirido — e conte", "adquirido, e conte", 1),
        ("Você mesmo resolve — ", "Você mesmo resolve: ", 5),
        ("' — reconfira antes de usar'", "'. Reconfira antes de usar'", 1),
        ("art. 11 — indisponibilidade", "art. 11: indisponibilidade", 1),
        ('<i id="rot-trilha">—</i>', '<i id="rot-trilha">…</i>', 1),
        ("'Trocar de trilha — você está em: '", "'Trocar de trilha. Você está em: '", 1),
        ("contagem — agora são", "contagem. Agora são", 1),
        ("lista — agora são", "lista. Agora são", 1),
        ("${t.sistema} — ${t.sigla}", "${t.sistema} (${t.sigla})", 1),
        ("'[preencher]'} — Seccional", "'[preencher]'}, Seccional", 1),
        ("Registro de ocorrência — falha", "Registro de ocorrência: falha", 2),
        ("Nome completo — OAB/PA", "Nome completo, OAB/PA", 1),
        ("Envie assim mesmo — mas", "Envie assim mesmo, mas", 1),
        ("AINDA NÃO ABERTO — será", "AINDA NÃO ABERTO; será", 1),
        ("`— — —`", "`* * *`", 1),
        ("cada passo — e a primeira", "cada passo, e a primeira", 1),
        ("seu caso — em vez de", "seu caso, em vez de", 1),
        ("canal certo — e abrir", "canal certo, e abrir", 1),
    ]:
        t = rep(t, old, new, n)
    t = t.replace(" — ", ", ").replace("—", "-")  # restam só comentários de código
    return t


# ---------------------------------------------------------- Guia de Honorários
def guia_honorarios():
    t = (orig / "guia-honorarios.html").read_text(encoding="utf-8")
    t = trocar_fontes(t)
    t = tokens(t)
    t = css_final(t, CSS_HON)

    t = rep(t, "<title>Guia de Honorários | CDD OAB Marabá</title>", "<title>Guia de Honorários | OAB/PA</title>")
    t = rep(t, 'content="Guia de Honorários da Comissão de Direito Digital da OAB/PA, Subseção Marabá: nova Tabela',
            'content="Guia de Honorários da Ordem dos Advogados do Brasil, Seção do Pará (OAB/PA): nova Tabela')
    t = rep(t, "GUIA DE HONORÁRIOS · Comissão de Direito Digital · OAB/PA · Subseção Marabá",
            "GUIA DE HONORÁRIOS · Ordem dos Advogados do Brasil, Seção do Pará (OAB/PA)")

    t = rep(t, '"comissao": "Comissão de Direito Digital",', '"comissao": "Ordem dos Advogados do Brasil, Seção do Pará",')
    t = re.sub(r'\n\s*"presidente": "[^"]*",\n\s*"inscricao": "[^"]*",', "", t, count=1)
    t = rep(t, '"versao": "1.3",', '"versao": "1.0 (Seccional)",')
    t = rep(t, '"atualizado_em": "2026-10-19",', f'"atualizado_em": "{ATUALIZADO}",')
    t = rep(t, '"lede": "A nova Tabela de Honorários da OAB/PA na prática:',
            '"lede": "A nova Tabela de Honorários da Ordem dos Advogados do Brasil, Seção do Pará (OAB/PA), na prática:')
    t = re.sub(r'"workshop": "[^"]*",', '"workshop": "",', t, count=1)
    t = rep(t, '"email": "direitodigitaloabmaraba@gmail.com",', '"email": "",')
    t = re.sub(r'"Guia de Honorários · versão 1\.3 · 20/10/2026 · Comissão de Direito Digital da OAB/PA, Subseção Marabá\."',
               '"Guia de Honorários · versão 1.0 (Seccional) · 16/11/2026 · Ordem dos Advogados do Brasil, Seção do Pará (OAB/PA)."', t, count=1)
    if "versão 1.0 (Seccional) · 16/11/2026" not in t:
        raise SystemExit("ERRO: linha de versão das fontes não trocada")

    # capa, barra e rodapé
    t = rep(t, '  <section class="capa" id="topo">\n    <div class="wrap">\n      <img class="marca-capa" id="marca-capa" alt="">',
            '  <div class="faixa-orgao"><div class="wrap"><span class="pill">Ordem dos Advogados do Brasil, Seção do Pará</span></div></div>\n  <section class="capa" id="topo">\n    <div class="wrap">\n      <span class="tag-guia">Guia de consulta</span>')
    t = rep(t, '  <img class="selo-oab" id="selo-oab" alt="OAB Pará">\n', '')
    t = rep(t, '<img class="selo" id="selo" alt="" aria-hidden="true">', '<img class="selo" id="selo" alt="OAB Pará">')
    t = rep(t, '      <img class="marca-rodape" id="marca-rodape" alt="">\n      <img class="marca-rodape marca-rodape-oab" id="marca-rodape-oab" alt="OAB Pará">',
            '      <img class="marca-rodape" id="marca-rodape" alt="OAB Pará">')
    t = rep(t, '    <p id="contato"></p>\n    <p class="assina" id="assina"></p>\n    <p id="cargo"></p>\n', '')
    t = rep(t, '      <div class="nota" id="nota-workshop"></div>\n', '')

    t = rep(t, '$("selo").src = MARCAS.escudoClaro; $("selo-oab").src = MARCAS.oab;', '$("selo").src = MARCAS.seccional;')
    t = rep(t, '  $("marca-capa").src = MARCAS.cddClaro; $("marca-capa").alt = D.meta.comissao + ", OAB Subseção Marabá";\n', '')
    t = rep(t, '$("marca-rodape").src = MARCAS.cddClaro; $("marca-rodape").alt = D.meta.comissao;', '$("marca-rodape").src = MARCAS.seccional;')
    t = rep(t, '  $("marca-rodape-oab").src = MARCAS.oabClaro;\n', '')
    t = re.sub(r'  \$\("contato"\)\.innerHTML = [^\n]*\n', '', t, count=1)
    t = rep(t, '  $("assina").textContent = D.meta.presidente + " · " + D.meta.inscricao;\n', '')
    t = rep(t, '  $("cargo").textContent = "Presidente da " + D.meta.comissao + " da OAB/PA, Subseção Marabá";\n', '')
    t = rep(t, '  $("nota-workshop").innerHTML = D.meta.workshop;\n', '')
    t = rep(t, 'localStorage.setItem("cdd-honorarios-"+k, v)', 'localStorage.setItem("oabpa-honorarios-"+k, v)')
    t = rep(t, 'localStorage.getItem("cdd-honorarios-"+k)', 'localStorage.getItem("oabpa-honorarios-"+k)')
    if "—" in t:
        raise SystemExit("ERRO: travessão no Guia de Honorários")
    return t


saida.mkdir(parents=True, exist_ok=True)
for nome, fn in (("guia-pje_seccional_v1.html", guia_pje), ("guia-honorarios_seccional_v1.html", guia_honorarios)):
    html = fn()
    (saida / nome).write_text(html, encoding="utf-8", newline="\n")
    print(nome, len(html.encode("utf-8")), "bytes")
