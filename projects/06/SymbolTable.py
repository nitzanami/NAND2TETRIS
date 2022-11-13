"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""


class SymbolTable:
    """
    A symbol table that keeps a correspondence between symbolic labels and 
    numeric addresses.
    """

    def __init__(self) -> None:
        """Creates a new symbol table initialized with all the predefined symbols
        and their pre-allocated RAM addresses, according to section 6.2.3 of the
        book.
        """
        self.values = {
            "SP": 0x0000,
            "LCL": 0x0001,
            "ARG": 0x0002,
            "THIS": 0x0003,
            "THAT": 0x0004,
            "R0": 0x0000,
            "R1": 0x0001,
            "R2": 0x0002,
            "R3": 0x0003,
            "R4": 0x0004,
            "R5": 0x0005,
            "R6": 0x0006,
            "R7": 0x0007,
            "R8": 0x0008,
            "R9": 0x0009,
            "R10": 0x000a,
            "R11": 0x000b,
            "R12": 0x000c,
            "R13": 0x000d,
            "R14": 0x000e,
            "R15": 0x000f,
            "SCREEN": 0x4000,
            "KBD": 0x6000
        }

    def add_entry(self, symbol: str, address: int) -> None:
        """Adds the pair (symbol, address) to the table.

        Args:
            symbol (str): the symbol to add.
            address (int): the address corresponding to the symbol.
        """
        if not self.contains(symbol):
            self.values.update({symbol: address})

    def contains(self, symbol: str) -> bool:
        """Does the symbol table contain the given symbol?

        Args:
            symbol (str): a symbol.

        Returns:
            bool: True if the symbol is contained, False otherwise.
        """
        return symbol in self.values

    def get_address(self, symbol: str) -> int:
        """Returns the address associated with the symbol.

        Args:
            symbol (str): a symbol.

        Returns:
            int: the address associated with the symbol.
        """
        return self.values[symbol]
