# ✈️ Algoritmo de Rotas Aéreas (Redes-Aereas)

Este projeto implementa uma simulação de rede de voos entre aeroportos utilizando a estrutura de **Grafo Direcionado Ponderado**. Cada aeroporto é um vértice, e cada voo é uma aresta com pesos (tempo e custo).

O núcleo da aplicação utiliza o **Algoritmo de Dijkstra** para calcular o caminho mais rápido ou mais barato entre dois aeroportos, além de funcionalidades CRUD para gerenciar a rede.

## 🎯 Requisitos Implementados

* **Representação do Grafo:** Utiliza dicionários e `defaultdict` em Python para armazenar a rede.
* **CRUD de Vértices/Arestas:** Adição e remoção de aeroportos e rotas.
* **Consultas Básicas:** Verificação de rotas e listagem de voos diretos.
* **Caminho Mínimo (Dijkstra):** Implementado para calcular a rota de menor **Tempo** e menor **Custo**.
* **Extra (Simulação de Conexão):** Cálculo do caminho mais rápido considerando um tempo mínimo de escala entre voos.

