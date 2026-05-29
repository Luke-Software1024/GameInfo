from sys import argv

if len(argv) < 2:
    print("Usage: nesinfo %CARTRIDGE_NAME%")
    exit(2)

nametable_arrs = {0b0: "Vertical", 0b1: "Horizontal"}
present = {0b1: "Present"}
yes = {0b1: "Yes"}
nes2 = {0b10: "Yes"}

try:
    file = open(argv[1], "rb")
except OSError as error:
    print(error)
    exit(2)

print("NESInfo v1.0 by Luke")
print("Extract cartridge info from NES ROMs.\n")

file_contents = file.read()
print(f"Cartridge info for {argv[1]}:\n")

if file_contents[0x0:0x4] == b"NES\x1A":
    print(f"    Header matches. ({file_contents[0x0:0x4]})")
else:
    print(f"    Header doesn't match. (stored: {file_contents[0x0:0x4]}, expected: b'NES\\x1a')")

nes2_v = (file_contents[0x7] & 0b00001100) >> 2
if nes2_v == 0b10:
    print(f"    PRG-ROM size: {(file_contents[0x9] & 0b00001111) << 8 + file_contents[0x4]} ({(file_contents[0x9] & 0b00001111) << 8 + file_contents[0x4] * 16} KiB)")
    print(f"    CHR-ROM size: {(file_contents[0x9] & 0b11110000) << 4 + file_contents[0x5]} ({(file_contents[0x9] & 0b11110000) << 4 + file_contents[0x5] * 8} KiB)")
else:
    print(f"    PRG-ROM size: {file_contents[0x4]} ({file_contents[0x4] * 16} KiB)")
    print(f"    CHR-ROM size: {file_contents[0x5]} ({file_contents[0x5] * 8} KiB)")
print(f"    Nametable arrangement: {file_contents[0x6] & 0b00000001} ({nametable_arrs.get(file_contents[0x6] & 0b00000001)}), alt: {(file_contents[0x6] & 0b00001000) >> 3} ({yes.get((file_contents[0x6] & 0b00001000) >> 3, "No")})")
print(f"    Flash memory: {(file_contents[0x6] & 0b00000010) >> 1} ({present.get((file_contents[0x6] & 0b00000010) >> 1, "Not present")})")
print(f"    Trainer: {(file_contents[0x6] & 0b00000100) >> 2} ({present.get((file_contents[0x6] & 0b00000100) >> 2, "Not present")})")

if nes2_v == 0b10:
    print(f"    Mapper ID: {(file_contents[0x8] & 0b00001111 << 8) + (file_contents[0x7] & 0b11110000) + (file_contents[0x6] & 0b11110000) >> 4}")
else:
    print(f"    Mapper ID: {(file_contents[0x7] & 0b11110000) + (file_contents[0x6] & 0b11110000) >> 4}")
print(f"    VS. System: {file_contents[0x7] & 0b00000001} ({yes.get(file_contents[0x7] & 0b00000001, "No")})")
print(f"    PlayChoice-10: {(file_contents[0x7] & 0b00000010) >> 1} ({yes.get((file_contents[0x7] & 0b00000010) >> 1, "No")})")
print(f"    NES 2.0: {nes2_v} ({nes2.get(nes2_v, "No")})")
if nes2_v == 0b10:
    print(f"Submapper: {(file_contents[0x8] & 0b11110000) >> 4}")