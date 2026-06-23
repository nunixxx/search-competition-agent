# Relatório

## Integrantes TURMA B

| Aluno   | Nome                                      | Cartão UFRGS            |
| ------- | ----------------------------------------- | ----------------------- |
| Aluno 1 | <mark>`Caio Felipe Ferreira Nunes`</mark> | <mark>`00588024`</mark> |
| Aluno 2 | <mark>`Renan Augusto da Silva Zen`</mark> | <mark>`00579490`</mark> |
| Aluno 3 | <mark>` `</mark>                          | <mark>` `</mark>        |

---

## Bibliotecas Extras

<mark>`Preencher se necessário`</mark>

---

# Tic-Tac-Toe – Poda Alfa-Beta

## (i) O minimax sempre ganha ou empata jogando contra o *randomplayer*?

Sim. O minimax nunca perde contra o *randomplayer*; ele sempre vence ou empata.

### Justificativa

* O algoritmo minimax com profundidade ilimitada joga de maneira ótima em todos os estados possíveis do jogo, escolhendo sempre a jogada que maximiza sua utilidade (**+1 vitória, 0 empate, -1 derrota**).
* Como o *randomplayer* realiza escolhas aleatórias entre as jogadas válidas, ele inevitavelmente comete erros em algumas partidas.
* O minimax consegue explorar esses erros e encontrar sequências vencedoras, como demonstrado pelo teste `test_proven_win_exploiting_first_blunder`.
* A única possibilidade de empate ocorre quando o *randomplayer*, por acaso, executa uma sequência equivalente ao jogo perfeito.

Portanto, contra um oponente aleatório, o minimax tende a vencer na maioria das partidas e empatar apenas em situações ocasionais.

---

## (ii) O minimax sempre empata consigo mesmo?

Sim. O minimax sempre empata quando joga contra outra instância do próprio minimax.

### Justificativa

O jogo **Tic-Tac-Toe Misère 3×3** é considerado um *solved game* (jogo resolvido), ou seja, seu resultado teórico é conhecido quando ambos os jogadores utilizam estratégia ótima.

Nesse cenário:

1. Ambos utilizam `make_move(state, -1, utility)` com profundidade ilimitada;
2. Ambos utilizam a mesma função `utility()` (**+1 vitória, 0 empate, -1 derrota**), considerando a perspectiva do jogador atual (`root_player = state.player`);
3. Ambos exploram exaustivamente a árvore de estados.

Como consequência, cada jogador escolhe sempre a melhor ação disponível, impedindo que o adversário obtenha vantagem.

Dessa forma, nenhum dos lados consegue forçar uma derrota do oponente e o resultado final é empate.

Esse comportamento também pode ser observado no teste `test_perfect_play`, no qual dois jogadores perfeitos terminam a partida sem vencedor.

---

## (iii) O minimax não perde para você quando você usa a sua melhor estratégia?

Durante os testes realizados, foram jogadas aproximadamente **20 partidas** contra o minimax.

Até compreendermos uma estratégia eficiente, o minimax venceu **8 partidas**, enquanto as outras **12 terminaram em empate**.

Como discutido anteriormente, o Tic-Tac-Toe é um *solved game*. Portanto, considerando jogo perfeito por parte do minimax, o pior resultado possível para ele é o empate, impossibilitando derrotá-lo utilizando apenas estratégia ótima.

---

# Othello

## Heurística Customizada

A heurística implementada em `evaluate_custom`, no arquivo `othello_minimax_custom.py`, realiza uma combinação linear de quatro métricas fundamentais do Othello, ajustando o peso de cada uma de acordo com o andamento do jogo (se está início, meio ou fim, controlados pela variável `n_empty`).

As quatro métricas são:

### Valor Posicional (Mask Score)

Utiliza a matriz estática (`EVAL_TEMPLATE`) para valorizar posições fortes (como bordas) e penalizar posições perigosas (como as adjacentes aos cantos).

### Mobilidade (Mobility)

Calcula a diferença entre o número de jogadas legais do jogador e do oponente. Maximizar opções restringe o adversário e o força a fazer jogadas piores.

### Fronteira (Frontier)

Avalia quantas peças estão adjacentes a espaços vazios. Ter menos peças de fronteira que o adversário é melhor, pois peças internas são mais difíceis de serem capturadas.

### Cantos (Corner Score)

Prioridade máxima no jogo, cantos são as posições definitivas e imunes à captura.

A ideia de utilizar essas métricas veio a partir de uma pesquisa sobre a literatura existente sobre o jogo e um pouco de intuição depois de jogar algumas partidas.

A estratégia ajusta dinamicamente os multiplicadores de cada métrica:

* **Início do jogo:** mais importância no valor posicional e controle de bordas;
* **Meio do jogo:** mobilidade e cantos recebem maior peso;
* **Fim do jogo:** mobilidade recebe o maior peso, focando em estrangular as opções finais do oponente.

---

## Resultados dos Confrontos

| Confronto                                        | Vencedor               | Resultado               |
| ------------------------------------------------ | ---------------------- | ----------------------- |
| (i) Contagem de peças × Valor posicional         | Valor posicional       | Peças B 19 × 45 Peças W |
| (ii) Valor posicional × Contagem de peças        | Contagem de peças      | Peças B 28 × 36 Peças W |
| (iii) Contagem de peças × Heurística customizada | Heurística customizada | Peças B 12 × 52 Peças W |
| (iv) Heurística customizada × Contagem de peças  | Heurística customizada | Peças B 48 × 16 Peças W |
| (v) Valor posicional × Heurística customizada    | Heurística customizada | Peças B 22 × 42 Peças W |
| (vi) Heurística customizada × Valor posicional   | Heurística customizada | Peças B 48 × 16 Peças W |

Logo, a Heurística customizada foi a mais bem-sucedida de todas, obtendo vitória sobre todos os adversários.

---

## Critério de Parada

O critério de parada principal para a árvore de busca sem limite de profundidade (quando `max_depth = -1`) é o Aprofundamento Iterativo (*Iterative Deepening*) controlado por tempo limite.

A função inicia com profundidade 1 e vai iterativamente aumentando a profundidade máxima da árvore (`current_depth += 1`).

A cada jogada avaliada, o algoritmo verifica o tempo gasto através de `time.time()`.

Se a diferença atingir o teto predefinido de **4.5 segundos** (seguro para o limite de **5s** imposto pelo servidor), o loop é imediatamente interrompido e a melhor jogada encontrada na profundidade completa anterior é retornada.

---

## Agente do Torneio

Para o agente oficial do torneio (`tournament_agent.py`), escolhemos uma implementação baseada no Minimax com Poda Alfa-Beta, realizando Aprofundamento Iterativo contínuo, alimentado pela Heurística Customizada.

Para otimizar o desempenho nos segundos finais, o agente possui uma verificação de fim de jogo mais agressiva:

Quando restam **12 ou menos espaços vazios no tabuleiro (`n_empty <= 12`)**, o algoritmo sabe que está perto do estado terminal e adapta seu comportamento para fechar a partida da forma mais eficiente possível.

---

## Uso de IA

Usei o Gemini para me dar um repertório teórico do que a literatura diz sobre heurísticas e adaptei para incluir minhas percepções do jogo.

Além disso, usamos para ajudar a debugar alguns poucos erros de compilação.
