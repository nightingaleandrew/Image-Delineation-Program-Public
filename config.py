#config file for configuable variables for the program

#TERMINOLOGY
#I will gradually move the program so Slice is removed from terminology throughout. This is a post project development to allow it to be used for not just MRI Slices but any images
EACH_FILE_NAME = "MRI Slice"
GROUP_OF_FILES_NAME = "MRI Stack"

#SECURITY - This not a real security risk :) 
PASSWORD_REQUIRED = False #if password is not required then just requires a username
PASSWORD = "" #security is not a central functional requirement in this program as files are on machine anyway.

#OTHER
FILETYPES_ACCEPTED = {".npy": True, ".png": False, ".jpg": False} #again linking to the fact to make program any img orientated
NPY_FILES_TYPES_NOT_WANTED = ["nor", "sus"] #these are typically at the end of .npy array filename and relate to a different version of that file
IMG_COLOURMAP = 'gray' #viridis is default, for instance if non gray imgs were to be allowed
MASK_COLOUR_OR_BLACK_WHITE = True #if this is false then mask produced will be black or white.

SYNCHRONISATION = True #if synchronisation is on for this program
DISREGARD_TRANSLATED_POLYGONS_WITH_GT_3_SLICE_NUMS = False #if the slices for the translated polygon extend over 3 different numbers, show/hide polygon altogether
