"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import JackTokenizer

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
        self.output_stream = output_stream
        self.input_stream = input_stream
        self.initial_space = ""

        # call compile class - each jack code must begin wth a class
        self.compile_class()
        # there is always just one class per file, thus we can assume that compile class is called once per call.

    def compile_class(self) -> None: # done!
        """Compiles a complete class."""
        # open a class block
        self.output_stream.write(self.initial_space + "<class>\n")
        self.increase_initial_space()

        #  "class"
        self.write_terminal_exp("keyword", self.get_token())

        # class name
        self.write_terminal_exp("identifier", self.get_token())
        #  "{"
        self.write_terminal_exp("symbol", self.get_token())

        # classVarDec*
        # for each iteration check if the next item is another classVarDec*
        # do that by checking if its starts with "static" or "field"
        while self.input_stream.keyword == "field" or self.input_stream.keyword == "static":
            self.compile_class_var_dec()

        # subroutineDec*
        # for each iteration check if there is another subroutineDec
        # do that by checking if the next token is not "}", thus not from a "SYMBOL" type
        while self.input_stream.token_type != "SYMBOL":
            self.compile_subroutine()

        # "}"
        self.write_terminal_exp("symbol", self.get_token())

        # close the class block
        self.decrease_initial_space()
        self.output_stream.write(self.initial_space + "</class>\n")

    def compile_class_var_dec(self) -> None: # done!
        """Compiles a static declaration or a field declaration."""
        # open the classVarDec block
        self.output_stream.write(self.initial_space + "<classVarDec>\n")
        self.increase_initial_space()

        # write "field" or "static"
        self.write_terminal_exp("keyword", self.get_token())

        # write type
        self.write_type()

        # varName - the next identifier
        self.write_terminal_exp("identifier", self.input_stream.identifier())
        self.input_stream.advance()

        # ("," varName)* , check if there is a ","
        while self.input_stream.symbol() == ",":
            # ","
            self.write_terminal_exp("symbol", self.get_token())
            # varName
            self.write_terminal_exp("identifier", self.get_token())

        # ";"
        self.write_terminal_exp("symbol", self.get_token())

        # close the classVarDec block
        self.decrease_initial_space()
        self.output_stream.write(self.initial_space + "</classVarDec>\n")


    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        # start the subroutine block
        self.output_stream.write(self.initial_space + "<subroutineDec>\n")
        self.increase_initial_space()

        # "constractor" | "function" | "method"
        self.write_terminal_exp("keyword", self.get_token())

        # "void" | type
        # check for "void" by checking if the next token type is "KEYWORD" - thus not type
        if self.input_stream.token_type == "KEYWORD":
            self.write_terminal_exp("keyword", self.get_token())
        else:
            self.write_type()

        # subroutine name - identifier
        self.write_terminal_exp("identifier", self.get_token())

        # "("
        self.write_terminal_exp("symbol", self.get_token())

        # parameterList
        self.compile_parameter_list()

        # subroutine body
        self.write_subroutine_body()

        # ")"
        self.write_terminal_exp("symbol", self.get_token())

        # end the subroutine block
        self.decrease_initial_space()
        self.output_stream.write(self.initial_space + "</subroutineDec>\n")

        pass

    def compile_parameter_list(self) -> None: # done!
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # start the parameterList block
        self.output_stream.write(self.initial_space + "<parameterList>\n")
        self.increase_initial_space()

        # while the next token is not ")", continue
        # type varName
        if not (self.input_stream.token_type == "SYMBOL" and self.input_stream.symbol == ")"):
            self.write_type()
            self.write_terminal_exp("identifier", self.get_token())

            # ("," type varName)*
            while self.input_stream.token_type == "SYMBOL" and not self.input_stream.symbol == ")":
                self.write_terminal_exp("symbol", self.get_token())
                self.write_terminal_exp("identifier", self.get_token())

        # end the parameterList block
        self.decrease_initial_space()
        self.output_stream.write(self.initial_space + "</parameterList>\n")

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
        while self.input_stream.symbol == ",":
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
        # start the statements block
        self.output_stream.write(self.initial_space + "<statements>\n")
        self.increase_initial_space()

        # statement*
        # we can know if the next expression is a statement if the next token is one of the folowing
        # "let" "if" "while" "do" "return"
        while self.input_stream.keyword in {"let", "if", "while", "do", "return"}:
            if self.input_stream.keyword == "let":
                self.compile_let()
            elif self.input_stream.keyword == "if":
                self.compile_if()
            elif self.input_stream.keyword == "while":
                self.compile_while()
            elif self.input_stream.keyword == "do":
                self.compile_do()
            elif self.input_stream.keyword == "return":
                self.compile_return()

        # end the statements block
        self.decrease_initial_space()
        self.output_stream.write(self.initial_space + "</statements>\n")



    def compile_do(self) -> None:
        """Compiles a do statement."""
        # start the doStatement block
        self.output_stream.write(self.initial_space + "<doStatement>\n")
        self.increase_initial_space()

        # "do"
        self.write_terminal_exp("keyword", self.get_token())

        # subroutineCall
        self.compile_subroutine_call()

        # ";"
        self.write_terminal_exp("symbol", self.get_token())

        # end the doStatement block
        self.decrease_initial_space()
        self.output_stream.write(self.initial_space + "</doStatement>\n")


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
        if self.input_stream.symbol == "[":
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
        # start the returnStatement block
        self.output_stream.write(self.initial_space + "<returnStatement>\n")
        self.increase_initial_space()

        # "return"
        self.write_terminal_exp("keyword",self.get_token())

        # expression?
        # check for ";"
        if not (self.input_stream.token_type == "SYMBOL" and self.input_stream.symbol == ";"):
            # expression
            self.compile_expression()

        # ";"
        self.write_terminal_exp("symbol", self.get_token())

        # end the returnStatement block
        self.decrease_initial_space()
        self.output_stream.write(self.initial_space + "</returnStatement>\n")


    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # start the ifStatement block
        self.output_stream.write(self.initial_space + "<ifStatement>\n")
        self.increase_initial_space()

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
        if self.input_stream.keyword == "else":
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
        # Your code goes here!
        pass

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
        # Your code goes here!
        pass

    def compile_subroutine_call(self) -> None:
        """Compiles a subroutine call"""
        # Your code here!
        pass

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!
        pass

    # ================================================HELPERS FUNCTIONS=================================================

    def increase_initial_space(self):
        self.initial_space = self.initial_space + "  "

    def decrease_initial_space(self):
        self.initial_space = self.initial_space[:-2]

    # gets the current token from the tokenizer, regardless of type, and advances the tokenizer
    def get_token(self):
        ret =''
        if self.input_stream.token_type() == "KEYWORD":
            ret = self.input_stream.keyword()
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

    def write_type(self): # !!!!!! NEED TO BE DONE !!!!!
        if self.input_stream.keyword in {"char", "int", "boolean"}:
            self.write_terminal_exp("keyword", self.get_token())
        else:
            self.write_terminal_exp("identifier", self.get_token())

    def write_subroutine_body(self): # done !
        # start the subroutineBody block
        self.output_stream.write("<subroutineBody>\n")
        self.increase_initial_space()

        # "{"
        self.write_terminal_exp("symbol", self.get_token())

        # varDec*
        # while the next token is "var" the next statement is a varDec
        while self.input_stream.keyword == "var":
            self.compile_var_dec()

        # statements
        self.compile_statements()

        # "}"
        self.write_terminal_exp("symbol", self.get_token())

        # end the subroutineBody block
        self.decrease_initial_space()
        self.output_stream.write("</subroutineBody>\n")




