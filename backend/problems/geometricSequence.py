import random
import re

import sympy as sp


class GeometricSequence:
    """A megadott minták egyikét generáló szöveges mértani sorozatos feladat."""

    def __init__(self):
        self.first_term = None
        self.ratio = None
        self.task_type = None
        self.given_index = None
        self.given_term = None
        self.second_given_index = None
        self.second_given_term = None
        self.target_index = None
        self.sum_count = None
        self.solution = None

    def generateTask(self):
        self.task_type = random.choice(["nth_term", "first_term", "sum"])
        if self.task_type == "nth_term":
            self.given_index = random.randint(2, 5)
            self.target_index = random.randint(self.given_index + 1, 10)
            self.given_term = sp.Rational(random.randint(2, 12), random.randint(1, 4))
            self.ratio = sp.Rational(
                random.choice([-3, -2, 2, 3]), random.choice([1, 2])
            )
            self.solution = self.given_term * self.ratio ** (
                self.target_index - self.given_index
            )
        elif self.task_type == "first_term":
            self.given_index = random.randint(2, 4)
            self.second_given_index = random.randint(self.given_index + 2, 9)
            self.given_term = random.choice([2, 4, 6, 8])
            self.ratio = random.choice([2, 3])
            self.second_given_term = self.given_term * self.ratio ** (
                self.second_given_index - self.given_index
            )
            self.solution = sp.Rational(
                self.given_term, self.ratio ** (self.given_index - 1)
            )
        else:
            self.given_index = random.randint(2, 5)
            self.sum_count = random.randint(self.given_index + 2, 10)
            self.given_term = sp.Rational(random.randint(2, 8), random.randint(1, 4))
            self.ratio = sp.Rational(
                random.choice([1, 2, 3]), random.choice([2, 3, 4])
            )
            while self.ratio == 1 or self.ratio == 0:
                self.ratio = sp.Rational(random.randint(1, 3), random.randint(2, 4))
            self.first_term = self.given_term / self.ratio ** (self.given_index - 1)
            self.solution = (
                self.first_term
                * (1 - self.ratio ** self.sum_count)
                / (1 - self.ratio)
            )
        return self.solution

    def get_latex(self):
        instruction = "Oldja meg a következő szöveges feladatot!"
        if self.task_type == "nth_term":
            expression = (
                rf"\text{{Egy mértani sorozat }}{self.given_index}\text{{. eleme }}"
                rf"{sp.latex(self.given_term)}\text{{, a kvóciense pedig }}"
                rf"{sp.latex(self.ratio)}\text{{. Mennyi a sorozat }}"
                rf"{self.target_index}\text{{. eleme?}}"
            )
        elif self.task_type == "first_term":
            expression = (
                rf"\text{{Egy mértani sorozat }}{self.given_index}\text{{. eleme }}"
                rf"{sp.latex(self.given_term)}\text{{, a(z) }}"
                rf"{self.second_given_index}\text{{. eleme pedig }}"
                rf"{sp.latex(self.second_given_term)}"
                rf"\text{{. A sorozat kvóciense egy pozitív szám. Mennyi a sorozat első eleme?}}"
            )
        else:
            expression = (
                rf"\text{{Egy mértani sorozat }}{self.given_index}\text{{. eleme }}"
                rf"{sp.latex(self.given_term)}"
                rf"\text{{, a kvóciense pedig }}{sp.latex(self.ratio)}"
                rf"\text{{. Mennyi a sorozat első }}{self.sum_count}"
                rf"\text{{ elemének összegét?}}"
            )
        return instruction, expression

    def get_text(self):
        if self.task_type == "nth_term":
            return (
                f"Egy mértani sorozat {self.given_index}. eleme {self.given_term}, "
                f"a kvóciense pedig {self.ratio}. Mennyi a sorozat "
                f"{self.target_index}. eleme?"
            )
        if self.task_type == "first_term":
            return (
                f"Egy mértani sorozat {self.given_index}. eleme {self.given_term}, "
                f"a(z) {self.second_given_index}. eleme pedig "
                f"{self.second_given_term}. A sorozat kvóciense egy pozitív szám. "
                "Mennyi a sorozat első eleme?"
            )
        return (
            f"Egy mértani sorozat {self.given_index}. eleme {self.given_term}, "
            f"a kvóciense pedig {self.ratio}. Mennyi a sorozat első "
            f"{self.sum_count} elemének összege?"
        )

    def getSolution(self, debug=False):
        return self.solution

    def get_answer_format(self):
        if self.task_type == "nth_term":
            return f"a{self.target_index} = ..."
        if self.task_type == "first_term":
            return "a1 = ..."
        return f"S{self.sum_count} = ..."

    def get_answer_fields(self):
        if self.task_type == "nth_term":
            label = rf"a_{{{self.target_index}}} ="
        elif self.task_type == "first_term":
            label = "a_1 ="
        else:
            label = rf"S_{{{self.sum_count}}} ="
        return [{"label": label, "name": "solution"}]

    def validateSolution(self, student_solution):
        try:
            answer = str(student_solution).replace("−", "-").replace(" ", "")
            answer = re.sub(r"a\d+=|s\d+=", "", answer, flags=re.IGNORECASE)
            answer = re.sub(r"\\frac\{(-?\d+)\}\{(\d+)\}", r"\1/\2", answer)
            values = re.findall(r"-?\d+(?:/\d+)?(?:[.,]\d+)?", answer)
            if len(values) != 1:
                return False
            return sp.Rational(values[0].replace(",", ".")) == self.solution
        except (TypeError, ValueError, sp.SympifyError):
            return False
