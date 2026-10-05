import random
import sympy as sp


class PowerSimplification():
    def __init__(self):
        self.type = None
        self.expression = None
        self.simplified_expr = None
        self.original_latex = None

    def generateTask(self):
        x = sp.Symbol('x')
        self.type = random.choice([0, 1, 2, 3])

        if self.type == 0:
            numerator_root = random.choice([3, 5, 6])
            numerator_power = random.randint(-6, -2)
            denominator_root = random.choice([3, 4, 6])
            inner_power = random.randint(-5, -1)
            inner_root = random.choice([2, 3, 5])
            numerator_exponent = sp.Rational(numerator_power, numerator_root)
            denominator_exponent = sp.Rational(
                inner_power + sp.Rational(1, inner_root), denominator_root
            )
            self.simplified_expr = x ** (numerator_exponent - denominator_exponent)
            self.original_latex = (
                rf"\frac{{\sqrt[{numerator_root}]{{x^{{{numerator_power}}}}}}}"
                rf"{{\sqrt[{denominator_root}]{{x^{{{inner_power}}} \cdot "
                rf"\sqrt[{inner_root}]{{x}}}}}}"
            )
        elif self.type == 1:
            outer_root = random.choice([3, 5, 6])
            inner_power = random.randint(-5, -1)
            inner_root = random.choice([2, 3, 4])
            denominator_root = random.choice([3, 4, 6])
            denominator_power = random.randint(2, 6)
            numerator_exponent = sp.Rational(
                inner_power + sp.Rational(1, inner_root), outer_root
            )
            denominator_exponent = sp.Rational(denominator_power, denominator_root)
            self.simplified_expr = x ** (numerator_exponent - denominator_exponent)
            self.original_latex = (
                rf"\frac{{\sqrt[{outer_root}]{{x^{{{inner_power}}} \cdot "
                rf"\sqrt[{inner_root}]{{x}}}}}}"
                rf"{{\left(\sqrt[{denominator_root}]{{x}}\right)^{{{denominator_power}}}}}"
            )
        elif self.type == 2:
            base_power = random.randint(-4, -2)
            outer_power = random.randint(2, 9)
            root_index = random.choice([3, 4, 5, 6])
            denominator_power = random.randint(1, 5)
            self.simplified_expr = x ** (
                base_power * outer_power
                + sp.Rational(1, root_index)
                - denominator_power
            )
            self.original_latex = (
                rf"\frac{{\left(x^{{{base_power}}}\right)^{{{outer_power}}}"
                rf" \cdot \sqrt[{root_index}]{{x}}}}{{x^{{{denominator_power}}}}}"
            )
        else:
            base_power = random.randint(2, 6)
            outer_power = random.randint(2, 6)
            root_index = random.choice([3, 4, 5, 6])
            numerator_power = random.randint(1, 5)
            self.simplified_expr = x ** (
                base_power * outer_power
                + numerator_power
                - sp.Rational(1, root_index)
            )
            self.original_latex = (
                rf"\frac{{\left(x^{{{base_power}}}\right)^{{{outer_power}}}"
                rf" \cdot x^{{{numerator_power}}}}}"
                rf"{{\sqrt[{root_index}]{{x}}}}"
            )

        self.expression = self.simplified_expr
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
                .replace('\\sqrt', 'sqrt')
                .replace('×', '*')
            )
            parsed = parse_expr(
                expression_text,
                transformations=transformations,
                evaluate=False,
                local_dict={'x': sp.Symbol('x'), 'sqrt': sp.sqrt},
            )
            x = sp.Symbol('x')

            if not parsed.is_Pow or parsed.base != x:
                return False
            return sp.simplify(parsed - self.simplified_expr) == 0
        except (TypeError, ValueError, SyntaxError):
            return False

    def get_latex(self):
        instruction = "Végezze el az alábbi műveletet, és írja fel x tört kitevőjű hatványaként!"
        return instruction, self.original_latex
