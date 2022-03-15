text = """        ##################################################
        # Constants
        ##################################################
        @self.pg.production('constant : INTEGER')
        def const_int(state: ParserState, p):
            return IntegerNode(p[0].getstr(), p[0].getsourcepos())

        @self.pg.production('constant : STRING')
        def const_int(state: ParserState, p):
            return StringNode(p[0].getstr(), p[0].getsourcepos())

        ##################################################
        # Primary Expression
        ##################################################

        @self.pg.production('primary-expr : IDENTIFIER')
        @self.pg.production('primary-expr : constant')
        def primary_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('primary-expr : ( expr )')
        def primary_expr_expr(state: ParserState, p):
            return p[1]

        ##################################################
        # Postfix Expression
        ##################################################
        @self.pg.production('postfix-expr : primary-expr')
        # @self.pg.production('postfix-expr : postfix-expr [ expr ]')
        # @self.pg.production('postfix-expr : postfix-expr "(" arg-expr-list ")"')
        # @self.pg.production('postfix-expr : postfix-expr . IDENTIFIER')
        # @self.pg.production('postfix-expr : postfix-expr ++')
        # @self.pg.production('postfix-expr : postfix-expr --')
        def postfix_expr(state: ParserState, p):
            return p[0]

        ##################################################
        # Argument Expression List
        ##################################################
        # @self.pg.production('arg-expr-list : assgn-expr')
        # @self.pg.production('arg-expr-list : arg-expr-list , assgn-expr')
        # def arg_expr_list(state: ParserState, p):
        #     return

        ##################################################
        # Unary Expression
        ##################################################
        @self.pg.production('unary-expr : postfix-expr')
        def unary_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('unary-expr : unary-op cast-expr')
        def unary_expr_op(state: ParserState, p):
            return UnaryOpNode(p[0], p[1], p[0].getsourcepos())

        ##################################################
        # Unary Operators
        ##################################################
        @self.pg.production('unary-op : &')
        @self.pg.production('unary-op : *')
        @self.pg.production('unary-op : +')
        @self.pg.production('unary-op : -')
        # @self.pg.production('unary-op : ~')
        @self.pg.production('unary-op : !')
        def unary_op(state: ParserState, p):
            return p[0].getstr()

        ##################################################
        # Cast Expression
        ##################################################
        @self.pg.production('cast-expr : unary-expr')
        def cast_expr(state: ParserState, p):
            return p[0]

        # @self.pg.production('cast-expr : "(" type-name ")" cast-expr')
        # def cast_expr_type(state: ParserState, p):
        #     return p[0]

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
        # additive Expression
        ##################################################
        @self.pg.production('add-expr : mult-expr')
        def add_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('add-expr : add-expr + mult-expr')
        @self.pg.production('add-expr : add-expr - mult-expr')
        def add_expr(state: ParserState, p):
            return BinaryOpNode(p[1].getstr(), p[0], p[2], p[0].getsourcepos())

        ##################################################
        # Shift Expression
        ##################################################
        @self.pg.production('shift-expr : add-expr')
        # @self.pg.production('shift-expr : shift-expr (<< | >>) add-expr')
        def shift_expr(state: ParserState, p):
            return p[0]

        ##################################################
        # Relation Expression
        ##################################################
        @self.pg.production('rel-expr : shift-expr')
        # @self.pg.production('rel-expr : rel-expr (< | > | <= | >=) shift-expr')
        def rel_expr(state: ParserState, p):
            return p[0]

        ##################################################
        # Equality Expression
        ##################################################
        @self.pg.production('eq-expr : rel-expr')
        def eq_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('eq-expr : eq-expr == eq-expr')
        @self.pg.production('eq-expr : eq-expr != eq-expr')
        def eq_expr_op(state: ParserState, p):
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
        # Bitwise XOR Expression
        ##################################################
        @self.pg.production('xor-expr : and-expr')
        def xor_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('xor-expr : xor-expr ^ and-expr')
        def xor_expr_op(state: ParserState, p):
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
        # Logical AND Expression
        ##################################################
        @self.pg.production('land-expr : or-expr')
        def land_expr(state: ParserState, p):
            return p[0]

        @self.pg.production('land-expr : land-expr && or-expr')
        def land_expr_op(state: ParserState, p):
            return BinaryOpNode(p[1].getstr(), p[0], p[2], p[0].getsourcepos())

        ##################################################
        # Logical OR Expression
        ##################################################
        @self.pg.production('lor-expr : land-expr')
        def lor_expr(state: ParserState, p):
            return

        @self.pg.production('lor-expr : lor-expr || land-expr')
        def lor_expr_op(state: ParserState, p):
            return BinaryOpNode(p[1].getstr(), p[0], p[2], p[0].getsourcepos())

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
        # @self.pg.production('assgn-op : <<=')
        # @self.pg.production('assgn-op : >>=')
        @self.pg.production('assgn-op : &=')
        @self.pg.production('assgn-op : ^=')
        # @self.pg.production('assgn-op : |=')
        def assgn_op(state: ParserState, p):
            return p[0].getstr()

        ##################################################
        # Expressions
        ##################################################
        @self.pg.production('expr : assgn-expr')
        # @self.pg.production('expr : expr , assgn-expr')
        def expr(state: ParserState, p):
            return p[0]
"""

lines = text.splitlines(True)
rev = []
buffer = ""
idx = 0
for line in lines:
    if line.startswith("        ##################################################"):
        idx += 1
        
    if idx == 3:        
        idx = 1
        rev.append(buffer)
        buffer = ""

    buffer += line

rev.append(buffer)

print("".join(reversed(rev)))