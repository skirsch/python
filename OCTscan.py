# See https://github.com/marksgraham/OCT-Converter/blob/main/README.md
# for 3D slicer see: https://discourse.slicer.org/t/oct-fds-image-in-3d-slicer/18219 
# Other tools: ImageJ, Fiji, or Python libraries (OpenCV, Scikit-image) 

from oct_converter.readers import FDS

# An example .fds file can be downloaded from the Biobank website:
# https://biobank.ndph.ox.ac.uk/showcase/refer.cgi?id=30
# Use: wget  -nd  biobank.ndph.ox.ac.uk/ukb/ukb/examples/eg_oct_fds.fds

basedir=r'C:\Users\stk\Downloads\OCT\'
filepath = basedir + 'eg_oct_fds.fds'   # raw format so Python will quote anything needed

import os
os.chdir(basedir)    # place for storing the output files and input files

fds = FDS(filepath)

oct_volume = fds.read_oct_volume()  # returns an OCT volume with additional metadata if available
oct_volume.peek(show_contours=True) # plots a montage of the volume, with 128 slices in a new window
# oct_volume.save('fds_testing.avi')  # save volume as a movie (this doesn't work)
oct_volume.save('fds_testing.png')  # save volume as a set of sequential images, fds_testing_[1...N].png
oct_volume.save_projection('projection.png') # save 2D projection

fundus_image = fds.read_fundus_image()  # returns a  Fundus image with additional metadata if available
fundus_image.save('fds_testing_fundus.jpg')

metadata = fds.read_all_metadata(verbose=True) # extracts all other metadata
with open("fds_metadata.json", "w") as outfile:
    outfile.write(json.dumps(metadata, indent=4))

# create and save a DICOM
from oct_converter.dicom import create_dicom_from_oct
# writes out to current path
dcm = create_dicom_from_oct(filepath)
