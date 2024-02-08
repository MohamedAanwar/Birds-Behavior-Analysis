import numpy as np
import tensorflow as tf
from keras.layers import Flatten, Dense
from tensorflow.keras.applications import ResNet50, MobileNet, VGG16, VGG19
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam

class CNNModelBuilder:
    def __init__(self, input_shape, num_classes, modelName='vgg16'):
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.modelName = modelName
        self.model = self.build_model()

    def build_model(self):
        if self.modelName == 'vgg16':
            base_model = VGG16(weights='imagenet',
                            include_top=False, input_shape=self.input_shape)
        elif self.modelName == 'vgg19':
            base_model = VGG19(weights='imagenet',
                            include_top=False, input_shape=self.input_shape)
        elif self.modelName == 'resnet':
            base_model = ResNet50(weights='imagenet',
                            include_top=False, input_shape=self.input_shape)
        elif self.modelName == 'mobilenet':
            base_model = MobileNet(weights='imagenet',
                            include_top=False, input_shape=self.input_shape)
        else:
            base_model = VGG16(weights='imagenet',
                            include_top=False, input_shape=self.input_shape)
        
        x = Flatten()(base_model.output)
        x = Dense(128, activation='relu')(x)
        output = Dense(self.num_classes, activation='softmax')(x)

        model = Model(inputs=base_model.input, outputs=output)

        # Freeze the layers of the pre-trained model
        for layer in base_model.layers:
            layer.trainable = False

        return model

    def compile_model(self):
        self.model.compile(loss='categorical_crossentropy',
                        optimizer=Adam(lr=0.0001), metrics=['accuracy'])

    def train_model(self, train_dir, batch_size, epochs):
        try:
            
            if self.modelName == 'vgg16':
                usedModel='vgg16'
                train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
                    preprocessing_function=tf.keras.applications.vgg16.preprocess_input)
            elif self.modelName == 'vgg19':
                usedModel='vgg19'
                train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
                    preprocessing_function=tf.keras.applications.VGG19.preprocess_input)
            elif self.modelName == 'resnet':
                usedModel='resnet'
                train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
                    preprocessing_function=tf.keras.applications.resnet.preprocess_input)
            elif self.modelName == 'mobilenet':
                usedModel='mobilenet'
                train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
                    preprocessing_function=tf.keras.applications.mobilenet.preprocess_input)
            else:
                usedModel='vgg16'
                train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
                    preprocessing_function=tf.keras.applications.vgg16.preprocess_input)
                
            print('Training using:',usedModel)

            train_generator = train_datagen.flow_from_directory(directory=train_dir,
                                                                target_size=self.input_shape[:2],
                                                                batch_size=batch_size,
                                                                class_mode='categorical',
                                                                shuffle=True)

            self.model.fit(train_generator,
                           steps_per_epoch=train_generator.samples // batch_size,
                        epochs=epochs)
        except Exception as ex:
            print(ex)
            return ex

    def save_model(self, model_path):
        try:
            self.model.save(model_path)
        except Exception as ex:
            print(ex)
            return ex

    def load_model(self, model_path):
        try:
            self.model = tf.keras.models.load_model(model_path)
        except Exception as ex:
            print(ex)
            return ex

    def predict(self, image_path):
        try:
            image = tf.keras.preprocessing.image.load_img(
                image_path, target_size=self.input_shape[:2])
            image = tf.keras.preprocessing.image.img_to_array(image)
            image = np.expand_dims(image, axis=0)
            image = image / 255.0
            prediction = self.model.predict(image)
            class_index = np.argmax(prediction)
            return class_index
        except Exception as ex:
            print(ex)
            return ex
