import aug
import cv2
import numpy as np

from PIL import Image


class AlphaBlender:
    def __init__(self, img, generator, transformation_ops):
        self.background = img
        self.generator = generator
        self.transformation_ops = transformation_ops
        self.background = cv2.cvtColor(self.background, cv2.COLOR_RGB2RGBA)

        if self.generator.get_font_type() in ["dotted", "normal"]:
            self.foreground = np.zeros(self.background.shape, dtype=np.uint8)
            self.foreground[:, :, 0:3] = np.average(img)
            self.insert_task = self.insert_with_blending_into_foreground
        else:
            self.foreground = self.background
            self.insert_task = self.default_insert_into_foreground

    def insert_into_foreground(self, img, date_crop, random_p1):
        self.insert_task(img, date_crop, random_p1)

    def insert_with_blending_into_foreground(self, background, crop, left_top_point):
        """ Insert single crop into drawing with blending. """
        crop_bg = np.zeros(crop.shape)
        crop_bg[:, :, 0:3] = np.average(background)

        crop = np.int16(crop)
        crop[:, :, 0:3] = np.where(crop[:, :, 0:3] < crop_bg[:, :, 0:3], crop[:, :, 0:3], crop_bg[:, :, 0:3])
        crop = np.uint8(crop)

        self.foreground[left_top_point[1]:left_top_point[1] + crop.shape[0],
                        left_top_point[0]:left_top_point[0] + crop.shape[1]] = crop

    def default_insert_into_foreground(self, background, crop, left_top_point):
        """ Insert single crop into drawing. """
        crop = cv2.cvtColor(crop, cv2.COLOR_RGB2RGBA)
        self.foreground[left_top_point[1]:left_top_point[1] + crop.shape[0],
                        left_top_point[0]:left_top_point[0] + crop.shape[1]] = crop

    def get_composite_img(self):
        """ Blend drawing and background """
        ops_pipeline = self.transformation_ops.foreground_ops
        if not ops_pipeline:
            return None

        # apply foreground transformations and join two images
        self.foreground = ops_pipeline.apply(aug.Sample(image=self.foreground.copy())).image
        foreground_pil = Image.fromarray(self.foreground)
        background_pil = Image.fromarray(self.background)
        composite = Image.alpha_composite(background_pil, foreground_pil)
        composite = np.array(composite)
        composite = cv2.cvtColor(composite, cv2.COLOR_RGBA2RGB)

        return composite
