from Objects.CraneObject import CraneObject
from Objects.LevelObject import LevelObject
from Objects.Platform import Platform
from Objects.BuildProcess import BuildProcess
from Objects.Part import Part
from Player import PlayerSprite


def ObjFactory(obj_type, var_dict):
    if obj_type.lower() == 'levelobject':
        return LevelObject(var_dict)
    elif obj_type.lower() == 'player':
        return PlayerSprite(var_dict)
    elif obj_type.lower() == 'craneobject':
        return CraneObject(var_dict)
    elif obj_type.lower() == 'platform':
        return Platform(var_dict)
    elif obj_type.lower() == 'buildprocess':
        return BuildProcess(var_dict)
    elif obj_type.lower() == 'part':
        return Part(var_dict)
    else:
        print("Unknown type sent to object factory.")