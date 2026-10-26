import random


import random


class RadicalFractionEquation:
    def __init__(self):
        self.has_solution = False
        self.solution = None
        self.variant = None
        self.numerator_constant = None
        self.numerator_coefficient = None
        self.denominator_coefficient = None
        self.denominator_constant = None
        self.right_side = None

    def generateTask(self):
        self.has_solution = False
        self.variant = random.choice([59, 60])
        self.numerator_constant = random.randint(3, 12)
        self.numerator_coefficient = random.randint(2, 9)
        self.denominator_coefficient = random.randint(2, 9)
        self.denominator_constant = random.randint(2, 12)
        self.right_side = random.randint(2, 8)
        return self.solution

    def get_latex(self):
        if self.variant == 59:
            return "", (
                rf"\frac{{\sqrt{{-{self.numerator_coefficient}x-"
                rf"{self.numerator_constant}}}}}"
                rf"{{\sqrt{{{self.denominator_coefficient}x-"
                rf"{self.denominator_constant}}}}} = {self.right_side}"
            )
        return "", (
            rf"\frac{{\sqrt{{{self.numerator_constant}-"
            rf"{self.numerator_coefficient}x}}}}"
            rf"{{\sqrt{{{self.denominator_coefficient}x-"
            rf"{self.denominator_constant}}}}} = {self.right_side}"
        )

    def get_text(self):
        if self.variant == 59:
            return (
                f"√(-{self.numerator_coefficient}x - {self.numerator_constant}) / "
                f"√({self.denominator_coefficient}x - {self.denominator_constant}) "
                f"= {self.right_side}"
            )
        return (
            f"√({self.numerator_constant} - {self.numerator_coefficient}x) / "
            f"√({self.denominator_coefficient}x - {self.denominator_constant}) "
            f"= {self.right_side}"
        )

    def getSolution(self, debug=False):
        return None

    def get_answer_fields(self):
        return [{"label": "x =", "name": "x"}]

    def validateSolution(self, student_solution):
        normalized = str(student_solution).strip().lower().replace(" ", "")
        return normalized in {"∅", "üres", "ures", "nincsmegoldás", "nincsmegoldas"}
