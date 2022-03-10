import json
from re import S


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

    def output(self, filename):
        json_object = json.dumps(self.config, indent=4)
        with open("data/"+filename + ".json", "w") as outfile:
            outfile.write(json_object)
        return outfile.name

    def json_output(self):
        return json.dumps(self.config, indent=4, sort_keys=False)

    def set_all(self, scan_size, img_pixel, line_rate, x_offset, y_offset, set_point, sample_bias, PID_KP, PID_KI, PID_KD):
        self.set_scan_size(scan_size)
        self.set_img_pixel(img_pixel)
        self.set_line_rate(line_rate)
        self.set_x_offset(x_offset)
        self.set_y_offset(y_offset)
        self.set_set_point(set_point)
        self.set_sample_bias(sample_bias)
        self.set_PID_KP(PID_KP)
        self.set_PID_KI(PID_KI)
        self.set_PID_KD(PID_KD)

    def set_scan_size(self, scan_size):
        self.config["scan_size"] = scan_size

    def set_img_pixel(self, img_pixel):
        self.config["img_pixel"] = img_pixel

    def set_line_rate(self, line_rate):
        self.config["line_rate"] = line_rate

    def set_x_offset(self, x_offset):
        self.config["offset"]["x"] = x_offset

    def set_y_offset(self, y_offset):
        self.config["offset"]["y"] = y_offset

    def set_set_point(self, set_point):
        self.config["set_point"] = set_point

    def set_sample_bias(self, sample_bias):
        self.config["sample_bias"] = sample_bias

    def set_PID_KP(self, PID_KP):
        self.config["PID"]["KP"] = PID_KP

    def set_PID_KI(self, PID_KI):
        self.config["PID"]["KI"] = PID_KI

    def set_PID_KD(self, PID_KD):
        self.config["PID"]["KD"] = PID_KD
