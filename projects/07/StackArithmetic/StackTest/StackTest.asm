@START
0;JMP
(eqHANDLER)
@SP
M=M-1
A=M
D=M
@label1
D;JGE
@SP
M=M-1
A=M
D=M
@SP
M=M+1
@label3
D;JLT
@SP
M=M-1
A=M
M=0
@label2
D;JMP
(label1)
@SP
M=M-1
A=M
D=M
@SP
M=M+1
@label3
D;JGE
@SP
M=M-1
A=M
M=0
@label2
D;JMP
(label3)
@SP
A=M
D=M
A=A-1
D=D-M
@label4
D;JEQ
@SP
A=M-1
M=0
@SP
M=M+1
@label2
D;JMP
(label4)
@SP
A=M-1
M=-1
@SP
M=M+1
@label2
D;JMP
(label2)
@SP
M=M-1
@SP
@R13
A=M
0;JMP
(ltHANDLER)
@SP
M=M-1
A=M
D=M
@label5
D;JGE
@SP
M=M-1
A=M
D=M
@SP
M=M+1
@label7
D;JLT
@SP
M=M-1
A=M
M=0
@label6
D;JMP
(label5)
@SP
M=M-1
A=M
D=M
@SP
M=M+1
@label7
D;JGE
@SP
M=M-1
A=M
M=-1
@label6
D;JMP
(label7)
@SP
A=M
D=M
A=A-1
D=D-M
@label8
D;JGT
@SP
A=M-1
M=0
@SP
M=M+1
@label6
D;JMP
(label8)
@SP
A=M-1
M=-1
@SP
M=M+1
@label6
D;JMP
(label6)
@SP
M=M-1
@SP
@R13
A=M
0;JMP
(gtHANDLER)
@SP
M=M-1
A=M
D=M
@label9
D;JGE
@SP
M=M-1
A=M
D=M
@SP
M=M+1
@label11
D;JLT
@SP
M=M-1
A=M
M=-1
@label10
D;JMP
(label9)
@SP
M=M-1
A=M
D=M
@SP
M=M+1
@label11
D;JGE
@SP
M=M-1
A=M
M=0
@label10
D;JMP
(label11)
@SP
A=M
D=M
A=A-1
D=D-M
@label12
D;JLT
@SP
A=M-1
M=0
@SP
M=M+1
@label10
D;JMP
(label12)
@SP
A=M-1
M=-1
@SP
M=M+1
@label10
D;JMP
(label10)
@SP
M=M-1
@SP
@R13
A=M
0;JMP
(START)
//push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
//shiftleft
@SP
A=M
A=A-1
M=M<<
//shiftright
@SP
A=M
A=A-1
M=M>>
//eq
@label13
D=A
@R13
M=D
@eqHANDLER
0;JMP
(label13)
//push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
//eq
@label14
D=A
@R13
M=D
@eqHANDLER
0;JMP
(label14)
//push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
//eq
@label15
D=A
@R13
M=D
@eqHANDLER
0;JMP
(label15)
//push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
//lt
@label16
D=A
@R13
M=D
@ltHANDLER
0;JMP
(label16)
//push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
//lt
@label17
D=A
@R13
M=D
@ltHANDLER
0;JMP
(label17)
//push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
//lt
@label18
D=A
@R13
M=D
@ltHANDLER
0;JMP
(label18)
//push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
//gt
@label19
D=A
@R13
M=D
@gtHANDLER
0;JMP
(label19)
//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
//gt
@label20
D=A
@R13
M=D
@gtHANDLER
0;JMP
(label20)
//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
//gt
@label21
D=A
@R13
M=D
@gtHANDLER
0;JMP
(label21)
//push constant 57
@57
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 31
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 53
@53
D=A
@SP
A=M
M=D
@SP
M=M+1
//add
@SP
M=M-1
A=M
D=M
A=A-1
M=M+D
//push constant 112
@112
D=A
@SP
A=M
M=D
@SP
M=M+1
//sub
@SP
M=M-1
A=M
D=M
A=A-1
M=M-D
//neg
@SP
A=M
A=A-1
M=-M
//and
@SP
M=M-1
A=M
D=M
A=A-1
M=M&D
//push constant 82
@82
D=A
@SP
A=M
M=D
@SP
M=M+1
//or
@SP
M=M-1
A=M
D=M
A=A-1
M=M|D
//not
@SP
A=M
A=A-1
M=!M
