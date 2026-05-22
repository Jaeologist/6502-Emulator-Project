from enum import Enum, auto
from pickle import FALSE

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

class CPU:
    def __init__(self):
        self.memory = []
        for _ in range(0, 65536):
            self.memory.append(0)

        self.a = 0x00
        self.x = 0x00
        self.y = 0x00
        self.pc = 0x1000

        
        self.carry = False;
        self.interrupt = False;
        self.overflow = False;
        self.decimal = False;
        self.equal = False;
        self.negative = False;

        self.commands = {  
            #Debugging commands
            0x42: {"func": self.print_status, "m": Mode.IMPLIED},

            #Load A Register commands
            0xA9: {"func": self.LDA, "m": Mode.IMMEDIATE},
            0xA5: {"func": self.LDA, "m": Mode.ZEROPAGE},
            0xB5: {"func": self.LDA, "m": Mode.ZEROPAGEX},
            0xBD: {"func": self.LDA, "m": Mode.ABSOLUTEX},
            0xB9: {"func": self.LDA, "m": Mode.ABSOLUTEY},

            #Load X Y Register commands
            0xA2: {"func": self.LDX, "m": Mode.IMMEDIATE},
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
        }

        self.increments = {
            Mode.IMMEDIATE: 2,
            Mode.ZEROPAGE: 2,
            Mode.ZEROPAGEX: 2,
            Mode.ABSOLUTE: 3,
            Mode.IMPLIED: 1,
            Mode.ABSOLUTEX: 3,
            Mode.ABSOLUTEY: 3,
            Mode.INDIRECT: 3
        }

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
            print(f"Command: {command} not implemented")

    #This will shortern our code by creating a method that gets the location based of the location.
    #While finding whether the mode is immediate of absolute. 
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
            
            #Gets JMP address from 2000 memory location.
            #Challenge: Focused on the JMP from memory location 2000. 
            lsb = self.memory[loc]
            msb = self.memory[loc + 1]
            loc = msb * 256 + lsb
        return loc

    #Wraps the 8 bitvalues
    def wrap(self, value):
        if value > 255:
            value = value % 256;
        if value < 0:
            value += 256
        return value

    # Components for loading values to CPU.  A = Accumulator, X = Index Register, Y = Index Register
    def LDA(self, mode):
        loc = self.get_location_by_mode(mode)
        #Loading value from memory
        val = self.memory[loc]
        #Putting the value in the accumulator
        self.a = val 

    #LDX
    def LDX(self, mode):
        loc = self.get_location_by_mode(mode)
        #Loading value from memory
        val = self.memory[loc]
        #Putting the value in the accumulator
        self.x = val 

    #LDY
    def LDY(self, mode):
        loc = self.get_location_by_mode(mode)
        #Loading value from memory
        val = self.memory[loc]
        #Putting the value in the accumulator
        self.y = val 
    
    #Storing values to CPU.  A = Accumulator, X = Index Register, Y = Index Register
    def STA(self, mode):
        # Find the location based on the mode
        loc = self.get_location_by_mode(mode)
        #Update memory
        self.memory[loc] = self.a
        

    def STX(self, mode):
        loc = self.get_location_by_mode(mode)
        #Update memory
        self.memory[loc] = self.x
        

    def STY(self, mode):
        loc = self.get_location_by_mode(mode)
        #Update memory
        self.memory[loc] = self.y
    
    def INX(self, mode):
        self.x += 1
        self.x = self.wrap(self.x)

    def INY(self, mode):
        self.y += 1
        self.y = self.wrap(self.y)

    def DEX(self, mode):
        self.x -= 1
        self.x = self.wrap(self.x)

    def DEY(self, mode):
        self.y -= 1
        self.y = self.wrap(self.y)

    def TAX(self, mode):
        self.x = self.a

    def TXA(self, mode):
        self.a = self.x

    def TAY(self, mode):
        self.y = self.a

    def TYA(self, mode):
        self.a = self.y

    #CLC
    def CLC(self, mode):
        self.carry = False 

    #SEC
    def SEC(self, mode):
        self.carry = True

    #CLI
    def CLI(self, mode):
        self.interrupt = False

    #SEI
    def SEI(self, mode):
        self.interrupt = True

    #CLV
    def CLV(self, mode):
        self.overflow = False

    #CLD
    def CLD(self, mode):
        self.decimal = False

    #SED
    def SED(self, mode):
        self.decimal = True

    def JMP(self, mode):
        loc = self.get_location_by_mode(mode)
        self.pc = loc - self.increments[mode]

    #Added the CMP command to compare the value in the accumulator with the value in the memory.
    def CMP(self, mode):
        loc = self.get_location_by_mode(mode)
        value = self.memory[loc]

        if value >= self.a:
            self.carry = True

        if value == self.a:
            self.equal = True
        
        print(f"equal: {self.equal}")
        if self.a >= 128:
            self.negative = True

        
    # Testing / Debugging
    def push(self, value):
        self.memory[self.pc] = value
        self.pc += 1 
    
    def print_status(self, mode):
        print(f"a: {self.a}, x: {self.x}, y: {self.y}, pc: {self.pc}")
        print(f"carry: {self.carry}, interrupt: {self.interrupt}")
        print(f"overflow: {self.interrupt}, decimal: {self.decimal}")
        print(f"equal: {self.equal}, negative: {self.negative}")
        input() 
