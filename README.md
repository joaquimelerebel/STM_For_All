# STM FOR ALL

- [STM FOR ALL](#stm-for-all)
  - [How to install](#how-to-install)
  - [To run the simulator](#to-run-the-simulator)
  - [To show an image](#to-show-an-image)
  - [Requierments](#requierments)
  - [What is currently not working](#what-is-currently-not-working)
  
## How to install

1. Setup your last version of docker,
2. Update everything
3. Clone the repo
4. Run setup.sh as root

It will setup an interactive container with the name you give it as first argument (default name is "STM")

## To run the simulator

Go into the folder src\_sim in the docker container

To do the firsts tests:

`python3 SIM_STM.py ../Test_Picture/ContactCopper.jpg -err 0.5`

Help:

`python3 SIM_STM.py -h`

More complexe test with expodential error (in this case print the contact copper with a normal error stdev of 0.5, mean of 0.12, expodential scaling at the output and statistics available of the different transformations) :
`python3 SIM_STM.py ../Test_Picture/ContactCopper.jpg -err 0.5 -errtype normal -stat -errM 0.12 -exp`

## To show an image

Got to `src_show`

To generate a matrix from a picture, use:

```
python3 ../src_sim/SIM_STM.py ../Test_Picture/ContactCopper.jpg -o output
```

To convert the matrix to an image:

```
python3 display.py output
```


## Requirements

Autofilled by the requirements.txt normally


## What is currently not working

* exponential voltage output -> re-read some paper on the translation and review the equation given in the source paper(IBM)
* JSON/stats output as a file

## binary files used 
****BIG ENDIAN****

||0|1|2|3|4|5|6|7|
|-|-|-|-|-|-|-|-|-|
|0|M|S|T|version|...|patch|...|length of point in power of 2|
|8|height|...|...|...|width|...|...|...|
|16|metadata*|...|...|...|...|...|...|...|
|24|...|...|...|...|...|...|...|...|

* metadata : corresponds to the STM specific data (STM version/code version/PID information ... bla bla ) will be available in the next version

