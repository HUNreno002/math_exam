import numpy as np
from utils.random_utils import random_not_zero_or_one

class LinearEquationComplex():
    """
    Komplex, egyváltozós lineáris egyenletek generátora.
    Pl: 6 + 3·(-(x/7) - 8) = 4 - 4x
    vagy: 2x + 5 = 3x - 7
    """
    def __init__(self):
        self.solution = None
        self.interval = (-5, 5)
        self.equation = None
        
    def generateTask(self, complexity='simple'):
        """
        Feladat generálása.
        complexity: 'simple' vagy 'complex'
            - simple: ax + b = cx + d
            - complex: a + b·(-x/c - d) = e - fx
        """
        self.solution = random_not_zero_or_one(*self.interval)
        
        if complexity == 'simple':
            self._generateSimpleEquation()
        else:
            self._generateComplexEquation()
    
    def _generateSimpleEquation(self):
        """
        Egyszerű lineáris egyenlet: ax + b = cx + d
        """
        a = random_not_zero_or_one(*self.interval)
        c = random_not_zero_or_one(*self.interval)
        while c == a:
            c = random_not_zero_or_one(*self.interval)
        
        b = random_not_zero_or_one(*self.interval)
        d = random_not_zero_or_one(*self.interval)
        
        # Bal oldal értéke
        left_value = a * self.solution + b
        # Jobb oldal: cx + d, ezért d = left_value - c*solution
        d = left_value - c * self.solution
        
        self.equation = {
            'type': 'simple',
            'left': {'a': a, 'b': b},
            'right': {'c': c, 'd': d},
            'solution': self.solution
        }
    
    def _generateComplexEquation(self):
        """
        Összetett egyenlet: constant + coeff·(-x/divisor - inner_constant) = right_const - right_a·x
        Az összes szám szép (egész) marad.
        """
        # Összes szám egész típushatásként
        const = random_not_zero_or_one(*self.interval)
        coeff = random_not_zero_or_one(*self.interval)
        divisor = random_not_zero_or_one(*self.interval)
        inner_const = random_not_zero_or_one(*self.interval)
        right_a = random_not_zero_or_one(*self.interval)
        
        # A megoldást úgy választjuk, hogy x/divisor egész szám legyen
        self.solution = self.solution * abs(divisor)
        
        # Számítások egészként (nincs lebegőpontos)
        # left_value = const + coeff * (-x/divisor - inner_const)
        x_div_d = self.solution // divisor
        
        # Erős int konverziók a közbenső értékekhez
        left_value = (const + coeff * (-x_div_d - inner_const))
        
        # A jobb oldal konstansa (right_const - right_a * x = left_value)
        right_const_value = left_value + right_a * self.solution
        
        # Explicit float-to-int konverziók az adatstruktúrában
        self.equation = {
            'type': 'complex',
            'left': {
                'const': int(const),
                'coeff': int(coeff),
                'divisor': int(divisor),
                'inner_const': int(inner_const)
            },
            'right': {
                'const': int(right_const_value),  # Erős int konverzió
                'a': int(right_a)
            },
            'solution': int(self.solution)
        }
    
    def displayTask(self):
        """Az egyenletet olvasható formában megjeleníti."""
        if self.equation['type'] == 'simple':
            self._displaySimpleEquation()
        else:
            self._displayComplexEquation()
    
    def _displaySimpleEquation(self):
        """Egyszerű egyenlet megjelenítése."""
        left = self.equation['left']
        right = self.equation['right']
        
        a, b = int(left['a']), int(left['b'])
        c, d = int(right['c']), int(right['d'])
        
        # Bal oldal
        if b >= 0:
            left_str = f"{a}x + {b}"
        else:
            left_str = f"{a}x - {abs(b)}"
        
        # Jobb oldal
        if c >= 0:
            right_first = f"{c}x"
        else:
            right_first = f"{c}x"
        
        if d >= 0:
            right_str = f"{right_first} + {d}"
        else:
            right_str = f"{right_first} - {abs(d)}"
        
        print("Oldd meg az alábbi egyenletet:")
        print(f"{left_str} = {right_str}")
        print()
    
    def _displayComplexEquation(self):
        """Összetett egyenlet megjelenítése."""
        left = self.equation['left']
        right = self.equation['right']
        
        # Explicit int konverziók biztosítása
        const = int(round(left['const']))
        coeff = int(round(left['coeff']))
        divisor = int(round(left['divisor']))
        inner_const = int(round(left['inner_const']))
        right_const = int(round(right['const']))
        right_a = int(round(right['a']))
        
        # Bal oldal formázása
        if coeff >= 0:
            coeff_str = str(coeff)
        else:
            coeff_str = f"({coeff})"
        
        if inner_const >= 0:
            left_str = f"{const} + {coeff_str}·(-x/{divisor} - {inner_const})"
        else:
            left_str = f"{const} + {coeff_str}·(-x/{divisor} + {abs(inner_const)})"
        
        # Jobb oldal formázása
        if right_a >= 0:
            right_str = f"{right_const} - {right_a}x"
        else:
            right_str = f"{right_const} + {abs(right_a)}x"
        
        print("Oldd meg az alábbi egyenletet:")
        print(f"{left_str} = {right_str}")
        print()
    
    def getSolution(self, debug=False):
        """Az egyenlet megoldása."""
        if debug:
            print(f"Megoldás: x = {self.solution}")
        return self.solution
    
    def validateSolution(self, student_solution):
        """A diák megoldásának validálása."""
        try:
            import re
            # A student_solution string lehet, pl. "x=3" vagy "3"
            solution_str = str(student_solution).replace(" ", "")
            
            # Regex: keressük a végét, vagy az x= utáni részt
            match = re.search(r'(-?\d+(?:\.\d+)?)', solution_str)
            if not match:
                return False
            student_x = float(match.group(1))
        except (ValueError, TypeError):
            return False
        
        tolerance = 1e-6
        return abs(student_x - self.solution) < tolerance
    
    def validateSolutionInteractive(self):
        """Interaktív validálás."""
        try:
            student_x = float(input("x = "))
        except ValueError:
            print("-------")
            print("Érvénytelen bemenet!")
            print("-------")
            return False
        
        result = self.validateSolution(student_x)
        
        if result:
            print("-------")
            print("Helyes!")
            print("-------")
            return True
        else:
            print("-------")
            print("Helytelen!")
            print(f"Helyes megoldás: x = {self.solution}")
            print("-------")
            return False
    
    def checkEquation(self):
        """Az egyenlet helyességének ellenőrzése."""
        solution = self.solution
        
        if self.equation['type'] == 'simple':
            left = self.equation['left']
            right = self.equation['right']
            
            left_value = left['a'] * solution + left['b']
            right_value = right['c'] * solution + right['d']
        else:
            left = self.equation['left']
            right = self.equation['right']
            
            # Összetett egyenleteknél egész osztást használunk
            left_value = left['const'] + left['coeff'] * (-(solution // left['divisor']) - left['inner_const'])
            right_value = right['const'] - right['a'] * solution
        
        is_equal = abs(left_value - right_value) < 1e-6
        
        print(f"Bal oldal (x={solution}): {left_value}")
        print(f"Jobb oldal (x={solution}): {right_value}")
        print(f"Egyenlő: {is_equal}")
        
        return is_equal

    def get_latex(self):
        eq = self.equation
        if eq['type'] == 'simple':
            instruction = "Oldja meg az alábbi egyenletet!"
            left, right = eq['left'], eq['right']
            a, b = int(left['a']), int(left['b'])
            c, d = int(right['c']), int(right['d'])
            
            l_side = f"{a}x"
            if b != 0: l_side += f" {'+' if b > 0 else '-'} {abs(b)}"
            
            r_side = f"{c}x"
            if d != 0: r_side += f" {'+' if d > 0 else '-'} {abs(d)}"
            
            latex_str = f"{l_side} = {r_side}"
        else:
            instruction = "Oldja meg az alábbi egyenletet!"
            left, right = eq['left'], eq['right']
            const, coeff = int(left['const']), int(left['coeff'])
            div, inner = int(left['divisor']), int(left['inner_const'])
            r_const, r_a = int(right['const']), int(right['a'])
            
            coeff_part = f"{coeff}" if coeff >= 0 else f"({coeff})"
            inner_sign = '-' if inner >= 0 else '+'
            
            # Törtes alak LaTeX-ben: \frac{számláló}{nevező}
            left_str = rf"{const} + {coeff_part} \cdot \left( -\frac{{x}}{{{div}}} {inner_sign} {abs(inner)} \right)"
            right_str = f"{r_const} {'-' if r_a > 0 else '+'} {abs(r_a)}x"
            
            latex_str = f"{left_str} = {right_str}"
            
        return instruction, latex_str

LinearEquation = LinearEquationComplex
