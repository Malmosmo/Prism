from typing import Generator

from rply import ParserGenerator
from rply.token import Token

from astree import *
from errors import *
from util import ParserState


EMPTY = EmptyNode()


class Parser:
    def __init__(self, tokens: list, precedence: list) -> None:
        self.pg = ParserGenerator(tokens, precedence)
        self.parser = self.generateParser()

    def generateParser(self):
        # ------------------------------------------------
        # program
        # ------------------------------------------------
        @self.pg.production('translation-unit : external-declaration')
        def translation_unit(state: ParserState, p):
            return BlockNode(p[0], p[0].getsourcepos())

        @self.pg.production('translation-unit : translation-unit external-declaration')
        def translation_unit(state: ParserState, p):
            p[0].add(p[1])

            return p[0]

        @self.pg.production('external-declaration : function-definition')
        @self.pg.production('external-declaration : declaration')
        def external_declaration(state: ParserState, p):
            return p[0]

        @self.pg.production('external-declaration : PRAGMA')
        def external_declaration(state: ParserState, p):
            return ValueNode(None, p[0].getstr(), p[0].getsourcepos())

        @self.pg.production('function-definition : declaration-specifiers declarator compound-statement')
        def function_definition(state: ParserState, p):
            return FunctionNode(p[0], p[1], p[2], p[0].getsourcepos())

        @self.pg.production('declaration-specifiers : declaration-qualifier')
        def declaration_specifiers(state: ParserState, p):
            return p[0]

        @self.pg.production('declaration-specifiers : declaration-qualifier declaration-specifiers')
        def declaration_specifiers(state: ParserState, p):
            return CombinationNode(p[0], p[1], p[0].getsourcepos())

        @self.pg.production('declaration-qualifier : storage-class-specifier')
        @self.pg.production('declaration-qualifier : type-specifier')
        @self.pg.production('declaration-qualifier : type-qualifier')
        @self.pg.production('declaration-qualifier : function-specifier')
        def declaration_qualifier(state: ParserState, p):
            return p[0]

        @self.pg.production('storage-class-specifier : TYPEDEF')
        @self.pg.production('storage-class-specifier : EXTERN')
        @self.pg.production('storage-class-specifier : STATIC')
        @self.pg.production('storage-class-specifier : AUTO')
        @self.pg.production('storage-class-specifier : REGISTER')
        def storage_class_specifier(state: ParserState, p):
            return ValueNode(None, p[0].getstr(), p[0].getsourcepos())

        @self.pg.production('type-specifier : SHORT')
        @self.pg.production('type-specifier : LONG')
        @self.pg.production('type-specifier : INT')
        @self.pg.production('type-specifier : FLOAT')
        @self.pg.production('type-specifier : DOUBLE')
        @self.pg.production('type-specifier : CHAR')
        @self.pg.production('type-specifier : VOID')
        @self.pg.production('type-specifier : SIGNED')
        @self.pg.production('type-specifier : UNSIGNED')
        def type_specifier(state: ParserState, p):
            return ValueNode(None, p[0].getstr(), p[0].getsourcepos())

        @self.pg.production('type-specifier : struct-or-union-specifier')
        # @self.pg.production('type-specifier : enum-specifier')
        @self.pg.production('type-specifier : typedef-name')
        def type_specifier(state: ParserState, p):
            return p[0]

        @self.pg.production('struct-or-union-specifier : struct-or-union IDENTIFIER { struct-declaration-list }')
        def struct_or_union_specifier(state: ParserState, p):
            return StructOrUnionNode(p[0], ValueNode(None, p[1].getstr(), p[1].getsourcepos()), p[3], p[0].getsourcepos())

        @self.pg.production('struct-or-union-specifier : struct-or-union { struct-declaration-list }')
        def struct_or_union_specifier(state: ParserState, p):
            return StructOrUnionNode(p[0], EMPTY, p[3], p[0].getsourcepos())

        @self.pg.production('struct-or-union-specifier : struct-or-union IDENTIFIER')
        def struct_or_union_specifier(state: ParserState, p):
            return StructOrUnionNode(p[0], ValueNode(None, p[1].getstr(), p[1].getsourcepos()), EMPTY, p[0].getsourcepos())

        @self.pg.production('struct-or-union : UNION')
        @self.pg.production('struct-or-union : STRUCT')
        def struct_or_union(state: ParserState, p):
            return ValueNode(None, p[0].getstr(), p[0].getsourcepos())

        @self.pg.production('struct-declaration-list : struct-declaration')
        def struct_declaration_list(state: ParserState, p):
            return BlockNode(p[0], p[0].getsourcepos())

        @self.pg.production('struct-declaration-list : struct-declaration-list struct-declaration')
        def struct_declaration_list(state: ParserState, p):
            p[0].add(p[1])

            return p[0]

        @self.pg.production('struct-declaration : specifier-qualifier-list struct-declarator-list ;')
        def struct_declaration(state: ParserState, p):
            return StructDeclarationNode(p[0], p[1], p[0].getsourcepos())

        @self.pg.production('specifier-qualifier-list : specifier-qualifier')
        def specifier_qualifier_list(state: ParserState, p):
            return BlockNode(p[0], p[0].getsourcepos())

        @self.pg.production('specifier-qualifier-list : specifier-qualifier specifier-qualifier-list')
        def specifier_qualifier_list(state: ParserState, p):
            p[1].add(p[0])

            return p[1]

        @self.pg.production('specifier-qualifier : type-specifier')
        @self.pg.production('specifier-qualifier : type-qualifier')
        def specifier_qualifier(state: ParserState, p):
            return p[0]

        @self.pg.production('type-qualifier : CONST')
        @self.pg.production('type-qualifier : VOLATILE')
        @self.pg.production('type-qualifier : RESTRICT')
        def type_qualifier(state: ParserState, p):
            return p[0]

        @self.pg.production('struct-declarator-list : struct-declarator')
        def struct_declarator_list(state: ParserState, p):
            return ListNode(p[0], ",", p[0].getsourcepos())

        @self.pg.production('struct-declarator-list : struct-declarator-list , struct-declarator')
        def struct_declarator_list(state: ParserState, p):
            p[0].add(p[2])

            return p[0]

        @self.pg.production('struct-declarator : declarator')
        def struct_declarator(state: ParserState, p):
            return p[0]

        @self.pg.production('struct-declarator : declarator DDOT const-expr')
        def struct_declarator(state: ParserState, p):
            return BinaryOpNode(p[1].getstr(), p[0], p[2], p[0].getsourcepos())

        @self.pg.production('declarator : direct-declarator')
        def declarator(state: ParserState, p):
            return DeclaratorNode(EMPTY, p[0], p[0].getsourcepos())

        @self.pg.production('declarator : pointer direct-declarator')
        def declarator(state: ParserState, p):
            return DeclaratorNode(p[0], p[1], p[0].getsourcepos())

        @self.pg.production('pointer : *')
        def pointer(state: ParserState, p):
            return PointerNode(EMPTY, p[0].getsourcepos())

        @self.pg.production('pointer : * pointer')
        @self.pg.production('pointer : * type-qualifier-list')
        def pointer(state: ParserState, p):
            return PointerNode(p[1], p[0].getsourcepos())

        @self.pg.production('pointer : * type-qualifier-list pointer')
        def pointer(state: ParserState, p):
            return PointerNode(CombinationNode(p[1], p[2], p[1].getsourcepos()), p[0].getsourcepos())

        @self.pg.production('type-qualifier-list : type-qualifier')
        def type_qualifier_list(state: ParserState, p):
            return BlockNode(p[0], p[0].getsourcepos())

        @self.pg.production('type-qualifier-list : type-qualifier-list type-qualifier')
        def type_qualifier_list(state: ParserState, p):
            p[0].add(p[1])

            return p[0]

        # TODO
        @self.pg.production('direct-declarator : IDENTIFIER')
        # @self.pg.production('direct-declarator : [ type-qualifier-list assgn-expr ]')
        # @self.pg.production('direct-declarator : [ type-qualifier-list ]')
        # @self.pg.production('direct-declarator : [ assgn-expr ]')
        # @self.pg.production('direct-declarator : [ STATIC type-qualifier-list assgn-expr ]')
        # @self.pg.production('direct-declarator : [ type-qualifier-list STATIC assgn-expr ]')
        # @self.pg.production('direct-declarator : [ type-qualifier-list * ]')
        # @self.pg.production('direct-declarator : [ * ]')
        def direct_declarator(state: ParserState, p):
            return ValueNode(None, p[0].getstr(), p[0].getsourcepos())

        @self.pg.production('direct-declarator : ( declarator )')
        def direct_declarator(state: ParserState, p):
            return BracketNode(p[1], "()", p[0].getsourcepos())

        @self.pg.production('direct-declarator : direct-declarator [  ]')
        def direct_declarator(state: ParserState, p):
            bracket = BracketNode(EMPTY, "[]", p[1].getsourcepos())

            return DirectDeclaratorNode(p[0], bracket, p[0].getsourcepos())

        @self.pg.production('direct-declarator : direct-declarator ( )')
        def direct_declarator(state: ParserState, p):
            bracket = BracketNode(EMPTY, "()", p[1].getsourcepos())

            return DirectDeclaratorNode(p[0], bracket, p[0].getsourcepos())

        @self.pg.production('direct-declarator : direct-declarator ( parameter-type-list )')
        @self.pg.production('direct-declarator : direct-declarator ( identifier-list )')    # TODO: possible TYPEDIDENT ?
        def direct_declarator(state: ParserState, p):
            bracket = BracketNode(p[2], "()", p[1].getsourcepos())

            return DirectDeclaratorNode(p[0], bracket, p[0].getsourcepos())

        # ------------------------------------------------
        # assign-expression
        # ------------------------------------------------
        @self.pg.production('assgn-expr : cond-expr')
        def assgn_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('assgn-expr : unary-expr assgn-op assgn-expr')
        def assgn_expr_op(state: ParserState, p):
            return BinaryOpNode(p[1], p[0], p[2], p[0].getsourcepos())

        @self.pg.production('assgn-op : =')
        @self.pg.production('assgn-op : *=')
        @self.pg.production('assgn-op : /=')
        @self.pg.production('assgn-op : %=')
        @self.pg.production('assgn-op : +=')
        @self.pg.production('assgn-op : -=')
        @self.pg.production('assgn-op : >>=')
        @self.pg.production('assgn-op : <<=')
        @self.pg.production('assgn-op : &=')
        @self.pg.production('assgn-op : ^=')
        @self.pg.production('assgn-op : OREQ')
        def assgn_op(state: ParserState, p):
            return p[0].getstr()

        # ------------------------------------------------
        # conditional-expression
        # ------------------------------------------------
        @self.pg.production('cond-expr : lor-expr')
        def cond_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('cond-expr : lor-expr ? expr DDOT cond-expr')
        def cond_expr_op(state: ParserState, p):
            return ConditionalNode(p[0], p[2], p[4], p[0].getsourcepos())

        # ------------------------------------------------
        # logical-or-expression
        # ------------------------------------------------
        @self.pg.production('lor-expr : land-expr')
        def lor_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('lor-expr : lor-expr LOR land-expr')
        def lor_expr_op(state: ParserState, p):
            return BinaryOpNode(p[1].getstr(), p[0], p[2], p[0].getsourcepos())

        # ------------------------------------------------
        # logical-and-expression
        # ------------------------------------------------
        @self.pg.production('land-expr : or-expr')
        def land_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('land-expr : land-expr && or-expr')
        def land_expr_op(state: ParserState, p):
            return BinaryOpNode(p[1].getstr(), p[0], p[2], p[0].getsourcepos())

        # ------------------------------------------------
        # bitwise-or-expression
        # ------------------------------------------------
        @self.pg.production('or-expr : xor-expr')
        def or_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('or-expr : or-expr OR xor-expr')
        def or_expr_op(state: ParserState, p):
            return BinaryOpNode(p[1].getstr(), p[0], p[2], p[0].getsourcepos())

        # ------------------------------------------------
        # bitwise-xor-expression
        # ------------------------------------------------
        @self.pg.production('xor-expr : and-expr')
        def xor_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('xor-expr : xor-expr ^ and-expr')
        def xor_expr_op(state: ParserState, p):
            return BinaryOpNode(p[1].getstr(), p[0], p[2], p[0].getsourcepos())

        # ------------------------------------------------
        # bitwise-and-expression
        # ------------------------------------------------
        @self.pg.production('and-expr : eq-expr')
        def and_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('and-expr : and-expr & eq-expr')
        def and_expr_op(state: ParserState, p):
            return BinaryOpNode(p[1].getstr(), p[0], p[2], p[0].getsourcepos())

        # ------------------------------------------------
        # equality-expression
        # ------------------------------------------------
        @self.pg.production('eq-expr : rel-expr')
        def eq_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('eq-expr : eq-expr == rel-expr')
        @self.pg.production('eq-expr : eq-expr != rel-expr')
        def eq_expr_op(state: ParserState, p):
            return BinaryOpNode(p[1].getstr(), p[0], p[2], p[0].getsourcepos())

        # ------------------------------------------------
        # relation-expression
        # ------------------------------------------------
        @self.pg.production('rel-expr : shift-expr')
        def rel_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('rel-expr : rel-expr < shift-expr')
        @self.pg.production('rel-expr : rel-expr > shift-expr')
        @self.pg.production('rel-expr : rel-expr <= shift-expr')
        @self.pg.production('rel-expr : rel-expr >= shift-expr')
        def rel_expr_(state: ParserState, p):
            return BinaryOpNode(p[1].getstr(), p[0], p[2], p[0].getsourcepos())

        # ------------------------------------------------
        # shift-expression
        # ------------------------------------------------
        @self.pg.production('shift-expr : add-expr')
        def shift_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('shift-expr : shift-expr << add-expr')
        @self.pg.production('shift-expr : shift-expr >> add-expr')
        def shift_expr_op(state: ParserState, p):
            return BinaryOpNode(p[1].getstr(), p[0], p[2], p[0].getsourcepos())

        # ------------------------------------------------
        # addiditve-expression
        # ------------------------------------------------
        @self.pg.production('add-expr : mult-expr')
        def add_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('add-expr : add-expr + mult-expr')
        @self.pg.production('add-expr : add-expr - mult-expr')
        def add_expr_op(state: ParserState, p):
            return BinaryOpNode(p[1].getstr(), p[0], p[2], p[0].getsourcepos())

        # ------------------------------------------------
        # multiplicative-expression
        # ------------------------------------------------
        @self.pg.production('mult-expr : cast-expr')
        def mult_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('mult-expr : mult-expr * cast-expr')
        @self.pg.production('mult-expr : mult-expr / cast-expr')
        @self.pg.production('mult-expr : mult-expr % cast-expr')
        def mult_expr_op(state: ParserState, p):
            return BinaryOpNode(p[1].getstr(), p[0], p[2], p[0].getsourcepos())

        # ------------------------------------------------
        # cast-expression
        # ------------------------------------------------
        @self.pg.production('cast-expr : unary-expr')
        def cast_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('cast-expr : ( type-name ) cast-expr')
        def cast_expr_type(state: ParserState, p):
            return CastNode(p[1], p[3], p[0].getstr())

        # ------------------------------------------------
        # unary-expression
        # ------------------------------------------------
        @self.pg.production('unary-expr : postfix-expr')
        def unary_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('unary-expr : unary-op cast-expr')
        def unary_expr_op(state: ParserState, p):
            return UnaryOpNode(p[0].getstr(), p[1], p[0].getsourcepos())

        @self.pg.production('unary-expr : SIZEOF unary-expr')
        def unary_size_of(state: ParserState, p):
            return SizeOfNode(p[1], p[0].getsourcepos())

        @self.pg.production('unary-expr : SIZEOF ( type-name )')
        def unary_size_of(state: ParserState, p):
            return SizeOfNode(p[2], p[0].getsourcepos())

        # ------------------------------------------------
        # postfix-expression
        # ------------------------------------------------
        @self.pg.production('unary-op : &')
        @self.pg.production('unary-op : *')
        @self.pg.production('unary-op : +')
        @self.pg.production('unary-op : -')
        @self.pg.production('unary-op : ~')
        @self.pg.production('unary-op : !')
        def unary_op(state: ParserState, p):
            return p[0]

        # ------------------------------------------------
        # postfix-expression
        # ------------------------------------------------
        @self.pg.production('postfix-expr : primary-expr')
        def postfix_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('postfix-expr : postfix-expr [ expr ]')
        def postfix_expr(state: ParserState, p):
            return ArrayAccessNode(p[0], p[2], p[0].getsourcepos())

        @self.pg.production('postfix-expr : postfix-expr ( )')
        def postfix_expr(state: ParserState, p):
            return FunctionCallNode(p[0], EMPTY, p[0].getsourcepos())

        @self.pg.production('postfix-expr : postfix-expr ( argument-expression-list )')
        def postfix_expr(state: ParserState, p):
            return FunctionCallNode(p[0], p[2], p[0].getsourcepos())

        @self.pg.production('postfix-expr : postfix-expr . IDENTIFIER')
        def postfix_expr(state: ParserState, p):
            return AttributeNode(p[0], p[2].getstr(), p[0].getsourcepos())

        @self.pg.production('postfix-expr : postfix-expr -> IDENTIFIER')
        def postfix_expr(state: ParserState, p):
            return AttributeArrowNode(p[0], p[2].getstr(), p[0].getsourcepos())

        @self.pg.production('postfix-expr : postfix-expr ++')
        @self.pg.production('postfix-expr : postfix-expr --')
        def postfix_expr(state: ParserState, p):
            return CombinationNode(p[0], ValueNode(None, p[1].getstr(), p[1].getsourcepos()), p[0].getsourcepos())

        @self.pg.production('postfix-expr : ( type-name ) { initalizer-list }')
        @self.pg.production('postfix-expr : ( type-name ) { initalizer-list , }')
        def postfix_expr(state: ParserState, p):
            return ArrayNode(p[1], p[4], p[0].getsourcepos())

        # ------------------------------------------------
        # argument-expression-list
        # ------------------------------------------------
        @self.pg.production('argument-expression-list : assgn-expr')
        def argument_expression_list(state: ParserState, p):
            return ListNode(p[0], ",", p[0].getsourcepos())

        @self.pg.production('argument-expression-list : argument-expression-list , assgn-expr')
        def argument_expression_list(state: ParserState, p):
            p[0].add(p[2])

            return p[0]

        # ------------------------------------------------
        # primary-expression
        # ------------------------------------------------
        @self.pg.production('primary-expr : IDENTIFIER')
        @self.pg.production('primary-expr : CONSTANT')
        @self.pg.production('primary-expr : STRING')
        def primary_expr(state: ParserState, p):
            return ValueNode(None, p[0].getstr(), p[0].getsourcepos())

        # @self.pg.production('enumeration-constant : IDENTIFIER')
        # def enumeration_constant(state: ParserState, p):
        #     return ValueNode(None, p[0].getstr(), p[0].getsourcepos())

        @self.pg.production('primary-expr : ( expr )')
        def primary_expr_expr(state: ParserState, p):
            return p[1]

        @self.pg.production('expr : assgn-expr')
        def expr(state: ParserState, p):
            return ListNode(p[0], ",", p[0].getsourcepos())

        @self.pg.production('expr : expr , assgn-expr')
        def expr(state: ParserState, p):
            p[0].add(p[2])

            return p[0]

        @self.pg.production('arg-expr-list : assgn-expr')
        def arg_expr_list(state: ParserState, p):
            return ListNode(p[0], ",", p[0].getsourcepos())

        @self.pg.production('arg-expr-list : arg-expr-list , assgn-expr')
        def arg_expr_list(state: ParserState, p):
            p[0].add(p[2])

            return p[0]

        @self.pg.production('type-name : specifier-qualifier-list')
        def type_name(state: ParserState, p):
            return CombinationNode(p[0], EMPTY, p[0].getsourcepos())

        @self.pg.production('type-name : specifier-qualifier-list abstract-declarator')
        def type_name(state: ParserState, p):
            return CombinationNode(p[0], p[1], p[0].getsourcepos())

        @self.pg.production('abstract-declarator : pointer')
        @self.pg.production('abstract-declarator : direct-abstract-declarator')
        def abstract_declarator(state: ParserState, p):
            return p[0]

        @self.pg.production('abstract-declarator : pointer direct-abstract-declarator')
        def abstract_declarator(state: ParserState, p):
            return CombinationNode(p[0], p[1], p[0].getsourcepos())

        # TODO
        @self.pg.production('direct-abstract-declarator : ( abstract-declarator )')
        # @self.pg.production('direct-abstract-declarator : direct-abstract-declarator? "[" "static" type-qualifier-list? assignment-expression "]"')
        # @self.pg.production('direct-abstract-declarator : direct-abstract-declarator? "[" type-qualifier-list "static" assignment-expression "]"')
        def direct_abstract_declarator(state: ParserState, p):
            return BracketNode(p[1], "()", p[0].getsourcepos())

        @self.pg.production('direct-abstract-declarator : [ ]')
        def direct_abstract_declarator(state: ParserState, p):
            return BracketNode(EMPTY, "[]", p[0].getsourcepos())

        @self.pg.production('direct-abstract-declarator : [ assgn-expr ]')
        def direct_abstract_declarator(state: ParserState, p):
            return BracketNode(p[1], "[]", p[0].getsourcepos())

        @self.pg.production('direct-abstract-declarator : direct-abstract-declarator [ ]')
        def direct_abstract_declarator(state: ParserState, p):
            bracket = BracketNode(EMPTY, "[]", p[1].getsourcepos())
            return CombinationNode(p[0], bracket, p[0].getsourcepos())

        @self.pg.production('direct-abstract-declarator : direct-abstract-declarator [ assgn-expr ]')
        def direct_abstract_declarator(state: ParserState, p):
            bracket = BracketNode(p[2], "[]", p[1].getsourcepos())
            return CombinationNode(p[0], bracket, p[0].getsourcepos())

        @self.pg.production('direct-abstract-declarator : [ * ]')
        def direct_abstract_declarator(state: ParserState, p):
            return BracketNode(ValueNode(None, "*", p[1].getsourcepos()), "[]", p[0].getsourcepos())

        @self.pg.production('direct-abstract-declarator : direct-abstract-declarator [ * ]')
        def direct_abstract_declarator(state: ParserState, p):
            bracket = BracketNode(ValueNode(None, "*", p[2].getsourcepos()), "[]", p[1].getsourcepos())
            return CombinationNode(p[0], bracket, p[0].getsourcepos())

        @self.pg.production('direct-abstract-declarator : ( )')
        def direct_abstract_declarator(state: ParserState, p):
            return BracketNode(EMPTY, "()", p[0].getsourcepos())

        @self.pg.production('direct-abstract-declarator : ( parameter-type-list )')
        def direct_abstract_declarator(state: ParserState, p):
            return BracketNode(p[1], "()", p[0].getsourcepos())

        @self.pg.production('direct-abstract-declarator : direct-abstract-declarator ( )')
        def direct_abstract_declarator(state: ParserState, p):
            bracket = BracketNode(EMPTY, "()", p[1].getsourcepos())
            return CombinationNode(p[0], bracket, p[0].getsourcepos())

        @self.pg.production('direct-abstract-declarator : direct-abstract-declarator ( parameter-type-list )')
        def direct_abstract_declarator(state: ParserState, p):
            bracket = BracketNode(p[2], "()", p[1].getsourcepos())
            return CombinationNode(p[0], bracket, p[0].getsourcepos())

        # -------------------------------------

        @self.pg.production('parameter-type-list : parameter-list')
        def parameter_type_list(state: ParserState, p):
            return p[0]

        @self.pg.production('parameter-type-list : parameter-list , ...')
        def parameter_type_list(state: ParserState, p):
            paramNode = ListNode(p[0], ",", p[0].getsourcepos())
            paramNode.add(p[2])

            return paramNode

        @self.pg.production('parameter-list : parameter-declaration')
        def parameter_list(state: ParserState, p):
            return ListNode(p[0], ",", p[0].getsourcepos())

        @self.pg.production('parameter-list : parameter-list , parameter-declaration')
        def parameter_list(state: ParserState, p):
            p[0].add(p[2])

            return p[0]

        @self.pg.production('parameter-declaration : declaration-specifiers')
        def parameter_declaration(state: ParserState, p):
            return CombinationNode(p[0], EMPTY, p[0].getsourcepos())

        @self.pg.production('parameter-declaration : declaration-specifiers declarator')
        @self.pg.production('parameter-declaration : declaration-specifiers abstract-declarator')
        def parameter_declaration(state: ParserState, p):
            return CombinationNode(p[0], p[1], p[0].getsourcepos())

        @self.pg.production('initalizer-list : init-qualifier')
        def initalizer_list(state: ParserState, p):
            return ListNode(p[0], ",", p[0].getsourcepos())

        @self.pg.production('initalizer-list : initalizer-list , init-qualifier')
        def initalizer_list(state: ParserState, p):
            p[0].add(p[2])

            return p[0]

        @self.pg.production('init-qualifier : initalizer')
        def init_qualifier(state: ParserState, p):
            return CombinationNode(p[0], EMPTY, p[0].getsourcepos())

        @self.pg.production('init-qualifier : designation initalizer')
        def init_qualifier(state: ParserState, p):
            return CombinationNode(p[0], p[1], p[0].getsourcepos())

        @self.pg.production('designation : designator-list =')
        def designation(state: ParserState, p):
            return DesignationNode(p[0], p[0].getsourcepos())

        @self.pg.production('designator-list : designator')
        def designator_list(state: ParserState, p):
            return BlockNode(p[0], p[0].getsourcepos())

        @self.pg.production('designator-list : designator-list designator')
        def designator_list(state: ParserState, p):
            p[0].add(p[1])

            return p[0]

        @self.pg.production('designator : [ const-expr ]')
        def designator(state: ParserState, p):
            return DesignatorNode(p[1], 0, p[0].getsourcepos())

        @self.pg.production('designator : . IDENTIFIER')
        def designator(state: ParserState, p):
            return DesignatorNode(p[1], 1, p[0].getsourcepos())

        @self.pg.production('const-expr : cond-expr')
        def const_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('initalizer : assgn-expr')
        def initalizer(state: ParserState, p):
            return p[0]

        @self.pg.production('initalizer : { initalizer-list }')
        @self.pg.production('initalizer : { initalizer-list , }')
        def initalizer(state: ParserState, p):
            return CurlyNode(p[1], p[0].getsourcepos())

        @self.pg.production('identifier-list : IDENTIFIER')
        def identifier_list(state: ParserState, p):
            ident = ValueNode(None, p[0].getstr(), p[0].getsourcepos())
            return ListNode(ident, ",", p[0].getsourcepos())

        @self.pg.production('identifier-list : identifier-list , IDENTIFIER')
        def identifier_list(state: ParserState, p):
            ident = ValueNode(None, p[2].getstr(), p[2].getsourcepos())

            p[0].add(ident)

            return p[0]

        # !!!!
        # !!!! shift / reduce - conflict
        # !!!!

        # @self.pg.production('enum-specifier : enum-qualifier')
        # def enum_specifier(state: ParserState, p):
        #     return EnumSpecifierNode(p[0], EMPTY, p[0].getsourcepos())

        # @self.pg.production('enum-specifier : enum-qualifier enum-list')
        # def enum_specifier(state: ParserState, p):
        #     # TODO: CombineNode candidate
        #     return EnumSpecifierNode(p[0], p[1], p[0].getsourcepos())

        # @self.pg.production('enum-qualifier : ENUM')
        # def enum_qualifier(state: ParserState, p):
        #     return EnumQualifierNode(EMPTY, p[0].getsourcepos())

        # @self.pg.production('enum-qualifier : ENUM IDENTIFIER')
        # def enum_qualifier(state: ParserState, p):
        #     return EnumQualifierNode(p[1].getstr(), p[0].getsourcepos())

        # @self.pg.production('enum-list : { enumerator-list }')
        # @self.pg.production('enum-list : { enumerator-list , }')
        # def enum_list(state: ParserState, p):
        #     return CurlyNode(p[1], p[0].getsourcepos())

        # @self.pg.production('enumerator-list : enumerator')
        # def enumerator_list(state: ParserState, p):
        #     return ListNode(p[0], ",", p[0].getsourcepos())

        # @self.pg.production('enumerator-list : enumerator-list , enumerator')
        # def enumerator_list(state: ParserState, p):
        #     p[0].add(p[2])

        #     return p[0]

        # @self.pg.production('enumerator : enumeration-constant')
        # def enumerator(state: ParserState, p):
        #     return EnumeratorNode(p[0], EMPTY, p[0].getsourcepos())

        # @self.pg.production('enumerator : enumeration-constant = const-expr')
        # def enumerator(state: ParserState, p):
        #     return EnumeratorNode(p[0], p[2], p[0].getsourcepos())

        # !!!!
        # !!!! shift / reduce - conflict
        # !!!!

        # TODO: --
        @self.pg.production('typedef-name : TYPEDIDENT')
        def typedef_name(state: ParserState, p):
            return ValueNode(None, p[0].getstr(), p[0].getsourcepos())

        @self.pg.production('function-specifier : INLINE')
        def function_specifier(state: ParserState, p):
            return ValueNode(None, p[0].getstr(), p[0].getsourcepos())

        @self.pg.production('declaration-list : declaration')
        def declaration_list(state: ParserState, p):
            return BlockNode(p[0], p[0].getsourcepos())

        @self.pg.production('declaration-list : declaration-list declaration')
        def declaration_list(state: ParserState, p):
            p[0].add(p[2])

            return p[0]

        @self.pg.production('declaration : declaration-specifiers init-declarator-list ;')
        def declaration(state: ParserState, p):
            return DeclarationNode(p[0], p[1], p[0].getsourcepos())

        @self.pg.production('init-declarator-list : init-declarator')
        def init_declarator_list(state: ParserState, p):
            return ListNode(p[0], ",", p[0].getsourcepos())

        @self.pg.production('init-declarator-list : init-declarator-list , init-declarator')
        def init_declarator_list(state: ParserState, p):
            p[0].add(p[2])

            return p[0]

        @self.pg.production('init-declarator : declarator')
        def init_declarator(state: ParserState, p):
            return DeclaratorInitNode(p[0], EMPTY, p[0].getsourcepos())

        @self.pg.production('init-declarator : declarator = initalizer')
        def init_declarator(state: ParserState, p):
            return DeclaratorInitNode(p[0], p[2], p[0].getsourcepos())

        @self.pg.production('compound-statement : { }')
        def compound_statement(state: ParserState, p):
            return CurlyNode(EMPTY, p[0].getsourcepos())

        @self.pg.production('compound-statement : { block-item-list }')
        def compound_statement(state: ParserState, p):
            return CurlyNode(p[1], p[0].getsourcepos())

        @self.pg.production('block-item-list : block-item')
        def block_item_list(state: ParserState, p):
            return BlockNode(p[0], p[0].getsourcepos())

        @self.pg.production('block-item-list : block-item-list block-item')
        def block_item_list(state: ParserState, p):
            p[0].add(p[1])

            return p[0]

        @self.pg.production('block-item : statement')
        @self.pg.production('block-item : declaration')
        def block_item(state: ParserState, p):
            return p[0]

        @self.pg.production('block-item : PRAGMA')
        def block_item(state: ParserState, p):
            return ValueNode(None, p[0].getstr(), p[0].getsourcepos())

        @self.pg.production('statement : expression-statement')
        @self.pg.production('statement : compound-statement')
        @self.pg.production('statement : labeled-statement')
        @self.pg.production('statement : selection-statement')
        @self.pg.production('statement : iteration-statement')
        @self.pg.production('statement : jump-statement')
        def statement(state: ParserState, p):
            return p[0]

        @self.pg.production('expression-statement : expr ;')
        def expression_statement(state: ParserState, p):
            return ExpressionNode(p[0], p[0].getsourcepos())

        @self.pg.production('labeled-statement : CASE const-expr DDOT statement')
        def labeled_statement(state: ParserState, p):
            return CaseNode(p[1], p[3], p[0].getsourcepos())

        @self.pg.production('labeled-statement : DEFAULT DDOT statement')
        def labeled_statement(state: ParserState, p):
            return CaseDefaultNode(p[2], p[0].getsourcepos())

        @self.pg.production('selection-statement : IF ( expr ) statement')
        def selection_statement(state: ParserState, p):
            return IfNode(p[2], p[4], p[0].getsourcepos())

        @self.pg.production('selection-statement : IF ( expr ) compound-statement ELSE statement')
        def selection_statement(state: ParserState, p):
            return IfElseNode(p[2], p[4], p[6], p[0].getsourcepos())

        @self.pg.production('selection-statement : SWITCH ( expr ) statement')
        def selection_statement(state: ParserState, p):
            return SwitchNode(p[2], p[4], p[0].getsourcepos())

        @self.pg.production('iteration-statement : WHILE ( expr ) statement')
        def iteration_statement(state: ParserState, p):
            return WhileNode(p[2], p[4], p[0].getsourcepos())

        @self.pg.production('iteration-statement : DO statement WHILE ( expr ) ;')
        def iteration_statement(state: ParserState, p):
            return DoWhileNode(p[4], p[1], p[0].getsourcepos())

        @self.pg.production('iteration-statement : FOR ( declaration expr ; expr ) statement')
        def iteration_statement(state: ParserState, p):
            return ForNode(p[2], p[3], p[5], p[7], p[0].getsourcepos())

        @self.pg.production('jump-statement : CONTINUE ;')
        @self.pg.production('jump-statement : BREAK ;')
        def jump_statement(state: ParserState, p):
            return JumpNode(p[0].getstr(), EMPTY, p[0].getsourcepos())

        @self.pg.production('jump-statement : RETURN expr ;')
        def jump_statement(state: ParserState, p):
            return JumpNode(p[0].getstr(), p[1], p[0].getsourcepos())

        ##################################################
        # Errors
        ##################################################

        @self.pg.error
        def errorHandler(state: ParserState, token: Token):
            position = token.getsourcepos()

            if position:
                InvalidSyntaxError(
                    position,
                    state.filename,
                    state.source,
                    f"Unexpected Token: {token.name}, \n {state.traceback}"
                )

            elif token.gettokentype() == '$end':
                UnexpectedEndError(
                    position,
                    state.filename,
                    state.source,
                    f"Unexpected End, \n {state.traceback}"
                )

            else:
                print("OHO!:", token, position)

                raise ValueError()
                # InvalidSyntaxError(
                #     None
                #     state.filename,
                #     state.source,
                #     f"Unexpected Token: {token.name}"
                # )

        return self.pg.build()

    def parse(self, tokens: Generator[Token, None, None], state: ParserState = None):
        return self.parser.parse(tokens, state)
