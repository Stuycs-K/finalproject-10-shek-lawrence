import mcschematic


bytes_to_blocks = ["minecraft:white_wool",
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

def main():
    build_schematic("test.txt")


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
        block = bytes_to_blocks[digit]
        schem.setBlock((x, 0, z), block)

    schem.save("/mnt/c/Users/lawre/AppData/Roaming/.minecraft/config/worldedit/schematics", "secret", mcschematic.Version.JE_1_21_5)

if __name__ == "__main__":
    main()
