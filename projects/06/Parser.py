"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """Encapsulates access to the input code. Reads an assembly program
    by reaing each command line-by-line, parseds the current command,
    and provides convenient access to the commands components (fields
    and symbols). In addition, removes all white space and comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        self.line = 0;
        self.current_command = None
        self.input_lines = input_file.read().replace(" ", "").replace("\t", "").splitlines()
        NoCommentsLines = []
        for line in self.input_lines:
            if not (line.startswith("//") or len(line)==0):
                NoCommentsLines.append(line.split('/')[0])
        self.input_lines = NoCommentsLines
        #for line in self.input_lines: #DEL=========================
        #    print(line)               #DEL=========================
        self.advance()

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """

        return self.line < len(self.input_lines)

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        self.current_command = self.input_lines[self.line]
        self.line += 1
        pass

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        # Your code goes here!
        if str(self.current_command).startswith('@'):
            return "A_COMMAND"
        elif str(self.current_command).startswith('('):
            return "L_COMMAND"
        else:
            return "C_COMMAND"

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """
        if str(self.current_command).startswith('@'): #if A command
            return self.current_command[1:]
        else: #if L command
            return self.current_command[1:-1]


    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        return str(self.current_command).split("=")[0] if "=" in str(self.current_command) else "null"



    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        return str(self.current_command).split('=')[-1].split(';')[0]

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        return str(self.current_command).split(';')[-1] if ";" in str(self.current_command) else "null"
