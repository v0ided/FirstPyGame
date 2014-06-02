__author__ = 'thvoidedline'


class BuildManager():
    def __init__(self, spawn_func):
        self.spawn_func = spawn_func

    def check_build(self, build):
        if len(build.built) > 0:
            print('building.')
            for output in build.built:
                var_dict = {}
                var_dict['type'] = 'part'
                var_dict['x'] = build.output_area.x
                var_dict['y'] = build.output_area.y
                var_dict['w'] = 0
                var_dict['h'] = 0
                var_dict['gravity'] = 'True'
                var_dict['collide'] = 'False'
                var_dict['layer'] = '15'
                var_dict['name'] = output
                var_dict['quality'] = 10
                self.spawn_func(var_dict)