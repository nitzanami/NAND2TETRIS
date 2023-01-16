"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class SymbolTable:
    """A symbol table that associates names with information needed for Jack
    compilation: type, kind and running index. The symbol table has two nested
    scopes (class/subroutine).
    """

    def __init__(self, class_name) -> None:
        """Creates a new empty symbol table."""
        # a dictionary to keep the indexes of types in the symbol table
        self.kindToIndex = {'STATIC': 0, 'FIELD': 0, 'ARG': 0, 'VAR': 0}
        self.subroutine_table = []
        self.class_table = []
        self.class_name = class_name

    def start_subroutine(self) -> None:
        """Starts a new subroutine scope (i.e., resets the subroutine's 
        symbol table).
        """
        # every method symbol table starts with the self object in argument 0
        self.subroutine_table = [TableCell(name='this', type=self.class_name, kind='argument', runningIndex=0)]

    def define(self, name: str, type: str, kind: str) -> None:
        """Defines a new identifier of a given name, type and kind and assigns 
        it a running index. "STATIC" and "FIELD" identifiers have a class scope,
        while "ARG" and "VAR" identifiers have a subroutine scope.

        Args:
            name (str): the name of the new identifier.
            type (str): the type of the new identifier.
            kind (str): the kind of the new identifier, can be:
            "STATIC", "FIELD", "ARG", "VAR".
        """
        # if 'STATIC' of 'FIELD' add to the class table
        if kind == 'STATIC' or kind == 'FIELD':
            self.add_class_row(name, type, kind)
        elif kind == 'ARG' or kind == 'VAR':
            self.add_subroutine_row(name, type, kind)
        else:
            print("got unexpected kind: " + kind)

    def var_count(self, kind: str) -> int:
        return self.kindToIndex[kind]

    def kind_of(self, name: str) -> str:
        """
        Args:
            name (str): name of an identifier.

        Returns:
            str: the kind of the named identifier in the current scope, or None
            if the identifier is unknown in the current scope.
        """
        # first search through the subroutine symbol table
        for row in self.subroutine_table:
            if row.name == name:
                return row.kind
        # if not found, go to the class level
        for row in self.class_table:
            if row.name == name:
                return row.kind
        # if still not found return None
        return None

    def type_of(self, name: str) -> str:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            str: the type of the named identifier in the current scope.
        """
        # first search through the subroutine symbol table
        for row in self.subroutine_table:
            if row.name == name:
                return row.type
        # if not found, go to the class level
        for row in self.class_table:
            if row.name == name:
                return row.type

        return None

    def index_of(self, name: str) -> int:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            int: the index assigned to the named identifier.
        """
        # first search through the subroutine symbol table
        for row in self.subroutine_table:
            if row.name == name:
                return row.runningIndex
        # if not found, go to the class level
        for row in self.class_table:
            if row.name == name:
                return row.runningIndex

        return 0

    # OUR METHODS ==================================================================

    # a table Cell class, to keep things organized
    class TableCell:
        def __init__(self, name, type, kind, runningIndex=0):
            self.name = name
            self.type = type
            self.kind = kind
            self.runningIndex = runningIndex

    # adds a row to our symbol table in a TableCell format
    def add_subroutine_row(self, name, type, kind):
        self.subroutine_table += [TableCell(name=name, type=type, kind=kind, runningIndex=self.kindToIndex[kind])]
        self.kindToIndex[kind] += 1

    def add_class_row(self, name, type, kind):
        self.class_table += [TableCell(name=name, type=type, kind=kind, runningIndex=self.kindToIndex[kind])]
        self.kindToIndex[kind] += 1
