import random
import sympy as sp


class ExponentialEquation:
    def __init__(self):
        self.base = self.coefficient = self.x_coefficient = self.shift = None
        self.solution = None

    def generateTask(self):
        self.base = random.choice([2, 3, 4, 5])
        self.coefficient = random.choice([1, 2, 3])
        self.x_coefficient = random.randint(1, 3)
        self.shift = random.choice([value for value in range(-5, 4) if value != 0])
        x = random.randint(-4, 6)
        self.solution = sp.Integer(x)
        exponent = self.x_coefficient * x + self.shift
        power = (
            sp.Integer(self.base) ** exponent
            if exponent >= 0
            else sp.Rational(1, self.base ** abs(exponent))
        )
        self.target = self.coefficient * power
        return self.solution

    def get_latex(self):
        coefficient = "" if self.coefficient == 1 else f"{self.coefficient}\\cdot "
        x_term = "x" if self.x_coefficient == 1 else f"{self.x_coefficient}x"
        shift = f"+{self.shift}" if self.shift > 0 else str(self.shift)
        return "", rf"{coefficient}{self.base}^{{{x_term}{shift}}} = {sp.latex(self.target)}"

    def get_text(self):
        coefficient = "" if self.coefficient == 1 else f"{self.coefficient}·"
        x_term = "x" if self.x_coefficient == 1 else f"{self.x_coefficient}x"
        shift = f"+{self.shift}" if self.shift > 0 else str(self.shift)
        return f"{coefficient}{self.base}^({x_term}{shift}) = {self.target}"

    def getSolution(self, debug=False):
        return self.solution

    def get_answer_fields(self):
        return [{"label": "x =", "name": "x"}]

    def validateSolution(self, student_solution):
        try:
            return sp.Rational(str(student_solution).replace(",", ".")) == self.solution
        except (TypeError, ValueError, sp.SympifyError):
            return False
