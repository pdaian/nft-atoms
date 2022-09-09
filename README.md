To generate : python3 atomic_nfts.py

To clean : rm -rf nfts

... will generate deterministically all 200 NFTs in the nftato.ms collection.

Generate constants: open("constants.py", "w").write(str("ELEMENTS = " + get_random_cmap(length=50000)))

The `website` subdirectory contains the nftato.ms static website.

The entire NFT collection can be saved/reproduced by cloning this Github
repository.

The original 
