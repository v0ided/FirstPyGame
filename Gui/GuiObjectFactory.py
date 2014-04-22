__author__ = 'thvoidedline'

from Gui.GuiListbox import GuiListbox
from Gui.GuiText import GuiText
from Gui.GuiWindow import GuiWindow
from Gui.GuiButton import GuiButton
from Gui.GuiTextbox import Textbox
from Constants import *


def GuiObjFactory(obj_type, var_dict):
    if obj_type == TXT_BOX:
        return Textbox(var_dict)
    if obj_type == LIST_BOX:
        return GuiListbox(var_dict)
    if obj_type == WINDOW:
        return GuiWindow(var_dict)
    if obj_type == TEXT:
        return GuiText(var_dict)
    if obj_type == BUTTON:
        return GuiButton(var_dict)

    print("Unknown gui object type passed to factory")
    return None