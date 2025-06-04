import mcschematic
import nbtlib 
import argparse 
import math
import random


SCHEMATICS_FOLDER = "/mnt/c/Users/lawre/AppData/Roaming/.minecraft/config/worldedit/schematics/"

BYTES_TO_BLOCKS = ["minecraft:white_wool",
                   "minecraft:light_gray_wool",
                   "minecraft:gray_wool", 
                   "minecraft:black_wool", 
                   "minecraft:brown_wool",
                   "minecraft:red_wool",  
                   "minecraft:orange_wool",
                   "minecraft:yellow_wool",
                   "minecraft:lime_wool",
                   "minecraft:green_wool",
                   "minecraft:cyan_wool",
                   "minecraft:light_blue_wool",
                   "minecraft:blue_wool",
                   "minecraft:purple_wool",
                   "minecraft:magenta_wool",
                   "minecraft:pink_wool"]

BLOCKS_TO_BYTES = {block: i for i, block in enumerate(BYTES_TO_BLOCKS)}

# random blocks 
with open("blocks.txt", "r") as f:
    random_blocks = f.read().split()
    BYTES_TO_BLOCKS += random_blocks

SEED = 7114238357002984737

# first 8 blocks of the file store the file size (32 bit integer) 
FILE_START = 8

def main():
    parser = argparse.ArgumentParser(description="Encode a file or decode a schematic file.")
    parser.add_argument("-m", "--mode", choices=["encode", "decode"], type=str.lower, help="Mode of operation")
    parser.add_argument("-i", "--input", help="Name of the file to process") 
    parser.add_argument("-o", "--output", help="Output file name")


    args = parser.parse_args()
    if args.mode == "encode":
        if args.output is None:
            args.output = "secret"
        build_schematic(args.input, args.output)
    elif args.mode == "decode":
        if args.output is None:
            args.output = "decrypted.txt"
        decode_schematic(SCHEMATICS_FOLDER + args.input, args.output)
    else:
        print("invalid mode")
        exit(1)



def read_bytes(filename):
    try: 
        with open(filename, "rb") as f:
            data = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        exit(1)
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        exit(1)


    hex_digits = []

    # prepend length of file in first 8 blocks (32 bit integer)
    file_size = len(data)
    for i in range(FILE_START):
        hex_digits.append(file_size & 0x0F)
        file_size = file_size >> 4
    
    for byte in data:
        hex_digits.append(byte >> 4)
        hex_digits.append(byte & 0x0F)   
    

    # incorporate random blocks outside of block list
    for i in range(len(hex_digits) // 4):
        hex_digits.append(random.randint(16, len(BYTES_TO_BLOCKS) - 1))
        hex_digits.append(random.randint(16, len(BYTES_TO_BLOCKS) - 1))
    
    return hex_digits


def build_schematic(filename, schematic_name):
    schem = mcschematic.MCSchematic()
    hex_digits = read_bytes(filename)

    total_blocks = len(hex_digits)
    
    # round up
    side_length = math.ceil(total_blocks ** (1 / 3))

    # fill in empty bytes with random blocks 
    total_blocks = side_length ** 3
    for i in range(len(hex_digits), total_blocks):
        hex_digits.append(random.randint(0, 15))

    pos = shuffle_pos(side_length, side_length, side_length, SEED)
    for i, val in enumerate(hex_digits):
        x, y, z = pos[i]
        block = BYTES_TO_BLOCKS[val]
        schem.setBlock((x, y, z), block)
    

    schem.save(SCHEMATICS_FOLDER, schematic_name, mcschematic.Version.JE_1_21_5)


def decode_schematic(filepath, output_file):
    try:
        schem = nbtlib.load(filepath)
    except FileNotFoundError:
        print(f"Error: Schematic file '{filepath}' not found.")
        exit(1)
    except Exception as e:
        print(f"Error loading schematic: {e}")
        exit(1)

    # palette is a dictionary that maps each block to an integer 
    palette = schem["Schematic"]["Blocks"]["Palette"]
    # data is a byte array storing the order that the blocks are stored, using the indices in palette corresponding to the name of the block
    data = schem["Schematic"]["Blocks"]["Data"]
    

    width = schem["Schematic"]["Width"]
    height = schem["Schematic"]["Height"]
    length = schem["Schematic"]["Length"]


    # list of positions of all blocks in the format (x, y, z)
    # (using the same seed to get original position blocks were placed in)
    block_positions = shuffle_pos(width, height, length, SEED)

    val_to_block = {v: k for k, v in palette.items()}
    # map pos to value in original byte array 
    pos_to_index = {pos : i for i, pos in enumerate(block_positions)}     

    
    byte_array = [-1] * len(block_positions)


    # convert values from block array to byte array 
    for i, byte in enumerate(data):
        # Byte objects in the data array are signed integers from -128 to 127, but the array is indexed 0-255
        block = val_to_block[byte % 256]
        if block not in BLOCKS_TO_BYTES:
            continue
        pos = get_pos(i, width, height, length)
        index = pos_to_index[pos]
        byte_array[index] = BLOCKS_TO_BYTES[block]

    # for random scattered blocks, read in the full array then create a new one without the extraneous blocks
    temp = []
    for byte in byte_array:
        if byte > -1:
            temp.append(byte)
    byte_array = temp

    total_bytes = get_file_size(byte_array[:FILE_START])

    # convert back to byte values
    temp = []
    for i in range(FILE_START, FILE_START + total_bytes * 2, 2):
        temp.append(16 * byte_array[i] + byte_array[i + 1])
    byte_array = temp

    byte_array = bytes(byte_array)


    with open(output_file, "wb") as f:
        f.write(byte_array)


def get_file_size(bits):
    total = 0
    for i, val in enumerate(bits):
        total += 16 ** i * val
    return total


def shuffle_pos(width, height, length, seed):
    pos = []
    for x in range(width):
        for y in range(height):
            for z in range(length):
                pos.append((x, y, z))
    random.Random(seed).shuffle(pos)
    return pos 


def get_pos(index, width, height, length):
    # blocks in the schematic are read in the order: x, z, y (all in the positive direction)
    x = index % width 
    z = (index // width) % length
    y = index // (width * length)
    return (x, y, z)  


if __name__ == "__main__":
    main()
