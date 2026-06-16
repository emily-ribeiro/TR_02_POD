import math
from collections import deque

# ==========================================
# 1. ESTRUTURAS DE DADOS DO FUNNEL SORT
# ==========================================

class NodeFunil:
    """
    Representa um nó na árvore de mesclagem (Funil).
    Utiliza buffers que só são preenchidos quando esvaziam (Lazy Fill).
    """
    def __init__(self, tamanho_buffer=0):
        self.esquerda = None
        self.direita = None
        self.buffer = deque()
        self.tamanho_buffer = tamanho_buffer
        self.is_folha = False

    def preencher(self):
        """
        Preenche o buffer atual mesclando elementos dos filhos.
        Se o buffer de um filho estiver vazio, exige que ele se preencha primeiro.
        """
        # Nós folhas já contêm os dados base, não buscam de baixo
        if self.is_folha:
            return

        # Continua puxando dados até encher o buffer ou esgotar as fontes
        while len(self.buffer) < self.tamanho_buffer:
            
            # Se o filho esquerdo secou mas ainda tem dados abaixo dele, manda ele recarregar
            if self.esquerda and len(self.esquerda.buffer) == 0 and not self.esquerda.esta_esgotado():
                self.esquerda.preencher()
            
            # Se o filho direito secou mas ainda tem dados abaixo dele, manda ele recarregar
            if self.direita and len(self.direita.buffer) == 0 and not self.direita.esta_esgotado():
                self.direita.preencher()
                
            esq_vazia = (not self.esquerda) or (len(self.esquerda.buffer) == 0)
            dir_vazia = (not self.direita) or (len(self.direita.buffer) == 0)
            
            # Se os dois lados secaram totalmente, paramos de preencher
            if esq_vazia and dir_vazia:
                break
                
            # Lógica de Merge: Compara os topos dos buffers e sobe o menor valor
            if esq_vazia:
                self.buffer.append(self.direita.buffer.popleft())
            elif dir_vazia:
                self.buffer.append(self.esquerda.buffer.popleft())
            else:
                if self.esquerda.buffer[0] <= self.direita.buffer[0]:
                    self.buffer.append(self.esquerda.buffer.popleft())
                else:
                    self.buffer.append(self.direita.buffer.popleft())

    def esta_esgotado(self):
        """Verifica se este nó e todas as suas ramificações estão completamente vazios."""
        if self.is_folha:
            return len(self.buffer) == 0
        else:
            esq_esg = self.esquerda is None or self.esquerda.esta_esgotado()
            dir_esg = self.direita is None or self.direita.esta_esgotado()
            return len(self.buffer) == 0 and esq_esg and dir_esg

# ==========================================
# 2. FUNÇÕES DO ALGORITMO
# ==========================================

def construir_funil(streams):
    """
    Constrói a árvore de mesclagem (K-Funnel).
    Recebe segmentos ordenados e monta uma árvore binária de buffers.
    """
    if len(streams) == 1:
        folha = NodeFunil(tamanho_buffer=len(streams[0]))
        folha.is_folha = True
        folha.buffer = deque(streams[0]) 
        return folha
        
    meio = len(streams) // 2
    no_esquerdo = construir_funil(streams[:meio])
    no_direito = construir_funil(streams[meio:])
    
    # O tamanho do buffer do pai suporta a soma dos filhos
    pai = NodeFunil(tamanho_buffer=no_esquerdo.tamanho_buffer + no_direito.tamanho_buffer)
    pai.esquerda = no_esquerdo
    pai.direita = no_direito
    
    return pai


def funnel_sort(arr):
    """
    Função principal do Funnel Sort.
    """
    n = len(arr)
    
    # Caso base: Arrays muito pequenos não compensam o overhead do funil.
    # Usamos a ordenação nativa (simulando um base-case de algoritmo).
    if n <= 16:
        return sorted(arr)
    
    # Divisão: A teoria dita dividir em K segmentos, onde K é aprox. a raiz cúbica de N.
    # Cada segmento terá tamanho aproximado de N^(2/3).
    k = max(2, int(math.ceil(n ** (1 / 3))))
    tamanho_segmento = int(math.ceil(n / k))
    
    segmentos_ordenados = []
    
    # Passo Recursivo: Ordena os sub-segmentos
    for i in range(k):
        inicio = i * tamanho_segmento
        fim = min((i + 1) * tamanho_segmento, n)
        if inicio < fim:
            # Recursão para ordenar as menores partes
            segmento = funnel_sort(arr[inicio:fim])
            segmentos_ordenados.append(segmento)
            
    # Mesclagem: Constrói o funil e puxa os dados ordenados da raiz
    raiz_funil = construir_funil(segmentos_ordenados)
    resultado = []
    
    # Executa o "Lazy Fill" na raiz até que toda a árvore esvazie
    while not raiz_funil.esta_esgotado():
        raiz_funil.preencher()
        while len(raiz_funil.buffer) > 0:
            resultado.append(raiz_funil.buffer.popleft())
            
    return resultado

# ==========================================
# 3. ROTINAS DE TESTE E VALIDAÇÃO
# ==========================================

def executar_testes():
    """
    Testa o algoritmo com diferentes tipos de entradas e exibe
    os resultados ANTES e DEPOIS da execução.
    """
    import random

    # Definindo 4 casos de teste diferentes para validar a robustez
    testes = {
        "1. Array Aleatório": [random.randint(0, 100) for _ in range(25)],
        "2. Array Já Ordenado": [i for i in range(1, 21)],
        "3. Array em Ordem Inversa": [i for i in range(20, 0, -1)],
        "4. Array com Elementos Repetidos": [5, 2, 9, 5, 2, 3, 5, 9, 1, 1, 4]
    }

    print("-" * 50)
    print("INICIANDO BATERIA DE TESTES - FUNNEL SORT")
    print("-" * 50)

    for nome_teste, dados in testes.items():
        print(f"\n--- {nome_teste} ---")
        
        # Apresenta o resultado ANTES
        print(f"ANTES da execução  : {dados}")
        
        # Executa a ordenação
        dados_ordenados = funnel_sort(dados)
        
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
            array_usuario_ordenado = funnel_sort(array_usuario)
            print(f"DEPOIS da execução : {array_usuario_ordenado}")
        except ValueError:
            print("Entrada inválida. Certifique-se de digitar apenas números inteiros.")

if __name__ == "__main__":
    executar_testes()