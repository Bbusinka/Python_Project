import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Funkcje definiujące rozmaitości algebraiczne
def func1(x, y):
    return x**2 + y**2

def func2(x, y):
    return np.sqrt(x**2 + y**2)

def func3(x, y):
    return -x**2 + y**2

def func4(x, y):
    z = np.zeros_like(x)
    z[(x == 0) | (y == 0)] = 0
    return z


# Tworzenie siatki punktów
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
x, y = np.meshgrid(x, y)

# Obliczanie wartości z dla każdej funkcji
z1 = func1(x, y)
z2 = func2(x, y)
z3 = func3(x, y)
z4 = func4(x, y)

# Rysowanie wykresów
fig = plt.figure(figsize=(16, 12))

# Wykres 1
ax1 = fig.add_subplot(221, projection='3d')
ax1.plot_surface(x, y, z1, cmap='viridis')
ax1.set_title('V(z - x^2 - y^2)')

# Wykres 2
ax2 = fig.add_subplot(222, projection='3d')
ax2.plot_surface(x, y, z2, cmap='viridis')
ax2.set_title('V(z^2 - x^2 - y^2)')

# Wykres 3
ax3 = fig.add_subplot(223, projection='3d')
ax3.plot_surface(x, y, z3, cmap='viridis')
ax3.set_title('V(z - x^2 + y^2)')

# Wykres 4
ax4 = fig.add_subplot(224, projection='3d')
ax4.plot_surface(x, y, z4, cmap='viridis')
ax4.set_title('V(xz, yz)')

plt.show()
