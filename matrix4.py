import numpy as np
from multiprocessing import Pool, cpu_count

# Функция перемножения элементов матриц
def element(index, A, B):
    i, j = index
    res = 0
    N = len(A[0]) or len(B)
    for k in range(N):
        res += A[i][k] * B[k][j]
    return res

# Функция для распараллеливания вычислений
def parallel_multiply_matrices(A, B, output_file):
    if len(A[0]) != len(B):
        raise ValueError("Количество столбцов матрицы A должно быть равно количеству строк матрицы B")

    # Создаем список индексов для каждого элемента результирующей матрицы
    indices = [(i, j) for i in range(len(A)) for j in range(len(B[0]))]

    # Открываем промежуточный файл для записи
    with open(output_file, 'w') as f:
        # Создаем пул процессов, используя количество доступных ядер процессора
        with Pool(cpu_count()) as pool:
            # Выполняем перемножение элементов матриц параллельно с помощью функции element
            for index, element_result in zip(indices, pool.starmap(element, [(index, A, B) for index in indices])):
                i, j = index
                # Записываем результат в промежуточный файл сразу после вычисления
                f.write(f"({i}, {j}): {element_result}\n")

    # Читаем промежуточный файл и формируем результирующую матрицу
    result_matrix = []
    with open(output_file, 'r') as f:
        for line in f:
            # Преобразуем строку обратно в числа
            element_result = int(line.split(': ')[1])
            result_matrix.append(element_result)

    # Преобразуем список результатов в матрицу
    result_matrix = np.reshape(result_matrix, (len(A), len(B[0])))

    return result_matrix

if __name__ == '__main':
    a, b = map(int, input("For matrix1, a, b: ").split())
    c, d = map(int, input("For matrix2, c, d: ").split())
    output_file = input("Enter the name of the output file: ")

    # Создаем две случайные матрицы размером a x b и c x d
    A = np.random.randint(0, 10, size=(a, b))
    B = np.random.randint(0, 10, size=(c, d))

    try:
        # Выполняем перемножение матриц с использованием многопроцессорности
        result = parallel_multiply_matrices(A, B, output_file)

        # Выводим результат
        print("Matrix A:")
        print(A)
        print("\nMatrix B:")
        print(B)
        print("\nResult:")
        print(result)
    except ValueError as e:
        print(e)
