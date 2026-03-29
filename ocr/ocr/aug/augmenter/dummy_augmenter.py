""" Generate synthetic dummy text. """
import random
import cv2
import aug

from ocr.aug.augmenter.augmenter import Augmenter
from vision.aug.transformations.transformation import Transformation


class DummyTextAugmenter(Augmenter):
    def __init__(self):
        super(DummyTextAugmenter, self).__init__(op_type="dummy")

    def get_synthetic_dummy_text(self):
        """ Generate dummy text as image. """
        clean_img, available_areas = random.choice(self.bg_data)
        clean_img = cv2.imread(clean_img)
        if clean_img is None:
            return None

        text_value = self.generator.get_dummy_text()
        # get background from real data set
        bg = self.position_finder.get_widest_crop(clean_img, available_areas, height=30)
        if bg is None:
            return None

        # render text images
        font = self.generator.load_font(font_type="normal", font_dir="normal-latin", font_size=random.randint(35, 80))
        text_img = self.generator.get_text_img(font, text_value, bg=bg)
        text_img = Transformation.fit_borders(text_img)

        # when generator is initialized, set font type (dotted, embossed, printed)
        self.font_type = self.generator.get_font_type()

        # apply text transformations
        ops_pipeline = self.transformation_ops[self.font_type].text_ops
        if ops_pipeline:
            text_img = ops_pipeline.apply(aug.Sample(image=text_img.copy())).image

        bg = cv2.resize(bg, (text_img.shape[1], text_img.shape[0]), interpolation=cv2.INTER_CUBIC)

        text_img = self.add_real_background_to_synthetic_crop(text_img, bg)

        # apply composite transformations
        ops_pipeline = self.transformation_ops[self.font_type].composite_ops
        if ops_pipeline:
            text_img = ops_pipeline.apply(aug.Sample(image=text_img.copy())).image

        return text_img, text_value


if __name__ == '__main__':
    dt = DummyTextAugmenter()
    while True:
        synth_text, _ = dt.get_synthetic_dummy_text()
        cv2.imshow("sss", synth_text)
        cv2.waitKey()
