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

May 21st, 2026

Challenges
  For the past two days I have been trying to get the correct loading and storing sequences in the system. The acculumator wouldn't give the correct value (2 at the time) it would only give me 0. I found out that my my TAX and TXA methods were incorrect. For TAX, I had to swap the line 'self.a = self.x' to 'self.x = self.a' and vise versa for TXA. 

Progress
- A correct running system program that loads 2 in the acculmulator and has a running JMP command.
- wrap method that wraps the 8 bit values.

May 22nd, 2026

Challenges
  When using git commit -m command in terminal, the termial would keep replying to the files from the git Hub and the local files were diverged. Meaning that I would be able to show changes in my GitHub, continuously showing old code from when the project was first being developed.

Progress
- Tested cases using CMP command where it was equal to, greater than, and less than.
- Merged local file and GitHub to show changes being made from IDE.
- Added Compare command.
- Added carry, interrupt, overflow, decimal, equal, and negative flags for COMP operations.

May 23rd, 2026

Challenges
  Didn't run across any challenges. 

Progress
- Changed the flag names to the abbrievations of each flag from the documentation.
- Added branch commands.
- Added Relative Mode.
- Converted boolean values to bits in print_status method.

May 24th, 2026

Challenges
  When running the code in the beginning, my termial was not picking up the BMI attribute BMI command on line 90. After finding out why my branch code wasn't running I decided to push my changes. The file wasn't taking in any commits unless I used git pull command before. After doing that my code change to the older version of the code from May 22nd. 

Progress
- found the GitHub command sequence to show my immediate changes.
- Added Branch commands
- Test Branch commands in system
- Restored code
  
May 27th, 2026

Challenges
  When trying to start my IDE, it ended up crashing. I had to reinstall Cursor and update it to the most current version. When loaded the Emulator file, the code when back to an older version where I was testing the DEQ.

Progress
- Created PLP
- Tested PHP
- Created PHA, PLA, PHP functionality. 

May 29th, 2026

Challenges 
  When testing my system code, it would crash at first because I would forget to use temp.a instead of temp_a variable. Then it would give me a a different program counter then crash. Turns out I had to a the debug after loading x and before it would run RTS command. 

Progress
- Created RTS command
- Created JSR command

June 2nd, 2026

Challenges 
When testing for the ORA operator in the system file, i kept running across an error that the accumulator would load 1 then in the next registers it would load 0. When looking over my ORA method instead of the vertical bar I used the logical and module. This caused it to operate as a AND operator rather than the OR operation intended. After the change, it loaded 5 in the next register as intended. 

Progress 
- Added Add with Carry(ADC) along with
- Added bitwise operators AND, ORA, EOR.
- Tested ADC with adding values 240 to 241 and 255 to 0.

June 3rd, 2026

Challenges
No challenges for today, Code went smoothly. 

Progress
- Added SBC instruction
- Added NOP instruction
- Added LSR instruction
- Added ASL instruction
- Successfully test SBC with and Without NOP.

June 4th, 2026

Challenges
No challenges for today, code went smoothly. 

Progress
- Added ROL instructions
- Added LOL instructions
