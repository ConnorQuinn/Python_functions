'''
Colour changing script to update figures consistently.
Often need to change colours of figures for some reason, e.g. increase contrast
for  projectors. This script reads in an image. You identify what colour you
want to change and what colour you want it to be afterwards.
'''
import os
from PIL import Image
import numpy as np


# want to change all blue colours to R:59, G:120, B:187
# The script should find all blues and adjust them to that


# dark blue = (56,83,164)
# light blue = (64,119,187)
#Dark red: 180; 16; 16
#light red: 238; 24; 27 ;   #EE181B
#Light blue: 44;123;182  ; #2C7BB6
#Dark blue: 0;0;99
# R:68, G:118, B:187
# R:0, G:127, B: 255
# R:0, G:0, B: 254
# R:58, G:83, B:165
# Dark blue =  (red == 0)  & (green == 127) & (blue  == 255)
# Light red = (red == 242)  & (green == 125) & (blue  == 128)
# also # Light red = (red == 255)  & (green == 127) & (blue  == 127)

'''
TARGET COLOURS
light blue = (65,120,250)  -> HEX: #4178FA
dark blue =  (55,50,200)   -> HEX: #3732C8
light red =  (255,100,100) -> HEX: #FF6464
dark red =   (237,42,44)   -> HEX: #ED2A2C
'''
DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(DIR, 'Main_data')
OUT_DIR = os.path.join(DIR, 'Main_data')

image_in_path = os.path.join(IMAGE_DIR, 'Uncorrected_main_bars_jan16.png') # get higher res .png
image_list = os.listdir(IMAGE_DIR)
image_out_path = (os.path.join(OUT_DIR, 'Adjusted_uncorrected_main_bars_jan16.png'))


im = Image.open(image_in_path)
im = im.convert('RGBA')
data = np.array(im)   # "data" is a height x width x 4 numpy array
red, green, blue, alpha = data.T

#orig_cols = [(65,127,255), (64,119,187),(255,127,127),(242,125,128)] # localiser
#tar_cols  = [(65,120,250),(65,120,250),(255,100,100),(255,100,100)] # localiser
#orig_cols = [(0,127,255), (255,127,127)]
#tar_cols  = [(65,120,250),(255,100,100)]
#           [light blue,  light blue,  dark blue, dark blue,   light red,...
#            light red,     dark red]
#orig_cols = [(0, 127, 255), (64, 119, 187), (56, 83, 164), (0, 0, 255),
#             (242, 125, 128), (255, 127, 127), (237, 42, 44)]
orig_cols = [(65, 120, 250), (55, 50, 200), (225, 2, 2), (255, 100, 100) ]

tar_cols = [(122, 194, 254), (0, 0, 160), (233, 28, 22),(255, 187, 187)]

for orig_col, tar_col in zip(orig_cols, tar_cols):
    # Replace blues with one blue... (leaves alpha values alone...)
    colours_to_change = (red == orig_col[0])&(green == orig_col[1])&(blue == orig_col[2])
    data[..., :-1][colours_to_change.T] = tar_col # Transpose back needed

im2 = Image.fromarray(data)
im2.show()
im2.save(image_out_path)


    