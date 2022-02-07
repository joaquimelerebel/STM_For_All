# setting up the default config
class Config:
    def __init__(self, args):
        self.size = args.size
        self.gui = args.gui
        self.verbose = args.verbose
        self.filter = args.filter
        self.simulation_filename = args.simulator
        self.is_exponential_scale = args.exponential

        self.is_normal_error = args.normal_error
        if args.normal_error is None:
            self.is_normal_error = 0

        self.error = args.error
        if args.error is None:
            self.error = 0

        if(args.save != ""):
            self.output_filename = args.save
        else:
            self.output_filename = ""
        # else :
            # self.output_filename = "OutputFiles/output.png";

        if(args.kp != 0):
            self.kp = args.kp
        else:
            self.kp = 1

        if(args.ki != 0):
            self.ki = args.ki
        else:
            self.ki = 1

        if(args.frequence != 0):
            self.frequence = args.frequence
        else:
            self.frequence = 100
