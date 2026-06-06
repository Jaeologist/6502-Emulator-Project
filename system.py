#6502 CPU System
from cpu6502 import *

#CPU object
cpu = CPU()
print(cpu.a)

cpu.pc = 0x1000

# Testing CPX,CPY,INC,DEC
cpu.push(0xA2) #LDX #0x01
cpu.push(0x01)

cpu.push(0xE0) #CPX #0x01
cpu.push(0x00)

cpu.push(0x42) #DBG

cpu.push(0xA0) #LDY #0x01
cpu.push(0x01)

cpu.push(0xC0) #CPY #0x01
cpu.push(0x01)

cpu.push(0x42) #DBG

cpu.push(0xA9) #LDA #0x01
cpu.push(0x01)

cpu.push(0x8D) # STA $4400
cpu.push(0x00)
cpu.push(0x44)

cpu.push(0x42) #DBG

cpu.push(0xCE) #DEC $4400
cpu.push(0x00)
cpu.push(0x44)

cpu.push(0xAD) #LDA $4400
cpu.push(0x00)
cpu.push(0x44)

cpu.push(0x42) #DBG

cpu.push(0xEE) #INC $4400
cpu.push(0x00)
cpu.push(0x44)

cpu.push(0xAD) #LDA $4400
cpu.push(0x00)
cpu.push(0x44)

cpu.push(0x42) #DBG

cpu.pc = 0x1000

for _ in range(30):
    cpu.tick()

print()
print(cpu.memory[0x4400])
print(cpu.memory[0x4401])
print(cpu.memory[0x4402])
