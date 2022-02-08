# STM FOR ALL 

## How to install
setup your last version of docker, update everything, clone the repo.

run setup.sh as root

## setup.sh 
will setup an interractive container with the name you give it as first argument (default name is "STM")

## what is currently not working 
* expodential voltage output -> re read some paper on the translation and review the equation given in the source paper(IBM)
* JSON/stats output as a file 
* error mean center cannot be chosen

## run the simulator 
go into the folder src\_sim in the docker container
help : 
`python3 SIM_STM.py -h`
to do the firsts tests : 
`python3 SIM_STM.py ../Test_Picture/ContactCopper.jpg -err 0.5`

more complexe test with expodential error (in this case print the contact copper with a normal error stdev of 0.5, mean of 0.12, expodential scaling at the output and statistics available of the different transformations) :
`python3 SIM_STM.py ../Test_Picture/ContactCopper.jpg -err 0.5 -errtype normal -stat -errM 0.12 -exp`
## requierments 
autofilled by the requirements.txt normally

## binary files used 

||0|1|2|3|4|5|6|7|
|-|-|-|-|-|-|-|-|-|
|0|M|S|T|version|...|...|patch|length of point in power of 2|
|8|height|...|...|...|width|...|...|...|
|16|metadata*|...|...|...|...|...|...|...|
|24|...|...|...|...|...|...|...|...|

* metadata : corresponds to the STM specific data (STM version/code version/PID information ... bla bla ) will be available in the next version
