[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/am3xLbu5)
# Encrypting Files in Minecraft 
 
### Best Game Ever

Lawrence Shek
       
### Project Description:

Since files are essentially a series a bits, files can be stored in Minecraft as a series of blocks. The bytes from a file can be encoded into a Minecraft schematic file, from which data can be decoded.  
  
### Libraries 

This project uses the following python libraries: 
- mcschematic 
- nbtlib 

MCSchematic can be installed using pip.

`pip install mcschematic`

nbtlib can also be installed with pip.

`pip install "nbtlib==1.12.1"` 

It also uses the [WorldEdit](https://worldedit.enginehub.org/en/latest/install/) mod, which runs on the Java edition of Minecraft. 


### Instructions:

There are 2 versions of this program: `simple` and `v2`. The only difference is that `v2` adds a little more complexity by introducing new random blocks into the schematic and by shuffling the order in which blocks are placed. 

#### Encoding 

Note that you would have to change this line 

`SCHEMATICS_FOLDER = "/mnt/c/Users/lawre/AppData/Roaming/.minecraft/config/worldedit/schematics/"`

to the location of your schematics folder on your computer. 

`make simple ARGS="-i [inputfile] -m encode -o [outputfile]` 

`make v2 ARGS="-i [inputfile] -m encode -o [outputfile]` 

##### Example
`make simple ARGS="-i input.txt -m encode -o secret"` 


#### Decoding 
`make simple ARGS="-i [schematic file] -m decode -o [outputfile]`

`make v2 ARGS="-i [schematic file] -m decode -o [outputfile]` 

##### Example 

`make v2 ARGS="-i encoded.schem -m decode -o decrypted"` 


#### In game:
To load a schematic: 

`//schem load [filename]`

(dont inclue `.schem` in the filename)

Paste into world:

`//paste` 

To make a selection of blocks, use the wooden axe to left click on one corner of the schematic and right click on the opposite corner. This way, the entire schematic will be selected. 


Copy a selection of blocks (to save):

`//copy`


Save blocks to a schematic:

`//schem save [filename] -f`

(dont inclue `.schem` in the filename)


### Presentation Video
[Link to video](https://drive.google.com/file/d/1FtvL76QucBWJOtHiNTxPSXoDKKbZZM90/view?usp=sharing)

### Resources/ References:

- https://pypi.org/project/mcschematic/ (thanks to souvik for the idea)
- https://github.com/vberlier/nbtlib (for reading block data)
- https://github.com/Radvylf/minecraft-lists (block list) 