# Summer Internship 2023
Kinematics of the Ionized Outflow in the Northwest of NGC 253.

====================================================================================
# LOG ONTO A UMD ASTRO COMPUTER REMOTELY
====================================================================================

Step 1: Open a terminal on your laptop.

Step 2: Type in the following and hit enter:

    ssh username@ssh.astro.umd.edu

Step 3: Put in your password. Then, type:

    ssh jansky

Step 4: Navigate to the the directory you want to work in by typing:

    cd /jansky/cronin/

To list all files in this directory, type:

    ls

To make a new sub directory in this directory, type:

    mkdir directory_name

To navigate to a new directory, type:

    cd path_to_directory

or, to navigate backwards:

    cd ../path_to_directory

The above assumes you will be working on the computer 'jansky' (which we recommend).

====================================================================================
# HOW TO RUN THE ROUTINE ON JANSKY
====================================================================================

Step 1: ssh into jansky using the steps above. Make sure you are in your directory:

    /jansky/cronin/your_directory

Step 2: Open a screen session (see below).

Step 3: Load in the proper anaconda environment by typing:

        astroload -v anaconda3-21 python

Step 4: Open a different terminal session on your laptop. To upload a file to jansky, type the following:

        scp your_file.py your_username@ssh.astro.umd.edu:'/home/your_username/'

To upload an entire folder, type:

        scp -r your_folder your_username@ssh.astro.umd.edu:'/home/your_username/'

Step 5: Your file is now in your home directory. Move it to your working directory by doing:

        mv your_file.py /jansky/cronin/your_directory/

Step 6: Make sure you have all the necessary files uploaded to your working directory on jansky.
Then you can run everything like usual using the steps below!

====================================================================================
# SET UP A CONDA ENVIRONMENT
====================================================================================

Step 0: Make sure you have Anaconda downloaded and ready to go: https://docs.anaconda.com/free/anaconda/install/

Step 1: Create the environment! Use a custom name, for example, "ngc253-project":

    conda create --name ngc253-project
    
Make sure you press 'y' when prompted.

Step 2: Activate your environment.

    source activate ngc253-project

Step 3: Add the packages and the specific versions you need using the following commands:

    conda install python=3.10.4 astropy=5.1 jupyter=1.0.0 matplotlib=3.6.2 numpy=1.23.5 pandas=1.5.3 scipy=1.10.0 tqdm=4.64.1
    pip install pyspeckit spectral-cube

Make sure you press 'y' when prompted. The specified versions are just to match what I have tested and run the fitting program on.

Step 4: To deactive your environment, type:

    source deactivate ngc253-project

You must activate your environment every time you open a new terminal.


====================================================================================
# WORKSPACE IDE
====================================================================================

I recommend using Spyder and Jupyter for this project. To open them, type into the terminal:

    spyder

and

    jupyter notebook

You will need separate terminals for each.


====================================================================================
# DATA
====================================================================================

Please download the datacube here (click "File Download"):

    http://archive.eso.org/dataset/ADP.2019-08-24T09:53:08.548

Warning! You will need 5.5 GB of free space to download this datacube.


====================================================================================
# SCREEN SESSION
====================================================================================

The fitting program will take several hours to run, even on a fast machine.
To make sure the program will run without interruption, I recommend using a screen session,
which is a terminal that runs in the background and won't stop even if your computer goes to sleep
(but *not* when the computer is off, so keep it on!).

To start a screen session, simply type in the terminal:

    screen

You may be prompted to press the space bar or enter when you load screen for the first time.

Now, activate your conda environment:

    source activate gradmap23

To detach the screen session (it will remain running in the background, but you can now
return to your regular terminal), press:

    Ctrl + a + d

To reattach the screen session, type:

    screen -r

And to end a screen session, type (in the screen session):

    exit


====================================================================================
# HOW TO RUN THE FITTING ROUTINE
====================================================================================

Please copy/download the following files to the same directory:

    routine.py
    run_template.py
    plot_fits.py

Start up a screen session so you can run the program for several hours without interruption 
(see "SCREEN SESSION" above).

Using Spyder, make a copy of 'run_template.py' called 'run.py'.
Directly edit in 'run.py' so that you will always have the original template to fall back on.
You will need to update run.py with your best initial guesses, correct file paths, etc.
You also have the option to test things on a small subset of the datacube before you run the routine
on the entire cube!

To run the fitting routine, type in the terminal:

    python run.py
