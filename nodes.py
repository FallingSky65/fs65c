class Node:
    name = "Node"
    def __init__(self, _parent=None) -> None:
        self.parent = _parent

class ScopeNode (Node):
    name = "Scope Node"
    def __init__(self, _parent=None) -> None:
        super().__init__(_parent)
        self.statements = []

class ExprNode (Node):
    name = "Expression Node"
    def __init__(self, _parent=None) -> None:
        super().__init__(_parent)

class ValueNode (ExprNode):
    name = "Value Node"
    def __init__(self, _parent=None, _value="") -> None:
        super().__init__(_parent)
        self.value = _value

class IntLitNode (ValueNode):
    name = "Int Lit Node"
    def __init__(self, _parent=None, _value="") -> None:
        super().__init__(_parent, _value)

class IdentNode (ValueNode):
    name = "Identifier Node"
    def __init__(self, _parent=None, _value="") -> None:
        super().__init__(_parent, _value)

class FuncNode (ExprNode):
    name = "Func Node"
    def __init__(self, _parent=None) -> None:
        super().__init__(_parent)
        self.params = []

class ExitNode (FuncNode):
    name = "Exit Node"
    def __init__(self, _parent=None) -> None:
        super().__init__(_parent)

class LetNode (ExprNode):
    name = "Let Node"
    def __init__(self, _parent=None) -> None:
        super().__init__(_parent)
        self.ident : IdentNode = IdentNode()
        self.expr : ExprNode = ExprNode()

class AddNode (FuncNode):
    name = "Add Node"
    def __init__(self, _parent=None) -> None:
        super().__init__(_parent)

class SubNode (FuncNode):
    name = "Sub Node"
    def __init__(self, _parent=None) -> None:
        super().__init__(_parent)
