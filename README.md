# Immersed in the Sounds of Space: NASA International Space Apps Challenge 2023

<video src="CosmicHarmonySonifyingSpace-1.mp4" controls title="Title"></video>

## Whats the challenge

The challenge is to create sonifications for 3D NASA space datasets, exploring various ways to convey the richness of this data through sound. This may involve converting 3D 'data cubes' into audio representations that capture the essence of the information. It could also extend to creating sonification fly-throughs by translating video imagery into accurate sound representations.

## Our Method

Together we worked to leverage Python, MIDI, and FluidSynth to interpret the NASA space fly-through into audio. We did this by selecting a search size and location, to find the average colour in that area of each frame. These RGB values were then converted into notes for three different instruments to play. 

## How to use our Program

### Chocolatey

Chocolatley is required to work with FluidSynth.\
To install Chocolatley on your Windows Device follow the instructions provided in their [documentation](https://chocolatey.org/install)

### FluidSynth

FluidSynth is required to convert our generated MIDI files into WAV files.\
To install FluidSynth using Chocolatey use the command ```choco install fluidsynth``` as found in their [documentation](https://github.com/FluidSynth/fluidsynth/wiki/Download)

### Build a Python Virtual Environment

It is recommended to build a virtual environment locally to maintain proper library management between your python projects.\
To do this follow the steps shown in the venv [documentation](https://docs.python.org/3/library/venv.html)

### Requirements 

Lastly running ```pip install -r requirements.txt``` will install all required libraries into your local virtual environment

### Running the Program

To run the program use the following command in the terminal of your virtual environment: ```python main.py```