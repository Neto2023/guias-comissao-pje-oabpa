# Briefing: logo da Comissão Estadual de Apoio Institucional ao PJe (OAB/PA)

## Cliente
Comissão Estadual de Apoio Institucional ao Processo Judicial Eletrônico (PJe) da Ordem dos Advogados do Brasil, Seção do Pará (OAB/PA). A Comissão apoia a advocacia paraense no uso do PJe: primeiro acesso, certificado digital, falhas de sistema, interlocução com os tribunais. Tom: institucional, confiável, de serviço; moderno sem ser "startup".

## Hierarquia do nome (decidida)
- Linha de apoio, menor, em caixa alta espaçada: "COMISSÃO ESTADUAL DE APOIO INSTITUCIONAL AO"
- Destaque, grande: "PJe" (sempre com P e J maiúsculos e "e" minúsculo; é a grafia oficial do sistema)
- Abaixo, uma régua e a marca OAB Pará (arquivo fornecido), que identifica a Seccional.

## Identidade obrigatória (mesma do Painel de Jurimetria e dos guias)
- Marinho #003399 (texto principal), azul #008BD2, vermelho #D2091E, texto #1B1B1B, fundo branco.
- Tipografia: Barlow (pesos 400 a 800). Nenhuma outra fonte.
- Marca OAB Pará: `_kit/oab_para.jpeg` (JPEG com fundo branco, 349 px de largura). Usar SEM recolorir, distorcer, recortar ou redesenhar. Em fundo marinho, ela vai sobre uma placa branca com cantos arredondados.

## Restrições
- Não pode lembrar a logo da Comissão de Direito Digital (CDD) da Subseção Marabá: escudo, cadeado, trilhas de circuito com terminais em bolinha, régua bicolor azul|vermelho exatamente embaixo do título. A regra interna separa o material da CDD do material da Comissão do PJe.
- Nada de travessão (—) em nenhum texto.
- Símbolo legível a 16 px (favicon) e a 32 px.
- Sem gradientes complexos, sombras ou efeitos 3D; vetor chapado, no máximo 3 cores do símbolo.
- Não usar brasão da República, balança copiada de banco de imagens nem a logo oficial do PJe/CNJ.

## Entregáveis de cada squad (na pasta do squad)
Todos em SVG autocontido (fonte Barlow embutida via `_kit/barlow_fontface.css` dentro de `<style>`, e a marca OAB via `_kit/oab_para_datauri.txt` em `<image href="...">`), e cada um renderizado em PNG com `_kit/render.py`:
1. `simbolo.svg` / `simbolo.png` (512x512)
2. `logo_horizontal.svg` / `.png` (1600 de largura, fundo branco)
3. `logo_horizontal_marinho.svg` / `.png` (fundo #003399, texto branco, OAB em placa branca)
4. `avatar.svg` / `.png` (1080x1080, para redes sociais; só símbolo, ou símbolo + "PJe")
5. `favicon.svg` + `favicon_32.png` e `favicon_16.png`
6. `prancha.png`: uma imagem só com todas as versões lado a lado, para o júri
7. `MEMORIAL.md`: conceito em até 150 palavras, construção, cores, por que funciona pequeno, por que não lembra a CDD.

Render: `python -I _kit/render.py entrada.svg saida.png LARGURA ALTURA [cor_fundo]` (rode a partir de `competicao_v1`).
