import random
import re


class WordLinearSystem:
    """Szöveges, kétismeretlenes egyenletrendszeres feladatok."""

    def __init__(self):
        self.task_type = None
        self.item_a = None
        self.item_b = None
        self.amount_a = None
        self.amount_b = None
        self.price_a = None
        self.price_b = None
        self.total_amount = None
        self.total_price = None
        self.solution = None

    def generateTask(self):
        self.task_type = random.choice([23, 24, 25, 26])
        self.price_a = random.randint(20, 90) * 10
        self.price_b = random.randint(20, 90) * 10
        while self.price_a == self.price_b:
            self.price_b = random.randint(20, 90) * 10

        if self.task_type == 23:
            self.item_a, self.item_b = "búzasör", "barna sör"
            self.amount_a, self.amount_b = random.randint(3, 8), random.randint(3, 8)
            self.total_amount = self.amount_a + self.amount_b
            self.total_price = (
                self.amount_a * self.price_a + self.amount_b * self.price_b
            )
        elif self.task_type == 24:
            self.item_a, self.item_b = "sör", "bor"
            self.amount_a, self.amount_b = random.randint(3, 8), random.randint(3, 8)
            self.total_amount = self.amount_a + self.amount_b
            self.total_price = (
                self.amount_a * self.price_a + self.amount_b * self.price_b
            )
        else:
            self.item_a, self.item_b = "krumpli", "hagyma"
            self.amount_a, self.amount_b = random.randint(3, 8), random.randint(3, 8)
            while self.amount_a == self.amount_b:
                self.amount_b = random.randint(3, 8)
            self.total_amount = self.amount_a + self.amount_b
            self.total_price = (
                self.amount_a * self.price_a + self.amount_b * self.price_b
            )

        self.solution = (self.price_a, self.price_b)
        return self.solution

    def get_latex(self):
        return "Oldja meg a következő szöveges feladatot!", ""

    def get_text(self):
        if self.task_type == 23:
            return (
                f"Egy bisztróban az italok árát deciliterenként adják meg. "
                f"Tudjuk, hogy {self.amount_a} dl búzasör és {self.amount_b} dl barna sör "
                f"összesen {self.total_price} Ft-ba kerül. {self.amount_a + 2} dl búzasör "
                f"és {self.amount_b - 1} dl barna sör pedig {self.total_price + self.price_a * 2 - self.price_b} Ft-ba kerül. "
                "Mennyibe kerül egy dl búzasör, és mennyibe egy dl barna sör?"
            )
        if self.task_type == 24:
            return (
                f"Egy kocsmában az italok árát deciliterenként adják meg. "
                f"Tudjuk, hogy {self.amount_a} dl sör és {self.amount_b} dl bor összesen "
                f"{self.total_price} Ft-ba kerül. {self.amount_a - 1} dl sör és "
                f"{self.amount_b + 2} dl bor összesen {self.total_price - self.price_a + self.price_b * 2} Ft-ba kerül. "
                "Mennyibe kerül egy dl sör, és mennyibe egy dl bor?"
            )
        if self.task_type == 25:
            return (
                f"Egy piacon a zöldségesnél egy vásárló {self.amount_a} kg krumpliért "
                f"és {self.amount_b} kg hagymáért {self.total_price} Ft-ot fizetett. "
                f"A következő vevő {self.amount_a - 1} kg hagymáért és "
                f"{self.amount_b - 1} kg krumpliért összesen "
                f"{self.total_price - self.price_a - self.price_b} Ft-ba került. "
                "Mennyibe került egy kg krumpli és mennyibe egy kg hagyma?"
            )
        return (
            f"Egy virágárusnál egy vásárló {self.amount_a} szál rózsa és "
            f"{self.amount_b} szál tulipán vásárlásáért {self.total_price} Ft-ot fizetett. "
            f"A következő vevő {self.amount_a - 1} szál rózsa és "
            f"{self.amount_b - 1} szál tulipán összesen "
            f"{self.total_price - self.price_a - self.price_b} Ft-ba került. "
            "Mennyibe került egy szál rózsa és mennyibe egy szál tulipán?"
        )

    def get_answer_fields(self):
        return [
            {"label": f"{self.item_a.capitalize()} ára =", "name": "first_price"},
            {"label": f"{self.item_b.capitalize()} ára =", "name": "second_price"},
        ]

    def getSolution(self, debug=False):
        return self.solution

    def validateSolution(self, student_solution):
        try:
            values = [
                value for value in re.split(r"[,;]", str(student_solution))
                if value.strip()
            ]
            if len(values) < 2:
                return False
            return (
                float(values[0].strip().replace(",", "."))
                == self.solution[0]
                and float(values[1].strip().replace(",", "."))
                == self.solution[1]
            )
        except (TypeError, ValueError):
            return False
