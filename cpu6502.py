from enum import Enum, auto
from pickle import FALSE
from re import A

#Gives numerical values
class Mode(Enum):
    IMMEDIATE = auto()
    ZEROPAGE = auto()
    ZEROPAGEX = auto()
    ABSOLUTE = auto()
    ABSOLUTEX = auto()
    ABSOLUTEY = auto()
    IMPLIED = auto()
    INDIRECT = auto()
    RELATIVE = auto()

class CPU:
    def __init__(self):
        self.memory = []
        for _ in range(0, 65536):
            self.memory.append(0)

        self.a = 0x00
        self.x = 0x00
        self.y = 0x00
        self.pc = 0x1000
        self.sp = 0xFF

        self.n = False #Negative flag
        self.v = False #Overflow flag
        self.b = False #Break flag
        self.d = False #Decimal flag
        self.i = False #Interrupt flag
        self.z = False #Zero flag
        self.c = False #Carry flag

        self.commands = {  
            #Debugging commands
            0x42: {"func": self.print_status, "m": Mode.IMPLIED},

            #Loading Commands
            0xA9: {"func": self.LDA, "m": Mode.IMMEDIATE},
            0xA5: {"func": self.LDA, "m": Mode.ZEROPAGE},
            0xB5: {"func": self.LDA, "m": Mode.ZEROPAGEX},
            0xBD: {"func": self.LDA, "m": Mode.ABSOLUTEX},
            0xB9: {"func": self.LDA, "m": Mode.ABSOLUTEY},

            #Load X Y Register commands
            0xA2: {"func": self.LDX, "m": Mode.IMMEDIATE},
            0xAE: {"func": self.LDX, "m": Mode.ABSOLUTE},
            0xA0: {"func": self.LDY, "m": Mode.IMMEDIATE},

            #Absolute Commands
            0x8D: {"func": self.STA, "m": Mode.ABSOLUTE},
            0x8E: {"func": self.STX, "m": Mode.ABSOLUTE},
            0x8C: {"func": self.STY, "m": Mode.ABSOLUTE},

            #Implied Commands
            0xE8: {"func": self.INX, "m": Mode.IMPLIED},
            0XC8: {"func":self.INY, "m": Mode.IMPLIED},

            #Transfer commands
            0XAA: {"func":self.TAX, "m": Mode.IMPLIED},
            0X8A: {"func":self.TXA, "m": Mode.IMPLIED},
            0XA8: {"func":self.TAY, "m": Mode.IMPLIED},
            0X98: {"func":self.TYA, "m": Mode.IMPLIED},
            0xCA: {"func":self.DEX, "m": Mode.IMPLIED},
            0x88: {"func":self.DEY, "m": Mode.IMPLIED},

            #Flag commands
            0X18: {"func":self.CLC, "m": Mode.IMPLIED},
            0X38: {"func":self.SEC, "m": Mode.IMPLIED},
            0X58: {"func":self.CLI, "m": Mode.IMPLIED},
            0X78: {"func":self.SEI, "m": Mode.IMPLIED},
            0XB8: {"func":self.CLV, "m": Mode.IMPLIED},
            0XD8: {"func":self.CLD, "m": Mode.IMPLIED},
            0XF8: {"func":self.SED, "m": Mode.IMPLIED},

            #Jump commands
            0x4C: {"func":self.JMP, "m": Mode.ABSOLUTE},
            0x6C: {"func":self.JMP, "m": Mode.INDIRECT},

            #Compare commands
            0xC9: {"func":self.CMP, "m": Mode.IMMEDIATE},
            0xC5: {"func":self.CMP, "m": Mode.ZEROPAGE},
            0xD5: {"func":self.CMP, "m": Mode.ZEROPAGEX},
            0xCD: {"func":self.CMP, "m": Mode.ABSOLUTE},
            0xDD: {"func":self.CMP, "m": Mode.ABSOLUTEX},
            0xD9: {"func":self.CMP, "m": Mode.ABSOLUTEY},

            #Branch commands
            0x10: {"func":self.BPL, "m": Mode.RELATIVE},
            0x30: {"func":self.BMI, "m": Mode.RELATIVE},
            0x50: {"func":self.BVC, "m": Mode.RELATIVE},
            0x70: {"func":self.BVS, "m": Mode.RELATIVE},
            0x90: {"func":self.BCC, "m": Mode.RELATIVE},
            0xB0: {"func":self.BCS, "m": Mode.RELATIVE},
            0xD0: {"func":self.BNE, "m": Mode.RELATIVE},
            0xF0: {"func":self.BEQ, "m": Mode.RELATIVE},

            #Stack command
            0x9A: {"func":self.TXS, "m": Mode.IMPLIED},
            0xBA: {"func":self.TSX, "m": Mode.IMPLIED},
            0x48: {"func":self.PHA, "m": Mode.IMPLIED},
            0x68: {"func":self.PLA, "m": Mode.IMPLIED},
            0x08: {"func":self.PHP, "m": Mode.IMPLIED},
            0x28: {"func":self.PLP, "m": Mode.IMPLIED},
        }


        self.increments = {
            Mode.IMMEDIATE: 2,
            Mode.ZEROPAGE: 2,
            Mode.ZEROPAGEX: 2,
            Mode.ABSOLUTE: 3,
            Mode.IMPLIED: 1,
            Mode.ABSOLUTEX: 3,
            Mode.ABSOLUTEY: 3,
            Mode.INDIRECT: 3,
            Mode.RELATIVE: 2
        }

    # Fetching and executing commands
    def tick(self):
        #fetching command
        command = self.memory[self.pc]
        #execution
        if command in self.commands:
            f = self.commands[command]["func"]
            m = self.commands[command]["m"]
            f(m)
            self.pc += self.increments[m]
        else:
            print(f"Command: {command} not implemented at location {hex(self.pc)}")
            input()

    def get_location_by_mode(self, mode):
        loc = 0

        if mode == Mode.IMMEDIATE:
            loc = self.pc + 1

        elif mode == Mode.ABSOLUTE:
            lsb = self.memory[self.pc+1] 
            msb = self.memory[self.pc+2] 
            loc = msb * 256 + lsb

        elif mode == Mode.ABSOLUTEX:
            lsb = self.memory[self.pc+1] 
            msb = self.memory[self.pc+2] 
            loc = msb * 256 + lsb
            loc += self.x

        elif mode == Mode.ABSOLUTEY:
            lsb = self.memory[self.pc+1] 
            msb = self.memory[self.pc+2] 
            loc = msb * 256 + lsb
            loc += self.y
        
        elif mode == Mode.ZEROPAGE:
            lsb = self.memory[self.pc+1] 
            loc = lsb

        elif mode == Mode.ZEROPAGEX:
            lsb = self.memory[self.pc+1] 
            loc = lsb + x

        elif mode == Mode.INDIRECT:
            lsb = self.memory[self.pc+1] 
            msb = self.memory[self.pc+2]
            loc = msb * 256 + lsb
            
            lsb = self.memory[loc]
            msb = self.memory[loc + 1]
            loc = msb * 256 + lsb
        elif mode == Mode.RELATIVE:
            loc = self.pc + 1

        return loc

    # Wrapping the 8 bit values
    def wrap(self, value):
        if value > 255:
            value = value % 256;
        if value < 0:
            value += 256
        return value

    # Loading Accumulator
    def LDA(self, mode):
        loc = self.get_location_by_mode(mode)
        #Loading value from memory
        val = self.memory[loc]
        #Putting the value in the accumulator
        self.a = val 

    # Loading X Register
    def LDX(self, mode):
        loc = self.get_location_by_mode(mode)
        #Loading value from memory
        val = self.memory[loc]
        #Putting the value in the accumulator
        self.x = val 

    # Loading Y Register
    def LDY(self, mode):
        loc = self.get_location_by_mode(mode)
        #Loading value from memory
        val = self.memory[loc]
        #Putting the value in the accumulator
        self.y = val 
    
    # Storing Accumulator
    def STA(self, mode):
        # Find the location based on the mode
        loc = self.get_location_by_mode(mode)
        #Update memory
        self.memory[loc] = self.a
        
    # Storing X Register
    def STX(self, mode):
        loc = self.get_location_by_mode(mode)
        #Update memory
        self.memory[loc] = self.x
        
    # Storing Y Register
    def STY(self, mode):
        loc = self.get_location_by_mode(mode)
        #Update memory
        self.memory[loc] = self.y
    
    # Incrementing X Register
    def INX(self, mode):
        self.x += 1
        self.x = self.wrap(self.x)

    # Incrementing Y Register
    def INY(self, mode):
        self.y += 1
        self.y = self.wrap(self.y)

    # Decrementing X Register
    def DEX(self, mode):
        self.x -= 1
        self.x = self.wrap(self.x)

    # Decrementing Y Register
    def DEY(self, mode):
        self.y -= 1
        self.y = self.wrap(self.y)

    # Transferring Accumulator to X Register
    def TAX(self, mode):
        self.x = self.a

    # Transferring X Register to Accumulator
    def TXA(self, mode):
        self.a = self.x

    # Transferring Accumulator to Y Register
    def TAY(self, mode):
        self.y = self.a

    # Transferring Y Register to Accumulator
    def TYA(self, mode):
        self.a = self.y

    # Clearing Carry Flag
    def CLC(self, mode):
        self.c = False 

    # Setting Carry Flag
    def SEC(self, mode):
        self.c = True

    # Clearing Interrupt Flag
    def CLI(self, mode):
        self.i = False

    # Setting Interrupt Flag
    def SEI(self, mode):
        self.i = True

    # Clearing Overflow Flag
    def CLV(self, mode):
        self.v = False

    # Clearing Decimal Flag
    def CLD(self, mode):
        self.d = False

    # Setting Decimal Flag
    def SED(self, mode):
        self.d = True

    # Jumping to a new location
    def JMP(self, mode):
        loc = self.get_location_by_mode(mode)
        self.pc = loc - self.increments[mode]

    # Comparing Accumulator with Memory
    def CMP(self, mode):
        loc = self.get_location_by_mode(mode)
        value = self.memory[loc]

        if value >= self.a:
            self.c = True

        if value == self.a:
            self.z = True
        
        if self.a >= 128:
            self.n = True
            
    #BMI
    def BMI(self, mode):
        loc = self.get_location_by_mode(mode)
        value = self.memory[loc]

        #Jump to the offset
        if self.n == True:
            #Recalculate if negative
            if value >= 128:
                value -= 256

            self.pc = self.pc + value

            print(f"Negative: {value}")

    # BPL
    def BPL(self, mode):
        loc = self.get_location_by_mode(mode)
        value = self.memory[loc]

        #Jump to the offset
        if self.n == False:
            #Recalculate if negative
            if value >= 128:
                value -= 256

            self.pc = self.pc + value

            print(f"Negative: {value}")
    # BVC
    def BVC(self, mode):
        loc = self.get_location_by_mode(mode)
        value = self.memory[loc]

        #Jump to the offset
        if self.v == True:
            #Recalculate if negative
            if value >= 128:
                value -= 256

            self.pc = self.pc + value

            print(f"Negative: {value}")
    # BVS
    def BVS(self, mode):
        loc = self.get_location_by_mode(mode)
        value = self.memory[loc]

        #Jump to the offset
        if self.v == False:
            #Recalculate if negative
            if value >= 128:
                value -= 256

            self.pc = self.pc + value

            print(f"Negative: {value}")
    # BCC
    def BCC(self, mode):
        loc = self.get_location_by_mode(mode)
        value = self.memory[loc]

        #Jump to the offset
        if self.c == False:
            #Recalculate if negative
            if value >= 128:
                value -= 256

            self.pc = self.pc + value

            print(f"Negative: {value}")
    # BCS
    def BCS(self, mode):
        loc = self.get_location_by_mode(mode)
        value = self.memory[loc]

        #Jump to the offset
        if self.c == True:
            #Recalculate if negative
            if value >= 128:
                value -= 256

            self.pc = self.pc + value

            print(f"Negative: {value}")
    # BNE
    def BNE(self, mode):
        loc = self.get_location_by_mode(mode)
        value = self.memory[loc]

        #Jump to the offset
        if self.z == False:
            #Recalculate if negative
            if value >= 128:
                value -= 256

            self.pc = self.pc + value

            print(f"Negative: {value}")
    # BEQ
    def BEQ(self, mode):
        loc = self.get_location_by_mode(mode)
        value = self.memory[loc]

        #Jump to the offset
        if self.z == True:
            #Recalculate if negative
            if value >= 128:
                value -= 256

            self.pc = self.pc + value

            print(f"Negative: {value}")

        #Transfer X Register to Stack Pointer
    def TXS(self, mode):
        self.sp = self.x

        #Transfer Stack Pointer to X Register
    def TSX(self, mode):
        self.x = self.sp

    #Push accumulator
    def PHA(self, mode):
        #Find the location
        loc = 0x100 + self.sp #self.sp is the stack pointer

        #Copy from the accumulator 
        self.memory[loc] = self.a

        # Decrement the stack pointer
        self.sp -= 1 

        self.sp = self.wrap(self.sp)

    #Pull Accumulator
    def PLA(self, mode):
        #Increments the stack pointer 
        self.sp += 1 

        #wrap
        self.sp = self.wrap(self.sp)

        # Finds location 
        loc = 0x100 + self.sp

        #Copies value to accumulator
        self.a = self.memory[loc]

    #PHP
    def PHP(self, mode):

        val = 0
        if self.n == True:
            val += 128
        if self.v == True:
            val += 64
        if self.b == True:
            val += 32
        val += 16
        if self.d == True:
            val += 8
        if self.i == True:
            val += 4
        if self.z == True:
            val += 2
        if self.c == True:
            val += 1

        print(f"PHP val: {val}")

         # Finds location 
        loc = 0x100 + self.sp

        # Copy from the accumulator 
        self.memory[loc] = val

        # Decrement the stack pointer
        self.sp -= 1 

        self.sp = self.wrap(self.sp)

    #PLP
    def PLP(self, mode):
        #Increments the stack pointer 
        self.sp += 1 

        #wrap
        self.sp = self.wrap(self.sp)

        # Finds location 
        loc = 0x100 + self.sp

        # Finds value
        val = self.memory[loc]

        print(f"PLP val: {val}")

        # Decode value and update flag
        if val & 128 == 128:  #& is logical and
            self.n = True
        else:
            self.n = False

        if val & 64 == 64:
            self.v = True
        else:
            self.v = False

        if val & 32 == 32:
            self.b = True
        else:
            self.b = False

        if val & 8 == 8:
            self.d = True
        else:
            self.d = False

        if val & 4 == 4:
            self.i = True
        else:
            self.i = False

        if val & 2 == 2:
            self.z = True
        else:
            self.z = False

        if val & 1 == 1:
            self.c = True
        else:
            self.c = False

        
        # Copies value to accumulator
        self.a = self.memory[loc]


    # Testing / Debugging
    def push(self, value):
        self.memory[self.pc] = value
        self.pc += 1 
    
    #Printing the status of the CPU. 
    def print_status(self, mode):
        print(f"acc: {self.a}, xreg: {self.x}, yreg: {self.y}, pc: {self.pc}")
        print(f"sp: {self.sp}")
        print(f"n v b d i z c ")
        print(f"{int(self.n)} {int(self.v)} {int(self.b)} {int(self.d)} {int(self.i)} {int(self.z)} {int(self.c)}")
        input() 
