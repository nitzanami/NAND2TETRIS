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
//push constant 7
@7
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 8
@8
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
//add
@SP
M=M-1
A=M
D=M
A=A-1
M=M+D
//shiftright
@SP
A=M
A=A-1
M=M>>
