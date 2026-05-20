# Notes of Project

May 18, 2026

Challenges
In the beginning of the session struggled figuring out how using the 'commit -m' command to keep a record of my progress of the day. Still currently finding a method to keep a constant track of my progress. when reorganizing my the commands I accidently delete line 25. After retying the line, I ran my program again and found that none of the bits were being returned to the system. I ended realizing that I set my mode to absolute instead of immediate which cause the program to run incorrectly. While formatting lines 195-218, I accidently deleted LDA (0xA9), LDX(0X4400). This caused my program to load the wrong values into the accumulator

Progress
- Added ABSOLUTEX, ABSOLUTEY, ZEROPAGE, ZEROPAGEX mode.
- Create a 0x42 command.
- Added push method. 
- Added DBG(0x42).  
- Added print_status method.

May 19th, 2026

Challenges
Before I finished my session for the day, I ran my code and noticed that my program is only running results from the program counter location 4110. I have to reread my lines and make adjustments to why my program is not working correctly. 

Progress
- Added INDIRECT mode
- Created flags carry, interrupt, overflow, decimal to determine whether it's on or off.
- Added commands CLC, SEC, CLI, SEI, CLV, CLD, SED, and JMP
- Created a system file to load, store, and jump data. 
