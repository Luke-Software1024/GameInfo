from sys import argv

def header_checksum(file):
    checksum = 0
    for address in range(0x134, 0x14D):
        checksum = checksum - file[address] - 1
    checksum &= 0b11111111
    return checksum

def global_checksum(file):
    checksum = 0
    for address, value in enumerate(file):
        if not address in (0x14E, 0x14F):
            checksum += value
            checksum &= 0b1111111111111111
    return checksum

mappers = {0x00: "ROM ONLY", 0x01: "MBC1", 0x02: "MBC1+RAM", 0x03: "MBC1+RAM+BATTERY", 0x05: "MBC2", 0x06: "MBC2+BATTERY", 0x08: "ROM+RAM", 0x09: "ROM+RAM+BATTERY", 0x0B: "MMM01", 0x0C: "MMM01+RAM", 0x0D: "MMM01+RAM+BATTERY", 0x0F: "MBC3+TIMER+BATTERY", 0x10: "MBC3+TIMER+RAM+BATTERY", 0x11: "MBC3", 0x12: "MBC3+RAM", 0x13: "MBC3+RAM+BATTERY", 0x19: "MBC5", 0x1A: "MBC5+RAM", 0x1B: "MBC5+RAM+BATTERY", 0x1C: "MBC5+RUMBLE", 0x1D: "MBC5+RUMBLE+RAM", 0x1E: "MBC5+RUMBLE+RAM+BATTERY", 0x20: "MBC6", 0x22: "MBC7+SENSOR+RUMBLE+RAM+BATTERY", 0xFC: "POCKET CAMERA", 0xFD: "BANDAI TAMA5", 0xFE: "HuC3", 0xFF: "HuC1+RAM+BATTERY"}
cgb_compats = {0x80: "CGB enhanced, DMG compatible", 0xC0: "CGB only"}
sgb_compat = {0x03: "Compatible"}
ram_sizes = {0x00: "None", 0x01: "2 KiB", 0x02: "8 KiB", 0x03: "32 KiB", 0x04: "128 KiB", 0x05: "64 KiB"}
region = {0x00: "Japan", 0x01: "Overseas"}

print("GBInfo v1.0 by Luke")
print("Extract cartridge info from Game Boy ROMs.\n")

def main():
    if len(argv) < 2:
        print("Usage: gbinfo %CARTRIDGE_NAME%")
        return 0

    try:
        file = open(argv[1], "rb")
    except OSError as error:
        print(error)
        return 0

    file_contents = file.read()
    print(f"Cartridge info for {argv[1]}:\n")

    if file_contents[0x143] in cgb_compats:
        print(f"    Game title: {file_contents[0x134:0x143]}")
        print(f"    CGB compatibility: {file_contents[0x143]} ({cgb_compats.get(file_contents[0x143], "DMG only")})")
    else:
        print(f"    Game title: {file_contents[0x134:0x144]}")

    if file_contents[0x14B] == 0x33:
        print(f"    Publisher: {file_contents[0x144:0x146]}")
    else:
        print(f"    Publisher: {file_contents[0x14B]}")

    print(f"    SGB compatibility: {file_contents[0x146]} ({sgb_compat.get(file_contents[0x146], "Incompatible")})")
    print(f"    Cartridge hardware: {file_contents[0x147]} ({mappers.get(file_contents[0x147], "Invalid value")})")
    print(f"    ROM size: {file_contents[0x148]} ({32 * (1 << file_contents[0x148])} KiB)")
    print(f"    RAM size: {file_contents[0x149]} ({ram_sizes.get(file_contents[0x149], "Invalid value")})")
    print(f"    Region: {file_contents[0x14A]} ({region.get(file_contents[0x14A], "Invalid value")})")
    print(f"    Revision: {file_contents[0x14C]}")

    print(f"    Header checksum...")
    checksum = header_checksum(file_contents)
    if checksum == file_contents[0x14D]:
        print(f"Checks out. ({checksum})")
    else:
        print(f"Doesn't check out. (stored: {file_contents[0x14D]}, calculated: {checksum})")

    print("    Global checksum...")
    checksum = global_checksum(file_contents)
    if checksum == (file_contents[0x14E] << 8) + file_contents[0x14F]:
        print(f"Checks out. ({checksum})")
    else:
        print(f"Doesn't check out. (stored: {(file_contents[0x14E] << 8) + file_contents[0x14F]}, calculated: {checksum})")

if __name__ == "__main__":
    main()