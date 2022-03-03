# setting up the default config
class Config:
    def __init__(self, args):
        self.verbose = args.verbose
        self.ts = args.ts
        if(args.save != ""):
            self.output_filename = args.save
        else:
            self.output_filename = ""

        self.test_type = args.test_type;
        self.device = args.device
