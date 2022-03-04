import json


class to_JSON:
    def __init__(self):
        self.config = {
            "scan_size": 0,
            "img_pixel": 0,
            "line_rate": 0,
            "offset": {
                "x": 0,
                "y": 0
            },
            "set_point": 0,
            "sample_bias": 0,
            "PID": {
                "KP": 0,
                "KI": 0,
                "KD": 0
            }
        }

    def __init__(self, filename):
        with open(filename, 'r') as openfile:
            # Reading from json file
            json_object = json.load(openfile)
            self.config = json_object

    def output(self, filename):
        json_object = json.dumps(self.config, indent=4)
        with open(filename, "w") as outfile:
            outfile.write(json_object)

    def set_scan_size(self, scan_size):
        self.config.scan_size = scan_size

    def set_img_pixel(self, img_pixel):
        self.config.img_pixel = img_pixel

    def set_line_rate(self, line_rate):
        self.config.line_rate = line_rate

    def set_x_offset(self, x_offset):
        self.config.offset.x = x_offset

    def set_y_offset(self, y_offset):
        self.config.offset.y = y_offset

    def set_set_point(self, set_point):
        self.config.set_point = set_point

    def set_sample_bias(self, sample_bias):
        self.config.sample_bias = sample_bias

    def set_PID_KP(self, PID_KP):
        self.config.PID.KP = PID_KP

    def set_PID_KI(self, PID_KI):
        self.config.PID.KI = PID_KI

    def set_PID_KD(self, PID_KD):
        self.config.PID.KI = PID_KD
