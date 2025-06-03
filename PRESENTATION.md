# Presentation 

## Mapping Bits to Blocks 

Since files are essentially just a series of bits, we can represent files in Minecraft as a series of blocks. 

At the simplest form, we can use two different blocks, one to represent the value `0`, and the other to represent the value `1`. 

The number `202` in binary is `1100 1010`. Substituting **0** for **black wool** and **1** for **white wool**, the number would like this: 


![binary representation](image.png)


To save a little bit of space, I decided to use 16 different blocks (16 different colors of wool), with each block representing 4 bits. 

![hex representation](image-1.png)

This way, every pair of blocks would represent a byte. Any given block could have 16 possible values (0-15), and any pair of blocks could hold 16 * 16 = 256 possible values (0-255). 


## Encoding a File

After reading a file and converting the data from bytes to blocks, I loaded the blocks into a Minecraft world using the WorldEdit mod and mcschematic python library. 

I initially laid the data out in a 2d array of blocks, although I later scaled that up into 3 dimensions to be more space efficient. 

![plain text 2d blocks](image-2.png)

*^ This is a plain text file* 

![plain text 3d blocks](image-3.png)

*^ Plain text file stored as a cube* 

I encoded blocks in the order `x, z, y`, all in the positive direction. The order in which blocks are encoded could be changed around, and anyone trying to crack the file would need to decode the blocks in the same order they were placed in. 

However, since the number of bytes in a file doesn't always fill a complete cubic shape, there are often missing blocks at the end of the file, which allow us to easily determine the order in which the blocks were placed. 

![xyz cube](image-4.png)
*^ x-y-z order* (block layers piled horizontally)


![xzy cube](image-5.png)
*^ x-z-y order* (block layers piled vertically)