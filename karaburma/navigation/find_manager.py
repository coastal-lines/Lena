from karaburma.navigation.template_matching.template_matching import TemplateMatchingElement
from karaburma.elements.objects.screenshot_element import ImageSourceObject
from karaburma.navigation.object_detection.base_find_actions import BaseFindActions
from karaburma.utils import general_helpers, files_helper, draw_helper


class FindManager(TemplateMatchingElement):

    def __init__(self, detection_mode: BaseFindActions):
        super().__init__()
        self.__detection_mode = detection_mode

    def __create_image_source(self, *args):
        if len(args) == 0:
            return ImageSourceObject(general_helpers.do_screenshot())
        else:
            return ImageSourceObject(files_helper.load_image(args[0]))

    def find_all_elements_in_base64image(self, base64image):
        image_source = ImageSourceObject(base64image)
        self.__detection_mode.find_all_elements(image_source)

        return image_source

    def find_all_elements(self, *args):
        image_source = self.__create_image_source(*args)
        self.__detection_mode.find_all_elements(image_source)

        return image_source

    def find_element(self, element_type, *args):
        image_source = self.__create_image_source(*args)
        self.__detection_mode.find_element(image_source, element_type)

        return image_source

    def find_table_and_expand(self, table_index: int=0, read_text_from_cells=False):
        if hasattr(self.__detection_mode, 'find_table_and_expand'):
            image_source = self.__create_image_source()
            self.__detection_mode.find_table_and_expand(image_source, table_index, read_text_from_cells)

            return image_source
        else:
            print("Method 'find Table and expand' not supported for this mode. \n Please use 'screenshot' mode.")

    def find_table_cell(self, column, row):
        if hasattr(self.__detection_mode, 'find_table_cell'):
            image_source = self.__create_image_source()
            self.__detection_mode.find_table_cell(image_source, column, row)
        else:
            print("Error: expand operations are not supported for current mode. Impossible to find custom cell.")

    def find_listbox_and_expand(self, listbox_index):
        image_source = None

        if hasattr(self.__detection_mode, 'find_listbox_and_expand'):
            image_source = self.__create_image_source()
            self.__detection_mode.find_listbox_and_expand(image_source, listbox_index)
        else:
            print("Operation not supported for this mode.")

        return image_source

    def find_element_by_patterns(self, patterns, mode, threshold, user_label, *args):
        image_source = self.__create_image_source(*args)
        super().find_element_by_patterns(patterns, mode, threshold, user_label, image_source)

        return image_source

    def find_all_elements_include_patterns(self, patterns, mode, threshold, user_label, *args):
        image_source_with_elements = self.find_all_elements(*args)
        super().find_element_by_patterns(patterns, mode, threshold, user_label, image_source_with_elements)

        return image_source_with_elements

    def find_all_elements_include_patterns_in_base64image(self, pattern, mode, threshold, user_label, base64image):
        image_source_with_elements = self.find_all_elements_in_base64image(base64image)
        super().find_element_by_pattern_in_base64image(pattern, mode, threshold, user_label, image_source_with_elements)

        return image_source_with_elements