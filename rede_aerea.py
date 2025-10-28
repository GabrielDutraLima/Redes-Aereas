import heapq
from collections import defaultdict

class RedeAerea:
   
    """
    Representa a rede de voos entre aeroportos como um grafo direcionado ponderado.
    Os pesos podem ser tempo, distância ou custo.
    """
    def __init__(self):
        self.grafo = defaultdict(lambda: {})
        self.aeroportos = set()


    def adicionar_aeroporto(self, codigo_aeroporto):
        """Adiciona um aeroporto (vértice) à rede."""
        if codigo_aeroporto not in self.aeroportos:
            self.aeroportos.add(codigo_aeroporto)
            if codigo_aeroporto not in self.grafo:
                self.grafo[codigo_aeroporto] = {}
            # print(f"Aeroporto {codigo_aeroporto} adicionado.")

    def remover_aeroporto(self, codigo_aeroporto):
        """Remove um aeroporto e todas as rotas que partem ou chegam a ele."""
        if codigo_aeroporto not in self.aeroportos:
            return f"Erro: Aeroporto {codigo_aeroporto} não encontrado."
            
        # Remove todas as rotas de SAÍDA do aeroporto
        if codigo_aeroporto in self.grafo:
            del self.grafo[codigo_aeroporto]
        
        # Remove todas as rotas de CHEGADA ao aeroporto
        aeroportos_a_remover_rota = []
        for origem in self.grafo:
            if codigo_aeroporto in self.grafo.get(origem, {}) and codigo_aeroporto in self.grafo[origem]:
                aeroportos_a_remover_rota.append(origem)
        
        for origem in aeroportos_a_remover_rota:
            del self.grafo[origem][codigo_aeroporto]
            
        self.aeroportos.remove(codigo_aeroporto)
        return f"Aeroporto {codigo_aeroporto} removido com todas as suas rotas."


    def adicionar_rota(self, origem, destino, tempo_voo, custo_voo):
        """Adiciona uma rota de voo (aresta direcionada com peso)."""
        for aero in [origem, destino]:
            if aero not in self.aeroportos:
                self.adicionar_aeroporto(aero)

        self.grafo[origem][destino] = {'tempo': tempo_voo, 'custo': custo_voo}
        return f"Rota {origem} -> {destino} adicionada (Tempo: {tempo_voo}h, Custo: R${custo_voo})."

    def remover_rota(self, origem, destino):
        """Remove uma rota de voo (aresta)."""
        if origem in self.grafo and destino in self.grafo[origem]:
            del self.grafo[origem][destino]
            return f"Rota {origem} -> {destino} removida."
        else:
            return f"Erro: Rota {origem} -> {destino} não encontrada."

    # --- Consultas ---

    def consultar_voos_disponiveis(self, origem):
        """Consulta voos diretos disponíveis a partir de um aeroporto."""
        if origem not in self.aeroportos:
            return f"Erro: Aeroporto {origem} não encontrado."
        
        voos = self.grafo.get(origem, {})
        if not voos:
            return f"Não há voos diretos disponíveis saindo de {origem}."
            
        resultado = [f"Voos diretos saindo de {origem}:"]
        for destino, dados in voos.items():
            resultado.append(f"  -> {destino}: Tempo: {dados['tempo']}h, Custo: R${dados['custo']}")
        return "\n".join(resultado)
    
    def verificar_rota(self, origem, destino):
        """Verifica se existe *alguma* rota entre dois aeroportos (Busca em Largura/BFS simplificada)."""
        if origem not in self.aeroportos or destino not in self.aeroportos:
            return False, "Aeroporto(s) não encontrado(s)."

        if origem == destino:
            return True, "Origem e destino são o mesmo aeroporto."
            
        fila = [origem]
        visitados = {origem}

        while fila:
            atual = fila.pop(0)
            if atual == destino:
                return True, "Rota encontrada."
            
            for vizinho in self.grafo.get(atual, {}):
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    fila.append(vizinho)
        
        return False, "Nenhuma rota encontrada."


    def dijkstra(self, origem, destino, tipo_peso='tempo'):
        """
        Calcula o caminho mais rápido/barato (Dijkstra).
        tipo_peso: 'tempo' (para mais rápido) ou 'custo' (para mais barato).
        """
        if origem not in self.aeroportos or destino not in self.aeroportos:
            return {"erro": "Aeroporto de origem ou destino não encontrado."}

        distancias = {aero: float('inf') for aero in self.aeroportos}
        distancias[origem] = 0
        caminhos = {aero: [origem] for aero in self.aeroportos}
        fila_prioridade = [(0, origem)] 

        while fila_prioridade:
            peso_atual, u = heapq.heappop(fila_prioridade)

            if peso_atual > distancias[u]:
                continue
            
            if u == destino:
                break

            for v, dados_rota in self.grafo.get(u, {}).items():
                peso_rota = dados_rota.get(tipo_peso)
                if peso_rota is None:
                    continue 

                novo_peso = peso_atual + peso_rota

                if novo_peso < distancias[v]:
                    distancias[v] = novo_peso
                    caminhos[v] = caminhos[u] + [v]
                    heapq.heappush(fila_prioridade, (novo_peso, v))

        peso_total = distancias[destino]
        caminho = caminhos[destino]
        
        if peso_total == float('inf'):
            return {"erro": f"Não foi possível encontrar uma rota de {origem} para {destino}."}
        else:
            return {
                'peso_total': round(peso_total, 2),
                'unidade': 'horas' if tipo_peso == 'tempo' else 'R$',
                'caminho': " -> ".join(caminho)
            }
            
    # --- (Adaptação Dijkstra) ---
    
    def dijkstra_com_conexao(self, origem, destino, tempo_conexao_minimo=1.0):
        """
        Calcula o caminho mais rápido, considerando um tempo mínimo de conexão.
        """
        if origem not in self.aeroportos or destino not in self.aeroportos:
            return {"erro": "Aeroporto de origem ou destino não encontrado."}
            
        distancias = {aero: float('inf') for aero in self.aeroportos}
        distancias[origem] = 0
        caminhos = {aero: [origem] for aero in self.aeroportos}
        fila_prioridade = [(0, origem)] 

        while fila_prioridade:
            tempo_acumulado, u = heapq.heappop(fila_prioridade)

            if tempo_acumulado > distancias[u]:
                continue
            
            if u == destino:
                break

            for v, dados_rota in self.grafo.get(u, {}).items():
                tempo_voo = dados_rota.get('tempo', 0)
                
                custo_conexao = 0
                if u != origem and len(caminhos[u]) > 1:
                    custo_conexao = tempo_conexao_minimo
                    
                novo_tempo = tempo_acumulado + tempo_voo + custo_conexao
                
                if novo_tempo < distancias[v]:
                    distancias[v] = novo_tempo
                    caminhos[v] = caminhos[u] + [v]
                    heapq.heappush(fila_prioridade, (novo_tempo, v))

        tempo_total = distancias[destino]
        caminho = caminhos[destino]
        
        if tempo_total == float('inf'):
            return {"erro": f"Não foi possível encontrar uma rota com conexões de {origem} para {destino}."}
        else:
            return {
                'tempo_total': round(tempo_total, 2),
                'unidade': 'horas',
                'conexao_minima': f"{tempo_conexao_minimo}h em cada escala.",
                'caminho': " -> ".join(caminho)
            }


# FUNÇÕES DE MENU E INTERAÇÃO

def inicializar_rede(rede):
    """Inicializa a rede com dados de exemplo."""
    # Adicionando rotas de exemplo
    rede.adicionar_rota("GRU", "GIG", tempo_voo=1.5, custo_voo=300)
    rede.adicionar_rota("GRU", "SSA", tempo_voo=3.0, custo_voo=500)
    rede.adicionar_rota("GIG", "SSA", tempo_voo=2.5, custo_voo=400)
    rede.adicionar_rota("GIG", "BSB", tempo_voo=2.0, custo_voo=350)
    rede.adicionar_rota("SSA", "BSB", tempo_voo=1.8, custo_voo=200)
    rede.adicionar_rota("BSB", "GRU", tempo_voo=2.0, custo_voo=320)
    rede.adicionar_rota("POA", "GRU", tempo_voo=2.0, custo_voo=450)
    
    rede.adicionar_aeroporto("FLN")
    rede.adicionar_aeroporto("MAO")
    
    print("\n[INFO] Rede Aérea de Exemplo Inicializada (7 rotas, 7 aeroportos).")
    print(f"[INFO] Aeroportos disponíveis: {', '.join(sorted(rede.aeroportos))}")


def exibir_menu():
    """Exibe as opções do menu principal."""
    print("\n" + "="*50)
    print("✈️ MENU PRINCIPAL - ROTAS AÉREAS ✈️")
    print("="*50)
    print("1. Adicionar/Remover Aeroporto/Rota")
    print("2. Consultar Voos Disponíveis (Diretos)")
    print("3. Verificar Existência de Rota")
    print("4. **Dijkstra:** Caminho Mais Rápido (Tempo)")
    print("5. **Dijkstra:** Caminho Mais Barato (Custo)")
    print("6. **Extra:** Caminho Mais Rápido com Conexão Mínima")
    print("0. Sair")
    print("="*50)

def sub_menu_crud(rede):
    """Sub-menu para operações CRUD."""
    while True:
        print("\n--- Opções de Gestão (CRUD) ---")
        print("1. Adicionar Aeroporto")
        print("2. Remover Aeroporto")
        print("3. Adicionar Rota de Voo")
        print("4. Remover Rota de Voo")
        print("0. Voltar ao Menu Principal")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            codigo = input("Código do Aeroporto (ex: GRU): ").upper()
            rede.adicionar_aeroporto(codigo)
            print(f"[SUCESSO] Aeroporto {codigo} adicionado.")
        elif opcao == '2':
            codigo = input("Código do Aeroporto a remover: ").upper()
            resultado = rede.remover_aeroporto(codigo)
            print(f"[RESULTADO] {resultado}")
        elif opcao == '3':
            origem = input("Aeroporto de Origem: ").upper()
            destino = input("Aeroporto de Destino: ").upper()
            try:
                tempo = float(input("Tempo de Voo em horas (ex: 1.5): "))
                custo = float(input("Custo do Voo em R$: "))
                resultado = rede.adicionar_rota(origem, destino, tempo, custo)
                print(f"[SUCESSO] {resultado}")
            except ValueError:
                print("[ERRO] Tempo e Custo devem ser números válidos.")
        elif opcao == '4':
            origem = input("Aeroporto de Origem: ").upper()
            destino = input("Aeroporto de Destino: ").upper()
            resultado = rede.remover_rota(origem, destino)
            print(f"[RESULTADO] {resultado}")
        elif opcao == '0':
            break
        else:
            print("[ERRO] Opção inválida. Tente novamente.")

def consulta_dijkstra(rede, tipo_peso, conexao=False):
    """Função auxiliar para consultar o caminho mais rápido/barato."""
    if not rede.aeroportos:
        print("[ERRO] A rede não possui aeroportos. Adicione rotas primeiro.")
        return
    
    print("\n--- Aeroportos Disponíveis ---")
    print(f"Códigos: {', '.join(sorted(rede.aeroportos))}")
        
    origem = input("Aeroporto de Origem: ").upper()
    destino = input("Aeroporto de Destino: ").upper()
    
    if conexao:
        try:
            tempo_min_conexao = float(input("Tempo mínimo de conexão (em horas, ex: 1.0): "))
        except ValueError:
            print("[ERRO] Tempo de conexão deve ser um número válido.")
            return

        resultado = rede.dijkstra_com_conexao(origem, destino, tempo_min_conexao)
        
        print("\n--- Resultado do Caminho com Conexão ---")
        if 'erro' not in resultado:
            print(f"Caminho: **{resultado['caminho']}**")
            print(f"Tempo Total (com escala): **{resultado['tempo_total']} {resultado['unidade']}**")
            print(f"Detalhe: {resultado['conexao_minima']}")
        else:
            print(resultado['erro'])
        return
    
    resultado = rede.dijkstra(origem, destino, tipo_peso)
    
    tipo = "Mais Rápido (Tempo)" if tipo_peso == 'tempo' else "Mais Barato (Custo)"
    print(f"\n--- Resultado do Caminho {tipo} ---")
    if 'erro' not in resultado:
        print(f"Caminho: **{resultado['caminho']}**")
        print(f"{'Tempo Total' if tipo_peso == 'tempo' else 'Custo Total'}: **{resultado['peso_total']} {resultado['unidade']}**")
    else:
        print(resultado['erro'])


def menu_principal():
    """Função principal do menu interativo."""
    rede = RedeAerea()
    inicializar_rede(rede)
    
    while True:
        exibir_menu()
        escolha = input("Digite sua escolha (0-6): ")
        
        if escolha == '1':
            sub_menu_crud(rede)
            
        elif escolha == '2':
            if not rede.aeroportos:
                print("[ERRO] A rede não possui aeroportos. Adicione rotas primeiro.")
                continue

            print("\n--- Aeroportos Disponíveis ---")
            print(f"Códigos: {', '.join(sorted(rede.aeroportos))}")
            
            origem = input("Código do Aeroporto de partida para consultar voos diretos: ").upper()
            print("\n--- Resultado da Consulta ---")
            print(rede.consultar_voos_disponiveis(origem))
            
        elif escolha == '3':
            if not rede.aeroportos:
                print("[ERRO] A rede não possui aeroportos. Adicione rotas primeiro.")
                continue
            
            print("\n--- Aeroportos Disponíveis ---")
            print(f"Códigos: {', '.join(sorted(rede.aeroportos))}")
            
            origem = input("Aeroporto de Origem: ").upper()
            destino = input("Aeroporto de Destino: ").upper()
            existe, msg = rede.verificar_rota(origem, destino)
            print(f"\n[RESULTADO] Rota de {origem} para {destino}: **{existe}** ({msg})")
            
        elif escolha == '4':
            consulta_dijkstra(rede, 'tempo')

        elif escolha == '5':
            consulta_dijkstra(rede, 'custo')

        elif escolha == '6':
            consulta_dijkstra(rede, 'tempo', conexao=True)
            
        elif escolha == '0':
            print("Saindo do simulador de Rotas Aéreas. Até logo!")
            break
        
        else:
            print("[ERRO] Opção inválida. Por favor, escolha um número entre 0 e 6.")

if __name__ == "__main__":
    menu_principal()