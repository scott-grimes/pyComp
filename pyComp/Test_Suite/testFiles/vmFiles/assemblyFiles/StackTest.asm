@17
D=A
@SP
M=M+1
A=M-1
M=D
@17
D=A
@SP
M=M+1
A=M-1
M=D
@SP
M=M-1
A=M
D=M
M=0
@SP
M=M-1
A=M
D=M-D
@LogicWasTrue0
D;JEQ
@SP
A=M
M=0
@EndLogic0
0;JMP
(LogicWasTrue0)
@SP
A=M
M=-1
(EndLogic0)
@SP
M=M+1
A=M
@892
D=A
@SP
M=M+1
A=M-1
M=D
@891
D=A
@SP
M=M+1
A=M-1
M=D
@SP
M=M-1
A=M
D=M
M=0
@SP
M=M-1
A=M
D=M-D
@LogicWasTrue1
D;JLT
@SP
A=M
M=0
@EndLogic1
0;JMP
(LogicWasTrue1)
@SP
A=M
M=-1
(EndLogic1)
@SP
M=M+1
A=M
@32767
D=A
@SP
M=M+1
A=M-1
M=D
@32766
D=A
@SP
M=M+1
A=M-1
M=D
@SP
M=M-1
A=M
D=M
M=0
@SP
M=M-1
A=M
D=M-D
@LogicWasTrue2
D;JGT
@SP
A=M
M=0
@EndLogic2
0;JMP
(LogicWasTrue2)
@SP
A=M
M=-1
(EndLogic2)
@SP
M=M+1
A=M
@56
D=A
@SP
M=M+1
A=M-1
M=D
@31
D=A
@SP
M=M+1
A=M-1
M=D
@53
D=A
@SP
M=M+1
A=M-1
M=D
@SP
M=M-1
A=M
D=M
M=0
@SP
M=M-1
A=M
M=M+D
@SP
M=M+1
A=M
@112
D=A
@SP
M=M+1
A=M-1
M=D
@SP
M=M-1
A=M
D=M
M=0
@SP
M=M-1
A=M
M=M-D
@SP
M=M+1
A=M
@SP
M=M-1
A=M
D=M
M=0
M=-D
@SP
M=M+1
A=M
@SP
M=M-1
A=M
D=M
M=0
@SP
M=M-1
A=M
M=M&D
@SP
M=M+1
A=M
@82
D=A
@SP
M=M+1
A=M-1
M=D
@SP
M=M-1
A=M
D=M
M=0
@SP
M=M-1
A=M
M=M|D
@SP
M=M+1
A=M