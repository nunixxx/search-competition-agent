# Relatório

## Integrantes

* **Aluno 1 – Nome:** <mark>`Caio Felipe Ferreira Nunes`</mark>

* **Aluno 1 – Cartão UFRGS:** <mark>`00588024`</mark>

* **Aluno 2 – Nome:** <mark>` `</mark>

* **Aluno 2 – Cartão UFRGS:** <mark>` `</mark>

* **Aluno 3 – Nome:** <mark>` `</mark>

* **Aluno 3 – Cartão UFRGS:** <mark>` `</mark>

---

## Bibliotecas Extras

<mark>`Preencher se necessário`</mark>

---

# Tic-Tac-Toe – Poda Alfa-Beta

### (i) O minimax sempre ganha ou empata jogando contra o *randomplayer*?

Sim. O minimax nunca perde contra o *randomplayer*; ele sempre vence ou empata.

**Justificativa:**

* O algoritmo minimax com profundidade ilimitada joga de maneira ótima em todos os estados possíveis do jogo, escolhendo sempre a jogada que maximiza sua utilidade (**+1 vitória, 0 empate, -1 derrota**).
* Como o *randomplayer* realiza escolhas aleatórias entre as jogadas válidas, ele inevitavelmente comete erros em algumas partidas.
* O minimax consegue explorar esses erros e encontrar sequências vencedoras, como demonstrado pelo teste `test_proven_win_exploiting_first_blunder`.
* A única possibilidade de empate ocorre quando o *randomplayer*, por acaso, executa uma sequência equivalente ao jogo perfeito.

Portanto, contra um oponente aleatório, o minimax tende a vencer na maioria das partidas e empatar apenas em situações ocasionais.

---

### (ii) O minimax sempre empata consigo mesmo?

Sim. O minimax sempre empata quando joga contra outra instância do próprio minimax.

**Justificativa:**

O jogo **Tic-Tac-Toe Misère 3×3** é considerado um *solved game* (jogo resolvido), ou seja, seu resultado teórico é conhecido quando ambos os jogadores utilizam estratégia ótima.

Nesse cenário:

1. Ambos utilizam `make_move(state, -1, utility)` com profundidade ilimitada;
2. Ambos utilizam a mesma função `utility()` (**+1 vitória, 0 empate, -1 derrota**), considerando a perspectiva do jogador atual (`root_player = state.player`);
3. Ambos exploram exaustivamente a árvore de estados.

Como consequência, cada jogador escolhe sempre a melhor ação disponível, impedindo que o adversário obtenha vantagem.

Dessa forma, nenhum dos lados consegue forçar uma derrota do oponente e o resultado final é empate.

Esse comportamento também pode ser observado no teste `test_perfect_play`, no qual dois jogadores perfeitos terminam a partida sem vencedor.

---

### (iii) O minimax não perde para você quando você usa a sua melhor estratégia?

Durante os testes realizados, foram jogadas aproximadamente **20 partidas** contra o minimax.

Até compreendermos uma estratégia eficiente, o minimax venceu **8 partidas**, enquanto as outras **12 terminaram em empate**.

Como discutido anteriormente, o Tic-Tac-Toe é um *solved game*. Portanto, considerando jogo perfeito por parte do minimax, o pior resultado possível para ele é o empate, impossibilitando derrotá-lo utilizando apenas estratégia ótima.
