"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""


class Code:
    """Translates Hack assembly language mnemonics into binary codes."""
    normal_comp_mnemonics = {
        '0': '101010',
        '1': '111111',
        '-1': '111010',
        'D': '001100',
        'A': '110000',
        '!D': '001101',
        '!A': '110001',
        '-D': '001111',
        '-A': '110011',
        'D+1': '011111',
        'A+1': '110111',
        'D-1': '001110',
        'A-1': '110010',
        'D+A': '000010',
        'D-A': '010011',
        'A-D': '000111',
        'D&A': '000000',
        'D|A': '010101',
    }
    shift_comp_mnemonics = {
        'A<<': '010',
        'D<<': '011',
        'M<<': '110',
        'A>>': '000',
        'D>>': '001',
        'M>>': '100'
    }
    jump_mnemonics = {
        'null': '000',
        'JGT': '001',
        'JEQ': '010',
        'JGE': '011',
        'JLT': '100',
        'JNE': '101',
        'JLE': '110',
        'JMP': '111',
    }

    @staticmethod
    def dest(mnemonic) -> str:
        """
        Args:
            mnemonic (str): a dest mnemonic string.

        Returns:
            str: 3-bit long binary code of the given mnemonic.
        """

        isA = "1" if (mnemonic.__contains__('A')) else "0"
        isD = "1" if (mnemonic.__contains__('D')) else "0"
        isM = "1" if (mnemonic.__contains__('M')) else "0"
        return isA + isD + isM

    @staticmethod
    def comp(mnemonic) -> str:
        """
        Args:
            mnemonic (str): a comp mnemonic string.

        Returns:
            str: the binary code of the given mnemonic.
        """
        if mnemonic in Code.shift_comp_mnemonics.keys():
            return '101' + Code.shift_comp_mnemonics[mnemonic] + '0' * 4
        result = '0'
        if 'M' in mnemonic:
            result = '1'
            mnemonic = mnemonic.replace("M", 'A')
        return '111' + result + Code.normal_comp_mnemonics[mnemonic]

    @staticmethod
    def jump(mnemonic) -> str:
        """
        Args:
            mnemonic (str): a jump mnemonic string.

        Returns:
            str: 3-bit long binary code of the given mnemonic.
        """
        # Your code goes here!
        return Code.jump_mnemonics[mnemonic]
