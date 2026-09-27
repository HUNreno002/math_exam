import random
import sympy as sp

class FractionSimplification():
    def __init__(self):
        self.a = None
        self.type = None
        self.expression = None
        self.simplified_expr = None
        self.interval = (1, 10)

    def generateTask(self):
        x = sp.Symbol('x')
        self.a = random.randint(*self.interval)
        self.type = random.choice([0, 1])

        if self.type == 0:
            numerator = x**2 + self.a * x
            denominator = x**2 + 2 * self.a * x + self.a**2
        else:
            numerator = x**2 - self.a**2
            denominator = x**2 + self.a * x
            
        self.expression = numerator / denominator
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
            s = student_expr_str.replace('\cdot', '*').replace('times', '*').replace('xx', '*')
            
            parsed = parse_expr(s, transformations=transformations)
            return sp.simplify(parsed) == self.simplified_expr
        except Exception as e:
            return False

    def get_latex(self):
        instruction = "Hozza egyszerűbb alakra az alábbi kifejezést!"
        
        if self.type == 0:
            num = f"x^2 {'+' if self.a>0 else '-'} {abs(self.a)}x"
            den = f"x^2 {'+' if self.a>0 else '-'} {2*abs(self.a)}x + {self.a**2}"
        else:
            num = f"x^2 - {self.a**2}"
            den = f"x^2 {'+' if self.a>0 else '-'} {abs(self.a)}x"
            
        latex_str = rf"\frac{{{num}}}{{{den}}}"
        return instruction, latex_str