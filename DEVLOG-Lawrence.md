# Dev Log:

This document must be updated daily every time you finish a work session.

## Lawrence Shek CHANGE THE NAME FOOL!

### 2025-05-15 - Encoding
- outlined project ideas
- read bytes from file in python, convert bits to blocks (somewhat working, still testing)
- experimneted with mcschematic library 

### 2025-05-16 - Decoding
- read blocks from the world
- converted from blocks to bytes in original file order
- worked on writing bytes to file, not yet working

### 2025-05-18 - Decoding working
- added command line args to specify encode/decode and output file name
- added error checking 
- changed mapping to 3d array of blocks instead of 2d to allow for larger file sizes 
- files still take up a lot of space, might use more blocks to represent data (instead of just 16)


### 2025-05-19 - Worked on changing block mapping
- instead of 16 blocks, trying to use 256 different blocks to represent a byte
	- should take up 16x less space
- need to modify block list
	- some blocks have extra data in the schematic, like the direction they face

### 2025-05-20 - Smaller block representation
- files now take up less space in the world, faster to load
- still need to further filter through block list
	- some blocks cause too much lag

### 2025-05-21 - Debugging
- block list should be good? might still have some issues
- decoding larger files doesn't work for some reason