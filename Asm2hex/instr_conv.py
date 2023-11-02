from collections import namedtuple

load_instr = {"lb", "lh", "lw", "lbu", "lhu"}
immediate_instr = {"addi", "slti", "sltiu", "xori", "ori", "andi"}
u_instr = {"auipc", "lui"}
store_inst = {"sw", "sh", "sb"}
r_instr = {"add", "sub", "sll", "slt", "sltu", "xor", "srl", "sra", "or", "and"}
branch_instr = {"beq", "bne", "blt", "bge", "bltu", "bgeu"}
jump_intr = {"jal"}
jump_reg_instr = {"jalr"}
i_shift_intr = {"slli", "srli", "srai"}


registers = {
    "x0": "00000",
    "x1": "00001",
    "x2": "00010",
    "x3": "00011",
    "x4": "00100",
    "x5": "00101",
    "x6": "00110",
    "x7": "00111",
    "x8": "01000",
    "x9": "01001",
    "x10": "01010",
    "x11": "01011",
    "x12": "01100",
    "x13": "01101",
    "x14": "01110",
    "x15": "01111",
    "x16": "10000",
    "x17": "10001",
    "x18": "10010",
    "x19": "10011",
    "x20": "10100",
    "x21": "10101",
    "x22": "10110",
    "x23": "10111",
    "x24": "11000",
    "x25": "11001",
    "x26": "11010",
    "x27": "11011",
    "x28": "11100",
    "x29": "11101",
    "x30": "11110",
    "x31": "11111",
    "zero": "00000",
    "ra": "00001",
    "sp": "00010",
    "gp": "00011",
    "tp": "00100",
    "t0": "00101",
    "t1": "00110",
    "t2": "00111",
    "s0": "01000",
    "fp": "01000",
    "s1": "01001",
    "a0": "01010",
    "a1": "01011",
    "a2": "01100",
    "a3": "01101",
    "a4": "01110",
    "a5": "01111",
    "a6": "10000",
    "a7": "10001",
    "s2": "10010",
    "s3": "10011",
    "s4": "10100",
    "s5": "10101",
    "s6": "10110",
    "s7": "10111",
    "s8": "11000",
    "s9": "11001",
    "s10": "11010",
    "s11": "11011",
    "t3": "11100",
    "t4": "11101",
    "t5": "11110",
    "t6": "11111",
}

R = namedtuple("R", ["op", "func3", "func7"])
# Structure of the dict instruction: [op,func3,func7]
r_instructions = {
    "add": R("0110011", "000", "0000000"),
    "sub": R("0110011", "000", "0100000"),
    "sll": R("0110011", "001", "0000000"),
    "slt": R("0110011", "010", "0000000"),
    "sltu": R("0110011", "011", "0000000"),
    "xor": R("0110011", "100", "0000000"),
    "srl": R("0110011", "101", "0000000"),
    "sra": R("0110011", "101", "0100000"),
    "or": R("0110011", "110", "0000000"),
    "and": R("0110011", "111", "0000000"),
}

I = namedtuple("I", ["op", "func3"])
# Structure of the dict instruction: [op,func3]
i_instructions = {
    "addi": I("0010011", "000"),
    "slti": I("0010011", "010"),
    "sltiu": I("0010011", "011"),
    "xori": I("0010011", "100"),
    "or": I("0010011", "110"),
    "and": I("0010011", "111"),
}
load_instructions = {
    "lb": I("0000011", "000"),
    "lh": I("0000011", "001"),
    "lw": I("0000011", "010"),
}
store_instructions = {
    "sb": I("0100011", "000"),
    "sh": I("0100011", "001"),
    "sw": I("0100011", "010"),
}
Is = namedtuple("Is", ["op", "func3", "func7"])
i_shift_instructions = {
    "slli": Is("0010011", "001", "0000000"),
    "srli": Is("0010011", "101", "0000000"),
    "srai": Is("0010011", "101", "0100000"),
}

U = namedtuple("U", ["op"])
u_instructions = {
    "auipc": "0110111",
    "lui": "0110111",
}

branch_instructions = {
    "beq": I("1100011", "000"),
    "bne": I("1100011", "001"),
    "blt": I("1100011", "100"),
    "bge": I("1100011", "101"),
    "bltu": I("1100011", "110"),
    "bgeu": I("1100011", "111"),
}

jump_instructions = {
    "jal": U("1101111")
}
jump_reg_instructions = {
    "jalr": I("1101111", "000")
}


# 12 bits space mean [0 4095] or [-2048, 2047]
# Must be less equal  0xFFF
def convert_I_imm(imm: str, space: int, isSigned: bool = True):
    imm = imm.strip()
    if imm.startswith("0b", ):
        # Binary number
        number = int(imm, 2)

    elif imm.startswith("0x"):
        # Hex number
        number = int(imm, 16)

    elif imm[0].isdigit() or imm[0] == "-":
        # decimal number
        number = int(imm)

    else:
        number = 1 << 25
        raise ValueError()

    assert number < 1 << space, "I Immediate {} is too long. It is only allowed {} bits" \
        .format(hex(number), space)

    if isSigned:
        number = number & (2 ** space - 1)

    number_str = f"{number:0{space}b}"
    return number_str


def conv_i_shift_instr(instr: str, remains: str):
    code = i_shift_instructions[instr]
    rd, rs1, imm = remains.split(",")
    rd, rs1 = registers[rd.strip()], registers[rs1.strip()]
    imm = convert_I_imm(imm, 5)

    binary = code.func7 + imm + rs1 + code.func3 + rd + code.op

    assert len(binary) == 32, "I Instruction encoding not 32 bit, its {} long.".format(len(binary))
    return '%0*X' % ((len(binary) + 3) // 4, int(binary, 2))


def conv_load_instr(instr: str, remains: str):
    code = load_instructions[instr]
    rd, imm = remains.split(",")
    imm, rs1 = imm.split("(")
    rd, rs1 = registers[rd.strip()], registers[rs1.strip(" )")]
    imm = convert_I_imm(imm, 12)
    binary = imm + rs1 + code.func3 + rd + code.op

    assert len(binary) == 32, "Load Instruction encoding not 32 bit, its {} long.".format(len(binary))
    return '%0*X' % ((len(binary) + 3) // 4, int(binary, 2))


def conv_immediate_instr(instr: str, remains: str):
    code = i_instructions[instr]
    rd, rs1, imm = remains.split(",")
    rd, rs1 = registers[rd.strip()], registers[rs1.strip()]
    imm = convert_I_imm(imm, 12)

    binary = imm + rs1 + code.func3 + rd + code.op

    assert len(binary) == 32, "I Instruction encoding not 32 bit, its {} long.".format(len(binary))
    return '%0*X' % ((len(binary) + 3) // 4, int(binary, 2))


def conv_u_instr(instr: str, remains: str):
    code = u_instructions[instr]
    rd, imm = remains.split(",")
    rd = registers[rd.strip()]
    imm = convert_I_imm(imm, 20)

    binary = imm + rd + code.op

    assert len(binary) == 32, "I Instruction encoding not 32 bit, its {} long.".format(len(binary))
    return '%0*X' % ((len(binary) + 3) // 4, int(binary, 2))


def conv_store_instr(instr: str, remains: str):
    code = store_instructions[instr]
    rs2, imm = remains.split(",")
    imm, rs1 = imm.split("(")
    rs1, rs2 = registers[rs1.strip(" )")], registers[rs2.strip()]

    imm = convert_I_imm(imm, 12)

    binary = imm[:7] + rs2 + rs1 + code.func3 + imm[-5:] + code.op

    assert len(binary) == 32, "Load Instruction encoding not 32 bit, its {} long.".format(len(binary))
    return '%0*X' % ((len(binary) + 3) // 4, int(binary, 2))


def conv_r_instr(instr: str, remains: str):
    code = r_instructions[instr]
    rd, rs1, rs2 = remains.split(",")
    rd, rs1, rs2 = registers[rd.strip()], registers[rs1.strip()], registers[rs2.strip()]

    binary = code.func7 + rs2 + rs1 + code.func3 + rd + code.op

    assert len(binary) == 32, "R Instruction encoding not 32 bit, it's {} bits long.".format(len(binary))
    return '%0*X' % ((len(binary) + 3) // 4, int(binary, 2))  # discard the "0x"


def conv_branch_instr(instr: str, remains: str, labels: dict, line_number: int):
    code = branch_instructions[instr]
    addr_space = 13
    rs1, rs2, label = remains.split(",")
    rs1, rs2, label = registers[rs1.strip()], registers[rs2.strip()], label.strip()
    imm = (labels[label] - line_number) * 4  # Times 4 since we address with multiples of 4
    imm = imm & (2 ** addr_space - 1)
    number_str = f"{imm:0{addr_space}b}"
    assert len(number_str) == addr_space, "BTA is not 13 bits"
    binary = number_str[0] + number_str[2:8] + rs2 + rs1 + code.func3 + number_str[8:12] + number_str[1] + code.op

    assert len(binary) == 32, "B Instruction encoding not 32 bit, it's {} bits long.".format(len(binary))
    return '%0*X' % ((len(binary) + 3) // 4, int(binary, 2))  # discard the "0x"


def conv_jump_intr(instr: str, remains: str, labels: dict, line_number: int):
    code = jump_instructions[instr]
    addr_space = 21
    rd, label = remains.split(",")
    rd, label = registers[rd.strip()], label.strip()

    imm = (labels[label] - line_number) * 4# Times 4 since we address with multiples of 4
    imm = imm & (2 ** addr_space - 1)
    number_str = f"{imm:0{addr_space}b}"

    assert len(number_str) == addr_space, "BTA is not 21 bits"
    binary = number_str[0] + number_str[10:20] + number_str[9] + number_str[1:9] + rd + code.op

    assert len(binary) == 32, "B Instruction encoding not 32 bit, it's {} bits long.".format(len(binary))
    return '%0*X' % ((len(binary) + 3) // 4, int(binary, 2))  # discard the "0x"


def conv_jump_reg_instr(instr: str, remains: str):
    pass


def assemble(asm : list,file_name : str):
    f = open(f"{file_name}.hex","w")

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
            raise ValueError()

        f.write(machine_code + "\n")
