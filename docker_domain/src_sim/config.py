#setting up the default config
class Config : 
    def __init__(self, args) :
        self.size = args.size;
        #self.filter = args.filter;
        self.simulation_filename = args.simulation_filename;
        self.is_exponential_scale = args.exponential;
        self.is_statistical = args.statisics;

        self.time = args.time;
        self.vtime = args.vtime;
        self.isSerial = False;
        self.isCtable = False;    
        self.output_filename = "";

        if( args.output_type == "ASCII" ) :
            self.isNumpyBin = False;
            self.is_bin = False;
            self.isCtable16 = False;
        if( args.output_type == "BIN_NP" ) :
            self.isNumpyBin = True;
            self.is_bin = True;
            self.isCtable16 = False;
        if( args.output_type == "BIN_MST" ) :
            self.isNumpyBin = False;
            self.is_bin = True;
            self.isCtable16 = False;
        if( args.output_type == "C_TABLE" ) :
            self.isNumpyBin = False;
            self.is_bin = True;
            self.isCtable = True;
            self.isCtable16 = False;
        if( args.output_type == "C_TABLE16" ) :
            self.isNumpyBin = False;
            self.is_bin = False; 
            self.isCtable = True;
            self.isCtable16 = True;
        
        if( args.error_type == "normal") : 
            self.is_normal_error = True;
            self.is_uniform_error = False;
        elif( args.error_type == "uniform") : 
            self.is_normal_error = False;
            self.is_uniform_error = True;

        self.error = args.error;
        self.error_mean  = args.error_mean

        if( args.save != "" and args.serial != "" ) :
            raise RuntimeError("You cannot output to a file and serial at same time")
        elif( args.save != "" ) :
            self.output_filename = args.save;
        elif( args.serial != "" ) :
            self.isSerial = True;
            self.output_filename = args.serial;
            if( self.isNumpyBin ) :
                raise RuntimeError("You cannot output Numpy arrays to serial")
            if( not self.is_bin ):
                raise RuntimeError("You cannot output ASCII to serial")
