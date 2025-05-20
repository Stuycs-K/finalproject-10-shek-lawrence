import mcschematic
import nbtlib 
import argparse 
import math

SCHEMATICS_FOLDER = "/mnt/c/Users/lawre/AppData/Roaming/.minecraft/config/worldedit/schematics/"

BYTES_TO_BLOCKS = []
with open("blocks.txt", "r") as f:
    for i in range(256):
        BYTES_TO_BLOCKS.append(f.readline().rstrip())

    
BLOCKS_TO_BYTES =  {block: i for i, block in enumerate(BYTES_TO_BLOCKS)}



def main():
    parser = argparse.ArgumentParser(description="Encode a file or decode a schematic file.")
    parser.add_argument("filename", help="The name of the file to process")
    parser.add_argument("-m", "--mode", choices=["encode", "decode"], type=str.lower, help="Mode of operation")
    parser.add_argument("-o", "--output", help="Output file name (for decode)")

    args = parser.parse_args()
    if args.output is None:
        print("Please specify the name of the output file")
        exit(1)
    if args.mode == "encode":
        if args.output is None:
            args.output = "secret"
        build_schematic(args.filename, args.output)
    elif args.mode == "decode":
        if args.output is None:
            args.output = "decrypted.txt"
        decode_schematic(SCHEMATICS_FOLDER + args.filename, args.output)
    else:
        print("Invalid mode. Please specify: '-m encode' or '-m decode'")
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

    byte_array = [b for b in data]
    return byte_array


def build_schematic(filename, schematic_name):
    schem = mcschematic.MCSchematic()
    byte_array = read_bytes(filename)

    total_blocks = len(byte_array)
    # round up
    side_length = math.ceil(total_blocks ** (1 / 3))
    for i, index in enumerate(byte_array):
        x = i % side_length
        z = (i // side_length) % side_length
        y = i // (side_length * side_length)
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
    palette = schem['Schematic']['Blocks']['Palette']
    # data is a byte array storing the order that the blocks are stored, using the indices in palette corresponding to the name of the block
    data = schem['Schematic']['Blocks']['Data']
    
    index_to_block = {v: k for k, v in palette.items()}

    # convert indices to block array to byte array 
    byte_array = []
    for byte in data:
        # some blocks have additional properties, such as:
        # minecraft:brown_mushroom_block[down=true,east=true,north=true,south=true,up=true,west=true]
        # so we can split by "[" to ignore those 
        block = index_to_block[byte].split("[")[0]
        # don't include extranneous blocks
        if block in BLOCKS_TO_BYTES:
            byte_array.append(BLOCKS_TO_BYTES[block])
    byte_array = bytes(byte_array)
    with open(output_file, "wb") as f:
        f.write(byte_array)





if __name__ == "__main__":
    main()
