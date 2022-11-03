// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// The program should swap between the max. and min. elements of an array.
// Assumptions:
// - The array's start address is stored in R14, and R15 contains its length
// - Each array value x is between -16384 < x < 16384
// - The address in R14 is at least >= 2048
// - R14 + R15 <= 16383
//
// Requirements:
// - Changing R14, R15 is not allowed.

// minI = maxI = Array start index
@R14
D = M
@minI
M = D
@maxI
M = D

//min = max =RAM[RAM[R14]]
A = D
D = M
@max
M = D
@min
M = D

//i + startindex + 1
@R14
D = M + 1
@i
M = D

(LOOP)

@i
A = M
D = M
@max
D = D - M
@MAX
D;JGT

@i
A = M
D = M
@min
D = D - M
@MIN
D;JLT

@LOOPEND
0;JMP

(MAX)
//maxI = i
@i
D = M
@maxI
M = D
//max = RAM[i]
A = D
D = M
@max
M = D

@LOOPEND
0;JMP

(MIN)
//minI = i
@i
D = M
@minI
M = D
//min = RAM[i]
A = D
D = M
@min
M = D

(LOOPEND)
//i = i + 1
@i
M = M + 1
//if 
D = M
@R14
D = D - M
@R15
D = D - M

@LOOP
D;JLT
//RAM[maxI] = min
@min
D = M
@maxI
A = M
M = D
//RAM[minI] = max
@max
D = M
@minI
A = M
M = D

@END
(END)
0;JMP





