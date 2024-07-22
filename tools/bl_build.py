#!/usr/bin/env python

# Copyright 2024 The MITRE Corporation. ALL RIGHTS RESERVED
# Approved for public release. Distribution unlimited 23-02181-25.

"""
Bootloader Build Tool

This tool is responsible for building the bootloader from source and copying
the build outputs into the host tools directory for programming.
"""
import os
import pathlib
import subprocess
from Crypto.Random import get_random_bytes
from pwn import *



REPO_ROOT = pathlib.Path(__file__).parent.parent.absolute()
BOOTLOADER_DIR = os.path.join(REPO_ROOT, "bootloader")

def arrayize(binary_string):
    return '{' + ','.join([hex(char) for char in binary_string]) + '}'

def make_bootloader() -> bool:
    # Build the bootloader from source.

    os.chdir(BOOTLOADER_DIR)

    # Write keys to secret_build_output.txt
    vkey = get_random_bytes(2)
    
    with open('secret_build_output.txt', 'wb+') as f:
        f.write(vkey)
    print(f"VKEY: {arrayize(vkey)}")
    with open('./src/secrets.h', 'w') as f:
        f.write("#ifndef SECRETS_H\n")
        f.write("#define SECRETS_H\n")
        f.write("const uint8_t V_KEY[2] = " + arrayize(vkey) + ";\n")
        f.write("#endif")

    result = subprocess.run("make clean", shell=True, stdout=subprocess.DEVNULL)
    status = subprocess.run("make",stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    if b"Error" in status.stderr:
        print("Errored! Your C code could not be compiled.",status.stderr)

    # Return True if make returned 0, otherwise return False.
    return status == 0


if __name__ == "__main__":
    make_bootloader()