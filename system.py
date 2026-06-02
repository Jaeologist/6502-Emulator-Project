#6502 CPU System
from cpu6502 import *

#CPU object
cpu = CPU()
print(cpu.a)

cpu.pc = 0x1000

cpu.push(0xA9) # LDA 0xFF
cpu.push(0xFF)

cpu.push(0x42) #DBG

cpu.push(0x38) # SEC

cpu.push(0x42) #DBG

cpu.push(0x69) #ADC 0x01 (adds one to accumulator)
cpu.push(0x01)

cpu.push(0x42) #DBG

cpu.pc = 0x1000

for _ in range(30):
    cpu.tick()

print()
print(cpu.memory[0x4400])
print(cpu.memory[0x4401])
print(cpu.memory[0x4402])
