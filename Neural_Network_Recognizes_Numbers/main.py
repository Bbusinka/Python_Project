import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import tensorflow as tf

# Ładowanie danych: pobierany jest zestaw danych MNIST
mnist = tf.keras.datasets.mnist
# Następnie dane są dzielone na zestawy treningowe i testowe
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Normalizacja danych: Obrazy cyfr są normalizowane, co sprowadza wartości pikseli do zakresu od 0 do 1.
x_train = tf.keras.utils.normalize(x_train, axis=1)
x_test = tf.keras.utils.normalize(x_test, axis=1)

# Tworzenie modelu:

model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28,28,1)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics='accuracy')

# Trenowanie modelu: Model jest trenowany na danych treningowych, odbywa się 5 treningów
model.fit(x_train, y_train, epochs=5)
#Zapisywanie modelu
model.save('handwritten.model')
model = tf.keras.models.load_model('handwritten.model')
# Ocena modelu na testowym zbiorze danych
loss, accuracy = model.evaluate(x_test, y_test)
# Wyświetlanie wartośći straty w zestawie danych testowych
print(loss)
# Wyświetlanie wartośći precyzji w testowym zbiorze danych
print(accuracy)

# Następuje pętla, która sprawdza istnienie plików obrazów

image_number = 1
while os.path.isfile(f"images/pic{image_number}.png"):
    try:
        img = cv2.imread(f"images/pic{image_number}.png")[:, :, 0]
        img = np.invert(np.array([img]))
        prediction = model.predict(img)
        print(f"This digit №{image_number} is probably a {np.argmax(prediction)}")
        plt.imshow(img[0], cmap=plt.cm.binary)
        plt.show()
    except:
        print("Error!")
    finally:
        image_number += 1

#Zwalnianie zasobów i zamykanie
tf.keras.backend.clear_session()

