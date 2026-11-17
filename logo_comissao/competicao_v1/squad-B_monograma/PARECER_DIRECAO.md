# Parecer da direção de arte: Squad B, Monograma PJe

Revisão v2, 16/11/2026. As PNGs anteriores à revisão não foram mantidas na pasta. Todos os arquivos foram regerados por `gerar.py`, com os mesmos nomes.

## 1. Crítica da versão entregue (v1)

| Ponto | Diagnóstico | Gravidade |
|---|---|---|
| Barra do e | A barra vermelha ia até a borda externa do anel, mas o braço superior do e terminava no meio dela. Metade da barra ficava solta na abertura e virava uma "língua" pendurada. Em fundo marinho o vermelho ficava cercado de marinho quase por inteiro. | Alta |
| Leitura do e em 16 e 32 px | Como o vermelho tem só cerca de 2:1 de contraste de luminosidade com o marinho, o e dependia da cor. Quando a barra sumia, ele virava um c. No favicon de 16 px a barra tinha 3x1 px. | Alta |
| Favicon de 32 px | O desenho de 30m em módulo de 1 px deixava as letras a 1 px da borda da placa: ficava apertado e sem respiro. | Média |
| Favicon de 16 px | O vão do P tinha 1x2 px, então o P quase fechava. O e era lido como c. | Média |
| Compensação óptica | O gancho do J e o e terminavam exatamente na linha de base e na altura do e. Ao lado da haste reta do P, as curvas pareciam menores e "flutuando". | Baixa |
| Linha de apoio | O espacejamento era excessivo (textLength de 1240 px): as letras se soltavam e o espaço entre palavras quase não se distinguia do espaço entre letras. O cinza #1B1B1B criava uma terceira cor no conjunto. | Média |
| Proporção da assinatura | O PJe (660 px) ficava estreito sob a linha de apoio e a régua de 1240 px. O bloco parecia um título pequeno embaixo de uma faixa larga. | Média |
| Respiro vertical | Os intervalos não eram iguais (58, 62 e 58 px, mais um ajuste manual de 12 px no marinho). | Baixa |
| Prancha | O simbolo.png tem fundo branco fora dos cantos arredondados, e os cantos brancos apareciam sobre o cinza da prancha. Os favicons ampliados também tinham cantos brancos. | Baixa |
| Fresta entre o bojo do P e a haste do J | O canal de 2m é estreito, mas sustenta a ligadura e não fecha em nenhum tamanho. | Mantido |
| Marca OAB Pará | Proporção conferida no JPEG (347x202 px), sem recolorir, distorcer ou recortar. A placa branca no marinho está correta. | Conforme |
| Semelhança com a CDD | Não há escudo, cadeado, circuito, bolinhas ou régua bicolor. A régua é monocromática e o símbolo é tipográfico. A ordem apoio, título, régua e OAB vem do briefing e não da CDD. | Conforme |

## 2. O que mudou (v2)

1. **O e foi redesenhado como forma fechada.** O braço direito do anel desce até a base da barra, com corte horizontal. A barra vermelha fica presa entre os dois lados do anel, com branco nas duas pontas na versão invertida. Assim o e se lê pela forma (contraforma em cima e abertura embaixo) mesmo quando o vermelho perde força, e a barra deixou de parecer peça solta. O anel é desenhado como um único caminho preenchido, por cima da barra, sem frestas de suavização.
2. **Compensação óptica.** O gancho do J e o e passam 0,35m da linha de base, e o e também passa 0,35m da sua altura. Isso vale só para o desenho mestre (símbolo, avatar e logos). No favicon a grade continua inteira.
3. **Versão compacta para 32 px.** O bojo do P termina 1m antes e o espaço entre o J e o e é de 1m: entre a haste reta e a curva o espaço óptico é menor. O conjunto tem 28m de largura, com margem de 2 px dos dois lados e altura centrada na placa. Hastes, barra (6x2 px) e vãos caem em pixels inteiros.
4. **Favicon de 16 px redesenhado pixel a pixel.** O vão do P passou a ter 2x2 px (o lado direito do bojo tem 1 px). O gancho do J tem miolo aberto. O e é fechado em cima, tem barra vermelha de 2x2 px com branco dos dois lados e cantos suavizados à mão. A grade fica legível no próprio `gerar.py` (GRADE16).
5. **Assinatura horizontal.**
   - A linha de apoio ficou com 1100 px e Barlow 600 de 36 px, em marinho. O conjunto agora tem só marinho e o vermelho do e, além das cores próprias da marca OAB.
   - A régua tem a mesma largura da linha de apoio.
   - O PJe subiu para m = 24 (720 px).
   - O respiro entre apoio, PJe, régua e OAB é de 54 px em todos os intervalos. O bloco é calculado e centrado na vertical, também na versão marinho (a placa branca entra na conta).
6. **Símbolo.** As letras passaram de 76% para 74% da placa, para dar mais respiro lateral.
7. **Prancha.** O símbolo e os favicons ampliados são recortados com os mesmos cantos da placa, e os cantos brancos sumiram. A legenda da grade foi atualizada. A grade mostra o desenho sem a compensação óptica, para os módulos ficarem legíveis.
8. **MEMORIAL.md** foi atualizado na construção, nas cores e em "por que funciona pequeno". O conceito continua com 113 palavras.

## 3. Riscos que permanecem (para o júri pesar)

- **Proximidade com a grafia do sistema.** Continua sendo "PJe" escrito, e é inevitável que lembre o nome do sistema do CNJ. A ligadura P e J e o e fechado com barra vermelha são o que distingue a marca da logo oficial. Não há uso nem cópia da logo oficial.
- **Vermelho sobre marinho.** O contraste de luminosidade é baixo (cerca de 2:1). Agora o vermelho funciona como acento e a leitura não depende dele, mas ele perde força em 16 px.
- **O PNG do símbolo tem cantos brancos.** O render do kit não gera transparência. Para uso sobre fundo colorido, use o `simbolo.svg`.
- **A logo horizontal é empilhada (1600x900),** não um arranjo com símbolo à esquerda e texto à direita. Fica bem em capa, banner e cabeçalho de página. Para barra de navegação estreita, recomenda-se usar o símbolo.

## 4. Conferência visual

Conferi visualmente: simbolo.png, logo_horizontal.png, logo_horizontal_marinho.png, prancha.png e as ampliações dos favicons de 32 e 16 px em tamanho real, sobre fundo claro e escuro. Também conferi pixel a pixel, decodificando as PNGs: o favicon de 16 px bate com a grade desenhada e o de 32 px tem margem de 2 px. Nada está cortado ou desalinhado. Não há travessão em nenhum arquivo da pasta.
