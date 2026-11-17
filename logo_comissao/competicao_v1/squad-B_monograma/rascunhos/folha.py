"""Folha de comparacao dos rascunhos (256 + 32 e 16 ampliados 4x e em tamanho real)."""
import pathlib, base64, subprocess, sys
AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parent.parent
nomes = sorted({p.stem.rsplit("_", 1)[0] for p in AQUI.glob("*_256.png")})
def uri(p): return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()
lin = []
for i, n in enumerate(nomes):
    y = 20 + i * 290
    lin.append(f'<text x="20" y="{y+14}" font-size="16" font-family="sans-serif">{n}</text>')
    lin.append(f'<image x="20" y="{y+24}" width="256" height="256" href="{uri(AQUI/(n+"_256.png"))}"/>')
    lin.append(f'<image x="300" y="{y+24}" width="128" height="128" style="image-rendering:pixelated" href="{uri(AQUI/(n+"_32.png"))}"/>')
    lin.append(f'<image x="450" y="{y+24}" width="128" height="128" style="image-rendering:pixelated" href="{uri(AQUI/(n+"_16.png"))}"/>')
    lin.append(f'<image x="300" y="{y+170}" width="32" height="32" href="{uri(AQUI/(n+"_32.png"))}"/>')
    lin.append(f'<image x="350" y="{y+170}" width="16" height="16" href="{uri(AQUI/(n+"_16.png"))}"/>')
H = 20 + len(nomes) * 290
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 {H}">{"".join(lin)}</svg>'
(AQUI / "folha.svg").write_text(svg, encoding="utf-8")
subprocess.run([sys.executable, "-I", str(RAIZ/"_kit/render.py"), str(AQUI/"folha.svg"), str(AQUI/"folha.png"), "600", str(H)], check=True, cwd=RAIZ)
