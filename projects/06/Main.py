"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code


def assemble_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    # Your code goes here!
    # A good place to start is to initialize a new Parser object:
    # parser = Parser(input_file)
    # Note that you can write to output_file like so:
    # output_file.write("Hello world! \n")
    parser = Parser(input_file)
    st = SymbolTable()
    lineCount = 0
    while parser.has_more_commands():
        if(parser.command_type()) == "L_COMMAND":
            tag = parser.symbol()
            st.add_entry(tag, lineCount)
        else:
            lineCount += 1
        parser.advance()
    parser.line = 0
    lineCount = 0
    varCount = 0
    while parser.has_more_commands():
        parser.advance()
        line = ""
        if(parser.command_type()).__eq__("L_COMMAND") :
            tag = parser.symbol()
            if not st.contains(tag):
                st.add_entry(tag, lineCount)
        elif parser.command_type().__eq__("A_COMMAND") :
            line += "0"
            if not parser.symbol().isnumeric():
                if st.contains(parser.symbol()):
                    line += str(bin(st.get_address(parser.symbol()))[2:].zfill(15))
                else:
                    st.add_entry(parser.symbol(), varCount+16)
                    line += str(bin(st.get_address(parser.symbol()))[2:].zfill(15))
                    varCount += 1
            else:
                line += str(bin(int(parser.symbol()))[2:].zfill(15))
            lineCount += 1
        else:
            line += "111"
            line += (Code.comp(parser.comp()))
            line += (Code.dest(parser.dest()))
            line += (Code.jump(parser.jump()))
            lineCount += 1

        if len(line) != 0:
            print(parser.current_command+" = "+line)
            output_file.write(line+"\n")



if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)

