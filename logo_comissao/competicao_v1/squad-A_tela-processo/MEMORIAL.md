# Memorial descritivo: Squad A, "Folha que atende"

## Conceito
O símbolo junta três ideias numa única forma: a **folha do processo eletrônico** (o quadrado com a dobra no canto), o **balão de atendimento** (a cauda que desce à esquerda) e o **selo de resolvido** (o check vazado no corpo da folha). É o processo que chega com dúvida e sai atendido. Lida como silhueta, a forma lembra um **P**, inicial de PJe e de processo, sem precisar desenhar a letra. Não há monitor, teclado nem ícone de sistema: a "tela" é a própria folha digital, chapada e quadrada como uma janela. O tom é de serviço público: firme, direto, sem enfeite.

## Construção
- Grade de 512 com módulo de 32 (1 módulo = 1 px no favicon de 16).
- Corpo: quadrado de 10 x 10 módulos, cantos externos com raio de 36.
- Dobra: triângulo a 45 graus com cateto de 3 módulos, em azul, separada do corpo por respiro em L de 20 unidades.
- Cauda: triângulo a 45 graus com cateto de 4 módulos, no canto oposto ao da dobra (as duas diagonais são paralelas, o que dá unidade à forma).
- Check: traço de 42 com pontas arredondadas, recortado (máscara), portanto transparente em qualquer fundo; a ponta longa aponta para a dobra e para antes do respiro.
- Logo horizontal (1600 x 990): bloco compacto. Linha de apoio em Barlow 600, caixa alta, em duas linhas ("COMISSÃO ESTADUAL DE APOIO" / "INSTITUCIONAL AO"), com espacejamento calculado (0,109 em) para que a primeira linha tenha exatamente a largura de "PJe"; "PJe" em Barlow 800 com espacejamento óptico por letra (P|J fechado em 0,04 em); régua de cor única com a ponta direita cortada a 45 graus, eco da dobra e da cauda; marca OAB Pará alinhada à haste do P, sem alteração (em fundo marinho, sobre placa branca de cantos arredondados, e a régua passa a branca). A base do corpo do símbolo coincide com a base da régua, e a cauda ocupa a faixa da marca OAB. Métricas da fonte medidas por `medir.py` (`metricas.json`). Largura mínima em tela: 400 px; abaixo disso, usar o símbolo ou o avatar.

## Cores
Marinho #003399 (corpo, textos), azul #008BD2 (dobra e régua), branco (check e fundo). Duas cores no símbolo; o vermelho #D2091E fica reservado à marca OAB, que já o contém. Régua azul no fundo branco e branca no fundo marinho (o azul sobre o marinho tem contraste de cerca de 2,9:1).

## Por que funciona pequeno
A silhueta é uma massa única, sem linhas finas nem texto interno. O favicon de 16 px é pixel art exata (`favicon_16.svg`, sem antisserrilhado): check com traços de 2 px a 45 graus, separado do recorte da dobra por uma linha cheia de corpo, dobra de 3 px com respiro de 1 px e cauda de 3 px. O de 32 px usa `favicon.svg`, desenhado na grade de 16. Manter dois arquivos para 16 e 32 px é a prática usual de ícones com ajuste por tamanho.

## Por que não lembra a CDD
A hierarquia do nome (linha de apoio, destaque, régua, OAB) é a mesma por exigência do briefing; por isso a régua foi diferenciada: tem a largura de "PJe", não de um título longo, cor única e ponta cortada a 45 graus. Não há escudo, cadeado, trilhas de circuito nem terminais em bolinha. A forma é retangular e aberta (folha e balão), não um brasão fechado. A régua é de cor única (azul), não bicolor azul e vermelho. A paleta do símbolo não usa vermelho, ao contrário da metade vermelha do escudo da CDD.

## Arquivos
`simbolo.svg/png`, `logo_horizontal.svg/png`, `logo_horizontal_marinho.svg/png`, `avatar.svg/png`, `favicon.svg`, `favicon_16.svg`, `favicon_32.png`, `favicon_16.png`, `prancha.png`. Os SVGs sem texto (símbolo e favicons) não levam a Barlow: não usam fonte e continuam autocontidos; embutir 144 KB de fonte num favicon seria erro técnico. Tudo é gerado por `gerar.py` (`python -I squad-A_tela-processo/gerar.py final`); rascunhos em `rascunhos/` (`python -I squad-A_tela-processo/gerar.py rascunhos`).
