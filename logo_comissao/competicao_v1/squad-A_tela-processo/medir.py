"""Mede metricas reais da Barlow (avanco e tinta) no Edge headless e grava metricas.json.

Uso (a partir de competicao_v1):  python -I squad-A_tela-processo/medir.py
Le _kit/barlow_fontface.css (sem exibi-lo) e mede com canvas.measureText a 1000 px.
"""
import json
import pathlib
import subprocess
import tempfile
import html as H

AQUI = pathlib.Path(__file__).resolve().parent
KIT = AQUI.parent / "_kit"
FONTE = (KIT / "barlow_fontface.css").read_text(encoding="utf-8")

AMOSTRAS = [
    ("800", "P"), ("800", "J"), ("800", "e"), ("800", "PJ"), ("800", "Je"), ("800", "PJe"),
    ("600", "COMISSÃO ESTADUAL DE APOIO"), ("600", "INSTITUCIONAL AO"),
    ("600", "COMISSÃO ESTADUAL DE APOIO INSTITUCIONAL AO"), ("600", "H"), ("800", "H"),
]

js = """
(async () => {
  const am = %s;
  for (const w of ['600','800']) await document.fonts.load(w + ' 1000px Barlow');
  const ctx = document.createElement('canvas').getContext('2d');
  const out = {};
  for (const [w, t] of am) {
    ctx.font = w + ' 1000px Barlow';
    const m = ctx.measureText(t);
    out[w + '|' + t] = {adv: m.width, l: m.actualBoundingBoxLeft, r: m.actualBoundingBoxRight,
                        asc: m.actualBoundingBoxAscent, desc: m.actualBoundingBoxDescent, n: [...t].length};
  }
  out.familia = document.fonts.check('800 20px Barlow');
  document.getElementById('o').textContent = JSON.stringify(out);
})();
""" % json.dumps(AMOSTRAS)

doc = f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONTE}</style></head>
<body><pre id="o">x</pre><script>{js}</script></body></html>"""
tmp = pathlib.Path(tempfile.mkdtemp()) / "m.html"
tmp.write_text(doc, encoding="utf-8")
edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
r = subprocess.run([edge, "--headless=new", "--disable-gpu", "--virtual-time-budget=5000", "--dump-dom", tmp.as_uri()],
                   capture_output=True, text=True, encoding="utf-8", timeout=90)
txt = r.stdout.split('<pre id="o">', 1)[1].split("</pre>", 1)[0]
dados = json.loads(H.unescape(txt))
(AQUI / "metricas.json").write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(dados, ensure_ascii=False, indent=1))
