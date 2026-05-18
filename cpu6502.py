from enum import Enum, auto

#Gives numerical values
class Mode(Enum):
    IMMEDIATE = auto()
    IMPLIED = auto()
    ABSOLUTE = auto()

class CPU:
    def __init__(self):
        self.memory = []
        for _ in range(0, 65536):
            self.memory.append(0)

        self.a = 0x00
        self.x = 0x00
        self.y = 0x00
        self.pc = 0x1000

        self.commands = { 
            #Immediate Mode
            0xA9: {"func": self.LDA, "m": Mode.IMMEDIATE},
            0xA2: {"func": self.LDX, "m": Mode.IMMEDIATE},
            0xA0: {"func": self.LDY, "m": Mode.IMMEDIATE},

            #Absolute Mode
            0x8D: {"func": self.STA, "m": Mode.ABSOLUTE},
            0x8E: {"func": self.STX, "m": Mode.ABSOLUTE},
            0x8C: {"func": self.STY, "m": Mode.ABSOLUTE},

            0xE8: {"func": self.INX, "m": Mode.IMPLIED},
            0XC8: {"func":self.INY, "m": Mode.IMPLIED},

            0XAA: {"func":self.TAX, "m": Mode.IMPLIED},
            0X8A: {"func":self.TXA, "m": Mode.IMPLIED},
            0XA8: {"func":self.TAY, "m": Mode.IMPLIED},
            0X98: {"func":self.TYA, "m": Mode.IMPLIED},

        }

        self.increments = {
            Mode.IMMEDIATE: 2,
            Mode.ABSOLUTE: 3,
            Mode.IMPLIED: 1
        }

    def tick(self):
        #fetching command
        command = self.memory[self.pc]
        
        #execution
        if command in self.commands:
            f = self.commands[command]["func"]
            m = self.commands[command]["m"]
            f(m)
            self.pc+= self.increments[m]
        else:
            print(f"Command: {command} not implemented")

    #This will shortern our code by creating a method that gets the location based of the location.
    #While finding whether the mode is immediate of absolute. 
    def get_location_by_mode(self, mode):
        loc = 0

        if mode == Mode.IMMEDIATE:
            loc = self.pc +1
        elif mode == Mode.ABSOLUTE:
            lsb = self.memory[self.pc+1] 
            msb = self.memory[self.pc+2] 
            loc = msb * 256 + lsb

        return loc

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
    
    def INY(self, mode):
        self.y += 1

    def DEX(self, mode):
        self.x -= 1

    def DEY(self, mode):
        self.y -= 1

    def TAX(self, mode):
        self.a = self.x

    def TXA(self, mode):
        self.x = self.a

    def TAY(self, mode):
        self.a = self.y

    def TYA(self, mode):
        self.y = self.a

    def push(self, value):
        self.memory[self.pc] = value
        self.pc += 1
    
#CPU object
cpu = CPU()
print(cpu.a)

cpu.pc = 0x1000

cpu.push(0xA9)   #LDA 0x44
cpu.push(0x44)

cpu.push(0xA2) #LDX 0x45
cpu.push(0x45)

cpu.push(0xA0) #LDY 0x46
cpu.push(0x46) 

cpu.push(0x8D) #STA $4400 
cpu.push(0x00)
cpu.push(0x44)

cpu.push(0x8E) #STX 
cpu.push(0x01)
cpu.push(0x44)

cpu.push(0x8C) #STY
cpu.push(0x02)
cpu.push(0x44)

cpu.push(0xE8) #INX
cpu.push(0xC8)

cpu.pc = 0x1000

for _ in range(100):
    cpu.tick()


print(cpu.a)
print(cpu.x)
print(cpu.y)

print()

print(cpu.memory[0x4400])
print(cpu.memory[0x4401])
print(cpu.memory[0x4402])


#print(0x1000)
# when print(0x1000) it prints out 4096 
