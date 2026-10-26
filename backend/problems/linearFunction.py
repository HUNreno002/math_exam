import random

import sympy as sp
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)


class LinearFunction:
    """Lineáris függvény meghatározása két adott pont alapján."""

    def __init__(self):
        self.slope = None
        self.intercept = None
        self.point_a = None
        self.point_b = None
        self.solution = None

    def generateTask(self):
        x1, x2 = random.sample(range(-9, 10), 2)
        self.slope = random.choice(
            [value for value in range(-5, 6) if value != 0]
        )
        self.intercept = random.randint(-8, 8)
        y1 = self.slope * x1 + self.intercept
        y2 = self.slope * x2 + self.intercept
        self.point_a = (x1, y1)
        self.point_b = (x2, y2)
        self.solution = self.slope * sp.Symbol("x") + self.intercept
        return self.solution

    def get_latex(self):
        instruction = (
            ""
        )
        expression = (
            rf"\text{{Egy lineáris függvény grafikonja átmegy a }}"
            rf"\left({self.point_a[0]};{self.point_a[1]}\right)"
            rf"\text{{ és }}"
            rf"\left({self.point_b[0]};{self.point_b[1]}\right)"
            rf"\text{{ pontokon. Adja meg a függvény hozzárendelési szabályát!}}"
        )
        return instruction, expression

    def get_text(self):
        return (
            "Egy lineáris függvény grafikonja átmegy a "
            f"({self.point_a[0]}; {self.point_a[1]}) és "
            f"({self.point_b[0]}; {self.point_b[1]}) pontokon. "
            "Adja meg a lineáris függvény hozzárendelési szabályát "
            "y = mx + b alakban!"
        )

    def getSolution(self, debug=False):
        return self.solution

    def get_answer_fields(self):
        return [{"label": "y =", "name": "function"}]

    def validateSolution(self, student_solution):
        try:
            expression = str(student_solution).strip()
            if "=" in expression:
                expression = expression.split("=", 1)[1]
            transformations = standard_transformations + (
                implicit_multiplication_application,
                convert_xor,
            )
            parsed = parse_expr(
                expression,
                transformations=transformations,
                local_dict={"x": sp.Symbol("x")},
            )
            return sp.simplify(parsed - self.solution) == 0
        except (TypeError, ValueError, SyntaxError, sp.SympifyError):
            return False
