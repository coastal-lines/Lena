from lena.elements.objects.element import Element
from lena.utils.image_processing import ocr_helper, augmentation, filters_helper

class ButtonElement(Element):
    def __init__(self, label, prediction_value, roi):
        super().__init__(label, prediction_value, roi)
        self.__text = None

    def prepare_roi_and_set_text(self):
        img = filters_helper.convert_to_grayscale(super().get_roi_element().get_roi())
        _, img = filters_helper.threshold(img, 127, 255)
        img = augmentation.bicubic_resize(img, (img.shape[1] * 1, img.shape[0] * 1))

        #DEBUG
        #files_helper.save_image(img)
        self.__text = ocr_helper.get_text(img, "--psm 3 --oem 3").replace(" ", "").replace("\n", "")
        print("button text: ", self.__text)

    def get_text(self):
        return self.__text