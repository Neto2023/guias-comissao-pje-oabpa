"""Renderiza um SVG em PNG com o Edge headless.
Uso: python -I render.py entrada.svg saida.png LARGURA ALTURA [cor_fundo]
O SVG e esticado para LARGURAxALTURA (mantendo proporcao). Fundo padrao: transparente -> branco.
"""
import sys, pathlib, subprocess, tempfile, os
svg, png, w, h = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
bg = sys.argv[5] if len(sys.argv) > 5 else "#FFFFFF"
svg_txt = pathlib.Path(svg).read_text(encoding="utf-8")
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;padding:0;background:{bg};width:{w}px;height:{h}px;overflow:hidden}}
.c{{width:{w}px;height:{h}px;display:flex;align-items:center;justify-content:center}}.c svg{{width:100%;height:100%;display:block}}</style></head>
<body><div class="c">{svg_txt}</div></body></html>"""
tmp = pathlib.Path(tempfile.mkdtemp()) / "r.html"
tmp.write_text(html, encoding="utf-8")
edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
out = str(pathlib.Path(png).resolve())
subprocess.run([edge, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                f"--window-size={w},{h}", f"--screenshot={out}", "--virtual-time-budget=3000", tmp.as_uri()],
               check=True, capture_output=True, timeout=90)
print("ok", out, os.path.getsize(out))
