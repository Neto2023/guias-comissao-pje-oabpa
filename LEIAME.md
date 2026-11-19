# Guias na identidade da Seccional (OAB/PA)

Versão 1, gerada em 16/11/2026, para levar ao aval da Seccional. Nada foi publicado. Os guias da Comissão de Direito Digital (CDD) da Subseção Marabá continuam no ar sem alteração.

## Arquivos

| Arquivo | O que é |
|---|---|
| `guia-pje_seccional_v1.html` | Guia Prático do PJe, assinado pela Comissão Estadual de Apoio Institucional ao PJe |
| `guia-honorarios_seccional_v1.html` | Guia de Honorários, na identidade da Ordem dos Advogados do Brasil, Seção do Pará (OAB/PA) |
| `amostras/amostras_layout_v1.html` | Amostras A e B do layout (escolhida: A) |
| `_referencia_originais_CDD/` | Cópia dos originais publicados pela CDD, sem alteração |
| `scripts/build_guias_seccional_v1.py` | Gera as duas versões a partir dos originais (reproduzível) |

Para gerar de novo:

```
python -I scripts/build_guias_seccional_v1.py _referencia_originais_CDD scripts/assets/oab_para_painel_comissao.jpeg scripts/assets/fontes_barlow .
```

## Decisões (16/11/2026)

1. Layout: Opção A, a mesma moldura do Painel de Jurimetria da Comissão. Inclui faixa azul, barra branca com a marca da OAB Pará, capa branca com sublinhado vermelho e rodapé marinho. Fonte Barlow embutida, fundo branco.
2. Guia do PJe: assinatura da Comissão Estadual de Apoio Institucional ao PJe, com nota de origem no rodapé ("1ª edição: Guia CDD 001/2026"). O canal de ajuda é o e-mail apoio_pje@oabpa.org.br, e o WhatsApp da CDD foi retirado.
3. Guia de Honorários: identidade da OAB/PA, sem comissão. O workshop de novembro e o contato da CDD foram retirados. O grupo Crimes Cibernéticos ficou como estava (valores da proposta CDD com selo, até a errata).

## Versão 2 do Guia do PJe (16/11/2026)

`guia-pje_seccional_v2.html` (versão 1.1) é a v1 com a logo oficial da Comissão, que está em `logo_comissao/OFICIAL/`. A logo aparece na capa, no rodapé e no cartão, e o "PJe" virou o ícone da aba. A barra superior continua com a marca OAB Pará. Para gerar de novo:

```
python -I scripts/build_guia_pje_seccional_v2.py guia-pje_seccional_v1.html logo_comissao/OFICIAL guia-pje_seccional_v2.html
```

## Versão 3 do Guia do PJe (18/11/2026)

`guia-pje_seccional_v3.html` (versão 1.2) é a v2 com a referência à Resolução CNJ nº 185/2013 atualizada. A última alteração dela agora é a Resolução CNJ nº 703/2026 (DJe/CNJ de 12/11/2026), que inclui os §§ 5º e 6º no art. 4º (assinatura eletrônica avançada gov.br). Ela não mexe nos arts. 8º a 12, então as citações do guia aos arts. 4º, § 2º, 9º e 11 continuam corretas. Mudaram só a nota do quadro "B · Resolução CNJ nº 185/2013", a lista de fontes, a versão e a data. Conferido em https://atos.cnj.jus.br/atos/detalhar/1933. Para gerar de novo:

```
python -I scripts/build_guia_pje_seccional_v3.py guia-pje_seccional_v2.html guia-pje_seccional_v3.html
```

## Versão 2 do Guia de Honorários (16/11/2026)

`guia-honorarios_seccional_v2.html` (versão 1.1) passa a sair pela Comissão Estadual de Apoio Institucional ao PJe, como o Guia do PJe. A logo da Comissão aparece na capa e no rodapé, o nome dela está na faixa azul e o "PJe" é o ícone da aba. O conteúdo não mudou, inclusive o grupo Crimes Cibernéticos. Para gerar de novo:

```
python -I scripts/build_guia_honorarios_seccional_v2.py guia-honorarios_seccional_v1.html logo_comissao/OFICIAL guia-honorarios_seccional_v2.html
```

## Pontos para o aval da Seccional

- Nenhum dos dois guias traz assinatura pessoal. Se a Seccional quiser, dá para incluir o nome de quem preside a Comissão (PJe) ou outro responsável.
- O Guia de Honorários ficou sem contato. Falta indicar se haverá algum, e qual.
- O Guia do PJe tem conteúdo conferido em agosto de 2026 (fontes de 31/07 e 13/08). Vale reconferir os contatos dos tribunais antes da divulgação.
- O texto da seção de Direito Digital do Guia de Honorários ainda credita a elaboração à CDD da Subseção Marabá, o que é um dado factual da Tabela.
