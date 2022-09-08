from PIL import Image
import math, random
from samila import GenerativeImage, Projection
import os
from cmap_utils import get_random_cmap
from constants import ELEMENTS


def f1(x, y):
    result = random.uniform(-1,1) * x**2  - math.sin(y**2) + abs(y-x)
    return result

def f2(x, y):
    result = random.uniform(-1,1) * y**3 - math.cos(x**2) + 2*x
    return result


def get_image(seeds, save_to_folder, colors):
    """ Fully deterministic function for reproducibly generating a single
        Atomic NFT PNG from a list of random seeds. """
    os.system("mkdir -p %s" % (save_to_folder))
    for seed_index in range(len(seeds)):
        # Generate component images, one for each seed. Save each component locally.
        seed = seeds[seed_index]
        g = GenerativeImage(f1, f2)
        g.generate(seed=seed)
        print("Using", colors[seed_index])
        g.plot(projection=Projection.POLAR, color=colors[seed_index], bgcolor="transparent")
        g.save_image('%s/seed_%d_%s.png' % (save_to_folder, seed_index, seed), depth=6)

    # Merge components into a single transparent PNG
    background = Image.open('%s/seed_0_%s.png' % (save_to_folder, seeds[0]))
    for seed_index in range(1, len(seeds)):
        foreground = Image.open("%s/seed_%d_%s.png" % (save_to_folder, seed_index, seeds[seed_index]))
        background.paste(foreground, (0, 0), foreground)
    background.save("%s/final_nft.png" % (save_to_folder))
    print("Saved complete NFT to %s" % (save_to_folder))


# hardcoded seed = deterministic generation
main_random = random.Random(69420)
# generate 1k contracts
for nft_num in range(0, 200):
    depth = int(main_random.random() * 8) + 1
    print("Depth", depth)
    seeds = []
    chosen_colors = []
    for i in range(0, depth):
        seed = int(10000000000000000000000000000000000000000000000 * main_random.random())
        seeds.append(seed)
        chosen_colors.append(random.Random(seed).choice(ELEMENTS))
        main_random = random.Random(seed)
    get_image(seeds, "nfts/atomic_nfts_%d" % (nft_num), chosen_colors)

    print("Finished NFT", nft_num)
