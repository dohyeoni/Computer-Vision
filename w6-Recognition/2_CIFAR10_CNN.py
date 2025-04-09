import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from keras import models, layers, losses, optimizers, callbacks
from keras.models import Sequential
from keras.datasets import cifar10
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

import matplotlib.pyplot as plt


# 50,000 training data set / 10,000 test data set
(train_images, train_labels), (test_images, test_labels) = cifar10.load_data()
train_images = train_images.reshape((50000, 32, 32, 3))
test_images = test_images.reshape((10000, 32, 32, 3))

# 픽셀 값을 0~1 사이로 정규화
train_images, test_images= train_images/ 255.0, test_images/ 255.0

model = models.Sequential()

model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D(2, 2))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))

model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dropout(0.5))  # 50% 뉴런 비활성화
model.add(layers.Dense(10, activation='softmax'))

model.summary()

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(train_images, 
          train_labels, 
          epochs=15,
          validation_data=(test_images, test_labels))

# 테스트 데이터셋으로 모델 평가
test_loss, test_accuracy = model.evaluate(test_images, test_labels, verbose=2)

# 테스트 정확도 출력
print(f"Test Accuracy: {test_accuracy * 100:.2f}%")


class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']

# 5개 테스트 이미지에 대한 예측
predictions = model.predict(test_images[:5])

for i in range(5):
    plt.imshow(test_images[i])
    plt.title(f"예측: {class_names[np.argmax(predictions[i])]}")
    plt.axis('off')
    plt.show()
