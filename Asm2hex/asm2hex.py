#!/usr/bin/python3


import copy
from instr_conv import *
import sys

filename = sys.argv[1]
name = filename.split(".")[0]
asm = []

load_instr = {"lb", "lh", "lw", "lbu", "lhu"}
immediate_instr = {"addi", "slti", "sltiu", "xori", "ori", "andi"}
u_instr = {"auipc", "lui"}
store_inst = {"sw", "sh", "sb"}
r_instr = {"add", "sub", "sll", "slt", "sltu", "xor", "srl", "sra", "or", "and"}
branch_instr = {"beq", "bne", "blt", "bge", "bltu", "bgeu"}
jump_intr = {"jal"}
jump_reg_instr = {"jalr"}
i_shift_intr = {"slli", "srli", "srai"}
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

f = open(f"{name}.hex","w")

for number, line in enumerate(asm):
    instr, remains = line.split(" ", 1)
    machine_code = ""
    if instr in load_instr:
        machine_code =conv_load_instr(instr, remains)
    elif instr in immediate_instr:
        machine_code =conv_immediate_instr(instr, remains)
    elif instr in u_instr:
        machine_code =conv_u_instr(instr, remains)
    elif instr in store_inst:
        machine_code =conv_store_instr(instr, remains)
    elif instr in r_instr:
        machine_code =conv_r_instr(instr, remains)
    elif instr in branch_instr:
        machine_code =conv_branch_instr(instr, remains,labels,number)
    elif instr in jump_intr:
        machine_code =conv_jump_intr(instr, remains,labels,number)
    elif instr in jump_reg_instr:
        machine_code =conv_jump_reg_instr(instr, remains)
    elif instr in i_shift_intr:
        machine_code =conv_i_shift_instr(instr, remains)
    else:
        ValueError()

    f.write(machine_code + "\n")

