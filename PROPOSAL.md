# Final Project Proposal

## Group Members:

Lawrence Shek

# Intentions:

In this project, my goal was to create a program that could store and encrypt your files in Minecraft and a decoder for the files stored in-game. 

# Intended usage:

The user runs the program with any file they want to encrypt in Minecraft, which then creates a schematic that maps the bytes of the file into Minecraft blocks. After opening a world, the user can load the schematic and paste it, revealing their block representation of the file. To decode, select the encoded blocks within the world and then save them to a schematic file. Then, run the decoder on that file. 
  
# Technical Details:

(CHANGE THIS!!!!!)

A description of your technical design. This should include: 
   
How you will be using the topics covered in class in the project.
     
How you are breaking down the project and who is responsible for which parts.

## Stegonography 
Files are represented as a seemingly random assortment of blocks in a Minecraft World. 

## Cryptography
Files are encrypted using an algorithm 
    
# Intended pacing:

## Week 1

## Day 1-3
- read bytes from file 
- create mapping of bytes --> blocks 
- save block representaiton of file in a schematic
- load schematic into Minecraft world

## Day 4-7 
- select blocks from world and save into a schematic file
- read schematic file, get block data (order of blocks arranged, type of blocks used)
- map from blocks --> bytes
- reconstruct original file

## Week 2
- addtional features? 
