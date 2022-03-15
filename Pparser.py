from rply import ParserGenerator
from rply.token import Token

from errors import *
from astree import *


class ParserState:
    def __init__(self, filename: str, source: str):
        self.filename = filename
        self.source = source

        self.traceback = ""


class Parser:
    def __init__(self, tokens: list, precedence: list) -> None:
        self.pg = ParserGenerator(tokens, precedence)
        self.parser = self.init()

    def init(self):
        ##################################################
        # Program
        ##################################################
        @self.pg.production('program : extended-statement-list')
        def program(state: ParserState, p):
            return p[0]

        @self.pg.production('extended-statement-list : extended-statement')
        def ext_stmt_list(state: ParserState, p):
            return BlockNode(p[0], p[0].getsourcepos())

        @self.pg.production('extended-statement-list : extended-statement-list extended-statement')
        def ext_stmt_list_rec(state: ParserState, p):
            p[0].add(p[1])

            return p[0]

        @self.pg.production('extended-statement : class-statement')
        @self.pg.production('extended-statement : function-statement')
        @self.pg.production('extended-statement : constant-statement')
        def ext_stmt(state: ParserState, p):
            return BlockNode(p[0], p[0].getsourcepos())

        @self.pg.production('constant-statement : CONST type declarator-list = initializer ;')
        def const_stmt(state: ParserState, p):
            return ConstantNode(p[1], p[2], p[4], p[0].getsourcepos())

        ##################################################
        # Class
        ##################################################
        @self.pg.production('class-statement : CLASS IDENTIFIER class-compound')
        def class_stmt(state: ParserState, p):
            return ClassNode(p[1].getstr(), p[2], p[0].getsourcepos())

        @self.pg.production('class-compound : { class-inner }')
        def class_compound(state: ParserState, p):
            return p[1]

        @self.pg.production('class-compound : { }')
        def class_compound_1(state: ParserState, p):
            return ClassCompoundNode(None, None, p[0].getsourcepos())

        @self.pg.production('class-inner : attribute-list')
        def class_inner(state: ParserState, p):
            return ClassCompoundNode(p[0], None, p[0].getsourcepos())

        @self.pg.production('class-inner : method-list')
        def class_inner_1(state: ParserState, p):
            return ClassCompoundNode(None, p[0], p[0].getsourcepos())

        @self.pg.production('class-inner : attribute-list method-list')
        def class_inner_2(state: ParserState, p):
            return ClassCompoundNode(p[0], p[1], p[0].getsourcepos())

        @self.pg.production('attribute-list : attribute')
        def attr_list(state: ParserState, p):
            return BlockNode(p[0], p[0].getsourcepos())

        @self.pg.production('attribute-list : attribute-list attribute')
        def attr_list_rec(state: ParserState, p):
            p[0].add(p[1])

            return p[0]

        @self.pg.production('attribute : parameter ;')
        def attr(state: ParserState, p):
            return p[0]

        @self.pg.production('method-list : function-statement')
        def method_list(state: ParserState, p):
            return BlockNode(p[0], p[0].getsourcepos())

        @self.pg.production('method-list : method-list function-statement')
        def method_list_rec(state: ParserState, p):
            p[0].add(p[1])

            return p[0]

        # @self.pg.production('attribute-list : attribute')
        # def attr_list(state: ParserState, p):
        #     return BlockNode(p[0], p[0].getsourcepos())

        # @self.pg.production('attribute-list : attribute-list attribute')
        # def attr_list_rec(state: ParserState, p):
        #     p[0].add(p[1])

        #     return p[0]

        # @self.pg.production('attribute : parameter')
        # def attr(state: ParserState, p):
        #     return p[0]

        ##################################################
        # Function
        ##################################################
        @self.pg.production('function-statement : function-signature compound-statement')
        def func_stmt(state: ParserState, p):
            return FunctionNode(p[0], p[1], p[0].getsourcepos())

        @self.pg.production('function-signature : function-declarator')
        def func_sig_(state: ParserState, p):
            return FunctionSignatureNode(p[0], EmptyNode(), p[0].getsourcepos())

        @self.pg.production('function-signature : function-declarator type')
        def func_sig(state: ParserState, p):
            return FunctionSignatureNode(p[0], p[1], p[0].getsourcepos())

        @self.pg.production('function-declarator : IDENTIFIER ( )')
        def func_decl_(state: ParserState, p):
            return FunctionDeclarationNode(p[0].getstr(), EmptyNode(), p[0].getsourcepos())

        @self.pg.production('function-declarator : IDENTIFIER ( parameter-list )')
        def func_decl(state: ParserState, p):
            return FunctionDeclarationNode(p[0].getstr(), p[2], p[0].getsourcepos())

        @self.pg.production('parameter-list : parameter')
        def parameter_list(state: ParserState, p):
            return ListNode(p[0], ",", p[0].getsourcepos())

        @self.pg.production('parameter-list : parameter-list , parameter')
        def parameter_list_rec(state: ParserState, p):
            p[0].add(p[2])

            return p[0]

        @self.pg.production('parameter : type declarator')
        def parameter(state: ParserState, p):
            return ParameterNode(p[0], p[1], p[0].getsourcepos())

        # ##################################################
        # # Statement
        # ##################################################
        @self.pg.production('statement-list : statement')
        def statement_list(state: ParserState, p):
            return BlockNode(p[0], p[0].getsourcepos())

        @self.pg.production('statement-list : statement-list statement')
        def statement_list_rec(state: ParserState, p):
            p[0].add(p[1])

            return p[0]

        @self.pg.production('statement : compound-statement')
        @self.pg.production('statement : selection-statement')
        @self.pg.production('statement : iteration-statement')
        @self.pg.production('statement : jump-statement')
        @self.pg.production('statement : simple-statement ;')
        @self.pg.production('statement : declaration')
        def statement(state: ParserState, p):
            return p[0]

        @self.pg.production('simple-statement : expr-statement')
        @self.pg.production('simple-statement : increment-decrement-statement')
        def simple_statement(state: ParserState, p):
            return p[0]

        ##################################################
        # Increment / Decrement Statement
        ##################################################
        @self.pg.production('increment-decrement-statement : expr INC')
        def inc_statement(state: ParserState, p):
            return IncrementNode(p[0], p[0].getsourcepos())

        @self.pg.production('increment-decrement-statement : expr DEC')
        def inc_statement(state: ParserState, p):
            return IncrementNode(p[0], p[0].getsourcepos())

        ##################################################
        # Iteration Statement
        ##################################################
        @self.pg.production('iteration-statement : WHILE ( expr ) statement')
        def statement_while(state: ParserState, p):
            return WhileNode(p[2], p[4], p[0].getsourcepos())

        @self.pg.production('iteration-statement : FOR ( declaration simple-statement ; simple-statement ) statement')
        def statement_for(state: ParserState, p):
            return ForNode(p[2], p[3], p[5], p[7], p[0].getsourcepos())

        ##################################################
        # Selection Statement
        ##################################################
        @self.pg.production('selection-statement : IF ( expr ) compound-statement ELSE compound-statement')
        def if_else_statement(state: ParserState, p):
            return IfElseNode(p[2], p[4], p[6], p[0].getsourcepos())

        @self.pg.production('selection-statement : IF ( expr ) compound-statement')
        def if_statement(state: ParserState, p):
            return IfNode(p[2], p[4], p[0].getsourcepos())

        ##################################################
        # Compound Statement
        ##################################################
        @self.pg.production('compound-statement : { statement-list }')
        def compound_statement(state: ParserState, p):
            return CompoundNode(p[1], p[0].getsourcepos())

        ##################################################
        # Expression Statement
        ##################################################
        @self.pg.production('expr-statement : expr')
        def expression_statement(state: ParserState, p):
            return p[0]

        ##################################################
        # Jump Statement
        ##################################################
        @self.pg.production('jump-statement : RETURN expr ;')
        def jump_statement(state: ParserState, p):
            return JumpNode(p[1], p[0].getsourcepos())

        ##################################################
        # Declarations
        ##################################################
        @self.pg.production('declaration : type declarator-list ;')
        def declaration(state: ParserState, p):
            return DeclarationNode(p[0], p[1], p[0].getsourcepos())

        @self.pg.production('declaration : type declarator-list = initializer ;')
        def declaration_assgn(state: ParserState, p):
            return DeclarationAssgnNode(p[0], p[1], p[3], p[0].getsourcepos())

        @self.pg.production('declarator-list : declarator')
        def declarator_list(state: ParserState, p):
            return ListNode(p[0], ",", p[0].getsourcepos())

        @self.pg.production('declarator-list : declarator-list , declarator')
        def declarator_list_rec(state: ParserState, p):
            p[0].add(p[2])

            return p[0]

        @self.pg.production('declarator : IDENTIFIER')
        def declarator(state: ParserState, p):
            return ValueNode(None, p[0].getstr(), p[0].getsourcepos())

        @self.pg.production('initializer : expr')
        def initalizer(state: ParserState, p):
            return p[0]

        ##################################################
        # Expressions
        ##################################################
        @self.pg.production('expr : assgn-expr')
        def expr(state: ParserState, p):
            return ListNode(p[0], ",", p[0].getsourcepos())

        @self.pg.production('expr : expr , assgn-expr')
        def expr_rec(state: ParserState, p):
            p[0].add(p[2])

            return p[0]

        ##################################################
        # Assign Expression
        ##################################################
        @self.pg.production('assgn-expr : cond-expr')
        def assgn_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('assgn-expr : unary-expr assgn-op assgn-expr')
        def assgn_expr_op(state: ParserState, p):
            return BinaryOpNode(p[1], p[0], p[2], p[0].getsourcepos())

        ##################################################
        # Assign Operators
        ##################################################
        @self.pg.production('assgn-op : =')
        @self.pg.production('assgn-op : *=')
        @self.pg.production('assgn-op : /=')
        @self.pg.production('assgn-op : MODEQ')
        @self.pg.production('assgn-op : +=')
        @self.pg.production('assgn-op : -=')
        @self.pg.production('assgn-op : LSHIFTEQ')
        @self.pg.production('assgn-op : RSHIFTEQ')
        @self.pg.production('assgn-op : &=')
        @self.pg.production('assgn-op : ^=')
        @self.pg.production('assgn-op : LOREQ')
        def assgn_op(state: ParserState, p):
            return p[0].getstr()

        ##################################################
        # Conditional Expression
        ##################################################
        @self.pg.production('cond-expr : lor-expr')
        def cond_expr(state: ParserState, p):
            return p[0]

        # @self.pg.production('cond-expr : lor-expr ? expr : cond-expr')
        # def cond_expr_op(state: ParserState, p):
        #     return BinaryOpNode(p[1].getstr(), p[0], p[2], p[0].getsourcepos())

        ##################################################
        # Logical OR Expression
        ##################################################
        @self.pg.production('lor-expr : land-expr')
        def lor_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('lor-expr : lor-expr LOR land-expr')
        def lor_expr_op(state: ParserState, p):
            return BinaryOpNode(p[1].getstr(), p[0], p[2], p[0].getsourcepos())

        ##################################################
        # Logical AND Expression
        ##################################################
        @self.pg.production('land-expr : or-expr')
        def land_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('land-expr : land-expr LAND or-expr')
        def land_expr_op(state: ParserState, p):
            return BinaryOpNode(p[1].getstr(), p[0], p[2], p[0].getsourcepos())

        ##################################################
        # Bitwise OR Expression
        ##################################################
        @self.pg.production('or-expr : xor-expr')
        def or_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('or-expr : or-expr OR xor-expr')
        def or_expr_op(state: ParserState, p):
            return BinaryOpNode(p[1].getstr(), p[0], p[2], p[0].getsourcepos())

        ##################################################
        # Bitwise XOR Expression
        ##################################################
        @self.pg.production('xor-expr : and-expr')
        def xor_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('xor-expr : xor-expr ^ and-expr')
        def xor_expr_op(state: ParserState, p):
            return BinaryOpNode(p[1].getstr(), p[0], p[2], p[0].getsourcepos())

        ##################################################
        # Bitwise AND Expression
        ##################################################
        @self.pg.production('and-expr : eq-expr')
        def and_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('and-expr : and-expr & eq-expr')
        def and_expr_op(state: ParserState, p):
            return BinaryOpNode(p[1].getstr(), p[0], p[2], p[0].getsourcepos())

        ##################################################
        # Equality Expression
        ##################################################
        @self.pg.production('eq-expr : rel-expr')
        def eq_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('eq-expr : eq-expr == rel-expr')
        @self.pg.production('eq-expr : eq-expr != rel-expr')
        def eq_expr_op(state: ParserState, p):
            return BinaryOpNode(p[1].getstr(), p[0], p[2], p[0].getsourcepos())

        ##################################################
        # Relation Expression
        ##################################################
        @self.pg.production('rel-expr : shift-expr')
        def rel_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('rel-expr : rel-expr < shift-expr')
        @self.pg.production('rel-expr : rel-expr > shift-expr')
        @self.pg.production('rel-expr : rel-expr <= shift-expr')
        @self.pg.production('rel-expr : rel-expr >= shift-expr')
        def rel_expr_(state: ParserState, p):
            return BinaryOpNode(p[1].getstr(), p[0], p[2], p[0].getsourcepos())

        # ##################################################
        # # Shift Expression
        # ##################################################
        @self.pg.production('shift-expr : add-expr')
        def shift_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('shift-expr : shift-expr LSHIFT add-expr')
        @self.pg.production('shift-expr : shift-expr RSHIFT add-expr')
        def shift_expr_op(state: ParserState, p):
            return BinaryOpNode(p[1].getstr(), p[0], p[2], p[0].getsourcepos())

        # ##################################################
        # # additive Expression
        # ##################################################
        @self.pg.production('add-expr : mult-expr')
        def add_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('add-expr : add-expr + mult-expr')
        @self.pg.production('add-expr : add-expr - mult-expr')
        def add_expr_op(state: ParserState, p):
            return BinaryOpNode(p[1].getstr(), p[0], p[2], p[0].getsourcepos())

        ##################################################
        # Multiplicative Expression
        ##################################################
        @self.pg.production('mult-expr : cast-expr')
        def mult_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('mult-expr : mult-expr * cast-expr')
        @self.pg.production('mult-expr : mult-expr / cast-expr')
        @self.pg.production('mult-expr : mult-expr MOD cast-expr')
        def mult_expr_op(state: ParserState, p):
            return BinaryOpNode(p[1].getstr(), p[0], p[2], p[0].getsourcepos())

        ##################################################
        # Cast Expression
        ##################################################
        @self.pg.production('cast-expr : unary-expr')
        def cast_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('cast-expr : < type > cast-expr')
        def cast_expr_type(state: ParserState, p):
            return CastNode(p[1], p[3], p[0].getstr())

        @self.pg.production('type : INT')
        @self.pg.production('type : IDENTIFIER')
        def type_spec(state: ParserState, p):
            # return IdentifierNode(p[0].getstr(), p[0].getsourcepos())
            return TypeNode(p[0].getstr(), p[0].getsourcepos())

        ##################################################
        # Unary Expression
        ##################################################
        @self.pg.production('unary-expr : postfix-expr')
        def unary_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('unary-expr : unary-op cast-expr')
        def unary_expr_op(state: ParserState, p):
            # Note: !! p[0].getsourcepos() -> p[0] str
            return UnaryOpNode(p[0], p[1], p[1].getsourcepos())

        ##################################################
        # Unary Operators
        ##################################################
        @self.pg.production('unary-op : &')
        @self.pg.production('unary-op : *')
        @self.pg.production('unary-op : +')
        @self.pg.production('unary-op : -')
        # @self.pg.production('unary-op : ^')  # << bitwise not
        @self.pg.production('unary-op : !')
        def unary_op(state: ParserState, p):
            return p[0].getstr()

        ##################################################
        # Postfix Expression
        ##################################################
        @self.pg.production('postfix-expr : primary-expr')
        # @self.pg.production('postfix-expr : postfix-expr [ expr ]')
        def postfix_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('postfix-expr : postfix-expr DOT primary-expr')
        def postfix_expr_acc(state: ParserState, p):
            return MemberAccessNode(p[0], p[2], p[0].getsourcepos())

        @self.pg.production('postfix-expr : postfix-expr ( arg-expr-list )')
        def postfix_expr_func(state: ParserState, p):
            return CallNode(p[0], p[2], p[0].getsourcepos())

        ##################################################
        # Argument Expression List
        ##################################################
        @self.pg.production('arg-expr-list : assgn-expr')
        def arg_expr_list(state: ParserState, p):
            return ListNode(p[0], ",", p[0].getsourcepos())

        @self.pg.production('arg-expr-list : arg-expr-list , assgn-expr')
        def arg_expr_list_rec(state: ParserState, p):
            p[0].add(p[2])

            return p[0]

        ##################################################
        # Primary Expression
        ##################################################
        @self.pg.production('primary-expr : IDENTIFIER')
        @self.pg.production('primary-expr : constant')
        def primary_expr(state: ParserState, p):
            # if isinstance(p[0], (IntegerNode, StringNode)):
            #     return ValueNode("INT", p[0].value, p[0].getsourcepos())

            # return ValueNode("IDENTIFIER", p[0].getstr(), p[0].getsourcepos())

            return ValueNode(None, p[0].getstr(), p[0].getsourcepos())

        @self.pg.production('primary-expr : ( expr )')
        def primary_expr_expr(state: ParserState, p):
            return p[1]

        ##################################################
        # Constants
        ##################################################
        @self.pg.production('constant : INTEGER')
        def const_int(state: ParserState, p):
            # return IntegerNode(p[0].getstr(), p[0].getsourcepos())
            return p[0]

        @self.pg.production('constant : STRING')
        def const_str(state: ParserState, p):
            return p[0]

        ##################################################
        # Errors
        ##################################################
        @self.pg.error
        def error_handler(state: ParserState, token: Token):
            pos = token.getsourcepos()

            if pos:
                InvalidSynatxError(
                    pos,
                    state.filename,
                    state.source,
                    f"Unexpected Token: {token.name}, \n {state.traceback}"
                )

            elif token.gettokentype() == '$end':
                UnexpectedEndError(
                    pos,
                    state.filename,
                    state.source,
                    f"Unexpected End, \n {state.traceback}"
                )

            else:
                InvalidSynatxError(
                    state.filename,
                    state.source,
                    f"Unexpected Token: {token.name}"
                )

        return self.pg.build()

    def parse(self, text: str, state: ParserState = None):
        return self.parser.parse(text, state)
