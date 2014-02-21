class Behavior():
    def __init__(self, conditions, action):
        self.conditions = conditions
        self.action = action

    def _check_conditions(self, obj1, obj2):
        if self.conditions(obj1, obj2):
            return True
        else:
            return False

    #Must Return True on Successfull use, False otherwise
    def behave(self, obj1, obj2, level):
        if self._check_conditions(obj1, obj2):
            self.action(obj1, obj2, level)
            return True
        else:
            return False