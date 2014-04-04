__author__ = 'thvoidedline'

from Constants import *
from GuiTextbox import Textbox
from GuiListbox import GuiListbox
from GuiWindow import GuiWindow
from GuiText import GuiText
from GuiButton import GuiButton
from GuiObjSearchTextbox import ObjSearchTextbox


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
    if obj_type == OBJ_S_TXT_BOX:
        return ObjSearchTextbox(var_dict)

    print("Unknown gui object type passed to factory")
    return None