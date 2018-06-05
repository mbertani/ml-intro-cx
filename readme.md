Workshop data cleaning

Work in process!  
To add: Information on data structure (float/meters)

# Background
Kolumbus is creating a project to predict delays in traffic... (add more)

# Task
You have been given one day of bus data. Your task is to clean this data and then train a machine learning model with it.

## Setup the environment
### Virtual machine setup
 Use this option if you don't want to install conda in your machine (but you will need vagrant and virtualbox). You will spin a virtual machine with the right setup:

1. Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
2. Install [Vagrant](https://www.vagrantup.com/)
3. If you have Git, clone this repository. Otherwise download the content as a ZIP archive and unpack it somewhere.
4. Open a command line interface/shell (PowerShell or Cmd on Windows, Terminal on Mac, your favourite terminal emulator on Linux)
5. Change directory to the location of this repository's files.
6. Run: `vagrant up --provision` the first time you start up the VM. Use just `vagrant up` for subsequent calls.
7. Get some coffee, eat a sandwich or surf the web or something, this will take about 10 minutes depending on your internet connection and computer.
8. Run `vagrant ssh` to log onto the VM from the shell. 
9. Inside the box, run `./run_lab.sh` to start the jupyter lab server.
10. Open your browser at [http://localhost:8888](http://localhost:8888) and log in with password `workshop`
11. When you want to stop the VM, use `Ctrl+c` to stop the server, then `exit` to leave the ssh session, and `vagrant halt` to stop the VM.

#### Notes

##### RAM

The VM has 2 GiB of RAM by default. If you want to increase performance, you may increase the `v.memory` in [Vagrantfile] to about half of what you have on your system. DO NOT SET THIS HIGHER THAN 75% OF YOUR SYSTEM'S RAM.

##### CPUs

The VM has 2 cores by default. If you want to increase performance, you may increase the `v.cpus` in [Vagrantfile] to half of the number of logical cores on your system. DO NOT SET THIS HIGHER THAN HALF THE NUMBER OF LOGICAL CORES ON YOUR SYSTEM.

### Conda

This should be the easiest method. [Download](https://conda.io/docs/user-guide/install/download.html) Anaconda3 with python 3.6 for your OS and then run:

```sh
conda install -c conda-forge jupyter lab
``` 

```sh
conda env create -f datavask_workshop.yml
```

```sh
# To activate this environment (linux/mac)
source activate datavask_workshop
# windows
activate datavask_workshop

# to deactivate the environment use (linux/mac)
source deactivate
# windows
deactivate
```

Start the jupyter lab:
```sh
jupyter lab
```
You will get a token link to the jupyter server. Open this in your browser.

## Where do I start?

Go to [Welcome.ipynb](http://localhost:8888/lab/tree/Welcome.ipynb) and follow instructions from there.

### Upload the data
 The data will be distributed in the confluence site of the workshop. Once you download the zip file, do:

1. Make a folder called `data` in jupyter lab.
2. Upload the zip file to that folder.

#Extra task/If you have time (?)
