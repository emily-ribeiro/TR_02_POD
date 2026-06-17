// ─────────────────────────────────────────────
// CARTESIAN TREE SORT  (Levcopoulos-Petersson)
// Algoritmo adaptativo: melhor em dados parcialmente ordenados.
// Complexidade: O(n log n) geral, O(n log Osc) em dados quase ordenados.
// ─────────────────────────────────────────────

// Nó da árvore cartesiana (min-heap por valor)
class CartesianNode {
  constructor(index, value) {
    this.index = index;   // posição original no array
    this.value = value;
    this.left  = null;
    this.right = null;
    this.parent = null;
  }
}

// Sobe pela árvore procurando o ancestral cujo valor < x
function findLowest(node, x) {
  if (node === null) return null;
  if (node.value < x) return node;
  return findLowest(node.parent, x);
}

// Constrói a árvore cartesiana (min-heap) a partir dos valores atuais
function buildCartesianTree(elements) {
  let root = null;
  let last = null;

  for (let i = 0; i < elements.length; i++) {
    const val  = getValue(elements[i]);
    const node = new CartesianNode(i, val);

    if (root === null) {
      root = node;
      last = node;
      continue;
    }

    const z = findLowest(last, val);

    if (z === null) {
      // novo nó se torna a nova raiz
      node.left  = root;
      root.parent = node;
      root = node;
    } else {
      // insere como filho direito de z
      node.left   = z.right;
      if (z.right) z.right.parent = node;
      z.right     = node;
      node.parent = z;
    }

    last = node;
  }

  return root;
}

// Fila de prioridade mínima simples (min-heap sobre CartesianNode)
class MinPQ {
  constructor() { this.heap = []; }

  push(node) {
    this.heap.push(node);
    this._bubbleUp(this.heap.length - 1);
  }

  pop() {
    const top  = this.heap[0];
    const last = this.heap.pop();
    if (this.heap.length > 0) {
      this.heap[0] = last;
      this._sinkDown(0);
    }
    return top;
  }

  get size() { return this.heap.length; }

  _bubbleUp(i) {
    while (i > 0) {
      const p = (i - 1) >> 1;
      if (this.heap[p].value <= this.heap[i].value) break;
      [this.heap[p], this.heap[i]] = [this.heap[i], this.heap[p]];
      i = p;
    }
  }

  _sinkDown(i) {
    const n = this.heap.length;
    while (true) {
      let smallest = i;
      const l = 2 * i + 1, r = 2 * i + 2;
      if (l < n && this.heap[l].value < this.heap[smallest].value) smallest = l;
      if (r < n && this.heap[r].value < this.heap[smallest].value) smallest = r;
      if (smallest === i) break;
      [this.heap[smallest], this.heap[i]] = [this.heap[i], this.heap[smallest]];
      i = smallest;
    }
  }
}

// ── Entrada principal ──────────────────────────────────────────────────────
async function cartesianTreeSort(elements) {
  const n = elements.length;

  // Fase 1: constrói a árvore cartesiana com os valores originais
  const treeRoot = buildCartesianTree(elements);

  // Mantém mapa: posição atual no array → posição lógica original
  // Para que os swaps do visualizador façam sentido, rastreamos onde
  // cada elemento parou usando um array de índices.
  const pos = Array.from({ length: n }, (_, i) => i);  // pos[orig] = atual
  const cur = Array.from({ length: n }, (_, i) => i);  // cur[atual] = orig

  // Fase 2: extrai o mínimo da fila de prioridade em ordem crescente,
  //         colocando-o na posição correta do array (in-place).
  const pq = new MinPQ();
  pq.push(treeRoot);

  for (let i = 0; i < n; i++) {
    // Pega o menor elemento disponível
    const node = pq.pop();

    // Empurra filhos do nó removido para a fila (percurso pré-ordem)
    if (node.left)  { await updateBox(elements, pos[node.left.index]);  pq.push(node.left);  }
    if (node.right) { await updateBox(elements, pos[node.right.index]); pq.push(node.right); }

    // Posição atual do elemento que queremos colocar em i
    const from = pos[node.index];

    if (from !== i) {
      // Troca visualmente e atualiza mapa de posições
      await swap(from, i);

      const displaced = cur[i];          // quem estava em i
      pos[displaced]   = from;
      cur[from]        = displaced;
      pos[node.index]  = i;
      cur[i]           = node.index;
    } else {
      await updateBox(elements, i);
    }
  }
}