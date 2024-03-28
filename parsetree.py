from tokenizer import Token
from tokens import Tokens
from errors import handleError
from nodes import *

class Parser:
    def __init__(self, _tokens, begin=0) -> None:
        self.tokens = _tokens
        self.index = begin
        self.rootNode = None

    def parseIntLit(self, parent) -> IntLitNode:
        if self.peek() is not None and self.peek().ttype == Tokens.INT_LIT:
            intLitNode = IntLitNode(_parent=parent, _value=self.peek().tval)
            self.consume()
            return intLitNode
        handleError(8)
        return IntLitNode()

    def parseIdent(self, parent) -> IdentNode:
        if self.peek() is not None and self.peek().ttype == Tokens.IDENT:
            identNode = IdentNode(_parent=parent, _value=self.peek().tval)
            self.consume()
            return identNode
        handleError(8)
        return IdentNode()

    def parseExit(self, parent) -> ExitNode:
        self.consume()
        if self.peek() is None:
            handleError(8)

        exitNode = ExitNode(parent)

        if self.peek().ttype == Tokens.OPENPAREN:
            self.consume()
            exitNode.params.append(self.parseExpr(exitNode))
            if self.peek() is None or self.peek().ttype != Tokens.CLOSEPAREN:
                handleError(8)
            self.consume()
        else:
            exitNode.params.append(self.parseExpr(exitNode))

        if self.peek() is None or self.peek().ttype != Tokens.SEMI:
            handleError(9)
        self.consume()

        return exitNode

    def parseLet(self, parent) -> LetNode:
        letNode = LetNode(parent)
        self.consume()
        if self.peek() is None or self.peek().ttype != Tokens.IDENT:
            handleError(8)
        letNode.ident = self.parseIdent(letNode)
        if self.peek() is None or self.peek().ttype != Tokens.EQ:
            handleError(8)
        self.consume()
        letNode.expr = self.parseExpr(letNode)
        if self.peek() is None or self.peek().ttype != Tokens.SEMI:
            handleError(9)
        self.consume()
        return letNode

    def parseAdd(self, parent) -> AddNode:
        self.consume()
        addNode = AddNode(parent)
        if self.peek() is None or self.peek().ttype != Tokens.OPENPAREN:
            handleError(8)
        self.consume()
        addNode.params.append(self.parseExpr(addNode))
        if self.peek() is None or self.peek().ttype != Tokens.COMMA:
            handleError(8)
        self.consume()
        addNode.params.append(self.parseExpr(addNode))
        if self.peek() is None or self.peek().ttype != Tokens.CLOSEPAREN:
            handleError(8)
        self.consume()

        return addNode

    def parseSub(self, parent) -> SubNode:
        self.consume()
        subNode = SubNode(parent)
        if self.peek() is None or self.peek().ttype != Tokens.OPENPAREN:
            handleError(8)
        self.consume()
        subNode.params.append(self.parseExpr(subNode))
        if self.peek() is None or self.peek().ttype != Tokens.COMMA:
            handleError(8)
        self.consume()
        subNode.params.append(self.parseExpr(subNode))
        if self.peek() is None or self.peek().ttype != Tokens.CLOSEPAREN:
            handleError(8)
        self.consume()

        return subNode

    def parseExpr(self, parent) -> ExprNode:
        if self.peek() is not None:
            if self.peek().ttype == Tokens.INT_LIT:
                return self.parseIntLit(parent)
            elif self.peek().ttype == Tokens.IDENT:
                return self.parseIdent(parent)
            elif self.peek().ttype == Tokens.EXIT:
                return self.parseExit(parent)
            elif self.peek().ttype == Tokens.LET:
                return self.parseLet(parent)
            elif self.peek().ttype == Tokens.ADD:
                return self.parseAdd(parent)
            elif self.peek().ttype == Tokens.SUB:
                return self.parseSub(parent)
            else:
                handleError(8)
                return ExprNode()
        else:
            handleError(8)
            return ExprNode()

    def parseScope(self, parent) -> ScopeNode:
        scopeNode = ScopeNode(parent)
        while self.peek() is not None:
            scopeNode.statements.append(self.parseExpr(scopeNode))
        return scopeNode

    def parse(self):
        self.rootNode = self.parseScope(None)
        return self.rootNode

    def printTreeFromNode(self, node, depth):
        if node is None:
            return
        for i in range(depth):
            print("\t",end="")
        if isinstance(node, LetNode):
            print(f"{node.name}")
            self.printTreeFromNode(node.ident, depth+1)
            self.printTreeFromNode(node.expr, depth+1)
        elif isinstance(node, ValueNode):
            print(f"{node.name} : {node.value}")
        elif isinstance(node, FuncNode):
            print(f"{node.name}")
            for param in node.params:
                self.printTreeFromNode(param, depth+1)
        elif isinstance(node, ScopeNode):
            print(f"{node.name}")
            for statement in node.statements:
                self.printTreeFromNode(statement, depth+1)
        else:
            print(f"{node.name}")

    def printTree(self):
        self.printTreeFromNode(self.rootNode, 0)

    def peek(self, ahead=1) -> Token | None:
        if self.index + ahead - 1 >= len(self.tokens):
            return None
        return self.tokens[self.index + ahead - 1]

    def consume(self) -> Token:
        self.index += 1
        return self.tokens[self.index-1]
