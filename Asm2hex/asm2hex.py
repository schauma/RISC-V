#!/usr/bin/python3
import copy
from instr_conv import *
import sys

filename = sys.argv[1]
name = filename.split(".")[0]
asm = []
# We dont do alignment of stuff
with open(filename, "r") as f:
    for line in f:
        # Skip all comments
        line = line.strip()
        if line and not line.startswith("#"):
            idx = line.find("#")
            asm += [line[0:idx]] if idx != -1 else [line]

# First find labels and corresponding line numbers
labels = {}
asm_copy = copy.copy(asm)
for number, line in enumerate(asm):
    words = line.strip().split(":")
    # Potentially necessary to skip directives starting with .xxxx
    # Lable ends with : Colon
    if len(words) >1:
        labels.update({words[0].strip(): number})

    asm_copy[number] = words[-1].strip()
asm = asm_copy
del asm_copy


assemble(asm,name)




