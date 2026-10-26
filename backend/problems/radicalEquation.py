import random
import sympy as sp


class RadicalEquation:
    def __init__(self):
        self.first = self.second = self.constant = None
        self.solution = None

    def generateTask(self):
        self.first = random.choice([-1, 1, 2])
        self.second = random.choice([-3, -2, 1, 2])
        self.constant = random.choice([1, 2, 3])
        x = sp.Symbol("x")
        equation = (self.first * x + self.second) * (x + self.second) - self.constant**2
        candidates = sp.solve(equation, x)
        valid = [
            value for value in candidates
            if value.is_real and self.first * value + self.second >= 0 and value + self.second >= 0
        ]
        if not valid:
            return self.generateTask()
        self.solution = valid[0]
        return self.solution

    def get_latex(self):
        first = f"{self.first}x" if self.first != 1 else "x"
        return "", rf"\sqrt{{{first}{self.second:+d}}}\cdot\sqrt{{x{self.second:+d}}} = {self.constant}"

    def get_text(self):
        return f"√({self.first}x {self.second:+d}) · √(x {self.second:+d}) = {self.constant}"

    def getSolution(self, debug=False):
        return self.solution

    def get_answer_fields(self):
        return [{"label": "x =", "name": "x"}]

    def validateSolution(self, student_solution):
        try:
            value = sp.sympify(str(student_solution).replace(",", ".").replace("^", "**"))
            return sp.simplify(value - self.solution) == 0
        except (TypeError, ValueError, sp.SympifyError):
            return False
