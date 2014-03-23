from CraneObject import CraneObject
from LevelObject import LevelObject
from Player import PlayerSprite


def ObjFactory(obj_type, var_dict):
    if obj_type.lower() == 'levelobject':
        return LevelObject(var_dict)
    elif obj_type.lower() == 'player':
        return PlayerSprite(var_dict)
    elif obj_type.lower() == 'craneobject':
        return CraneObject(var_dict)
    else:
        print("Unknown type sent to object factory.")

