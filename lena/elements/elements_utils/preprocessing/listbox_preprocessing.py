import cv2
import numpy as np
from PIL import Image as PIL_Image
from sklearn.preprocessing import MinMaxScaler

from lena.elements.features.scroll_element_features import ScrollElementDetectionsFeatures
from lena.elements.objects.roi_element import RoiElement
from lena.elements.objects.element import Element
from lena.elements.objects.listbox_element import ListBoxElement
from lena.utils.config_manager import ConfigManager
from lena.utils.image_processing import filters_helper, morphological_helpers


class ListboxPreprocessing:
    def __init__(self, model_for_common_elements, model_for_listbox, common_element_features,
                 scroll_buttons_patterns, shift_threshold_for_scrolls):
        self.model_for_common_elements = model_for_common_elements
        self.__model_for_listbox = model_for_listbox
        self.__scroll_element_features = ScrollElementDetectionsFeatures(common_element_features,
                                                                         scroll_buttons_patterns,
                                                                         shift_threshold_for_scrolls)

    def image_processing_for_listbox(self, image):
        grey_ = filters_helper.convert_to_grayscale(image)
        grey_ = filters_helper.LevelsCorrection(grey_, ConfigManager().config.elements_parameters.listbox.preprocessing["level_correction_1"])
        grey_ = filters_helper.LevelsCorrection(grey_, ConfigManager().config.elements_parameters.listbox.preprocessing["level_correction_2"])
        grey_ = morphological_helpers.erosion(grey_)
        grey_ = filters_helper.LevelsCorrection(grey_, ConfigManager().config.elements_parameters.listbox.preprocessing["level_correction_3"])
        grey_ = filters_helper.LevelsCorrection(grey_, ConfigManager().config.elements_parameters.listbox.preprocessing["level_correction_4"])

        ret, grey_ = filters_helper.threshold(grey_, ConfigManager().config.elements_parameters.listbox.preprocessing["threshold_min"],
                                              ConfigManager().config.elements_parameters.listbox.preprocessing["threshold_max"])

        return grey_

    def prepare_features_for_listbox(self, image):
        grey_ = filters_helper.convert_to_grayscale(image)
        colours = filters_helper.calculate_white_colour(grey_)
        prepared_img = self.image_processing_for_listbox(grey_)

        #general_helpers.show(prepared_img)

        train_image_dimension = ConfigManager().config.elements_parameters.listbox.preprocessing["sample_dimension"]
        resized_prepared_img = np.array(PIL_Image.fromarray(prepared_img).resize(tuple(train_image_dimension), PIL_Image.BICUBIC))

        scaler = MinMaxScaler()
        resized_prepared_img = scaler.fit_transform(resized_prepared_img)

        image_features = np.array(resized_prepared_img)
        image_features = image_features.reshape(image_features.shape[0], -1).flatten()

        concatenated_features = np.concatenate((image_features, colours))

        return concatenated_features

    def get_contours_for_listbox(self, image):
        results = []

        grey_ = self.image_processing_for_listbox(image)

        min_w = ConfigManager().config.elements_parameters.listbox.contours_parameters["min_w"]
        max_w = ConfigManager().config.elements_parameters.listbox.contours_parameters["max_w"]
        min_h = ConfigManager().config.elements_parameters.listbox.contours_parameters["min_h"]
        max_h = ConfigManager().config.elements_parameters.listbox.contours_parameters["max_h"]
        contours, hierarchy = cv2.findContours(grey_, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        for i in range(len(contours)):
            x, y, w, h = cv2.boundingRect(contours[i])
            if (min_w < w < max_w and min_h < h < max_h):
                parent_index = hierarchy[0][i][3]
                #print(parent_index)

                # the parent contour may turn out to be the global contour, i.e., it can be excluded
                # check the parent even if its parent index is not equal to "-1"
                if(parent_index != -1):
                    temp_parent_x, temp_parent_y, temp_parent_w, temp_parent_h = cv2.boundingRect(contours[parent_index])
                    if(temp_parent_w > w * 1.5 or temp_parent_h > h * 1.5):
                        results.append((x, y, w, h))
                        #cv2.drawContours(screenshot, [contours[i]], -1, (0, 255, 0), 1)

        #general_helpers.show(screenshot)

        #DEBUG - most likely no need to filter. Cleared through contours.
        #filtered_contours = contours_helper.remove_similar_contours(results, 0.1)
        filtered_contours = results

        return filtered_contours
