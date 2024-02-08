import os
from ModelBuilder import CNNModelBuilder
if __name__ == '__main__':

    train_dir = r"D:\Modeling\Frames\chronic crow 2nd green blue object novelty TS h"

    input_shape = (128, 128, 3)
    classes_names = [d for d in os.listdir(
        train_dir) if os.path.isdir(os.path.join(train_dir, d))]
    num_classes = len(classes_names)

    # you can use vgg16,vgg19,resnet,mobilenet
    model = CNNModelBuilder(input_shape, num_classes,'resnet')  #You can choose model from [mobilenet-resnet-vgg16-vgg19]

    model.compile_model()

    batch_size = 32
    epochs = 50

    model.train_model(train_dir, batch_size, epochs)

    model_path = r'D:\Modeling\Traning_Model\chronic crow 2nd green blue object novelty TS h.h5'
    model.save_model(model_path)
