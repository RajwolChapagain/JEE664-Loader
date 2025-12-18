# Introduction
This program parses a Motorola S-Record object file, converts it into contiguous hex data, and downloads it onto the lower 32k memory space of the Jameco JEE 664 EPROM programmer.

# Usage
After cloning the project and installing the required libraries listed in requirements.txt, run the loader program as follows with the JEE 664 connected to a serial port on your computer:
```
python loader.py -f sample_object_file.O -p COM1
```
