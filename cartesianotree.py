import heapq

# ==========================================
# 1. ESTRUTURA DE DADOS (ÁRVORE CARTESIANA)
# ==========================================

class NodeCartesiano:
    """
    Representa um nó dentro da Árvore Cartesiana.
    Armazena o valor do array, o índice original e os ponteiros para os filhos.
    """
    def __init__(self, valor, indice):
        self.valor = valor
        self.indice = indice
        self.esquerda = None
        self.direita = None

def construir_arvore_cartesiana(arr):
    """
    Constrói a Árvore Cartesiana em tempo O(N) usando uma pilha.
    Garante as duas propriedades vitais:
    1. Propriedade de Min-Heap (o pai é sempre menor que os filhos).
    2. Propriedade in-order (o percurso in-order devolve o array original).
    """
    if not arr:
        return None
        
    pilha = []
    
    for i, valor in enumerate(arr):
        novo_no = NodeCartesiano(valor, i)
        ultimo_removido = None
        
        # Se o novo valor for menor que o topo da pilha, o topo perde a posição de "pai"
        # Removemos da pilha até encontrar um valor menor ou a pilha esvaziar
        while pilha and pilha[-1].valor > valor:
            ultimo_removido = pilha.pop()
            
        # O último nó que foi desbancado torna-se o filho esquerdo do novo nó
        novo_no.esquerda = ultimo_removido
        
        # Se ainda sobrou alguém na pilha, esse nó sobrevivente vira o pai do novo nó
        # (O novo nó entra como filho direito)
        if pilha:
            pilha[-1].direita = novo_no
            
        # O novo nó entra na espinha direita da árvore (topo da pilha)
        pilha.append(novo_no)
        
    # A raiz da árvore inteira será o elemento que ficou na base da pilha
    return pilha[0]


# ==========================================
# 2. ALGORITMO DE ORDENAÇÃO
# ==========================================

def cartesian_tree_sort(arr):
    """
    Função principal do Cartesian Tree Sort.
    Constrói a árvore e extrai os elementos de forma ordenada.
    """
    if not arr:
        return []
        
    # Passo 1: Construir a árvore em tempo linear O(N)
    raiz = construir_arvore_cartesiana(arr)
    
    # Passo 2: Extração ordenada usando Fila de Prioridade (Min-Heap)
    # A fila guardará tuplas no formato: (valor_do_nó, id_na_memória, objeto_nó)
    # O "id_na_memória" evita que o Python tente comparar objetos NodeCartesiano caso os valores empatem
    fila_prioridade = []
    heapq.heappush(fila_prioridade, (raiz.valor, id(raiz), raiz))
    
    array_ordenado = []
    
    # Extrai o menor elemento e insere seus filhos na fila
    while fila_prioridade:
        valor_atual, _, no_atual = heapq.heappop(fila_prioridade)
        array_ordenado.append(valor_atual)
        
        if no_atual.esquerda:
            heapq.heappush(fila_prioridade, (no_atual.esquerda.valor, id(no_atual.esquerda), no_atual.esquerda))
        if no_atual.direita:
            heapq.heappush(fila_prioridade, (no_atual.direita.valor, id(no_atual.direita), no_atual.direita))
            
    return array_ordenado


# ==========================================
# 3. ROTINAS DE TESTE E VALIDAÇÃO
# ==========================================

def executar_testes_cartesian():
    """
    Testa o algoritmo Cartesian Tree Sort com diferentes tipos de entradas 
    e exibe os resultados ANTES e DEPOIS da execução.
    """
    import random

    # Definindo 4 casos de teste práticos
    testes = {
        "1. Array Aleatório": [random.randint(0, 100) for _ in range(15)],
        "2. Array Já Ordenado": [10, 20, 30, 40, 50, 60],
        "3. Array em Ordem Inversa": [99, 88, 77, 66, 55, 44, 33],
        "4. Array com Elementos Repetidos": [8, 4, 12, 4, 8, 1, 1, 9]
    }

    print("-" * 50)
    print("INICIANDO BATERIA DE TESTES - CARTESIAN TREE SORT")
    print("-" * 50)

    for nome_teste, dados in testes.items():
        print(f"\n--- {nome_teste} ---")
        
        # Apresenta o resultado ANTES
        print(f"ANTES da execução  : {dados}")
        
        # Executa a ordenação
        dados_ordenados = cartesian_tree_sort(dados)
        
        # Apresenta o resultado DEPOIS
        print(f"DEPOIS da execução : {dados_ordenados}")
        
        # Validação automática
        esta_correto = dados_ordenados == sorted(dados)
        print(f"Validação: {'✅ Sucesso' if esta_correto else '❌ Falha'}")

    print("\n" + "-" * 50)
    print("TESTE INTERATIVO (ENTRADA DO USUÁRIO)")
    print("-" * 50)
    
    # Permite ao usuário testar sua própria entrada
    entrada = input("Digite números inteiros separados por espaço (ou pressione Enter para pular): ")
    if entrada.strip():
        try:
            array_usuario = [int(x) for x in entrada.split()]
            print(f"\nANTES da execução  : {array_usuario}")
            array_usuario_ordenado = cartesian_tree_sort(array_usuario)
            print(f"DEPOIS da execução : {array_usuario_ordenado}")
        except ValueError:
            print("Entrada inválida. Certifique-se de digitar apenas números inteiros.")


if __name__ == "__main__":
    executar_testes_cartesian()