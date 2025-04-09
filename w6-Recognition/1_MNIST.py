import tensorflow as tf
from tensorflow import keras
from keras.datasets import mnist
from tensorflow.keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense


# 데이터 불러오기
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# 0~255 범위를 0~1로 정규화
x_train = x_train / 255.0
x_test = x_test / 255.0

# 입력 형식: (batch_size, 28, 28) → (batch_size, 784)
x_train = x_train.reshape(-1, 28 * 28)
x_test = x_test.reshape(-1, 28 * 28)


# 모델 정의
model = Sequential([
    Dense(128, activation='relu', input_shape=(784,)),  # 은닉층
    Dense(10, activation='softmax')                     # 출력층: 숫자 0~9
])

# 컴파일
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# 훈련
model.fit(x_train, y_train, epochs=5, batch_size=32, validation_split=0.1)

# 테스트 세트에서 평가
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f'\n테스트 정확도: {test_acc:.4f}')
