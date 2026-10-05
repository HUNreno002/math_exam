import random
import sympy as sp

class FractionSimplification():
    def __init__(self):
        self.type = None
        self.expression = None
        self.numerator = None
        self.denominator = None
        self.simplified_expr = None
        self.interval = (1, 10)

    def generateTask(self):
        x = sp.Symbol('x')
        self.type = random.choice([0, 1, 2, 3])
        scale = random.randint(2, 5)

        if self.type in (0, 1):
            cancel_root = random.randint(-9, 9)
            first_root = random.randint(-9, 9)
            while first_root == cancel_root:
                first_root = random.randint(-9, 9)

            right_offset = random.randint(1, 9)
            self.numerator = (x - first_root) * (x - cancel_root)
            self.denominator = scale * (x - cancel_root) * (x + right_offset)
        elif self.type == 2:
            value = random.randint(1, 9)
            self.numerator = (x - value) * (x + value)
            self.denominator = scale * x * (x + value)
        else:
            value = random.randint(1, 9)
            self.numerator = (x + value) ** 2
            self.denominator = scale * x * (x + value)

        self.expression = self.numerator / self.denominator
        self.simplified_expr = sp.simplify(self.expression)
        return self.expression, self.simplified_expr
    
    def displayTask(self):
        pass

    def getSolution(self, debug=False):
        return self.simplified_expr
    
    def validateSolution(self, student_expr_str):
        try:
            # Asciimath feldolgozás: implicit szorzás és hatványozás konverzió (pl. x^2 -> x**2, 2x -> 2*x)
            from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
            transformations = (standard_transformations + (implicit_multiplication_application,) + (convert_xor,))
            
            # Kicseréljük az asciimath specifikus maradék karaktereket, ha lennének
            s = student_expr_str.replace('\\cdot', '*').replace('times', '*').replace('xx', '*')
            
            parsed = parse_expr(s, transformations=transformations, evaluate=False)
            if sp.simplify(parsed - self.simplified_expr) != 0:
                return False

            # Az eredeti tört vagy bármely más, még le nem egyszerűsített alak
            # nem fogadható el, ha a számláló és a nevező nem konstans tényezőt oszt.
            parsed_numerator, parsed_denominator = sp.fraction(parsed)
            parsed_numerator = sp.expand(parsed_numerator)
            parsed_denominator = sp.expand(parsed_denominator)
            common_factor = sp.gcd(parsed_numerator, parsed_denominator)
            return sp.degree(common_factor, gen=sp.Symbol('x')) == 0
        except Exception as e:
            return False

    def get_latex(self):
        instruction = "Hozza egyszerűbb alakra az alábbi kifejezést!"
        num = sp.latex(sp.expand(self.numerator))
        den = sp.latex(sp.expand(self.denominator))
        latex_str = rf"\frac{{{num}}}{{{den}}}"
        return instruction, latex_str