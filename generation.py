from errors import handleError
from nodes import *

class Generator:
    def __init__(self, rootNode : ScopeNode) -> None:
        self.root : ScopeNode = rootNode
        self.code : str = ""
        self.globalvars : dict[str, int] = dict()
        self.stacksize = 0

    # Stack operations
    # Important to Note for Darwin aarch64
        # Stack must change by increments of 16 bytes (twice the size of a register (64 bits/8 bytes))
        # Darwin aarch64 uses Little Endian format, so bits increase as memory address increases
            # bit representation    higher to lower address --->
            # X0                    63 62 ... 32 ... 0 (bits)
            # memory rep.           lower to higher address --->
            # X0                    0 ... 32 ... 62 63 (bits)
    def push(self, register : str) -> str:
        self.stacksize += 1
        return f"\tstr {register}, [SP, #-16]!\n"

    def pop(self, register : str) -> str:
        self.stacksize -= 1
        return f"\tldr {register}, [SP], #16\n"

    def push2(self, register1 : str, register2 : str) -> str:
        self.stacksize += 1
        return f"\tstp {register1}, {register2}, [SP, #-16]!\n"

    def pop2(self, register1 : str, register2 : str) -> str:
        self.stacksize -= 1
        return f"\tldr {register1}, {register2}, [SP], #16\n"

    def ldrFromStack(self, register : str) -> str:
        return f"\tldr {register}, [SP]\n"

    # mov register into register
    def mov(self, register1 : str, register2 : str) -> str:
        return f"\tmov {register1}, {register2}\n"

    # mov data into register
    def mov2byte(self, register : str, value : int) -> str:
        return f"\tmov {register}, #{hex(int(value) % 2**16)}\n"

    def movInt(self, register : str, value : int) -> str:
        p16 = 2**16
        p32 = 2**32
        p48 = 2**48
        p64 = 2**64
        value = int(value) % p64
        instructions = self.mov2byte(register, value)
        if value >= p16:
            instructions += f"\tmovk {register}, #{hex((value//p16) % p16)}, lsl#16\n"
        if value >= p32:
            instructions += f"\tmovk {register}, #{hex((value//p32) % p16)}, lsl#32\n"
        if value >= p48:
            instructions += f"\tmovk {register}, #{hex((value//p48) % p16)}, lsl#48\n"
        return instructions

    # Supervisor call https://opensource.apple.com/source/xnu/xnu-7195.81.3/bsd/kern/syscalls.master.auto.html
        # 1 - exit
            # X0 - return code
        # 4 - write
            # X0 - place to write (1 = STDOUT)
            # X1 - output string address
            # X2 - length of string in bytes/chars
    def syscall(self, number : int, args : list) -> str:
        instructions = ""
        for i in range(min(len(args), 11)):
            if isinstance(args[i], str):
                instructions += self.mov(f"X{i}", args[i])
            else:
                instructions += self.mov2byte(f"X{i}", args[i])
        instructions += self.mov2byte("X16", number)
        instructions += "\tsvc #0xffff\n"
        return instructions

    # math
    def sub(self, dest : str, arg1 : str | int, arg2 : str | int) -> str:
        instructions = f"\tsub {dest}, "
        if isinstance(arg1, str):
            instructions += arg1
        else:
            instructions += hex(int(arg1) % 2**16)
        instructions += ", "
        if isinstance(arg2, str):
            instructions += arg2
        else:
            instructions += hex(int(arg2) % 2**16)
        instructions += "\n"
        return instructions

    def add(self, dest : str, arg1 : str | int, arg2 : str | int) -> str:
        instructions = f"\tadd {dest}, "
        if isinstance(arg1, str):
            instructions += arg1
        else:
            instructions += hex(int(arg1) % 2**16)
        instructions += ", "
        if isinstance(arg2, str):
            instructions += arg2
        else:
            instructions += hex(int(arg2) % 2**16)
        instructions += "\n"
        return instructions

    def gen_expr(self, node : Node) -> None:
        if isinstance(node, LetNode):
            if node.ident.value in self.globalvars:
                handleError(10)
            else:
                self.gen_expr(node.expr)
                self.code += self.pop("X0") # get return value from stack
                self.code += self.push("X0") # put variable onto stack
                self.globalvars[node.ident.value] = self.stacksize
                self.code += self.push("X0") # put return value onto stack
                return
        elif isinstance(node, ExitNode):
            self.gen_expr(node.params[0]) # process 1st parameter
            self.code += self.pop("X0") # get return value from stack
            self.code += self.mov("X11", "X0") # move return value into X11
            self.code += self.syscall(1, ["X11"])
        elif isinstance(node, IntLitNode):
            self.code += self.movInt("X0", int(node.value))
            self.code += self.push("X0") # push return value onto stack
        elif isinstance(node, IdentNode):
            if node.value not in self.globalvars:
                handleError(11)
            else:
                # put variable value into X0
                self.code += self.add("SP", "SP", 16*(self.stacksize - self.globalvars[node.value]))
                self.code += self.ldrFromStack("X0")
                self.code += self.sub("SP", "SP", 16*(self.stacksize - self.globalvars[node.value]))

                self.code += self.push("X0") # push return value onto stack
                return
        elif isinstance(node, AddNode):
            self.gen_expr(node.params[0])
            self.gen_expr(node.params[1])
            self.code += self.pop("X1")
            self.code += self.pop("X2")
            self.code += self.add("X0", "X1", "X2")
            self.code += self.push("X0")
        elif isinstance(node, SubNode):
            self.gen_expr(node.params[0])
            self.gen_expr(node.params[1])
            self.code += self.pop("X1")
            self.code += self.pop("X2")
            self.code += self.sub("X0", "X2", "X1")
            self.code += self.push("X0")

    def generate(self) -> str:
        self.code = ""
        self.code += "// compiled with fs65c for Darwin arm64/aarch64\n\n"
        self.code += ".global _start\n"
        self.code += ".p2align 2\n\n"

        self.code += "_start:\n"

        for statement in self.root.statements:
            self.gen_expr(statement)
            self.code += self.pop("X0") # remove return value

        return self.code
