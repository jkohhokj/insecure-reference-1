import argparse



from pwn import *

def decrypt_firmware(firmware):
    with open(firmware,"rb") as f:
        data = f.read()

    key = 0
    while (True):
        if (xor(data,p16(key,endian="big"))[-4:] == b"AAA\00"):
            print(key,xor(data,p16(key,endian="big")))
            break
        if (key % 1000 == 0):
            print(key)
        key += 1



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Firmware Decrypt Tool")
    parser.add_argument("--firmware", help="Path to the firmware image to decrypt.", required=True)
    args = parser.parse_args()

    decrypt_firmware(firmware=args.firmware)
