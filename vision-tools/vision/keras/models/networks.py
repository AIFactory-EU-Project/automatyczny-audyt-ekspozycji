import cv2
import numpy as np

from vision.imgproc import preprocess


class GeneralNeuralNetwork:

    def __init__(self, weights_path, classes, img_size=(224, 224, 3), pad_image=False, grayscale=False, model="mobilenet", activation="softmax"):
        # classifier works in another process,
        # so cannot import anything from keras in main process (beginning of this file) due to CUDA errors
        from vision.keras.models.models import get_model
        self.img_size = img_size[:2]
        self.pad_image = pad_image
        self.grayscale = grayscale
        self.model = get_model(model, weights=weights_path, class_number=classes, input_shape=img_size, activation=activation)

    def prepare(self, imgs):
        from keras.applications import imagenet_utils
    
        processed_imgs = []
        for img in imgs:
            if self.pad_image:
                img, _, _ = preprocess.pad_to_aspect_ratio(img, 1.0)

            img = cv2.resize(img, self.img_size, interpolation=cv2.INTER_AREA if max(img.shape) > max(self.img_size) else cv2.INTER_LINEAR)

            if self.grayscale:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

            img = imagenet_utils.preprocess_input(img.astype(np.float32), mode='tf')

            processed_imgs.append(img)

        return np.array(processed_imgs)

    def predict(self, imgs):
        if not isinstance(imgs, list):
            raise ValueError("Network can be run only on a list of images")

        imgs = self.prepare(imgs)
        return self.model.predict(imgs)
