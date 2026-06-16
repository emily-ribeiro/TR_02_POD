# ==========================================
# 1. FUNÇÕES DO ALGORITMO PANCAKE SORT
# ==========================================

def flip(arr, k):
    """
    Simula o uso da espátula.
    Inverte (faz o 'flip') dos primeiros k+1 elementos do array.
    """
    inicio = 0
    while inicio < k:
        arr[inicio], arr[k] = arr[k], arr[inicio]
        inicio += 1
        k -= 1

def encontrar_indice_maximo(arr, n):
    """
    Retorna o índice do maior elemento no array, 
    olhando apenas até a posição 'n' (a parte da pilha ainda não ordenada).
    """
    indice_max = 0
    for i in range(1, n):
        if arr[i] > arr[indice_max]:
            indice_max = i
    return indice_max

def pancake_sort(arr):
    """
    Função principal do Pancake Sort.
    Retorna uma nova lista ordenada para preservar o array original durante os testes.
    """
    # Criamos uma cópia para não mutar a entrada original (facilita exibir o ANTES)
    arr_ordenado = arr.copy()
    n = len(arr_ordenado)

    # Começamos considerando o tamanho total do array e reduzimos em 1 a cada iteração.
    # A ideia é: colocar a maior panqueca na base, depois a segunda maior acima dela, etc.
    for tamanho_atual in range(n, 1, -1):
        
        # 1. Encontra a posição da maior "panqueca" na parte ainda não ordenada da pilha
        indice_max = encontrar_indice_maximo(arr_ordenado, tamanho_atual)

        # Se a maior panqueca já estiver na base desta sub-pilha, não precisamos virar
        if indice_max != tamanho_atual - 1:
            
            # Se a maior panqueca não estiver no topo (índice 0), 
            # viramos a pilha até ela para trazê-la para o topo.
            if indice_max != 0:
                flip(arr_ordenado, indice_max)
            
            # Agora que a maior panqueca está no topo (índice 0),
            # viramos toda a sub-pilha para jogá-la para a sua base definitiva.
            flip(arr_ordenado, tamanho_atual - 1)
            
    return arr_ordenado


# ==========================================
# 2. ROTINAS DE TESTE E VALIDAÇÃO
# ==========================================

def executar_testes_pancake():
    """
    Testa o algoritmo Pancake Sort com diferentes tipos de entradas 
    e exibe os resultados ANTES e DEPOIS da execução.
    """
    import random

    # Definindo 4 casos de teste clássicos
    testes = {
        "1. Array Aleatório": [random.randint(0, 100) for _ in range(15)],
        "2. Array Já Ordenado": [1, 2, 3, 4, 5, 6, 7, 8],
        "3. Array em Ordem Inversa": [9, 8, 7, 6, 5, 4, 3, 2, 1],
        "4. Array com Elementos Repetidos": [7, 3, 7, 1, 9, 3, 4, 4]
    }

    print("-" * 50)
    print("INICIANDO BATERIA DE TESTES - PANCAKE SORT")
    print("-" * 50)

    for nome_teste, dados in testes.items():
        print(f"\n--- {nome_teste} ---")
        
        # Apresenta o resultado ANTES
        print(f"ANTES da execução  : {dados}")
        
        # Executa a ordenação
        dados_ordenados = pancake_sort(dados)
        
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
            array_usuario_ordenado = pancake_sort(array_usuario)
            print(f"DEPOIS da execução : {array_usuario_ordenado}")
        except ValueError:
            print("Entrada inválida. Certifique-se de digitar apenas números inteiros.")


if __name__ == "__main__":
    executar_testes_pancake()