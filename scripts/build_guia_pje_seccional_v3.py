"""Guia Prático do PJe, versão Seccional v3 (1.2): atualiza a referência à Resolução CNJ nº 185/2013
sobre a v2 (guia-pje_seccional_v2.html), sem alterar a v2.

Mudança (18/11/2026): a Resolução CNJ nº 703/2026 (DJe/CNJ de 12/11/2026) é agora a última alteração da
Resolução CNJ nº 185/2013. Ela inclui os §§ 5º e 6º no art. 4º (assinatura eletrônica avançada gov.br) e
não mexe nos arts. 8º a 12, de modo que as citações do guia aos arts. 4º, § 2º, 9º e 11 continuam corretas.
Conferido em https://atos.cnj.jus.br/atos/detalhar/1933 e no compilado oficial do CNJ.

Uso (na pasta GUIAS SECCIONAL OAB-PA):
  python -I scripts/build_guia_pje_seccional_v3.py guia-pje_seccional_v2.html guia-pje_seccional_v3.html
"""
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8")
entrada, saida = map(pathlib.Path, sys.argv[1:3])
if saida.exists():
    raise SystemExit(f"ERRO: {saida} já existe; não sobrescrevo.")


def rep(t, old, new, n=1):
    c = t.count(old)
    if c != n:
        raise SystemExit(f"ERRO: esperado {n} ocorrência(s), achei {c}: {old[:90]!r}")
    return t.replace(old, new)


t = entrada.read_text(encoding="utf-8")

t = rep(t, "Texto vigente com as alterações posteriores, a última pela Resolução CNJ nº 656/2025.",
        "Texto vigente com as alterações posteriores, a última pela Resolução CNJ nº 703/2026.")
t = rep(t, "com as alterações das Resoluções nº 569/2024, 624/2025 e 656/2025.",
        "com as alterações das Resoluções nº 569/2024, 624/2025, 656/2025 e 703/2026 (esta conferida em "
        "18 de novembro de 2026).")
t = rep(t, '"versao": "1.1 (Seccional)",', '"versao": "1.2 (Seccional)",')
t = rep(t, '"atualizado_em": "2026-11-16"', '"atualizado_em": "2026-11-18"')

for proibido in ("—", "–"):
    if proibido in t and proibido not in entrada.read_text(encoding="utf-8"):
        raise SystemExit("ERRO: travessão novo no texto.")

saida.write_text(t, encoding="utf-8")
print(f"OK: {saida} ({saida.stat().st_size} bytes)")
