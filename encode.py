import mcschematic
import nbtlib 

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
    build_schematic("test.txt")
    decoded_bytes = decode_schematic(SCHEMATICS_FOLDER + "encoded.schem")
    # with open("decrypted.txt", "wb") as f:
        # f.write(decoded_bytes)


def read_bytes(filename):
    with open(filename, "rb") as f:
        data = f.read()
    hex_digits = []
    for byte in data:
        hex_digits.append(byte >> 4)     
        hex_digits.append(byte & 0x0F)   
    return hex_digits


def build_schematic(filename):
    schem = mcschematic.MCSchematic()
    hex_digits = read_bytes(filename)

    for i, digit in enumerate(hex_digits):
        x = i % 16
        z = i // 16
        block = BYTES_TO_BLOCKS[digit]
        schem.setBlock((x, 0, z), block)

    schem.save(SCHEMATICS_FOLDER, "secret", mcschematic.Version.JE_1_21_5)


def decode_schematic(filepath):
    schem = nbtlib.load(filepath)
    # palette is a dictionary that maps each block to an integer 
    palette = schem['Schematic']['Blocks']['Palette']
    # data is a byte array storing the order that the blocks are stored, using the indices in palette corresponding to the name of the block
    data = schem['Schematic']['Blocks']['Data']
    
    index_to_block = {v: k for k, v in palette.items()}
    ordered_blocks = [index_to_block[byte] for byte in data]
    for i, block in enumerate(ordered_blocks):
        print(f"{i}: {block}")


    return


if __name__ == "__main__":
    main()
