'''
Function to replace specific colours in a raster figure.

Often you need to change the colour of a raster graphic for some reason, e.g. to increase contrast. Recreating these images can be time consuming. To speed up the process this script reads in an imageand changes the colours for you.

TODO: 
- Add example of usage
- Add example of using a colour range, rather than specific colour

#TARGET COLOURS
#light blue = (65,120,250)  -> HEX: #4178FA
#dark blue =  (55,50,200)   -> HEX: #3732C8
#light red =  (255,100,100) -> HEX: #FF6464
#dark red =   (237,42,44)   -> HEX: #ED2A2C

#DIR = os.path.dirname(os.path.abspath(__file__))
#IMAGE_DIR = os.path.join(DIR, 'Main_data')
#OUT_DIR = os.path.join(DIR, 'Main_data')

'''
from sys import argv
from PIL import Image
import numpy as np


for i, arg in enumerate(argv):
    print('argument {} is {}'.format(i, arg))

# IMAGE_DIR = '/home/connor/PhD/study_1/outputs/figures/'
# OUT_DIR = '/home/connor/PhD/study_1/outputs/figures/'
#
# image_in = os.path.join(IMAGE_DIR, 'plot_training.png')
# image_list = os.listdir(IMAGE_DIR)
# image_out_path = (os.path.join(OUT_DIR, 'adjusted_plot_training.png'))#
#
# orig_cols = [(65, 120, 250), (55, 50, 200), (225, 2, 2), (255, 100, 100) ]
# tar_cols = [(122, 194, 254), (0, 0, 160), (233, 28, 22),(255, 187, 187)]


def main(argv_args):
    if len(argv_args) < 5:
        print('Please provide details of im_in, \
im_out_path, orig_cols, target_cols')
    im_in, im_out_path, orig_cols, target_cols = argv_args
    print im_in
    im_out = change_colours(im_in, orig_cols, target_cols)
    im_out.save(im_out_path)


def change_colours(image_in, orig_cols, tar_cols):
    """Replace specific colours in a raster image.

       args:
       (1) The image that you want to change.
       (2) A list of colours that you want to remove.
       (3) A list of the colours you want to replace them.

       returns: an image file with the adjusted colours
    """
    im = Image.open(image_in)
    im = im.convert('RGBA')
    data = np.array(im)   # "data" is a height x width x 4 numpy array
    red, green, blue, alpha = data.T

    for orig_col, tar_col in zip(orig_cols, tar_cols):
        colours_to_change = (red == orig_col[0]) and \
                            (green == orig_col[1]) and \
                            (blue == orig_col[2])
        data[..., :-1][colours_to_change.T] = tar_col  # Need to back transpose

    im_out = Image.fromarray(data)
    im_out.show()
    return im_out

if __name__ == "__main__":
    main(argv[1:])
