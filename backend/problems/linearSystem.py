import numpy as np
import random

def random_not_zero_or_one(start, end):
    res = random.randint(start, end)
    while res in [0, 1, -1]:
        res = random.randint(start, end)
    return res

class LinearSystem():
    def __init__(self):
        self.coefficents = None
        self.rightside = None
        self.solution = None
        self.interval = (-5, 5)

    def generateTask(self):
        while True:
            try:
                x_val = random_not_zero_or_one(*self.interval)
                y_val = random_not_zero_or_one(*self.interval)
                self.solution = (x_val, y_val)

                self.coefficents = np.array([
                    [random_not_zero_or_one(*self.interval), random_not_zero_or_one(*self.interval)],
                    [random_not_zero_or_one(*self.interval), random_not_zero_or_one(*self.interval)]
                ])
                
                # Csak akkor lépünk ki, ha a determináns nem 0 (van megoldás)
                if np.linalg.det(self.coefficents) != 0:
                    self.rightside = self.coefficents @ np.array([x_val, y_val])
                    break
            except:
                continue

    def get_latex(self):
        instruction = "Oldja meg az alábbi egyenletrendszert!"
        
        a11, a12 = int(self.coefficents[0,0]), int(self.coefficents[0,1])
        a21, a22 = int(self.coefficents[1,0]), int(self.coefficents[1,1])
        b1, b2 = int(self.rightside[0]), int(self.rightside[1])

        def format_line(ax, ay, b):
            # Formázás szépítése (ne legyen 1x vagy -1y)
            x_str = f"{ax}x" if ax not in [1, -1] else ("x" if ax == 1 else "-x")
            y_val = abs(ay)
            y_str = f"y" if y_val == 1 else f"{y_val}y"
            sign = "+" if ay > 0 else "-"
            return f"{x_str} {sign} {y_str} = {b}"

        line1 = format_line(a11, a12, b1)
        line2 = format_line(a21, a22, b2)

        latex_str = rf"\begin{{cases}} {line1} \\ {line2} \end{{cases}}"
        
        return instruction, latex_str

    def getSolution(self, debug=False):
        return self.solution
    
    def validateSolution(self, student_solution):
        try:
            # student_solution egy string (ascii-math), pl: "x=3, y=5" vagy "3, 5" vagy "(3, 5)"
            import re
            
            x_true, y_true = self.solution
            
            # Kikeressük az összes számot (lehet negatív, meg tizedestört is)
            nums = re.findall(r'-?\d+(?:\.\d+)?', student_solution)
            
            if len(nums) < 2:
                return False
            
            # Ha pontosan "x=... y=..." formátum
            if 'x' in student_solution and 'y' in student_solution:
                x_match = re.search(r'x\s*=\s*(-?\d+(?:\.\d+)?)', student_solution)
                y_match = re.search(r'y\s*=\s*(-?\d+(?:\.\d+)?)', student_solution)
                if x_match and y_match:
                    x_student = float(x_match.group(1))
                    y_student = float(y_match.group(1))
                else:
                    x_student, y_student = float(nums[0]), float(nums[1])
            else:
                # Csak sormintában vesszük az első kettőt
                x_student, y_student = float(nums[0]), float(nums[1])
                
            return (float(x_true) == x_student and float(y_true) == y_student)
        except:
            return False