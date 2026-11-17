# Parecer da direção de arte | Squad C | Balança digital

Data: 16/11/2026. Avaliei todas as PNGs da entrega do designer e a logo da CDD, que serve de referência negativa. Corrigi o que encontrei no próprio gerar.py e regerei todos os arquivos com os mesmos nomes.

## 1. Crítica da entrega recebida

| Ponto | Diagnóstico | Gravidade |
|---|---|---|
| Símbolo grande com respiro de 14% | Os quadrados soltos formavam um mosaico de LED. O travessão parecia uma linha pontilhada e as cordas pareciam pontos isolados. Esse é o "8 bits" que o próprio designer temia. Além disso, o símbolo grande e o favicon eram dois desenhos diferentes. | Alta |
| Peso do símbolo na horizontal | O símbolo tinha a altura do bloco inteiro, incluindo a faixa da OAB, e ficava com cerca de 580 px de largura contra 775 px de texto. O peso disputava com o "PJe". | Alta |
| Vazio à direita do "PJe" | A linha de apoio, esticada por textLength, era cerca de 130 px mais larga que o "PJe". O bloco não fechava como retângulo e o tracking ficou exagerado. | Média |
| Faixa da OAB | A marca tinha 96 px de altura, ficava pequena e solta no canto, e havia um vazio grande à esquerda dela, embaixo da régua. | Média |
| Alinhamento óptico | O recuo do P foi ajustado a olho. A OAB estava alinhada pela caixa do JPEG, não pela tinta, que tem recuo interno de 3,3% à direita. | Baixa |
| Contraste no marinho | O azul #008BD2 sobre o #003399 dá cerca de 3:1, e os pratos sumiam no avatar pequeno. O vermelho sobre o marinho dá cerca de 2:1. | Média |
| Leitura a 16 px | Está boa: um módulo por pixel, sem borrão. A silhueta em T, os dois pratos e o ponto vermelho se reconhecem. Não mexi nisso. | OK |
| CDD | Não há escudo, cadeado, circuito, bolinha nem régua bicolor, e o vermelho aparece num ponto só. Não lembra a CDD. | OK |
| Marca OAB | Não foi recolorida, distorcida nem recortada (proporção 347 x 202 preservada) e vai em placa branca no marinho. Está correto. | OK |

## 2. O que mudou

1. **Símbolo de desenho único em todos os tamanhos.** Os módulos agora se fundem também nas versões grandes, e o símbolo de 512 px é o próprio favicon ampliado. A leitura digital vem dos degraus (cordas, pratos, base) e do remate quadrado, sem depender das juntas. Cada cor vira um único `path`, então não aparecem emendas de antisserrilhado entre as linhas da grade. O resultado tem leitura de pictograma institucional, não de mosaico.
2. **A horizontal foi recomposta sobre a grade.** O módulo vale 1/11 da altura de versal do "PJe", e o resto se encaixa nele:
   - o travessão começa exatamente no topo do P;
   - o pé da balança pousa na linha de base do "PJe";
   - o remate vermelho ocupa a faixa da linha de apoio, com o topo alinhado à versal dela;
   - o espaço entre o símbolo e o texto mede 2 módulos e a margem de proteção mede 3 módulos.
3. **O bloco de texto agora fecha como retângulo.** O "PJe" passou para 400 e a linha de apoio para 24, com tracking de cerca de 0,11 em. A tinta da linha de apoio tem a mesma largura da tinta do "PJe", medida no Edge: as duas vão de x = 677 a 1503 na PNG. Assim, o vazio à direita do "PJe" desapareceu.
4. **A régua e a OAB ficam na mesma faixa.** A régua azul, de uma cor só, parte do pé do símbolo e corre até a marca OAB, que assina à direita. A régua passa pelo centro do selo, e a tinta da marca alinha com o "e" (x = 1503). A marca cresceu de 96 para cerca de 140 px de altura. O vazio sob a régua deixou de existir, e a régua corrida sob o conjunto inteiro, terminando no selo, se afasta ainda mais da régua bicolor da CDD.
5. **Versão marinho.** A estrutura e os pratos ficam em branco, e o vermelho vai só no remate, apoiado sobre o branco do travessão, que o recorta. A placa da OAB tem a mesma altura da tinta da marca na versão clara, então as duas horizontais têm o mesmo formato (1600 x 807) e se trocam sem ajuste.
6. **Avatar.** A tinta do "PJe" tem exatamente a largura do degrau inferior da base, que mede 10 módulos, e começa no mesmo x. O conjunto fica centrado, com 166 px livres em cima e embaixo, e cabe no recorte circular das redes.
7. **Prancha.** Ganhou o avatar no recorte circular, em 160 e em 40 px. Os textos da faixa inferior foram quebrados em duas linhas.
8. **MEMORIAL.md** foi atualizado na construção, nas cores e nos tamanhos. O conceito continua igual, com 123 palavras.

## 3. Riscos que ainda existem (para o júri saber)

- A estética de pixel continua sendo uma escolha: quem associa pixel a jogo pode resistir. Com o desenho fundido e as proporções clássicas, o risco caiu bastante.
- O vermelho sobre o marinho continua com contraste baixo nas bordas laterais do remate. A leitura se sustenta porque ele se apoia no branco.
- As métricas do Barlow foram medidas no Edge. A linha de apoio fica presa por textLength, mas o "PJe" pode variar 1 ou 2 px em outro renderizador. Para a arte-final, recomendo converter os textos em curvas.
- Abaixo de cerca de 400 px de largura, a linha de apoio da horizontal fica ilegível, o que é normal para um nome desse tamanho. Nesses usos vale o avatar ou o símbolo.

## 4. Verificação

Conferi visualmente todas as PNGs depois de gerá-las de novo: simbolo, logo_horizontal, logo_horizontal_marinho, avatar, favicon_32, favicon_16 e prancha. Medi os alinhamentos pela tinta, decodificando as PNGs. Nada ficou cortado e não há travessão em nenhum arquivo. Para regerar tudo: `python -I squad-C_balanca/gerar.py final`, a partir de competicao_v1.
