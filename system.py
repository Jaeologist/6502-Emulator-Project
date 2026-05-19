#6502 CPU System

from cpu6502 import *

#CPU object
cpu = CPU()
print(cpu.a)

cpu.pc = 0x1000

cpu.push(0xA9) #LDA #0x0A
cpu.push(0x0A)

cpu.push(0x42) #DBG

cpu.push(0x8D) #STA 4401 
cpu.push(0x01)
cpu.push(0x44)

cpu.push(0x42) #DBG

cpu.push(0xA2)   #LDX #0x01
cpu.push(0x01)

cpu.push(0xBD)   #LDA 0x4400, X
cpu.push(0x00)
cpu.push(0x44)

cpu.push(0x42) #DBG

cpu.push(0xA5) #LDA 
cpu.push(0x55) 

cpu.push(0x42) #DBG

cpu.pc = 0x1000

for _ in range(100):
    cpu.tick()

print()
print(cpu.memory[0x4400])
print(cpu.memory[0x4401])
print(cpu.memory[0x4402])
