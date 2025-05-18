import mcschematic
import nbtlib 
import argparse 

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

BLOCKS_TO_BYTES =  {block: i for i, block in enumerate(BYTES_TO_BLOCKS)}



def main():
    parser = argparse.ArgumentParser(description="Encode a file or decode a schematic file.")
    parser.add_argument("filename", help="The name of the file to process")
    parser.add_argument("--mode", choices=["encode", "decode"], type=str.lower, help="Mode of operation")
    parser.add_argument("-o", "--output", help="Output file name (for decode)")

    args = parser.parse_args()
    if args.mode == "encode":
        if args.output is None:
            args.output = "secret"
        build_schematic(args.filename, args.output)
    elif args.mode == "decode":
        if args.output is None:
            args.output = "decrypted.txt"
        decode_schematic(SCHEMATICS_FOLDER + args.filename, args.output)
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
    for byte in data:
        hex_digits.append(byte >> 4)     
        hex_digits.append(byte & 0x0F)   
    return hex_digits


def build_schematic(filename, schematic_name):
    schem = mcschematic.MCSchematic()
    hex_digits = read_bytes(filename)
    # print(hex_digits)
    for i, digit in enumerate(hex_digits):
        x = i % 16
        z = i // 16
        block = BYTES_TO_BLOCKS[digit]
        schem.setBlock((x, 0, z), block)

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
    palette = schem['Schematic']['Blocks']['Palette']
    # data is a byte array storing the order that the blocks are stored, using the indices in palette corresponding to the name of the block
    data = schem['Schematic']['Blocks']['Data']
    
    index_to_block = {v: k for k, v in palette.items()}

    # convert indices to block array to byte array 
    byte_array = []
    for byte in data:
        block = index_to_block[byte]
        # don't include extranneous blocks
        if block in BLOCKS_TO_BYTES:
            byte_array.append(BLOCKS_TO_BYTES[block])
    
    # convert back to byte values
    temp = []
    for i in range(0, len(byte_array), 2):
        temp.append(16 * byte_array[i] + byte_array[i + 1])
    byte_array = temp


    byte_array = bytes(byte_array)


    with open(output_file, "wb") as f:
        f.write(byte_array)





if __name__ == "__main__":
    main()
