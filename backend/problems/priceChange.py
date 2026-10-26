import random
import re

import sympy as sp


class PriceChange:
    """Ismételt százalékos árváltozásokat gyakorló szöveges feladatok."""

    def __init__(self):
        self.task_type = None
        self.initial_price = None
        self.rate = None
        self.months = None
        self.rounds = None
        self.solution = None
        self.answer_unit = None

    def generateTask(self):
        self.task_type = random.randint(75, 80)

        if self.task_type == 75:
            self.initial_price = random.choice([12, 15, 19, 24, 30])
            self.rate = sp.Rational(random.choice([8, 12, 14, 18]), 10)
            self.months = random.randint(6, 15)
            price_in_forints = (
                self.initial_price
                * 1_000_000
                * (1 + self.rate / 100) ** self.months
            )
            self.solution = int(sp.floor(price_in_forints + sp.Rational(1, 2)))
            self.answer_unit = "millió Ft"
        elif self.task_type == 76:
            self.initial_price = random.choice([3, 5, 7, 10])
            self.rate = sp.Rational(random.choice([2, 3, 5, 8]), 10)
            self.months = random.randint(6, 14)
            percentage = ((1 + self.rate / 100) ** self.months - 1) * 100
            self.solution = int(sp.floor(percentage + sp.Rational(1, 2)))
            self.answer_unit = "%"
        elif self.task_type in (77, 78):
            self.initial_price = random.choice([8, 12, 20, 25])
            first_discount = sp.Rational(5 if self.task_type == 77 else 1, 1)
            second_discount = sp.Rational(5 if self.task_type == 77 else 4, 1)
            self.rounds = 2
            self.rate = (first_discount, second_discount)
            percentage = (
                (1 - first_discount / 100)
                * (1 - second_discount / 100)
                - 1
            ) * 100
            self.solution = int(sp.floor(percentage + sp.Rational(1, 2)))
            self.answer_unit = "%"
        else:
            self.initial_price = random.choice([10, 15, 20, 30])
            self.rate = sp.Rational(13 if self.task_type == 79 else 8, 1)
            self.rounds = 3 if self.task_type == 79 else 4
            decrease = sp.Rational(2, 1)
            percentage = (
                ((1 + self.rate / 100) * (1 - decrease / 100) ** self.rounds - 1)
                * 100
            )
            self.solution = int(sp.floor(percentage + sp.Rational(1, 2)))
            self.answer_unit = "%"
        return self.solution

    @staticmethod
    def _number(value):
        return str(value) if value.q == 1 else f"{value.p}/{value.q}"

    @staticmethod
    def _percent(value):
        return f"{float(value):g}".replace(".", ",")

    def get_text(self):
        if self.task_type == 75:
            return (
                f"Egy terméket {self.initial_price} millió Ft-ért vásároltunk. "
                f"Értéke minden hónapban {self._percent(self.rate)}%-kal nő. Mennyi a termék "
                f"{self.months} hónap múlva forintban?"
            )
        if self.task_type == 76:
            return (
                f"Egy terméket {self.initial_price} millió Ft-ért vásároltunk. "
                f"Értéke minden hónapban {self._percent(self.rate)}%-kal nő. Hány %-os a "
                f"változás összességében {self.months} hónap alatt a kiinduló "
                "árhoz képest?"
            )
        if self.task_type in (77, 78):
            return (
                "Egy terméket egymás után kétszer leáraznak, először "
                f"{self._percent(self.rate[0])}%-kal, majd {self._percent(self.rate[1])}%-kal. "
                "Összességében "
                "mennyit változott a termék értéke?"
            )
        increase = self.rate
        return (
            f"Egy termék árát felemelik {increase}%-kal, majd "
            f"{self.rounds} alkalommal csökkentik, minden alkalommal 2%-kal. "
            "Mennyit változott a termék ára összességében?"
        )

    def get_latex(self):
        instruction = "Oldja meg a következő szöveges feladatot!"
        if self.task_type == 75:
            expression = (
                rf"\text{{Egy terméket }}{self.initial_price}\text{{ millió Ft-ért vásároltunk. }}"
                rf"\text{{ Értéke minden hónapban }}{self._percent(self.rate)}\%"
                rf"\text{{-kal nő. Mennyi a termék }}{self.months}"
                rf"\text{{ hónap múlva forintban?}}"
            )
        elif self.task_type == 76:
            expression = (
                rf"\text{{Egy terméket }}{self.initial_price}\text{{ millió Ft-ért vásároltunk. }}"
                rf"\text{{ Értéke minden hónapban }}{self._percent(self.rate)}\%"
                rf"\text{{-kal nő. Hány \%-os a változás összességében }}"
                rf"{self.months}\text{{ hónap alatt a kiinduló árhoz képest?}}"
            )
        elif self.task_type in (77, 78):
            expression = (
                rf"\text{{Egy terméket egymás után kétszer leáraznak, először }}"
                rf"{self._percent(self.rate[0])}\%\text{{-kal, majd }}"
                rf"{self._percent(self.rate[1])}\%\text{{-kal. Összességében }}"
                rf"\text{{ mennyit változott a termék értéke?}}"
            )
        else:
            expression = (
                rf"\text{{Egy termék árát felemelik }}{self.rate}\%\text{{-kal, majd }}"
                rf"\text{{ }}{self.rounds}\text{{ alkalommal csökkentik, minden alkalommal }}"
                rf"\text{{ 2\%-kal. Mennyit változott a termék ára összességében?}}"
            )
        return instruction, expression

    def getSolution(self, debug=False):
        return self.solution

    def get_answer_fields(self):
        return [{"label": "", "name": "solution"}]

    def get_solution_latex(self):
        if self.task_type == 75:
            return sp.latex(self.solution) + r"\,\mathrm{Ft}"
        return sp.latex(self.solution) + r"\,\%"

    def validateSolution(self, student_solution):
        try:
            answer = str(student_solution).replace(",", ".").replace(" ", "")
            percent_match = re.fullmatch(r"(-?\d+(?:\.\d+)?)%", answer)
            decimal_match = re.fullmatch(r"-?\d+(?:\.\d+)?", answer)
            if percent_match:
                if self.task_type == 75:
                    return False
                submitted_percent = sp.Rational(percent_match.group(1))
            elif decimal_match:
                submitted_value = sp.Rational(answer)
                submitted_percent = (
                    submitted_value
                    if self.task_type == 75
                    else submitted_value * 100
                )
            else:
                return False
            return submitted_percent == self.solution
        except (TypeError, ValueError):
            return False
