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

## requierments 
autofilled by the requirements.txt normally


