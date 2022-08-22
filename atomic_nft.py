from PIL import Image
import math, random
import matplotlib.pyplot as plt
from samila import GenerativeImage, Projection
import os

def rand_cmap(nlabels, type='bright', first_color_black=True, last_color_black=False, verbose=True):
    """
    Creates a random colormap to be used together with matplotlib. Useful for segmentation tasks
    :param nlabels: Number of labels (size of colormap)
    :param type: 'bright' for strong colors, 'soft' for pastel colors
    :param first_color_black: Option to use first color as black, True or False
    :param last_color_black: Option to use last color as black, True or False
    :param verbose: Prints the number of labels and shows the colormap. True or False
    :return: colormap for matplotlib
    """
    from matplotlib.colors import LinearSegmentedColormap
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
            randRGBcolors.append(colorsys.hsv_to_rgb(HSVcolor[0], HSVcolor[1], HSVcolor[2]))

        if first_color_black:
            randRGBcolors[0] = [0, 0, 0]

        if last_color_black:
            randRGBcolors[-1] = [0, 0, 0]


    # Generate soft pastel colors, by limiting the RGB spectrum
    if type == 'soft':
        low = 0.6
        high = 0.95
        randRGBcolors = [(np.random.uniform(low=low, high=high),
                          np.random.uniform(low=low, high=high),
                          np.random.uniform(low=low, high=high)) for i in range(nlabels)]

        if first_color_black:
            randRGBcolors[0] = [0, 0, 0]

        if last_color_black:
            randRGBcolors[-1] = [0, 0, 0]

    return randRGBcolors

def f1(x, y):
    result = random.uniform(-1,1) * x**2  - math.sin(y**2) + abs(y-x)
    return result

def f2(x, y):
    result = random.uniform(-1,1) * y**3 - math.cos(x**2) + 2*x
    return result


for nft_num in range(0, 200):
    os.system("mkdir -p nfts/%d" % (nft_num))
    new_cmap = rand_cmap(10, type=random.choice(['soft', 'bright']), first_color_black=False, last_color_black=False, verbose=True)
    new_cmap.append(rand_cmap(10, type=random.choice(['soft', 'bright']), first_color_black=False, last_color_black=False, verbose=True))
    random.shuffle(new_cmap)

    depth = 3
    for i in range(0, depth):

        g = GenerativeImage(f1, f2)
        seed = int(1000000000000 * random.random())
        open("nfts/%d/%d_seed" % (nft_num ,i), "w").write(str(seed) + "\n")
        g.generate(seed=seed)
        if i < 0:
            g.plot(projection=Projection.POLAR, bgcolor="black", color=new_cmap[i])
        else:
            g.plot(projection=Projection.POLAR, color=new_cmap[i], bgcolor="transparent")
        #plt.savefig('/tmp/%d.png' % (i), transparent=(i != 0))
        g.save_image('nfts/%d/%d.png' % (nft_num, i), depth=8)

    background = Image.open("nfts/%d/0.png" % (nft_num))
    for i in range(1, depth):
        foreground = Image.open("nfts/%d/%d.png" % (nft_num, i))
        background.paste(foreground, (0, 0), foreground)
    background.save("nfts/%d/image.png" % (nft_num))


    print("Finished NFT", nft_num)
