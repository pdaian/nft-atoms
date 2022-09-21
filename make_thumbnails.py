import os

for i in range(0,200):
    os.system("convert nfts/atomic_nfts_%d/final_nft.png -resize 800x800 atomic_nft_thumbnails/nft_%d.png" % (i,i))
    print("Done with", i)
