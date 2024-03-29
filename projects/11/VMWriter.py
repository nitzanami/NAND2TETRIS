"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import sys
import typing


class VMWriter:
    """
    Writes VM commands into a file. Encapsulates the VM command syntax.
    """
    binary_op_to_name = {
        "+": "add", "-": "sub", "=": 'eq', '>': 'gt', '<': 'lt', '&': 'and', '|': "or",
        '*': 'call Math.multiply 2', '/': "call Math.divide 2"
    }
    unary_op_to_name = {
        '~': 'not', '-': 'neg', '^': 'shiftleft', '#': 'shiftright'
    }

    def generate_if(self):
        i = 0
        while True:
            yield f'IF_TRUE{i}', f'IF_FALSE{i}', f'IF_END{i}'
            i += 1

    def generate_while(self):
        i = 0
        while True:
            yield f'WHILE_EXP{i}', f'WHILE_END{i}'
            i += 1

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Creates a new file and prepares it for writing VM commands."""
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.while_label_generator = self.generate_while()
        self.if_label_generator = self.generate_if()
        self.output = output_stream

    def write_push(self, segment: str, index: int) -> None:
        """Writes a VM push command.

        Args:
            segment (str): the segment to push to, can be "CONST", "ARG", 
            "LOCAL", "STATIC", "THIS", "THAT", "POINTER", "TEMP"
            index (int): the index to push to.
        """
        self.__write(f"push {segment} {index}")

    def write_pop(self, segment: str, index: int) -> None:
        """Writes a VM pop command.

        Args:
            segment (str): the segment to pop from, can be "CONST", "ARG", 
            "LOCAL", "STATIC", "THIS", "THAT", "POINTER", "TEMP".
            index (int): the index to pop from.
        """
        # Your code goes here!
        self.__write(f"pop {segment} {index}")

    def write_arithmetic(self, command: str) -> None:
        """Writes a VM arithmetic command.

        Args:
            command (str): the command to write, can be "ADD", "SUB", "NEG", 
            "EQ", "GT", "LT", "AND", "OR", "NOT", "SHIFTLEFT", "SHIFTRIGHT".
        """
        self.__write(command)

    def write_label(self, label: str) -> None:
        """Writes a VM label command.

        Args:
            label (str): the label to write.
        """
        self.__write(f"label {label}")

    def write_goto(self, label: str) -> None:
        """Writes a VM goto command.

        Args:
            label (str): the label to go to.
        """
        self.__write(f"goto {label}")

    def write_if(self, label: str) -> None:
        """Writes a VM if-goto command.

        Args:
            label (str): the label to go to.
        """
        self.__write(f"if-goto {label}")

    def write_call(self, name: str, n_args: int) -> None:
        """Writes a VM call command.

        Args:
            name (str): the name of the function to call.
            n_args (int): the number of arguments the function receives.
        """
        self.__write(f"call {name} {n_args}")

    def write_function(self, name: str, n_locals: int) -> None:
        """Writes a VM function command.

        Args:
            name (str): the name of the function.
            n_locals (int): the number of local variables the function uses.
        """
        self.__write(f"function {name} {n_locals}")

    def write_return(self) -> None:
        """Writes a VM return command."""
        self.__write(f"return")

    def __write(self, string):
        self.output.write(string + '\n')

    def write(self, string):
        self.output.write(string + '\n')

    def write_push_var(self, param):
        self.write_push(param[0], param[1])

    def write_pop_var(self, param):
        self.write_pop(param[0], param[1])


if __name__ == "__main__":
    writer = VMWriter(sys.stdout)
