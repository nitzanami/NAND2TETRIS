"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import sys
import typing
import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter

VOID_RETURN = 0


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: JackTokenizer, output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """

        # set the parameters of the class
        self.symbol_table = None
        self.output_stream = VMWriter(output_stream)
        self.input_stream = input_stream
        self.input_stream.advance()
        self.initial_space = ""

        # call compile class - each jack code must begin wth a class
        self.compile_class()
        # self.compile_do()
        # there is always just one class per file, thus we can assume that compile class is called once per call.

    def compile_class(self) -> None: # done!
        """Compiles a complete class."""
        #  "class" - skip
        # self.write_terminal_exp("keyword", self.get_token())
        self.get_token()

        # class name - save and initial the symbol table
        # self.write_terminal_exp("identifier", self.get_token())
        self.symbol_table = SymbolTable(self.get_token())

        #  "{" - skip
        # self.write_terminal_exp("symbol", self.get_token())
        self.get_token()

        # classVarDec*
        # for each iteration check if the next item is another classVarDec*
        # do that by checking if its starts with "static" or "field"
        while self.input_stream.keyword() == "FIELD" or self.input_stream.keyword() == "STATIC":
            self.compile_class_var_dec()

        # subroutineDec*
        # for each iteration check if there is another subroutineDec
        # do that by checking if the next token is not "}", thus not from a "SYMBOL" type
        while self.input_stream.token_type() != "SYMBOL":
            self.compile_subroutine()

        # "}" - skip
        # self.write_terminal_exp("symbol", self.get_token())
        self.get_token()

    def compile_class_var_dec(self) -> None: # done!
        """Compiles a static declaration or a field declaration."""
        # write "field" or "static" - save the kind
        # self.write_terminal_exp("keyword", self.get_token())
        kind = self.get_token()

        # write type - save type
        type = self.write_type()

        # varName - the next identifier - save
        varName = self.get_token()

        self.symbol_table.define(varName, type, kind)

        # ("," varName)* , check if there is a ","
        while self.input_stream.symbol() == ",":
            # "," - skip
            # self.write_terminal_exp("symbol", self.get_token())
            self.get_token()

            # varName - save and add to the table
            # self.write_terminal_exp("identifier", self.get_token())
            varName = self.get_token()
            self.symbol_table.define(varName, type, kind)

        # ";" - skip
        # self.write_terminal_exp("symbol", self.get_token())
        self.get_token()

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        # "constractor" | "function" | "method"
        # self.write_terminal_exp("keyword", self.get_token())
        token = self.get_token()
        if token == "function":
            self.compile_function()
        elif token == "method":
            self.compile_method()
        else:
            self.compile_constractor()
        """  
        # "void" | type
        # check for "void" by checking if the next token type is "KEYWORD" - thus not type
        if self.input_stream.token_type() == "KEYWORD":
            self.write_terminal_exp("keyword", self.get_token())
        else:
            self.write_type()

        # subroutine name - identifier
        self.write_terminal_exp("identifier", self.get_token())

        # "("
        self.write_terminal_exp("symbol", self.get_token())

        # parameterList
        self.compile_parameter_list()

        # ")"
        self.write_terminal_exp("symbol", self.get_token())

        # subroutine body
        self.write_subroutine_body()

        # end the subroutine block
        self.decrease_initial_space()
        self.output_stream.write(self.initial_space + "</subroutineDec>\n")

        pass
        """

    def compile_parameter_list(self): # done!
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        n_vars = 0
        # while the next token is not ")", continue and increase n_vars
        # type varName
        if not (self.input_stream.token_type() == "SYMBOL" and self.input_stream.symbol() == ")"):
            self.write_type()
            # self.write_terminal_exp("identifier", self.get_token())
            self.get_token()
            n_vars += 1

            # ("," type varName)*
            while self.input_stream.token_type() == "SYMBOL" and not self.input_stream.symbol() == ")":
                # self.write_terminal_exp("symbol", self.get_token())
                self.get_token()
                self.write_type()
                # self.write_terminal_exp("identifier", self.get_token())
                self.get_token()
                n_vars += 1
        return n_vars

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        # start the varDec block
        self.output_stream.write(self.initial_space + "<varDec>\n")
        self.increase_initial_space()

        # "var"
        self.write_terminal_exp("keyword", self.get_token())

        # type
        self.write_type()

        # varName
        self.write_terminal_exp("identifier", self.get_token())

        # (',' varName)*
        while self.input_stream.symbol() == ",":
            self.write_terminal_exp("symbol", self.get_token())
            self.write_terminal_exp("identifier", self.get_token())

        # ";"
        self.write_terminal_exp("symbol", self.get_token())

        # end the varDec block
        self.decrease_initial_space()
        self.output_stream.write(self.initial_space + "</varDec>\n")
        pass

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """

        # statement*
        # we can know if the next expression is a statement if the next token is one of the folowing
        # "let" "if" "while" "do" "return"
        while self.input_stream.keyword() in {"LET", "IF", "WHILE", "DO", "RETURN"}:
            if self.input_stream.keyword() == "LET":
                self.compile_let()
            elif self.input_stream.keyword() == "IF":
                self.compile_if()
            elif self.input_stream.keyword() == "WHILE":
                self.compile_while()
            elif self.input_stream.keyword() == "DO":
                self.compile_do()
            elif self.input_stream.keyword() == "RETURN":
                self.compile_return()



    def compile_do(self) -> None:
        """Compiles a do statement."""
        #do
        self.get_token()

        # subroutineCall
        self.compile_subroutine_call()
        self.output_stream.write_pop("temp",0)
        #;
        self.get_token()


    def compile_let(self) -> None:
        """Compiles a let statement."""
        # start the letStatement block
        self.output_stream.write(self.initial_space + "<letStatement>\n")
        self.increase_initial_space()

        # "let"
        self.write_terminal_exp("keyword", self.get_token())

        # varName
        self.write_terminal_exp("identifier", self.get_token())

        # ("[" expression "]")?
        # check for the token "["
        if self.input_stream.symbol() == "[":
            # "["
            self.write_terminal_exp("symbol", self.get_token())

            # expression
            self.compile_expression()

            # "]"
            self.write_terminal_exp("symbol", self.get_token())

        # '='
        self.write_terminal_exp("symbol", self.get_token())

        # expression
        self.compile_expression()

        # ";"
        self.write_terminal_exp("symbol", self.get_token())

        # end the letStatement block
        self.decrease_initial_space()
        self.output_stream.write(self.initial_space + "</letStatement>\n")

        pass

    def compile_while(self) -> None:
        """Compiles a while statement."""
        # start the whileStatement block
        self.output_stream.write(self.initial_space + "<whileStatement>\n")
        self.increase_initial_space()

        # while
        self.write_terminal_exp("keyword", self.get_token())

        # "("
        self.write_terminal_exp("symbol", self.get_token())

        # expression
        self.compile_expression()

        # ")"
        self.write_terminal_exp("symbol", self.get_token())

        # "{"
        self.write_terminal_exp("symbol", self.get_token())

        # statements
        self.compile_statements()

        # "}"
        self.write_terminal_exp("symbol", self.get_token())

        # end the whileStatement block
        self.decrease_initial_space()
        self.output_stream.write(self.initial_space + "</whileStatement>\n")
        pass

    def compile_return(self) -> None:
        """Compiles a return statement."""

        self.get_token()
        # expression?
        # check for ";"
        if not (self.input_stream.token_type() == "SYMBOL" and self.input_stream.symbol() == ";"):
            # expression
            self.compile_expression()
        else:
            self.output_stream.write_push("constant", VOID_RETURN)
        self.output_stream.write_return()
        self.get_token()

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # start the ifStatement block
        self.output_stream.write(self.initial_space + "<ifStatement>\n")
        self.increase_initial_space()
        self.write_terminal_exp("keyword", self.get_token())
        # "("
        self.write_terminal_exp("symbol", self.get_token())

        # expression
        self.compile_expression()

        # ")"
        self.write_terminal_exp("symbol", self.get_token())

        # "{"
        self.write_terminal_exp("symbol", self.get_token())

        # statements
        self.compile_statements()

        # "}"
        self.write_terminal_exp("symbol", self.get_token())

        # ("else" "{" statements "}")?
        # search for "else"
        if self.input_stream.keyword() == "ELSE":
            # "else"
            self.write_terminal_exp("keyword", self.get_token())

            # "{"
            self.write_terminal_exp("symbol", self.get_token())

            # statements
            self.compile_statements()

            # "}"
            self.write_terminal_exp("symbol", self.get_token())

        # end the ifStatement block
        self.decrease_initial_space()
        self.output_stream.write(self.initial_space + "</ifStatement>\n")

    def compile_expression(self) -> None:
        """Compiles an expression."""

        # term
        self.compile_term()
        while self.input_stream.currentToken in self.input_stream.binary_operations:
            # op
            op = self.get_token()
            # term
            self.compile_term()

            self.output_stream.write_arithmetic(self.output_stream.binary_op_to_name[op])
        # end the expression block

    def compile_term(self) -> None:
        """Compiles a term. 
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """

        token_type = self.input_stream.token_type()
        if token_type == "INT_CONST":
            self.output_stream.write_push("constant", self.get_token())
        elif token_type == "STRING_CONST":
            self.write_terminal_exp("stringConstant", self.get_token())  # TODO use a call to string function
        elif token_type == "KEYWORD":
            self.write_terminal_exp("keyword", self.get_token())
        # (unaryOp term) | '(' expression ')'
        elif token_type == "SYMBOL":
            token = self.get_token()
            # self.write_terminal_exp("symbol", token)
            # '(' expression ')'
            if token == '(':
                self.compile_expression()
                self.get_token()
            # (unaryOp term)
            else:
                self.compile_term()
                self.output_stream.write_arithmetic(self.output_stream.unary_op_to_name[token])
        # starts with identifier
        else:
            var = self.get_token()
            # '[' expression ']'
            if self.input_stream.currentToken == '[':
                self.write_terminal_exp("identifier", var)
                self.write_terminal_exp("symbol", self.get_token())
                self.compile_expression()
                self.write_terminal_exp("symbol", self.get_token())
            # subroutineCall
            elif self.input_stream.currentToken in ['(', '.']:
                self.compile_subroutine_call(var)
            else:
                self.write_terminal_exp("identifier", var)

    def compile_subroutine_call(self, name=None) -> None:
        """Compiles a subroutine call"""
        # # start the subroutineCall block
        # if name is None and False:
        #     self.output_stream.__write(self.initial_space + "<subroutineCall>\n")
        #     self.increase_initial_space()

        # subroutineName'('expressionList')' | (className|varName)'.'subroutineNAme'('expressionList')'

        # subroutine name | (className|varName) - they are both identifiers
        identifier = name if name is not None else self.get_token()

        # search for a '.', if found, implement option 2

        if self.input_stream.symbol() == ".":
            # scenario - (className|varName)'.'subroutineNAme'('expressionList')'

            # '.' - symbol
            identifier += self.get_token()

            # subroutineName - identifier
            identifier+= self.get_token()
        # '('
        self.get_token()

        # expression list
        n_args = self.compile_expression_list()

        self.output_stream.write_call(identifier, n_args)
        # ')'
        self.get_token()



    def compile_expression_list(self) -> int:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        exp_count = 0
        # if there is no expression in the expressionList we expect to find ')' or ']' of '}'
        if self.input_stream.token_type() != "SYMBOL" or not self.input_stream.symbol() in {")", "]", "}"}:
            # expression
            self.compile_expression()
            exp_count +=1
            # (','expression)*
            while self.input_stream.token_type() == "SYMBOL" and self.input_stream.symbol() == ",":
                # ',' - symbol
                self.get_token()

                # expression
                self.compile_expression()
                exp_count +=1
        return exp_count
    # ================================================HELPERS FUNCTIONS=================================================

    def increase_initial_space(self):
        self.initial_space = self.initial_space + "  "

    def decrease_initial_space(self):
        self.initial_space = self.initial_space[:-2]

    # gets the current token from the tokenizer, regardless of type, and advances the tokenizer
    def get_token(self):
        ret = ''
        if self.input_stream.token_type() == "KEYWORD":
            ret = self.input_stream.keyword().lower()
        if self.input_stream.token_type() == "SYMBOL":
            ret = self.input_stream.symbol()
        if self.input_stream.token_type() == "IDENTIFIER":
            ret = self.input_stream.identifier()
        if self.input_stream.token_type() == "INT_CONST":
            ret = self.input_stream.int_val()
        if self.input_stream.token_type() == "STRING_CONST":
            ret = self.input_stream.string_val()
        self.input_stream.advance()
        return ret

    def write_terminal_exp(self, type: str, keyword: str) -> None:
        self.output_stream.write(self.initial_space + "<" + type + ">" + " " + keyword + " </" + type + ">\n")

    def write_type(self):
        # if self.input_stream.keyword() in {"CHAR", "INT", "BOOLEAN"}:
        #     self.write_terminal_exp("keyword", self.get_token())
        # else:
        #     self.write_terminal_exp("identifier", self.get_token())
        # return the type
        return self.get_token()

    def write_subroutine_body(self): # done !

        # "{" - skip -
        self.get_token()

        # varDec*
        # while the next token is "var" the next statement is a varDec
        while self.input_stream.keyword()== "VAR":
            self.compile_var_dec()

        # statements
        self.compile_statements()

        # "}" - skip -
        # self.write_terminal_exp("symbol", self.get_token())
        self.get_token()



    # PROJECT 11 HELPER FUNCTIONS ============================================

    def compile_function(self):
        # "void" | type - we dont care! only the  caller care -- skip! --
        # check for "void" by checking if the next token type is "KEYWORD" - thus not type
        # if self.input_stream.token_type() == "KEYWORD":
        #     self.write_terminal_exp("keyword", self.get_token())
        # else:
        #     self.write_type()
        self.get_token()

        # write on VM "CLASS_NAME + .FUNCTION_NAME + NUM_OF_PARAMETERS"

        # subroutine name - identifier -- save! --
        # self.write_terminal_exp("identifier", self.get_token())
        function_name = self.get_token()

        # "(" -- skip! --
        # self.write_terminal_exp("symbol", self.get_token())
        self.get_token()

        # parameterList
        n_vars = self.compile_parameter_list()

        # ")" -- skip! --
        # self.write_terminal_exp("symbol", self.get_token())
        self.get_token()

        self.output_stream.write_function(self.symbol_table.class_name + "." + function_name, n_vars)

        #
        # subroutine body
        self.write_subroutine_body()

    def compile_method(self):
        pass

    def compile_constractor(self):
        pass
