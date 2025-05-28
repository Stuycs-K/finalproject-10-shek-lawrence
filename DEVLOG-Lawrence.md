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

### 2025-05-22/23 - More debugging
For some reason, the number of bytes read from a schematic file is greater than the number of bytes in the original file. Only noticed this happening with larger files, like images, and this didn't happen with the previous version, with 16 blocks instead of 256. Still, can't seem to figure out why program is reading more bytes than there exists. 


### 2025-05-24 - Modified Encoding 
- appended random blocks to end of block schematic
	- file bytes don't always fill entire cube 

### 2025-05-25 - Worked on fixing decode
- removed duplicate block in blocks.txt file, which could have been causing problems
	- added --bytes option to know when to stop decoding 

### 2025-05-26 - Encryption 
- added random blocks within schematic to make decoding more difficult 
- couldn't get encoding with 256 blocks working

### 2025-05-27 - More Encryption
- idea: randomly generate key using a seed 
- use this key to rearrange order of blocks --> decode using key 