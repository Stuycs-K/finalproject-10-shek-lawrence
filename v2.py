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
    for i in range(240):
        BYTES_TO_BLOCKS.append(f.readline().rstrip())


TOTAL_BYTES = 0
SEED = 7114238357002984737

def main():
    parser = argparse.ArgumentParser(description="Encode a file or decode a schematic file.")
    parser.add_argument("-m", "--mode", choices=["encode", "decode"], type=str.lower, help="Mode of operation")
    parser.add_argument("-i", "--input", help="Name of the file to process") 
    parser.add_argument("-o", "--output", help="Output file name")
    parser.add_argument("-b", "--bytes", type=int, help="Number of bytes")


    args = parser.parse_args()
    if args.mode == "encode":
        if args.output is None:
            args.output = "secret"
        build_schematic(args.input, args.output)
    elif args.mode == "decode":
        if args.output is None:
            args.output = "decrypted.txt"
        global TOTAL_BYTES
        TOTAL_BYTES = args.bytes 
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
    additional_bytes = 0
    for byte in data:
        hex_digits.append(byte >> 4)

        # random block
        hex_digits.append(random.randint(16, 255))
        additional_bytes += 1

        hex_digits.append(byte & 0x0F)   


    print("number of bytes", str(len(data) + additional_bytes))
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
        hex_digits.append(random.randint(16, 255))

    pos = shuffle_pos(side_length, side_length, side_length, SEED)
    for i, index in enumerate(hex_digits):
        x, y, z = pos[i]
        # x = i % side_length
        # z = (i // side_length) % side_length
        # y = i // (side_length * side_length)
        block = BYTES_TO_BLOCKS[index]
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
    block_positions = shuffle_pos(width, height, length, SEED)

    
    # map pos to value in original byte array 
    pos_to_value = {pos : i for i, pos in enumerate(block_positions)}     
    value_to_block = {v: k for k, v in palette.items()}

    
    # convert values from block array to byte array 
    byte_array = []


    for pos in block_positions:
        val = pos_to_value[pos]
        block = value_to_block(val)
    # for byte in data[:TOTAL_BYTES * 2]:
    #     # Byte objects in the data array are signed integers from -128 to 127, but the array is indexed 0-255
    #     byte = byte % 256
    #     block = value_to_block[byte]
    #     # don't include extranneous blocks
    #     if block in BLOCKS_TO_BYTES:
    #         byte_array.append(BLOCKS_TO_BYTES[block])
    
    # convert back to byte values
    temp = []
    for i in range(0, len(byte_array), 2):
        temp.append(16 * byte_array[i] + byte_array[i + 1])
    byte_array = temp


    byte_array = bytes(byte_array)


    with open(output_file, "wb") as f:
        f.write(byte_array)


def shuffle_pos(width, height, length, seed):
    pos = []
    for x in range(width):
        for y in range(height):
            for z in range(length):
                pos.append((x, y, z))
    random.Random(seed).shuffle(pos)
    return pos 


if __name__ == "__main__":
    main()
