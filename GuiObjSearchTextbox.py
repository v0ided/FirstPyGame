__author__ = 'thvoidedline'

from GuiTextbox import Textbox
from HelpFunctions import search_file


class ObjSearchTextbox(Textbox):
    def __init__(self, var_dict):
        Textbox.__init__(self, var_dict)
        try:
            self.data_path = var_dict['data_path']
        except KeyError:
            print('Not all required arguments passed to ObjSearchTextbox')

    def update(self):
        results = search_file(self.data_path, self.text)
        if self.attached:
            self.attached[0].update_list(results, self.changed)
        Textbox.update(self)