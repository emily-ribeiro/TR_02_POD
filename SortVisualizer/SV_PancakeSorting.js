function flip(arr, k) {
    let left = 0;
    while (left < k) {
        [arr[left], arr[k]] = [arr[k], arr[left]];
        k--;
        left++;
    }
}

function max_index(arr, k) {
    let index = 0;
    for (let i = 0; i < k; i++) {
        if (arr[i] > arr[index]) {
            index = i;
        }
    }
    return index;
}

function pancakeSort(arr) {
    let n = arr.length;
    while (n > 1) {
        let maxdex = max_index(arr, n);
        if (maxdex != n) {
            flip(arr, maxdex);
            flip(arr, n-1);
        }
        n--;
    }
}