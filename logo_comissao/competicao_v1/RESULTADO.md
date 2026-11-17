# Resultado da competição de design: logo da Comissão Estadual de Apoio Institucional ao PJe

Comissão Estadual de Apoio Institucional ao Processo Judicial Eletrônico (PJe) da Ordem dos Advogados do Brasil, Seção do Pará (OAB/PA). Parecer do orquestrador da competição, 16/11/2026.

Prancha comparativa: `juri/comparativo.png` (símbolo, logo horizontal e favicon das três propostas, lado a lado, a partir dos arquivos originais de cada squad, sem alteração). Para regerar, a partir de `competicao_v1`: `python -I juri/montar_comparativo.py` (usa `_kit/render.py`).

## 1. Notas por lente e média

| Squad | Proposta | Identidade | Técnica | Originalidade | Média | Posição |
|---|---|---:|---:|---:|---:|:---:|
| **A** | Folha que atende | 8,0 | 8,5 | 7,0 | **7,83** | **1º** |
| B | Monograma PJe | 6,5 | 5,5 | 6,0 | 6,00 | 2º |
| C | Balança digital | 5,5 | 8,0 | 4,0 | 5,83 | 3º |

Média simples das três lentes. Rankings individuais: identidade A, B, C; técnica A, C, B; originalidade A, B, C. O Squad A ficou em primeiro nas três lentes. B e C ficaram separados por apenas 0,17: C ganha na técnica, B ganha em identidade e originalidade.

## 2. Vencedora: Squad A, "Folha que atende"

**Decisão do orquestrador: Squad A, sem divergência do júri.** Abri as pranchas e os favicons das três propostas e cheguei à mesma ordem no primeiro lugar.

Por que A vence:

- **Cumpre o briefing no que está desenhado.** A hierarquia decidida está exata: linha de apoio em caixa alta espaçada, "PJe" dominante em Barlow 800, régua e, abaixo dela, a marca OAB Pará íntegra, alinhada à haste do P. No fundo marinho, a OAB vai sobre placa branca, como exigido.
- **É o único símbolo próprio da disputa.** Folha com dobra, cauda de balão e check vazado formam uma massa só, cuja silhueta lê como P sem que a letra tenha sido desenhada. Fala do serviço da Comissão (o processo chega com dúvida e sai atendido), e não do sistema do Conselho Nacional de Justiça (CNJ).
- **Paleta disciplinada.** Duas cores no símbolo (marinho e azul); o vermelho fica reservado à marca OAB, que já o contém. Isso também afasta a peça da Comissão de Direito Digital (CDD) da Subseção Marabá, cujo escudo usa a metade vermelha.
- **Execução mais rigorosa.** Linha de apoio, "PJe" e régua com a mesma largura de tinta; base do símbolo na base da régua; favicon de 16 pixels (px) desenhado pixel a pixel; arquivos vetoriais (SVG, Scalable Vector Graphics) enxutos, com check em máscara, transparente em qualquer fundo.

Onde eu pesaria diferente do júri, sem mudar o resultado:

- A crítica de que o lockup de A repete a estrutura da CDD procede em parte, mas vale mais para C (régua longa sob todo o conjunto, assinatura no fim da régua). Em A, a régua tem só a largura de "PJe" e a OAB fica embaixo, como o briefing manda.
- Na minha leitura, o favicon de 16 px de C é o mais limpo dos três, e o de B é ilegível (lê-se "PJc" ou "Rlc"). O de A funciona como silhueta, com o check apenas sugerido. Por isso trago a disciplina de grade de C como enxerto, a seguir.

## 3. Ajustes recomendados na vencedora antes do aval da Seccional

Em ordem de prioridade.

1. **Dobra no fundo marinho.** A dobra azul #008BD2 sobre #003399 tem contraste de cerca de 2,9:1, o mesmo motivo que levou a régua a ficar branca. Passar a dobra a branco (ou eliminar o vão em L) na versão marinho e no avatar. Correção simples, apontada pela lente técnica.
2. **Check proprietário e validado pela Seccional.** Duas lentes levantaram o mesmo ponto: o check é o elemento mais genérico do conjunto e pode ser lido como "validação oficial" ou garantia de resultado. Redesenhar o check com terminais cortados a 45 graus, na mesma diagonal da dobra e da cauda, para que vire sinal da marca e não ícone de interface. Submeter a leitura à Seccional; se houver ressalva, trocar por sinal neutro de atendimento.
3. **Versão empilhada centralizada (enxerto do Squad B).** Criar uma assinatura empilhada: símbolo em cima, linha de apoio em uma linha, "PJe", régua e OAB centralizados, com o respiro vertical uniforme que B usou (mesmo espaço entre os quatro elementos). Isso dá uma versão claramente distinta do lockup da CDD e resolve usos verticais (capas, banners, cartaz).
4. **Favicon de 32 px próprio (enxerto do Squad C).** Hoje o de 32 é o desenho da grade de 16 ampliado, com bordas macias. Desenhar o 32 na sua própria grade, em pixel inteiro, com 1 px de margem no 16 e 2 px no 32, como C fez com a balança.
5. **Ponta da régua.** O chanfro de 45 graus tem só 9 unidades e parece falha de renderização. Ampliar até ficar legível como eco da dobra ou retirar.
6. **Reforçar a leitura do P.** Ajustar a proporção entre corpo e cauda para a silhueta ler P antes de ler "balão de chat", e testar lado a lado com ícones de documento e de mensagem de grandes aplicativos.
7. **Arte-final.** Converter "PJe" e a linha de apoio em curvas nos arquivos de entrega (ou declarar fallback `Barlow, Arial, sans-serif`), já que a largura medida no Edge pode variar 1 ou 2 px em outro navegador.
8. **Manual de uso.** Registrar área de proteção e tamanho mínimo da marca OAB Pará dentro da assinatura, largura mínima da horizontal (400 px; abaixo disso, símbolo ou avatar) e a regra de duas fontes de favicon (16 e 32).

Outros enxertos de boas ideias:

- **Do Squad C:** a prancha com o avatar no recorte circular a 160 e 40 px e a aba de navegador simulada, como teste padrão de aprovação; a amarração por módulo entre símbolo e texto (topo, linha de base e faixa da linha de apoio), que A já pratica e deve documentar no manual.
- **Do Squad B:** a régua fina e monocromática com a mesma largura da linha de apoio, para a versão empilhada; a documentação da grade em prancha própria (módulo, alturas, raios).

## 4. O que cada squad fez de melhor

- **Squad A, Folha que atende:** o único pictograma realmente próprio, com a letra P escondida na silhueta e o conceito de serviço ("processo que sai atendido"). O sistema de alinhamento mais rigoroso, kerning óptico medido da Barlow e a faixa de redução (400, 300 e 200 px) na prancha.
- **Squad B, Monograma PJe:** a assinatura mais distante da CDD, empilhada e centralizada, com respiro uniforme entre os quatro elementos; a ligadura P com J é letreiramento de fato, e o acento vermelho no "e" é memorável. Pesou contra: "PJe" desenhado fora da Barlow, emendas visíveis na ligadura e favicon de 16 px ilegível.
- **Squad C, Balança digital:** a melhor execução de favicon a 16 e 32 px, desenhado na própria grade, um pixel por módulo; tipografia em Barlow bem resolvida, com linha de apoio na largura de tinta do "PJe", e o cuidado de passar a estrutura a branco no marinho por contraste. Pesou contra: OAB ao lado da régua (fora da hierarquia), estética de jogo retrô e a fórmula "símbolo jurídico mais textura digital", próxima do raciocínio da CDD.

## 5. Próximo passo

Aplicar os ajustes 1 a 5 no Squad A (rodada v2), regerar a prancha e levar à Seccional para aval, junto com a pergunta sobre a leitura do check (ajuste 2).
