import random
import re
import sympy as sp


class FunctionRange:
    def __init__(self):
        self.solution_domain = r"\mathbb{R}"
        self.solution_range = None
        self.variant = None

    def generateTask(self):
        self.variant = random.choice(["absolute", "quadratic", "exponential"])
        if self.variant == "absolute":
            AbsoluteValueRange.generateTask(self)
        elif self.variant == "quadratic":
            QuadraticRange.generateTask(self)
        else:
            ExponentialRange.generateTask(self)
        return self.getSolution()

    def get_latex(self):
        if self.variant == "absolute":
            return AbsoluteValueRange.get_latex(self)
        if self.variant == "quadratic":
            return QuadraticRange.get_latex(self)
        return ExponentialRange.get_latex(self)

    def get_text(self):
        return self.get_latex()[1]

    def get_answer_fields(self):
        return [
            {"label": "ÉT:", "name": "domain"},
            {"label": "ÉK:", "name": "range"},
        ]

    def getSolution(self, debug=False):
        return self.solution_domain, self.solution_range

    def validateSolution(self, student_solution):
        values = [value.strip() for value in str(student_solution).split(",")]
        if len(values) != 2:
            return False
        return self._normalize(values[0]) == self._normalize(self.solution_domain) and (
            self._normalize(values[1]) == self._normalize(self.solution_range)
        )

    @staticmethod
    def _normalize(value):
        return re.sub(r"\s+", "", value).replace("∞", r"\infty").lower()


class AbsoluteValueRange(FunctionRange):
    def generateTask(self):
        self.coefficient = random.randint(2, 8)
        self.vertex_x = random.randint(-5, 5)
        self.vertex_y = random.randint(-5, 5)
        self.solution_range = rf"(-\infty,{self.vertex_y}]"
        return self.getSolution()

    def get_latex(self):
        if self.vertex_x < 0:
            sign = f"+{abs(self.vertex_x)}"
        elif self.vertex_x > 0:
            sign = f"-{self.vertex_x}"
        else:
            sign = ""
        return (
            "Ábrázolja az alábbi képletű függvényt és adja meg intervallumos alakban "
            "a legbővebb értelmezési tartományát és értékkészletét!",
            rf"f(x)=-{self.coefficient}\lvert x{sign}\rvert",
        )


class QuadraticRange(FunctionRange):
    def generateTask(self):
        self.root_a = random.randint(-5, 3)
        self.root_b = random.randint(self.root_a + 1, self.root_a + 7)
        self.vertex_x = sp.Rational(self.root_a + self.root_b, 2)
        self.vertex_y = -(
            self.vertex_x - self.root_a
        ) * (self.vertex_x - self.root_b)
        self.solution_range = rf"(-\infty,{sp.latex(self.vertex_y)}]"
        return self.getSolution()

    def get_latex(self):
        first = f"x-{self.root_a}" if self.root_a >= 0 else f"x+{abs(self.root_a)}"
        second = f"x-{self.root_b}" if self.root_b >= 0 else f"x+{abs(self.root_b)}"
        return (
            "Ábrázolja az alábbi képletű függvényt és adja meg intervallumos alakban "
            "a legbővebb értelmezési tartományát és értékkészletét!",
            rf"f(x)=-({first})({second})",
        )


class ExponentialRange(FunctionRange):
    def generateTask(self):
        self.coefficient = random.randint(2, 6)
        self.base = random.choice([2, 3, 5])
        self.shift = random.randint(-6, 6)
        self.solution_range = rf"({self.shift},\infty)"
        return self.getSolution()

    def get_latex(self):
        return (
            "Ábrázolja az alábbi képletű függvényt és adja meg intervallumos alakban "
            "a legbővebb értelmezési tartományát és értékkészletét!",
            rf"f(x)={self.coefficient}\cdot {self.base}^x"
            rf"{'+' if self.shift >= 0 else ''}{self.shift}",
        )
