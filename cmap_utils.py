import random
from samila.functions import is_valid_color as is_valid_color

def rand_cmap(nlabels, type='bright', verbose=True):
    """
    Creates a random colormap to be used together with matplotlib. Useful for segmentation tasks
    :param nlabels: Number of labels (size of colormap)
    :param type: 'bright' for strong colors, 'soft' for pastel colors
    :param verbose: Prints the number of labels and shows the colormap. True or False
    :return: colormap for matplotlib
    """
    import colorsys
    import numpy as np


    if type not in ('bright', 'soft'):
        print ('Please choose "bright" or "soft" for type')
        return

    if verbose:
        print('Number of labels: ' + str(nlabels))

    # Generate color map for bright colors, based on hsv
    if type == 'bright':
        randHSVcolors = [(np.random.uniform(low=0.0, high=1),
                          np.random.uniform(low=0.2, high=1),
                          np.random.uniform(low=0.9, high=1)) for i in range(nlabels)]

        # Convert HSV list to RGB
        randRGBcolors = []
        for HSVcolor in randHSVcolors:
            randRGBcolor = colorsys.hsv_to_rgb(HSVcolor[0], HSVcolor[1], HSVcolor[2])
            if is_valid_color(randRGBcolor):
                randRGBcolors.append(randRGBcolor)


    # Generate soft pastel colors, by limiting the RGB spectrum
    if type == 'soft':
        low = 0.6
        high = 0.95
        randRGBcolors = list(filter(is_valid_color, [(np.random.uniform(low=low, high=high),
                          np.random.uniform(low=low, high=high),
                          np.random.uniform(low=low, high=high)) for i in range(nlabels)]))


    for color in randRGBcolors:
        if len(color) != 3:
            randRGBcolors.remove(color)

    return randRGBcolors


def get_random_cmap():
    new_cmap = rand_cmap(10, type=random.choice(['soft', 'bright']))
    new_cmap = new_cmap + rand_cmap(10, type=random.choice(['soft', 'bright']))
    random.shuffle(new_cmap)
    return new_cmap
