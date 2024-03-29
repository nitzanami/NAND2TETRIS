"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from Constants import *


def generate_label():
    i = 0
    while True:
        i += 1
        yield "label" + str(i)
    pass


class CodeWriter:
    """Translates VM commands into Hack assembly code."""
    segment_dict = {'local': 'LCL',
                    'argument': 'ARG',
                    'this': 'THIS',
                    'that': 'THAT',
                    }
    binary_operator_dict = {'add': '+',
                            'sub': '-',
                            'and': '&',
                            'or': '|'}
    unary_operator_dict = {'neg': '-',
                           'not': '!',
                           'shiftleft': '<<',
                           'shiftright': '>>'}
    numeral_operator_dict = {'lt': 'JGT', 'gt': 'JLT', 'eq': 'JEQ'}

    labels = generate_label()

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.function_name = None
        self.file_name = None
        self.output_stream = output_stream

    def write_bootstrap(self):
        self.output_stream.write('@START\n0;JMP\n')
        self.write_compare_start('eq')
        self.write_compare_start('lt')
        self.write_compare_start('gt')
        self.output_stream.write('(START)\n\n')
        self.output_stream.write(f'@256\nD=A\n@SP\nM=D\n')
        self.write_call('Sys.init', 0)

    def set_file_name(self, filename: str) -> None:
        self.file_name = filename
        """Informs the code writer that the translation of a new VM file is 
        started.
        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        # This function is useful when translating code that handles the
        # static segment. For example, in order to prevent collisions between two
        # .vm files which push/pop to the static segment, one can use the current
        # file's name in the assembly variable's name and thus differentiate between
        # static variables belonging to different files.
        # To avoid problems with Linux/Windows/MacOS differences with regards
        # to filenames and paths, you are advised to parse the filename in
        # the function "translate_file" in Main.py using python's os library,
        # For example, using code similar to:
        # input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))

    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """
        result = ''
        if command in ['add', 'sub', 'and', 'or']:
            result = '@SP\n' \
                     'M=M-1\n' \
                     'A=M\n' \
                     'D=M\n' \
                     'A=A-1\n' \
                     f'M=M{self.binary_operator_dict[command]}D\n'
        elif command in ['neg', 'not']:
            result = '@SP\n' \
                     'A=M\n' \
                     'A=A-1\n' \
                     f"M={self.unary_operator_dict[command]}M\n"
        elif command in ['shiftleft', 'shiftright']:
            result = '@SP\n' \
                     'A=M\n' \
                     'A=A-1\n' \
                     f'M=M{self.unary_operator_dict[command]}\n'
        elif command in ['eq', 'lt', 'gt']:
            endAddress = next(self.labels)
            result = f'@{endAddress}\n' \
                     f'D=A\n' \
                     f'@R13\n' \
                     f'M=D\n' \
                     f'@{self.get_compare_label(command)}\n' \
                     f'0;JMP\n' \
                     f'({endAddress})\n'
        self.output_stream.write(result)

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        if command == 'C_PUSH':
            result = self.get_push_string(index, segment)
        else:  # POP
            result = self.get_pop_string(index, segment)
        self.output_stream.write(result)

        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.

    def get_pop_string(self, index, segment):
        # decrement SP
        result = '@SP\nM=M-1\n'
        # if static, complete the pop
        if segment == 'static':
            result += f'A=M\nD=M\n@{self.file_name}.{index}\nM=D\n'
        elif segment == 'pointer':  # if pointer just change the THAT of THIS value with respect to index
            result += f'A=M\nD=M\n'
            if int(index) == 0:
                result += '@THIS\nM=D\n'
            else:
                result += '@THAT\nM=D\n'
        else:
            # store in D the segment address
            if segment == 'temp':
                result += f'@5\nD=A\n'

            else:  # local,argument,this,that
                result += f'@{self.segment_dict[segment]}\nD=M\n'
            result += f'@{index}\nD=D+A\n'  # add the offset to find the result address
            result += '@R13\nM=D\n'  # save the address to write into in R13
            result += '@SP\nA=M\nD=M\n'  # save the value of pop in D
            result += '@R13\nA=M\nM=D\n'  # RAM[R13] = D
        return result

    def get_push_string(self, index, segment):
        # put the value to push in D
        if segment == 'constant':
            result = f'@{index}\nD=A\n'
        elif segment == 'static':
            result = f'@{self.file_name}.{index}\nD=M\n'
        elif segment == 'temp':
            result = f'@5\nD=A\n@{index}\nA=D+A\nD=M\n'
        elif segment == 'pointer':
            if int(index) == 0:
                result = '@THIS\n'
            else:
                result = '@THAT\n'
            result += 'D=M\n'

        elif segment in self.segment_dict.keys():  # if lcl,this,that,argument
            result = f'@{self.segment_dict[segment]}\nD=M\n@{index}\nA=A+D\nD=M\n'
        elif segment in ['LCL', 'ARG', 'THIS', 'THAT']:
            result = f'@{segment}\nD=M\n'
        else:
            result = f'@{segment}\nD=A\n'  # if segment is an address that we jump to

        # do the push
        result += '@SP\nA=M\nM=D\n@SP\nM=M+1\n'
        return result

    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command. 
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
            @param label:
        """
        self.output_stream.write(f'({self.get_label_string(label)})\n')

    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        self.output_stream.write(f'@{self.get_label_string(label)}\n0;JMP\n')

    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command. 

        Args:
            label (str): the label to go to.
        """
        result = '@SP\n' + \
                 'M=M-1\n' + \
                 'A=M\n' \
                 'D=M\n' + \
                 f'@{self.get_label_string(label)}\n' + \
                 'D;JNE\n'
        self.output_stream.write(result)

    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command. 
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this 
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        # The pseudo-code of "function function_name n_vars" is:
        # (function_name)       // injects a function entry label into the code
        # repeat n_vars times:  // n_vars = number of local variables
        #   push constant 0     // initializes the local variables to 0
        repeatLabel = next(self.labels)
        self.output_stream.write(f'({self.get_function_label_string(function_name)})\n')  # write the entry label for
        # the function
        # push n_vars times constant 0 ==>
        start_loop = '@' + str(n_vars) + '\nD=A\n@R14\nM=D\n' + \
                     '(' + repeatLabel + ')\n'
        end_loop = '@R14\n' + \
                   'M=M-1\n' + \
                   'D=M\n' + \
                   '@' + repeatLabel + '\n' + \
                   'D;JGT\n'
        if n_vars > 0:
            self.output_stream.write(start_loop)
            self.write_push_pop(C_PUSH, 'constant', 0)
            self.output_stream.write(end_loop)

    def get_function_label_string(self, function_name):
        return function_name
        if function_name == 'Sys.init':
            return 'Sys.init'
        return f'{self.file_name}.{function_name}'

    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command. 
        Let "Xxx.foo" be a function within the file Xxx.vm.
        The handling of each "call" command within Xxx.foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "Xxx.foo").
        This symbol is used to mark the return address within the caller's 
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        # The pseudo-code of "call function_name n_args" is:

        return_address = next(self.labels)

        # push return_address   // generates a label and pushes it to the stack
        # push LCL              // saves LCL of the caller
        # push ARG              // saves ARG of the caller
        # push THIS             // saves THIS of the caller
        # push THAT             // saves THAT of the caller
        for label in [return_address, 'LCL', 'ARG', 'THIS', 'THAT']:
            self.write_push_pop(C_PUSH, label, 0)
        # ARG = SP-5-n_args     // repositions ARG
        self.output_stream.write(f'@SP\nD=M\n@5\nD=D-A\n@{n_args}\nD=D-A\n@ARG\nM=D\n')
        # LCL = SP              // repositions LCL
        self.output_stream.write(f'@SP\nD=M\n@LCL\nM=D\n')

        # goto function_name    // transfers control to the callee
        self.output_stream.write(f'@{self.get_function_label_string(function_name)}\n0;JMP\n')

        # (return_address)      // injects the return address label into the code
        self.output_stream.write(f'({return_address})\n')

    def write_return(self) -> None:
        """Writes assembly code that affects the return command."""

        # r14 = frame = LCL                   // frame is a temporary variable
        result = '@LCL\n' \
                 'D=M\n' \
                 '@R14\n' \
                 'M=D\n'
        # return_address = *(frame-5)   // puts the return address in a temp var
        result += '@5\nD=A\n@R14\n' \
                  'A=M-D\nD=M\n' \
                  '@R13\n' \
                  'M=D\n'
        # *ARG = pop()                  // repositions the return value for the caller
        # SP = ARG + 1                  // repositions SP for the caller
        result += '@SP\nA=M\nA=A-1\nD=M\n' \
                  '@ARG\n' \
                  'A=M\nM=D\n' \
                  '@ARG\n' \
                  'D=M\n' \
                  '@SP\nM=D+1\n'
        # THAT = *(frame-1)             // restores THAT for the caller
        # THIS = *(frame-2)             // restores THIS for the caller
        # ARG = *(frame-3)              // restores ARG for the caller
        # LCL = *(frame-4)              // restores LCL for the caller
        # goto return_address           // go to the return address
        result += '@R14\nM=M-1\nA=M\nD=M\n' \
                  '@THAT\nM=D\n' \
                  '@R14\nM=M-1\nA=M\nD=M\n' \
                  '@THIS\nM=D\n' \
                  '@R14\nM=M-1\nA=M\nD=M\n' \
                  '@ARG\nM=D\n' \
                  '@R14\nM=M-1\nA=M\nD=M\n' \
                  '@LCL\nM=D\n' \
                  '@R13\nA=M\nD;JMP\n'
        self.output_stream.write(result)

    def write_compare_start(self, command: str):
        positive = f'positive.{command}'
        done = f'done.{command}'
        default = f'default.{command}'
        yes = f'yes.{command}'
        result = f'({self.get_compare_label(command)})\n' \
                 f'@SP\n' \
                 'M=M-1\n' \
                 'A=M\n' \
                 'D=M\n' \
                 f'@{positive}\n' \
                 'D;JGE\n' \
                 '@SP\n' \
                 'M=M-1\n' \
                 'A=M\n' \
                 'D=M\n' \
                 '@SP\n' \
                 'M=M+1\n' \
                 f'@{default}\n' \
                 'D;JLT\n' \
                 '@SP\n' \
                 'M=M-1\n' \
                 'A=M\n' \
                 f"M={-1 if command.__eq__('gt') else 0}\n" \
                 f'@{done}\n' \
                 'D;JMP\n' \
                 f'({positive})\n' \
                 '@SP\n' \
                 'M=M-1\n' \
                 'A=M\n' \
                 'D=M\n' \
                 '@SP\n' \
                 'M=M+1\n' \
                 f'@{default}\n' \
                 'D;JGE\n' \
                 '@SP\n' \
                 'M=M-1\n' \
                 'A=M\n' \
                 f"M={-1 if command.__eq__('lt') else 0}\n" \
                 f'@{done}\n' \
                 'D;JMP\n' \
                 f'({default})\n' \
                 '@SP\n' \
                 'A=M\n' \
                 'D=M\n' \
                 'A=A-1\n' \
                 'D=D-M\n' \
                 f'@{yes}\n' \
                 f'D;{self.numeral_operator_dict[command]}\n' \
                 '@SP\n' \
                 'A=M-1\n' \
                 'M=0\n' \
                 '@SP\n' \
                 'M=M+1\n' \
                 f'@{done}\n' \
                 'D;JMP\n' \
                 f'({yes})\n' \
                 '@SP\n' \
                 'A=M-1\n' \
                 'M=-1\n' \
                 '@SP\n' \
                 'M=M+1\n' \
                 f'@{done}\n' \
                 'D;JMP\n' \
                 f'({done})\n' \
                 '@SP\n' \
                 'M=M-1\n' \
                 '@SP\n' \
                 '@R13\n' \
                 'A=M\n' \
                 '0;JMP\n'

        self.output_stream.write(result)

    def set_function(self, function_name):
        self.function_name = function_name

    def get_compare_label(self, command):
        return f'{command}.HANDLER'

    def get_label_string(self, label):
        return f'{self.function_name}${label}'
