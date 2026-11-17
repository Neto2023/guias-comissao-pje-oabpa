# Memorial descritivo | Squad C | Balança digital

## Conceito
A balança da Justiça é o sinal mais antigo do Direito; o pixel é a unidade mínima da tela onde o processo hoje tramita. O símbolo une os dois: uma balança clássica, de pratos suspensos por cordas em V, desenhada inteiramente sobre uma grade de 16 x 16 módulos quadrados. Quem olha reconhece primeiro a Justiça e só depois percebe que ela é feita de pixels, que é exatamente a missão da Comissão: levar a advocacia, com segurança e sem ruptura, do papel para o PJe. O módulo vermelho no topo é o ponto de dado, o cursor ativo: a Comissão como o ponto onde o processo eletrônico encontra o advogado. Leitura tradicional, desenho contemporâneo, tom de serviço público, sem estética de startup.

## Construção
- Grade de 16 x 16 módulos; o desenho ocupa as 16 colunas e as linhas 1 a 13.
- Coluna com 2 módulos de largura; travessão com 1 módulo; pratos em tigela (5 + 3 módulos) presos por cordas diagonais em V; base em dois degraus (6 e 10 módulos); remate vermelho de 2 x 2 módulos.
- Os módulos se fundem em todos os tamanhos: o símbolo de 512 px é exatamente o mesmo desenho do favicon, ampliado. A grade aparece nos degraus das cordas, dos pratos e da base, não em juntas entre quadrados (revisão da direção de arte; ver PARECER_DIRECAO.md).
- Logo horizontal: o módulo da grade vale 1/11 da altura de versal do "PJe". O travessão alinha com o topo do P, o pé da balança pousa na linha de base do "PJe" e o remate vermelho ocupa a faixa da linha de apoio. A linha de apoio (Barlow 600, caixa alta espaçada) tem exatamente a largura de tinta do "PJe" (Barlow 800, grafia oficial). Abaixo, a régua de uma cor parte do pé do símbolo e corre até a marca OAB Pará, que assina à direita, alinhada pela tinta com o "e", sem recorte nem recoloração. Na versão marinho, a marca OAB vai sobre placa branca de cantos arredondados, com a mesma altura.

## Cores
- Marinho #003399: coluna, travessão, base e textos.
- Azul #008BD2: pratos e cordas (o que se pesa) e a régua.
- Vermelho #D2091E: apenas o remate 2 x 2, o ponto de dado.
- Fundo marinho: estrutura e pratos em branco, remate vermelho apoiado sobre o branco do travessão (o azul sobre o marinho ficava sem contraste). Três cores no símbolo, chapadas, sem gradiente, sombra ou 3D.

## Por que funciona pequeno
O símbolo foi desenhado na própria resolução do favicon: em 16 px cada módulo é exatamente um pixel, então não há antisserrilhado, borrão nem traço que some. Em 32 px cada módulo vira 2 x 2 pixels, igualmente nítido. A silhueta (T com dois pratos e base) é reconhecível mesmo sem distinguir as cordas, e o ponto vermelho no topo marca a orientação.

## Por que não lembra a CDD
- Não há escudo, cadeado nem moldura fechada: a forma é aberta e simétrica.
- Não há trilhas de circuito nem terminais em bolinha: a linguagem digital vem só de módulos quadrados numa grade.
- A régua sob o título é de uma cor só (azul no fundo branco, branca no marinho), nunca bicolor azul | vermelho.
- O vermelho não divide o símbolo em metades: aparece num único ponto, no eixo central.
- A balança é desenho próprio sobre grade, não imagem de banco; não usa brasão nem a logo oficial do PJe/CNJ.

## Arquivos
simbolo.svg/.png (512), logo_horizontal.svg/.png (1600 x 807), logo_horizontal_marinho.svg/.png (1600 x 807), avatar.svg/.png (1080; a tinta do "PJe" tem a largura do degrau inferior da base), favicon.svg, favicon_32.png, favicon_16.png, prancha.png. Tudo gerado por gerar.py (python -I squad-C_balanca/gerar.py final, a partir de competicao_v1). Rascunhos em rascunhos/.
