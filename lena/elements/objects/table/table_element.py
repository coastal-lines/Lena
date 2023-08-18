from typing import Optional

from lena.elements.objects.roi_element import RoiElement
from lena.elements.objects.element import Element
from lena.elements.objects.scroll_element import ScrollElement
from lena.elements.objects.table.table_cells_element import TableCellsElement


class TableElement(Element):
    def __init__(self, label: str, prediction_value: float, roi: RoiElement, h_scroll, v_scroll, cells_area_element: TableCellsElement):
        super().__init__(label, prediction_value, roi)
        self.__h_scroll = h_scroll
        self.__v_scroll = v_scroll
        self.__cells_area_element = cells_area_element
        self.__full_table_area: Optional[TableElement] = None

    def add_scroll(self, label: str, prediction_value: str, roi: RoiElement, first_button: Element,
                   second_button: Element):
        if(label == ElementTypesEnum.h_scroll.name):
            self.__h_scroll = ScrollElement(label, prediction_value, roi, first_button, second_button)

        elif(label == ElementTypesEnum.v_scroll.name):
            self.__v_scroll = ScrollElement(label, prediction_value, roi, first_button, second_button)

    def set_full_table_area(self, roi: RoiElement, cells_area_element):
        self.__full_table_area = TableElement("table", 1.0, roi, None, None, cells_area_element)