import numpy as np
import matplotlib.pyplot as plt


# Definicja funkcji r(theta)
def r(theta):
    return np.sin(2 * theta)

# Zakres wartości theta od 0 do 2*pi
theta_values = np.linspace(0, 2 * np.pi, 1000)

# Obliczenie wartości r dla każdej wartości theta
r_values = r(theta_values)

# Konwersja z współrzędnych biegunowych na kartezjańskie
x_values = r_values * np.cos(theta_values)
y_values = r_values * np.sin(theta_values)


# Narysowanie wykresu
plt.figure(figsize=(8, 8))
plt.plot(x_values, y_values, color='blue')
plt.title('Krzywa czterolistna: r(θ) = sin(2θ)')
plt.xlabel('x')
plt.ylabel('y')
plt.axis('equal')
plt.grid(True)
plt.show()
