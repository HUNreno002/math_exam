import random
import sympy as sp


class FractionCombination():
    def __init__(self):
        self.type = None
        self.expression = None
        self.term1 = None
        self.term2 = None
        self.simplified_expr = None

    def generateTask(self):
        x, y = sp.symbols('x y')
        self.type = random.choice([0, 1, 2, 3])

        if self.type == 0:
            first_denominator = x - random.randint(1, 9)
            second_denominator = x + random.randint(1, 9)
            self.term1 = (random.randint(2, 8) * x + random.randint(-8, 8)) / first_denominator
            self.term2 = -(random.randint(1, 8) * x + random.randint(-8, 8)) / second_denominator
        elif self.type == 1:
            first_denominator = x + random.randint(1, 9)
            second_denominator = x - random.randint(1, 9)
            self.term1 = (random.randint(2, 8) * x + random.randint(-8, 8)) / first_denominator
            self.term2 = (random.randint(1, 8) * x + random.randint(-8, 8)) / second_denominator
        elif self.type == 2:
            x_coefficient = random.randint(3, 9)
            y_coefficient = random.randint(2, 8)
            multiplier = random.randint(2, 6)
            self.term1 = 1 / (x_coefficient * x + y_coefficient * y)
            self.term2 = -multiplier / (x_coefficient * x - y_coefficient * y)
        else:
            x_coefficient = random.randint(3, 9)
            y_coefficient = random.randint(2, 8)
            multiplier = random.randint(2, 6)
            self.term1 = 1 / (x_coefficient * x - y_coefficient * y)
            self.term2 = -multiplier / (x_coefficient * x + y_coefficient * y)

        self.expression = self.term1 + self.term2
        self.simplified_expr = sp.factor(self.expression)
        return self.expression, self.simplified_expr

    def displayTask(self):
        pass

    def getSolution(self, debug=False):
        return self.simplified_expr

    def validateSolution(self, student_expr_str):
        try:
            from sympy.parsing.sympy_parser import (
                convert_xor,
                implicit_multiplication_application,
                parse_expr,
                standard_transformations,
            )

            transformations = standard_transformations + (
                implicit_multiplication_application,
                convert_xor,
            )
            expression_text = (
                student_expr_str.replace('\\cdot', '*')
                .replace('\\times', '*')
                .replace('\\ast', '*')
                .replace('×', '*')
                .replace('times', '*')
                .replace('xx', '*')
            )
            parsed = parse_expr(
                expression_text,
                transformations=transformations,
                evaluate=False,
            )

            if sp.simplify(parsed - self.simplified_expr) != 0:
                return False

            terms = sp.Add.make_args(parsed)
            fraction_term_count = sum(
                sp.fraction(sp.together(term))[1] != 1
                for term in terms
            )
            return fraction_term_count <= 1
        except (TypeError, ValueError, SyntaxError):
            return False

    def get_latex(self):
        instruction = "Végezze el az alábbi műveletet a tört kifejezések összevonásával!"
        if self.term2.could_extract_minus_sign():
            operator = "-"
            second_term = -self.term2
        else:
            operator = "+"
            second_term = self.term2
        latex_str = f"{sp.latex(self.term1)} {operator} {sp.latex(second_term)}"
        return instruction, latex_str
