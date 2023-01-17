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
        self.symbol_table: SymbolTable = None
        self.output_stream = VMWriter(output_stream)
        self.input_stream = input_stream
        self.input_stream.advance()
        self.initial_space = ""

        # call compile class - each jack code must begin wth a class
        self.compile_class()
        # self.compile_do()
        # there is always just one class per file, thus we can assume that compile class is called once per call.

    def compile_class(self) -> None:  # done!
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

    def compile_class_var_dec(self) -> None:  # done!
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
        self.symbol_table.start_subroutine()
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

    def compile_parameter_list(self):  # done!
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        n_vars = 0
        # while the next token is not ")", continue and increase n_vars
        # type varName
        if not (self.input_stream.token_type() == "SYMBOL" and self.input_stream.symbol() == ")"):
            type = self.get_token()

            self.symbol_table.define(self.get_token(), type, "argument")
            n_vars += 1

            # ("," type varName)*
            while self.input_stream.token_type() == "SYMBOL" and not self.input_stream.symbol() == ")":
                # self.write_terminal_exp("symbol", self.get_token())
                self.get_token()

                type = self.get_token()
                # self.write_terminal_exp("identifier", self.get_token())
                self.symbol_table.define(self.get_token(), type, "argument")
                n_vars += 1
        return n_vars

    def compile_var_dec(self) -> int:
        """Compiles a var declaration."""
        var_count = 0
        # "var"
        self.get_token()

        # type
        type = self.write_type()

        # varName
        name = self.get_token()
        self.symbol_table.define(name, type, "local")
        var_count += 1
        # (',' varName)*
        while self.input_stream.symbol() == ",":
            self.get_token()
            self.symbol_table.define(self.get_token(), type, "local")
            var_count += 1
        # ";"
        self.get_token()
        return var_count

    def compile_statements(self, is_constractor = False) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """

        # statement*
        # we can know if the next expression is a statement if the next token is one of the folowing
        # "let" "if" "while" "do" "return"
        while self.input_stream.keyword() in {"LET", "IF", "WHILE", "DO", "RETURN"}:
            if self.input_stream.keyword() == "LET":
                self.compile_let(is_constractor=is_constractor)
            elif self.input_stream.keyword() == "IF":
                self.compile_if()
            elif self.input_stream.keyword() == "WHILE":
                self.compile_while()
            elif self.input_stream.keyword() == "DO":
                self.compile_do(is_constractor=is_constractor)
            elif self.input_stream.keyword() == "RETURN":
                self.compile_return()

    def compile_do(self, is_constractor=False) -> None:
        """Compiles a do statement."""
        # do
        self.get_token()

        # subroutineCall
        self.compile_subroutine_call(is_constractor=is_constractor)
        self.output_stream.write_pop("temp", 0)
        # ;
        self.get_token()

    def compile_let(self, is_constractor = False) -> None:
        """Compiles a let statement."""

        # "let"
        self.get_token()

        # varName
        name = self.get_token()

        # ("[" expression "]")?
        # check for the token "["

        if self.input_stream.symbol() == "[":

            # "["
            self.get_token()

            # expression
            self.compile_expression()

            # array var
            self.output_stream.write_push_var(self.symbol_table.kind_and_index(name))

            self.output_stream.write_arithmetic("add")
            # "]"
            self.get_token()

            # '='
            self.get_token()

            # expression
            self.compile_expression()
            self.output_stream.write_pop("temp", 0)
            self.output_stream.write_pop("pointer", 1)
            self.output_stream.write_push("temp", 0)
            self.output_stream.write_pop("that", 0)
        else:
            # '='
            self.get_token()

            # expression
            self.compile_expression()
            if is_constractor:

                self.output_stream.write_pop_var(("this",self.symbol_table.kind_and_index(name)[1]))
            else:
                self.output_stream.write_pop_var(self.symbol_table.kind_and_index(name))
        # ";"
        self.get_token()

    def compile_while(self) -> None:
        """Compiles a while statement."""
        while_exp, while_end = next(self.output_stream.while_label_generator)

        # while - skip -
        # self.write_terminal_exp("keyword", self.get_token())
        self.get_token()

        # "(" - skip -
        # self.write_terminal_exp("symbol", self.get_token())
        self.get_token()

        # write label 1
        self.output_stream.write_label(while_exp)

        # expression
        self.compile_expression()

        # neg
        self.output_stream.write_arithmetic("not")

        # write if-goto label 2
        self.output_stream.write_if(while_end)

        # ")" - skip
        # self.write_terminal_exp("symbol", self.get_token())
        self.get_token()

        # "{" - skip -
        # self.write_terminal_exp("symbol", self.get_token())
        self.get_token()

        # statements
        self.compile_statements()

        # goto label1
        self.output_stream.write_goto(while_exp)

        # label2
        self.output_stream.write_label(while_end)

        # "}" - skip -
        # self.write_terminal_exp("symbol", self.get_token())
        self.get_token()

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
        if_true, if_false, if_end = next(self.output_stream.if_label_generator)
        # if - skip
        # self.write_terminal_exp("keyword", self.get_token())
        self.get_token()

        # "(" - skip
        # self.write_terminal_exp("symbol", self.get_token())
        self.get_token()

        # expression
        self.compile_expression()

        # if goto label 1
        self.output_stream.write_if(if_true)

        self.output_stream.write_goto(if_false)

        self.output_stream.write_label(if_true)

        # ")" - skip
        # self.write_terminal_exp("symbol", self.get_token())
        self.get_token()

        # "{" - skip
        # self.write_terminal_exp("symbol", self.get_token())
        self.get_token()

        # statements
        self.compile_statements()

        # "}" - skip
        # self.write_terminal_exp("symbol", self.get_token())
        self.get_token()

        # ("else" "{" statements "}")?
        # search for "else"
        if self.input_stream.keyword() == "ELSE":
            # goto if_false
            self.output_stream.write_goto(if_end)

            # write: label if_false
            self.output_stream.write_label(if_false)

            # "else" - skip
            self.get_token()

            # "{" - skip
            self.get_token()

            # statements
            self.compile_statements()

            # "}" - skip
            # self.write_terminal_exp("symbol", self.get_token())
            self.get_token()

            self.output_stream.write_label(if_end)
        else:
            self.output_stream.write_label(if_false)

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
            self.compile_string_const()
        elif token_type == "KEYWORD":
            self.compile_keyowrd_term()
        # (unaryOp term) | '(' expression ')'
        elif token_type == "SYMBOL":
            token = self.get_token()
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
                self.get_token()
                self.compile_expression()
                self.output_stream.write_push_var(self.symbol_table.kind_and_index(var))
                self.output_stream.write_arithmetic("add")
                self.output_stream.write_pop("pointer", 1)
                self.output_stream.write_push("that",0)
                self.get_token()
            # subroutineCall
            elif self.input_stream.currentToken in ['(', '.']:
                self.compile_subroutine_call(var)
            else:
                self.output_stream.write_push_var(self.symbol_table.kind_and_index(var))

    def compile_subroutine_call(self, name=None, is_constractor = False) -> None:
        """Compiles a subroutine call"""

        # subroutineName'('expressionList')' | (className|varName)'.'subroutineName'('expressionList')'

        # subroutine name | (className|varName) - they are both identifiers
        identifier = name if name is not None else self.get_token()

        # search for a '.', if found, implement option 2
        n_args = 0
        if self.input_stream.symbol() == ".":
            # scenario - (className|varName)'.'subroutineNAme'('expressionList')'
            type = self.symbol_table.type_of(identifier)
            # if a method
            if type is not None:
                self.output_stream.write_push_var(self.symbol_table.kind_and_index(identifier))
                identifier = self.symbol_table.type_of(identifier)
                n_args = 1
            # '.' - symbol
            identifier += self.get_token()

            # subroutineName - identifier
            identifier += self.get_token()
        else:   # subroutineName'('expressionList')'
            if identifier == 'hide':
                print("hide")
            self.output_stream.write_push("pointer",0)
            identifier = self.symbol_table.class_name + '.' + identifier
            n_args = 1

        # '('
        self.get_token()

        # expression list
        n_args += self.compile_expression_list()

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
            exp_count += 1
            # (','expression)*
            while self.input_stream.token_type() == "SYMBOL" and self.input_stream.symbol() == ",":
                # ',' - symbol
                self.get_token()

                # expression
                self.compile_expression()
                exp_count += 1
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

    def write_subroutine_body(self, function_name, is_method = False, is_constractor = False):  # done !

        # "{" - skip -
        self.get_token()

        # varDec*
        # while the next token is "var" the next statement is a varDec
        var_count = 0
        param_count = 0
        param_count = self.symbol_table.get_field_count()
        while self.input_stream.keyword() == "VAR":
            var_count += self.compile_var_dec()

        self.output_stream.write_function(function_name, var_count)
        if is_constractor:
            # push the num of vars to the stack
            self.output_stream.write_push("constant", param_count)

            # search for available memory segment of said length
            self.output_stream.write_call("Memory.alloc", 1)

            # pop the segment location to the stack and place it in pointer 0 - the pointer to our memory segment location
            self.output_stream.write_pop("pointer", 0)

        if is_method:
            self.output_stream.write_push("argument", 0)
            self.output_stream.write_pop("pointer", 0)
        # statements
        self.compile_statements(is_constractor=is_constractor)

        # "}" - skip -
        # self.write_terminal_exp("symbol", self.get_token())
        self.get_token()

    # PROJECT 11 HELPER FUNCTIONS ============================================

    def compile_function(self):
        # type
        self.get_token()

        # write on VM "CLASS_NAME + .FUNCTION_NAME + NUM_OF_PARAMETERS"

        # subroutine name - identifier -- save! --
        function_name = self.get_token()

        # "(" -- skip! --
        # self.write_terminal_exp("symbol", self.get_token())
        self.get_token()

        # parameterList
        self.compile_parameter_list()

        # ")" -- skip! --
        # self.write_terminal_exp("symbol", self.get_token())
        self.get_token()

        function_name = self.symbol_table.class_name + "." + function_name
        #
        # subroutine body
        self.write_subroutine_body(function_name)

    def compile_method(self):


        # type
        type = self.get_token()

        self.symbol_table.define("this",type,"argument")

        # write on VM "CLASS_NAME + .FUNCTION_NAME + NUM_OF_PARAMETERS"

        # subroutine name - identifier -- save! --
        function_name = self.get_token()

        # "(" -- skip! --
        # self.write_terminal_exp("symbol", self.get_token())
        self.get_token()

        # parameterList
        self.compile_parameter_list()

        # ")" -- skip! --
        # self.write_terminal_exp("symbol", self.get_token())
        self.get_token()

        function_name = self.symbol_table.class_name + "." + function_name
        #
        # subroutine body
        self.write_subroutine_body(function_name, True)

    def compile_constractor(self):
        # first we want to find an available memory segment of size n (the num of inputs)

        # type
        self.get_token()

        # write on VM "CLASS_NAME + .FUNCTION_NAME + NUM_OF_PARAMETERS"

        # subroutine name - identifier -- save! --
        function_name = self.get_token()

        # "(" -- skip! --
        # self.write_terminal_exp("symbol", self.get_token())
        self.get_token()

        # parameterList
        self.compile_parameter_list()

        # ")" -- skip! --
        # self.write_terminal_exp("symbol", self.get_token())
        self.get_token()

        function_name = self.symbol_table.class_name + "." + function_name

        # subroutine body
        self.write_subroutine_body(function_name, is_constractor=True)






    def compile_keyowrd_term(self):
        token = self.get_token()
        if token == 'true':
            self.output_stream.write_push('constant', 0)
            self.output_stream.write_arithmetic("not")
        elif token == 'false':
            self.output_stream.write_push('constant', 0)
        elif token == 'null':
            self.output_stream.write_push('constants', 0)
        elif token == 'this':
            self.output_stream.write_push('pointer', 0)

    def compile_string_const(self):
        string = self.get_token().replace('"','')
        self.output_stream.write_push("constant",len(string))
        self.output_stream.write_call("String.new", 1)
        for c in string:
            self.output_stream.write_push("constant",ord(c))
            self.output_stream.write_call("String.appendChar",2)

