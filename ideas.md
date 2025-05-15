# Storing/Encrypting Files in Minecraft

Since files are essentially just a series of bytes, we can represent files in minecraft as a series of blocks.  

## Ideas
- 16 different colors, each pair (2 colored blocks) represents a byte 
- more space efficient: create one-to-one mapping of each possible byte (0-255) to a block 
   - in theory this could be expanded to as many blocks as the game offers, but stick to 1 byte = 256 blocks for simplicity (for now)

## Block Choice


Since the blocks are going to be placed down in the world, we are limited by our choices: 

### Limitations
- blocks cannot be affected by gravity (no sand, gravel, anvils)
- blocks shouldn't change due to possible changes in the environment (no dirt, grass, mycelium, wood)
- blocks should take up a 1x1 space (no beds, doors)     
- blocks must be able to be placed anywhere (no torches, lanterns, flower pots)


## Encrypting 
1. Read through file, map from bytes to blocks. 
2. Place blocks down in the same order file was read in.

### more layers of encryption
- vary order of block placements
- apply encryption algorithm before converting from bytes to blocks



# sources 
https://pypi.org/project/mcschematic/