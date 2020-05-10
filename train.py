import tensorflow.keras as tf
import tensorflow as kf
import numpy as np

class Model:
    def __init__(self):
        self. model = tf.Sequential()
        self.model.add(tf.layers.Conv2D(
                input_shape=[20,20,1],
                filters=32,
                kernel_size=5,
                strides=5,
                activation=kf.nn.tanh,
                padding='same',
                kernel_initializer=kf.keras.initializers.VarianceScaling()
                ))
        
        self.model.add(tf.layers.Conv2D(
                filters=64,
                kernel_size=3,
                strides=2,
                activation=kf.nn.tanh,
                padding='same',
                kernel_initializer=kf.keras.initializers.VarianceScaling()
                ))
        self.model.add(tf.layers.Conv2D(
                filters=128,
                kernel_size=3,
                strides=1,
                activation=kf.nn.tanh,
                padding='same',
                kernel_initializer=kf.keras.initializers.VarianceScaling()
                ))
        self.model.add(tf.layers.Flatten())
        self.model.add(tf.layers.Dense(
                 units=512,
                 activation=kf.nn.tanh,
                 kernel_initializer=kf.keras.initializers.VarianceScaling()
                 ))
        self.model.add(tf.layers.Dense(
                units=256,
                activation=kf.nn.tanh,
                kernel_initializer=kf.keras.initializers.VarianceScaling()
                ))
        self.model.add(tf.layers.Dense(
                units=44,
                kernel_initializer=kf.keras.initializers.VarianceScaling(),
                activation=kf.nn.softmax
                ))
        self.model.compile(optimizer=tf.optimizers.Adam(0.0005),loss=tf.losses.CategoricalCrossentropy(), metrics=['accuracy'])
        self.model.summary()

    def trainModel(self, x, y):
        h = self.model.fit(states, actions, batch_size=100, epochs=100, validation_data=[states, actions])

    def saveModel(self):
        self.model.save('model_save.h5')

    def loadModel(self, f):
        self.model = tf.load_model('model_save.h5')

    def predict(self, state):
        output = self.model.predict(state.reshape([1,1,20,20]))
        return np.argmax(output[0])
        
if __name__ == "__main__":
    m = Model()
    with np.load('./all_game/all_game.npz') as data:
         states  = data['arr_0']
         actions = data['arr_1']
    m.trainModel(states, actions)
    m.saveModel()
