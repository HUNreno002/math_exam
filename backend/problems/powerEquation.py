import random
import sympy as sp
from sympy.parsing.sympy_parser import convert_xor, parse_expr, standard_transformations


class PowerEquation:
    def __init__(self):
        self.a = self.solution = None
        self.left = self.right = None

    def generateTask(self):
        self.a = random.choice([2, 3, 5, 6, 8])
        x = random.randint(-5, 8)
        p, q = random.randint(1, 10), random.randint(-8, 4)
        self.left = (p, q)
        self.right = p * x + q
        self.solution = sp.Integer(x)
        return self.solution

    def get_latex(self):
        sign = f"+{self.left[1]}" if self.left[1] >= 0 else str(self.left[1])
        return "", rf"{self.a}^{{{self.left[0]}x{sign}}} = {self.a}^{{{self.right}}}"

    def get_text(self):
        return (
            f"{self.a} a {self.left[0]}x {self.left[1]:+d} kitevőn egyenlő "
            f"{self.a} a {self.right}. kitevőn."
        )

    def getSolution(self, debug=False):
        return self.solution

    def get_answer_fields(self):
        return [{"label": "x =", "name": "x"}]

    def validateSolution(self, student_solution):
        try:
            answer = str(student_solution).replace(",", ".").replace("^", "**")
            return sp.simplify(sp.sympify(answer) - self.solution) == 0
        except (TypeError, ValueError, sp.SympifyError):
            return False


class _ParsedEquation(PowerEquation):
    def _parse(self, value):
        transformations = standard_transformations + (convert_xor,)
        return parse_expr(
            str(value).replace(",", "."),
            transformations=transformations,
            local_dict={"x": sp.Symbol("x")},
        )
