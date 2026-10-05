import random
import sympy as sp


class RadicalRationalization():
    def __init__(self):
        self.type = None
        self.expression = None
        self.simplified_expr = None
        self.original_latex = None

    def generateTask(self):
        x = sp.Symbol('x')
        self.type = random.choice([0, 1, 2, 3])

        if self.type == 0:
            first_radical = random.choice([2, 3, 5, 6, 7, 13])
            second_radical = random.choice([2, 3, 5, 7, 11, 17])
            while second_radical == first_radical:
                second_radical = random.choice([2, 3, 5, 7, 11, 17])
            coefficient = random.choice([1, 2, 4, 5])
            numerator = random.choice([-1, 1])
            denominator = sp.sqrt(first_radical) + coefficient * sp.sqrt(second_radical)
        elif self.type == 1:
            first_radical = random.choice([2, 3, 5, 7, 13])
            second_radical = random.choice([2, 3, 5, 7, 11, 17])
            while second_radical == first_radical:
                second_radical = random.choice([2, 3, 5, 7, 11, 17])
            coefficient = random.choice([-5, -4, -2, 2, 4, 5])
            numerator = random.choice([-60, -52, -40, -25])
            denominator = coefficient * sp.sqrt(first_radical) + sp.sqrt(second_radical)
        elif self.type == 2:
            radicand_coefficient = random.choice([3, 5, 6])
            radicand_constant = random.randint(-8, 8)
            constant = random.choice([-9, -4, -2, 2, 4, 9])
            numerator = random.choice([-2, 1, 2, 6])
            denominator = sp.sqrt(radicand_coefficient * x + radicand_constant) + constant
        else:
            first_radicand = random.choice([3, 5, 6, 7]) * x + random.randint(-8, 2)
            second_radicand = random.choice([3, 5, 6, 7]) * x + random.randint(-2, 8)
            numerator = random.choice([-52, -12, 6, 10])
            denominator = sp.sqrt(first_radicand) - sp.sqrt(second_radicand)

        self.expression = numerator / denominator
        self.simplified_expr = sp.radsimp(self.expression)
        self.original_latex = sp.latex(self.expression)
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
                .replace('×', '*')
                .replace('\\sqrt', 'sqrt')
            )
            parsed = parse_expr(
                expression_text,
                transformations=transformations,
                evaluate=False,
                local_dict={'x': sp.Symbol('x'), 'sqrt': sp.sqrt},
            )

            if sp.simplify(parsed - self.simplified_expr) != 0:
                return False

            denominator = sp.denom(sp.together(parsed))
            return not any(
                power.exp.is_Rational and power.exp.q != 1
                for power in denominator.atoms(sp.Pow)
            )
        except (TypeError, ValueError, SyntaxError):
            return False

    def get_latex(self):
        instruction = "Egyszerűsítse az alábbi kifejezést a nevező gyöktelenítésével!"
        return instruction, self.original_latex
