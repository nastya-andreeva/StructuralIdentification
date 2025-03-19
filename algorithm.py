import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Исходный код
file_path = "Москва_2021.txt"
with open(file_path, 'r') as file:
    data = file.read().splitlines()

# Преобразуем данные в целые числа
data = list(map(int, data))

# Создаем дискретный ряд распределения
un_data = set(data)  # Уникальные значения
un_val = sorted(un_data)  # Сортируем уникальные значения
freq = [data.count(i) for i in un_val]  # Частоты для каждого уникального значения

# Округляем уникальные значения (x) и частоты (y) до сотых
un_val = [round(val, 2) for val in un_val]
freq = [round(f, 2) for f in freq]

# Функции для вычисления средних
def avg1(a):
    return round((a[0] + a[-1]) / 2, 1)  # Среднее арифметическое первого и последнего элемента ((a1 + a_n)/2)

def avg2(a):
    return round((a[0] * a[-1]) ** 0.5, 1)  # Среднее геометрическое первого и последнего элемента (a1 * a_n)^(0.5)

def avg3(a):
    return round((2 * a[0] * a[-1]) / (a[0] + a[-1]), 1)  # Среднее гармоническое, модифицированное ((2*a1*a_n)/(a1 + a_n))

# Функция для линейной интерполяции
def experimental(x_s, y_exp, un_val, freq):
    if x_s not in un_val or y_exp != freq[un_val.index(x_s)]:
        for i in range(1, len(un_val)):
            if un_val[i-1] <= x_s <= un_val[i]:
                x_i = un_val[i-1]
                y_i = freq[i-1]
                x_next = un_val[i]
                y_next = freq[i]

                # Линейная интерполяция
                y_exp = y_i + (y_next - y_i) * (x_s - x_i) / (x_next - x_i)
                break
    return round(y_exp, 2)

# Используем функции для расчета зависимостей
dependencies = pd.DataFrame({
    'structure': ['y = ax + b', 'y = ax**b', 'y = ab**x', 'y = a + b/x', 'y = 1/(ax + b)', 'y = x/(ax + b)', 'y = a*ln(x) + b'],
    'x': [avg1(un_val), avg2(un_val), avg1(un_val), avg3(un_val), avg1(un_val), avg3(un_val), avg2(un_val)],
    'y': [avg1(freq), avg2(freq), avg2(freq), avg1(freq), avg3(freq), avg3(freq), avg1(freq)]
})

# Список для хранения результатов
y_exp_list = []
for i in range(len(dependencies)):
    # Вычисляем результат для каждой зависимости
    y_exp_list.append(experimental(dependencies['x'].iloc[i], dependencies['y'].iloc[i], un_val, freq))



# Добавляем результаты в DataFrame
dependencies['y_exp'] = y_exp_list

# Вычисляем отклонения Δs = |y̅s − ys|
dependencies['ds'] = abs(dependencies['y'] - dependencies['y_exp'])

# Вычисляем, какой вид зависимости имеет наименьшее отклонение Δs
min_ds_index = dependencies['ds'].idxmin()
min_ds = dependencies.loc[min_ds_index]

# Вычисляем отклонения в процентах по отношению к общей сумме частот
total_freq = sum(freq)
dependencies['ds, %'] = round(dependencies['ds'] / total_freq * 100, 2)

# Выводим зависимости с отклонениями
print("\nРезультаты с отклонениями Δs и отклонениями в процентах:")
print(dependencies)


##########################################################################




# Находим зависимость с минимальным отклонением
min_ds_id = dependencies[dependencies['ds'] == min(dependencies['ds'])].index[0]
print('Зависимость, которой соответствует минимальное значение отклонения: ', dependencies['structure'].iloc[min_ds_id], f' ({min_ds_id})')

# Определение показателя степени аппроксимирующего многочлена
def diff(data, order=1):   # Функция diff вычисляет разности для последовательности данных
    for _ in range(order):
        data = np.diff(data)
    return data

def polynomial_degree(data, lim_percent=2):
    lim = sum(data) * (lim_percent / 100)
    differences = data
    order = 0

    while True:
        differences = abs(diff(differences))
        max_difference = max(differences)
        if max_difference <= lim:
            break
        order += 1

    return order, max_difference, lim

# Пример использования функции polynomial_degree
order, max_difference, lim = polynomial_degree(freq)

# Выводим результаты
print(f"Показатель степени аппроксимирующего многочлена: {order+1}")
print(f"Максимальная разность: {max_difference}")
print(f"Пороговое значение (2% от суммы частот): {lim}")