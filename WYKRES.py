import matplotlib.pyplot as plt
import numpy as np
import math

# Wczytaj dane z pliku .dat
with open('aaa.dat', 'r') as file:
    lines = file.readlines()

# Wyciągnij ostatni wiersz z informacją o funkcji uproszczonej
last_line = lines[-1]

# Wyodrębnij funkcję uproszczoną z wiersza
simplified_function = last_line.split(',')[5]

# Przygotuj funkcję do obliczeń za pomocą numpy
def custom_eval(x):
    try:
        x1 = x  # Zmienna X1
        custom_formula_result = math.sin(x) + math.cos(x)  # Obliczenie wyniku dla własnego wzoru
        result = eval(simplified_function.replace('X1', str(x1))) + custom_formula_result
        return result
    except ZeroDivisionError:
        return None  # Możesz obsłużyć dzielenie przez zero zwracając np. None

# Przygotuj dane do wykresu
x = np.linspace(0, 10, 100)  # Zakres x
y_custom_formula = [math.sin(x_val) + math.cos(x_val) for x_val in x]  # Wynik własnego wzoru
y_simplified_function = [custom_eval(x_val) for x_val in x]  # Oblicz wartości funkcji uproszczonej dla każdego x

# Stwórz wykres z dwoma krzywymi
plt.plot(x, y_custom_formula, label='Własny wzór', color='blue')
plt.plot(x, y_simplified_function, label='Funkcja uproszczona', color='red')

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Wykres funkcji')
plt.grid(True)

# Wyświetl legendę
plt.legend()

# Wyświetl wykres
plt.show()
