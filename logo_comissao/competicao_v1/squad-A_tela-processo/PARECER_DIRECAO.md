# Parecer da direção de arte: Squad A, "Folha que atende"

Data: 16/11/2026. Peças avaliadas: prancha, símbolo, favicons de 16 e 32 px, logo horizontal (branco e marinho) e avatar.

## Veredito
O símbolo é a parte mais forte da proposta. Ele é uma forma própria, construída em grade, e junta folha com dobra, balão e check. A silhueta em "P" é um achado. Os problemas estavam na composição da logo horizontal e no favicon de 16 px. Os dois foram corrigidos. O símbolo não foi alterado.

## Crítica e decisões

| Ponto | Diagnóstico | Decisão |
|---|---|---|
| Equilíbrio da horizontal | A linha de apoio numa linha só ocupava 973 px, e "PJe" ocupava 417 px. Sobrava um vazio de cerca de 550 px à direita, e o peso caía para a esquerda. | A logo virou um bloco compacto. A linha de apoio foi quebrada em duas ("COMISSÃO ESTADUAL DE APOIO" / "INSTITUCIONAL AO"). O espacejamento (0,109 em) é calculado para a primeira linha ter a mesma largura de "PJe", e a régua também. O vazio acabou, e "PJe" ficou 15% maior em relação ao conjunto. |
| Peso e escala | Na versão antiga, a altura de versal da linha de apoio era 1,7% da largura da logo. | Na nova, é 2,2%. Proporcionalmente, a linha de apoio ficou maior, mesmo com corpo menor. |
| Alinhamento e grade | O símbolo tinha a altura do bloco, mas nenhuma linha interna coincidia. | A base do corpo do símbolo agora coincide com a base da régua, e a cauda ocupa a faixa da marca OAB. O topo do símbolo continua na altura de versal da linha de apoio. As bordas de tinta da linha de apoio, da haste do P, da régua e da marca OAB estão alinhadas por métrica medida, e não a olho. |
| Kerning de "PJe" | O letter-spacing uniforme de -4 deixava o vão P\|J aberto (o gancho do J cria um buraco sob o bojo do P) e o vão J\|e mais fechado. | "PJe" agora tem posição absoluta por letra: kerning da fonte, P\|J fechado em 0,04 em e J\|e em 0,012 em. As métricas reais da Barlow foram medidas no Edge por `medir.py` e estão em `metricas.json`. |
| Régua no marinho | O azul #008BD2 sobre o #003399 tem contraste de cerca de 2,9:1, abaixo de 3:1. | No marinho, a régua passou a branca. No branco, continua azul. |
| Semelhança com a CDD | O esqueleto da logo é o da CDD (apoio, destaque, régua e OAB), mas isso é imposto pelo briefing. O risco estava na régua corrida por baixo de tudo. | A régua é de cor única, tem só a largura de "PJe" e ganhou a ponta direita cortada a 45 graus, eco da dobra e da cauda. Não há escudo, cadeado, circuito nem bicolor. O risco é baixo. |
| Favicon de 16 px | O check tinha 1 px, estava quebrado em degraus e encostava no recorte da dobra. | Refeito como pixel art exata (`FAV16` no gerar.py, com crispEdges e sem antisserrilhado). O check tem traços de 2 px a 45 graus, braços de 2 e 3 linhas e uma linha cheia de corpo que o separa do recorte. A dobra tem 3 px, com respiro de 1 px. Conferido a 24x: lê como folha com check. |
| Favicon de 32 px | Bom. O check tem 4 px e a dobra é legível. | Mantido. |
| Avatar | "PJe" com espacejamento uniforme e sem relação de largura com o símbolo. | "PJe" agora usa o mesmo espacejamento óptico da logo e tem a largura exata do corpo do símbolo. O conteúdo cabe no recorte em círculo. |
| Prancha | A prancha mostrava os tamanhos de 24, 48 e 96 px a partir de um PNG reduzido e não tinha teste de redução da logo. | Os tamanhos pequenos passaram a ser renderizados em vetor no tamanho real. Foi incluída uma faixa de redução (400, 300 e 200 px, e o marinho a 400), com a largura mínima indicada. |
| Marca OAB Pará | Usada sem recolorir nem distorcer (proporção 347 x 202, conferida no cabeçalho do JPEG). No marinho, fica sobre placa branca de cantos arredondados. | Mantida. A borda da placa se alinha à haste do P. |
| Fonte nos SVGs sem texto | `simbolo.svg` e os favicons não levam Barlow. | Mantido e justificado no memorial. Esses arquivos não usam fonte e são autocontidos. Embutir 144 KB num favicon seria erro técnico. |

## Pontos que continuam em aberto (para o júri saber)
1. **Linha de apoio em tamanhos pequenos.** Abaixo de 400 px de largura, a linha de apoio fica pequena demais para ler. A largura mínima em tela foi fixada em 400 px. Abaixo disso, usar o símbolo ou o avatar.
2. **Parentesco com ícones genéricos.** Isolada, a cauda de balão lembra ícones de chat. A forma combinada (folha, balão, check e silhueta em P) é própria.
3. **Dobra no fundo marinho.** No avatar e no marinho, a dobra azul tem contraste moderado. Ela é acento, e não portadora de leitura: a forma se sustenta só com a silhueta branca.
4. **Dois arquivos de favicon.** Há dois arquivos-fonte, um para 16 e outro para 32 px. É a prática usual de ícone com ajuste por tamanho, mas exige manter os dois sincronizados.

## Arquivos alterados
`gerar.py` (novos: `lockup`, `pje`, `linha_apoio`, `regua`, `FAV16`; prancha refeita), `medir.py` (novo), `metricas.json` (novo) e `MEMORIAL.md`. Todos os entregáveis foram regerados com os mesmos nomes. `logo_horizontal*.png` passou de 1600 x 620 para 1600 x 990, porque o bloco compacto é mais alto (o briefing fixa só a largura).
