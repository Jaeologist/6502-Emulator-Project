#6502 CPU System
from cpu6502 import *

#CPU object
cpu = CPU()
print(cpu.a)

cpu.pc = 0x1000

cpu.push(0xA9) #Loading accumuluator with 0x01
cpu.push(0x90) #It's negative so it will set the N flag

cpu.push(0xC9) #Comparing accumulator with 0x02
cpu.push(0x01)

cpu.push(0x30)
cpu.push(0x03) #BMI LDX #0xFF

# Loading a negative value into X register to test branching instructions. 
cpu.push(0xA2) #LDX #0x01
cpu.push(0x01)

cpu.push(0x42) #DBG

cpu.push(0xA2) #LDX #0xFF
cpu.push(0xFF)

cpu.push(0x42) #Debugging

cpu.pc = 0x1000

for _ in range(30):
    cpu.tick()

print()
print(cpu.memory[0x4400])
print(cpu.memory[0x4401])
print(cpu.memory[0x4402])
