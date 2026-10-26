import random
import sympy as sp
from sympy.parsing.sympy_parser import implicit_multiplication_application, parse_expr, standard_transformations


class LogEquation:
    def __init__(self):
        self.base = self.constant = self.coefficient = self.offset = None
        self.solution = None

    def generateTask(self):
        self.base = random.choice([2, 3, 4, 5, 10])
        self.coefficient = random.choice([2, 3, 4])
        self.offset = random.choice([-3, -2, 1, 3])
        self.constant = random.randint(2, 5)
        argument = self.base ** self.constant
        self.solution = sp.Rational(argument - self.offset, self.coefficient)
        return self.solution

    def get_latex(self):
        sign = f"+ {self.offset}" if self.offset >= 0 else f"- {abs(self.offset)}"
        return "", rf"\log_{{{self.base}}}({self.coefficient}x {sign}) = {self.constant}"

    def get_text(self):
        sign = f"+ {self.offset}" if self.offset >= 0 else f"- {abs(self.offset)}"
        return f"logaritmus alapja {self.base}, az argumentum: {self.coefficient}x {sign}, értéke {self.constant}."

    def getSolution(self, debug=False):
        return self.solution

    def get_answer_fields(self):
        return [{"label": "x =", "name": "x"}]

    def validateSolution(self, student_solution):
        try:
            value = sp.Rational(str(student_solution).replace(",", "."))
            return value == self.solution
        except (TypeError, ValueError, sp.SympifyError):
            return False
