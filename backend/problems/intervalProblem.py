import random
import sympy as sp
import re

class IntervalProblem():
    def __init__(self):
        self.type = None
        self.equation_str = ""
        self.prompt_str = ""
        self.solution_set = None
        self.expr = None
        self.a = self.b = self.c_val = self.k = None

    def generateTask(self):
        x = sp.Symbol('x')
        while True:
            try:
                self.type = random.choice([0, 1, 2, 3, 4, 5])
                if self.type == 0: # Logaritmusos, masodfoku
                    r1, r2 = random.randint(-5, 0), random.randint(1, 5)
                    a = random.choice([-2, -1, 1, 2])
                    self.k = random.randint(2, 9)
                    self.expr = a*x**2 + (-a*(r1+r2))*x + (a*r1*r2)
                    self.prompt_str = "Adja meg a függvény legbővebb értelmezési tartományát!"
                    self.solution_set = sp.solveset(self.expr > 0, x, domain=sp.S.Reals)
                elif self.type == 1: # Gyokos, masodfoku
                    r1, r2 = random.randint(-5, 0), random.randint(1, 5)
                    a = random.choice([-2, -1, 1, 2])
                    self.expr = a*x**2 + (-a*(r1+r2))*x + (a*r1*r2)
                    self.prompt_str = "Adja meg a függvény legbővebb értelmezési tartományát!"
                    self.solution_set = sp.solveset(self.expr >= 0, x, domain=sp.S.Reals)
                elif self.type == 2: # Logaritmusos, elsofoku
                    a = random.choice([-5, -4, -3, 3, 4, 5])
                    b = random.randint(-9, 9)
                    self.k = random.randint(2, 9)
                    self.expr = a*x + b
                    self.prompt_str = "Adja meg a függvény legbővebb értelmezési tartományát!"
                    self.solution_set = sp.solveset(self.expr > 0, x, domain=sp.S.Reals)
                elif self.type == 3: # Gyokos, elsofoku
                    a = random.choice([-5, -4, -3, 3, 4, 5])
                    b = random.randint(-9, 9)
                    self.expr = a*x + b
                    self.prompt_str = "Adja meg a függvény legbővebb értelmezési tartományát!"
                    self.solution_set = sp.solveset(self.expr >= 0, x, domain=sp.S.Reals)
                elif self.type == 4: # Tört egyenlotlenseg
                    numerator = random.choice([-5, -4, -3, 3, 4, 5])
                    denominator_root = random.randint(-9, 9)
                    self.expr = sp.Rational(numerator, 1) / (x - denominator_root)
                    self.prompt_str = "Oldja meg az egyenlőtlenséget a valós számok halmazán!"
                    self.solution_set = sp.solveset(self.expr >= 0, x, domain=sp.S.Reals)
                else: # Abszolútérték
                    self.a, self.b = random.randint(1, 5), random.randint(-5, 5)
                    self.c_val = random.randint(1, 5)
                    self.prompt_str = "Oldja meg az egyenlőtlenséget a valós számok halmazán!"
                    rhs = -self.c_val
                    if rhs <= 0:
                        self.solution_set = sp.S.Reals
                    else:
                        v1 = sp.Rational(-rhs - self.b, self.a)
                        v2 = sp.Rational(rhs - self.b, self.a)
                        lower, upper = min(v1, v2), max(v1, v2)
                        self.solution_set = sp.Union(sp.Interval(-sp.oo, lower), sp.Interval(upper, sp.oo))
                
                if self.solution_set is not None and self.solution_set != sp.S.EmptySet:
                    break
            except:
                continue

    def get_latex(self):
        x = sp.Symbol('x')
        if self.type == 0:
            latex_expr = rf"f(x) = \log_{{{self.k}}}\left( {sp.latex(self.expr)} \right)"
        elif self.type in (1, 3):
            latex_expr = rf"f(x) = \sqrt{{ {sp.latex(self.expr)} }}"
        elif self.type == 2:
            latex_expr = rf"f(x) = \log_{{{self.k}}}\left( {sp.latex(self.expr)} \right)"
        elif self.type == 4:
            latex_expr = rf"\frac{{{sp.latex(self.expr.as_numer_denom()[0])}}}{{{sp.latex(self.expr.as_numer_denom()[1])}}} \geq 0"
        else:
            inner = self.a * x + self.b
            sign = "+" if self.c_val >= 0 else "-"
            latex_expr = rf"\left| {sp.latex(inner)} \right| {sign} {abs(self.c_val)} \geq 0"
        return self.prompt_str, latex_expr

    def format_solution(self):
        """Átalakítja a SymPy halmazt a kért (-inf, 3] U [4, inf) alakra."""
        s = self.solution_set
        if s == sp.S.Reals:
            return "R (vagy (-inf, inf))"
        if s == sp.S.EmptySet:
            return "ures"
        
        def _format_single_interval(interval):
            left = "(" if interval.left_open else "["
            right = ")" if interval.right_open else "]"
            # Végtelenek cseréje: oo -> inf
            start = str(interval.start).replace("oo", "inf").replace("-oo", "-inf")
            end = str(interval.end).replace("oo", "inf").replace("-oo", "-inf")
            return f"{left}{start}, {end}{right}"

        if isinstance(s, sp.Union):
            return " U ".join([_format_single_interval(arg) for arg in s.args])
        if isinstance(s, sp.Interval):
            return _format_single_interval(s)
        return str(s)

    def getSolution(self):
        return self.solution_set

    def _parse_interval_str(self, s):
        # MathLive ASCII math, vagy sima text: "oo" / "inf" konverzió
        s = s.replace(" ", "").replace("inf", "oo").replace("\u221e", "oo")
        s = s.replace("uu", "U").replace("\cup", "U").replace("∪", "U") 
        if s.lower() in ["r", "reals", "(-oo,oo)", "rr", "bbbr", "mathbb{r}"]: return sp.S.Reals
        if s.lower() in ["empty", "ures", "{}"]: return sp.S.EmptySet
        try:
            parts = s.split('U')
            sets = []
            for p in parts:
                match = re.match(r'([\[\(])([^,]+),([^\]\)]+)([\]\)])', p)
                if match:
                    lb, lv, rv, rb = match.groups()
                    sets.append(sp.Interval(sp.sympify(lv), sp.sympify(rv), lb == '(', rb == ')'))
                else: 
                    return None
            res = sets[0]
            for s_ in sets[1:]: res = sp.Union(res, s_)
            return res
        except: return None

    def validateSolution(self, student_expr_str):
        try:
            student_set = self._parse_interval_str(student_expr_str)
            return sp.simplify(student_set) == sp.simplify(self.solution_set)
        except: return False