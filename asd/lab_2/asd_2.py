import math
import random
import timeit
from tabulate import tabulate

STATS = {}

def insertion_sort(lst):
    comparisons = 0
    swaps = 0
    for i in range(1, len(lst)):
        key = lst[i]
        j = i - 1
        while j >= 0 and lst[j] > key:
            lst[j + 1] = lst[j]
            j -= 1
            comparisons += 1
            swaps += 1
        lst[j + 1] = key
        if j >= 0:
            comparisons += 1
    return lst, comparisons, swaps

def quicksort(lst):
    comparisons = 0
    swaps = 0
    def _quicksort(arr):
        nonlocal comparisons, swaps
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left, middle, right = [], [], []
        for x in arr:
            comparisons += 1
            if x < pivot:
                left.append(x)
                swaps += 1
            elif x == pivot:
                middle.append(x)
            else:
                right.append(x)
                swaps += 1
        return _quicksort(left) + middle + _quicksort(right)
    sorted_lst = _quicksort(lst)
    return sorted_lst, comparisons, swaps

def get_list(n, max_val=100):
    return [random.randint(1, max_val) for _ in range(n)]

def shortener(lst, chunk_size=5):
    if chunk_size > len(lst):
        return lst

    first_chunk = lst[:chunk_size]
    las_chunk = lst[-chunk_size:]

    return first_chunk + ['...'] + las_chunk

#теоретичне значення для С та М
def theoretical_values(n, func_name):
    if 'insertion' in func_name:
        return {'comps': round(((n - 1) * n) / 2), 'swaps': round(((n-1) * n) / 4)}
    elif 'quick' in func_name:
        value = round(n * math.log(n, 2))
        return {'comps': value, 'swaps': value}
    else:
        return {'comps': 0, 'swaps': 0}

def print_results(stats):
    for method, sizes in stats.items():
        table_data = []
        headers = ["N", "Перестановки (Екс.)", "Перестановки (Теор.)", "Співвідношення перестановок",
                   "Порівняння (Екс.)", "Порівняння (Теор.)", "Співвідношення порівнянь", "Час (с)"]
        for n, data in sizes.items():
            swaps = data['swaps']
            theo_swaps = data['theoretical']['swaps']
            comps = data['comps']
            theo_comps = data['theoretical']['comps']
            swaps_ratio = swaps / theo_swaps if theo_swaps else 0
            comps_ratio = comps / theo_comps if theo_comps else 0
            row = [n, swaps, theo_swaps, f"{swaps_ratio:.2f}",
                   comps, theo_comps, f"{comps_ratio:.2f}", data["time"]]
            table_data.append(row)
        print(method.replace('_', ' ').title())
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print("\n")

def main():
    list_100 = get_list(100)
    list_1k = get_list(1000, 1000)
    list_10k = get_list(10_000, 7000)

    for lst in (list_100, list_1k, list_10k):
        print(f"\n{len(lst)} елементів")
        print(f"\tДано список: {shortener(lst)}")
       
        start = timeit.default_timer()
        sorted_lst, comps, swaps = insertion_sort(lst.copy())
        elapsed = timeit.default_timer() - start
        print("\tСортування вставками:")
        print(f"\t\tВідсортований список: {shortener(sorted_lst)}")
        print(f"\t\tПорівняння: {comps}, Перестановки: {swaps}, Час: {elapsed:.6f} секунди")
        STATS['insertion_sort'] = STATS.get('insertion_sort', {})
        STATS['insertion_sort'][len(lst)] = {
            'comps': comps,
            'swaps': swaps,
            'time': round(elapsed, 4),
            'theoretical': theoretical_values(len(lst), 'insertion_sort')
        }
       
        start = timeit.default_timer()
        sorted_lst, comps, swaps = quicksort(lst.copy())
        elapsed = timeit.default_timer() - start
        print("\tШвидке сортування:")
        print(f"\t\tВідсортований список: {shortener(sorted_lst)}")
        print(f"\t\tПорівняння: {comps}, Перестановки: {swaps}, Time: {elapsed:.6f} секунди")
        STATS['quicksort'] = STATS.get('quicksort', {})
        STATS['quicksort'][len(lst)] = {
            'comps': comps,
            'swaps': swaps,
            'time': round(elapsed, 4),
            'theoretical': theoretical_values(len(lst), 'quicksort')
        }


    print("\nРезультати:\n")
    print_results(STATS)

if __name__ == '__main__':
    main()


