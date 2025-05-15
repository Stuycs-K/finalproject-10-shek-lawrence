import mcschematic

schem = mcschematic.MCSchematic()

blocks = ["minecraft:white_wool",
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
    file_bytes = read_bytes("test.txt");
    bytes_list = []
    for byte in file_bytes:
        to_hex = hex(byte)
        bytes_list.append(convert(to_hex[-2]))
        bytes_list.append(convert(to_hex[-1]))

    for i in bytes_list:
        schem.setBlock((-8 + i, -1, 0), blocks[int(bytes_list[i])])

    schem.save("/mnt/c/Users/lawre/AppData/Roaming/.minecraft/config/worldedit/schematics", "secret", mcschematic.Version.JE_1_21_5)
    


def read_bytes(filename):
    with open(filename, "rb") as f:
        f_bytes = f.read()
        return f_bytes

def convert(x):
    if x.isnumeric():
        return int(x)
    return int(ord(x) - ord('a')) + 10

if __name__ == "__main__":
    main()
