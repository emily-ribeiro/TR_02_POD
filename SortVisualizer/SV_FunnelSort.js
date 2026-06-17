async function funnelSort(elements) {
  const n = elements.length;

  // Funnel Sort usa a ideia de um "lazy funnel" (heap binário implícito)
  // Fase 1: Constrói o heap máximo (max-heapify)
  for (let i = Math.floor(n / 2) - 1; i >= 0; i--) {
    await heapify(elements, n, i);
  }

  // Fase 2: Extrai elementos do heap um a um
  for (let i = n - 1; i > 0; i--) {
    await swap(0, i);
    await heapify(elements, i, 0);
  }
}

async function heapify(elements, size, root) {
  let largest = root;
  const left  = 2 * root + 1;
  const right = 2 * root + 2;

  if (left < size && getValue(elements[left]) > getValue(elements[largest])) {
    largest = left;
  }

  if (right < size && getValue(elements[right]) > getValue(elements[largest])) {
    largest = right;
  }

  if (largest !== root) {
    await updateBox(elements, root, largest);
    await swap(root, largest);
    await heapify(elements, size, largest);
  } else {
    await updateBox(elements, root);
  }
}