# Notes of Project

May 18, 2026

Challenges
In the beginning of the session struggled figuring out how using the 'commit -m' command to keep a record of my progress of the day. Still currently finding a method to keep a constant track of my progress. when reorganizing my the commands I accidently delete line 25. After retying the line, I ran my program again and found that none of the bits were being returned to the system. I ended realizing that I set my mode to absolute instead of immediate which cause the program to run incorrectly. While formatting lines 195-218, I accidently deleted LDA (0xA9), LDX(0X4400). This caused my program to load the wrong values into the accumulator

Progress

-Added ABSOLUTEX, ABSOLUTEY, ZEROPAGE, ZEROPAGEX mode.
-Create a 0x42command.
-Added push method. 
-Added DBG(0x42).  
-Added print_status method.
