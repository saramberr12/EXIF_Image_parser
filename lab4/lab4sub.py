#This script parses images for all exil contents
#human-readable date and time
#!/usr/bin/python

# import statements include PILLOW library to take care of 
# a lot of EXIF accessing
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import pprint, os, hashlib

__author__ = 'Sarah Higgins'
__date__ = '20190404'
__version__ = '0.5'

cwd = os.getcwd()

# funtion get_exif simply aquires the EXIF data from all of the images
# that have been extracted to the current working directory.  The EXIF
# file itself is numerically listed so to see the actual categorical 
# information, the PILLOW's TAGS option will convert the numbers to 
# the wanted information names.
# This function also determines whether or not an image is valid or 
# invalid.
def get_exif(filename):
    try:
        image = Image.open(filename)
        image.verify()
        print('Valid Image: ' + filename)
        info = image._getexif()
        return {TAGS.get(tag): value for tag, value in info.items()}
    except Exception:
        print('Invalid Image: ' + filename)

# Function get_lableled_exif takes care of adding all of the EXIF
# information to an array to be displayed to the user.  This will 
# be displayed in the same order as the valid images that appeared
# above in the printout to the user's screen.
def get_labeled_exif():
    labeled = []
    for file in [x for x in os.listdir(cwd) if os.path.isfile(x)]:
        exifs = get_exif(file)
        if exifs:
            labeled.append(exifs)
    return labeled

# Function get_md5 opens the FBI hash database that is saved in a 
# .txt file within the current working directory, and stores that 
# information as contents.  This function also creates the md5 
# hash value to then be compared to the FBI hash values.  If an md5
# hash value is found to be a match, it is added to the matches array
# to be returned to the user and flagged as an Illicit Image.
def get_md5():
    values = open('FBI-hash_list.txt', 'r')
    if values.mode == 'r':
        try:
            contents = values.readlines()
            files = []
            matches = []
            for file in [x for x in os.listdir(cwd) if os.path.isfile(x)]:
                files.append(hashlib.md5(open(file, 'rb').read()).hexdigest())
            for line in contents:
                for i in files:
                    if line.startswith(i):
                        matches.append(line)
            return matches
        except Exception: 
            print('Did not work as expected')

# executes the above functions to display printouts to user
labeled = get_labeled_exif()
print('\n')
print('EXIF Information: ')
print('\n')
pprint.pprint(labeled)
print('\n')
print('Illicit Images With Listing of Other Information Found!: ')
hashes = get_md5()
for hash in hashes:
    print(hash)

