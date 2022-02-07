# setting up the default config
class Config:
    def __init__(self, args):
        self.size = args.size
        self.gui = args.gui
        self.verbose = args.verbose
        #self.filter = args.filter;
        self.simulation_filename = args.simulation_filename
        self.is_exponential_scale = args.exponential
        self.is_statistical = args.statisics

        if(args.error_type == "normal"):
            self.is_normal_error = True
            self.is_uniform_error = False
        elif(args.error_type == "uniform"):
            self.is_normal_error = False
            self.is_uniform_error = True

        self.error = args.error
        if args.error is None:
            self.error = 0

        if(args.save != ""):
            self.output_filename = args.save
        else:
            self.output_filename = ""

        # else :
            # self.output_filename = "OutputFiles/output.png";
        """
        if( args.kp != 0 ) :
            self.kp = args.kp;
        else :
            self.kp = 1;

        if( args.ki != 0 ) :
            self.ki = args.ki;
        else :
            self.ki = 1;


        if( args.frequence != 0 ) :
            self.frequence = args.frequence;
        else :
            self.frequence = 100;
        """
