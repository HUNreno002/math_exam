from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid

from problems.fractionSimplification import FractionSimplification
from problems.fractionCombination import FractionCombination
from problems.powerSimplification import PowerSimplification
from problems.radicalRationalization import RadicalRationalization
from problems.intervalProblem import IntervalProblem
from problems.linearEquation import LinearEquation
from problems.linearSystem import LinearSystem
from problems.arithmeticSequence import ArithmeticSequence
from problems.geometricSequence import GeometricSequence
from problems.priceChange import PriceChange
from problems.linearFunction import LinearFunction
from problems.wordLinearSystem import WordLinearSystem
from problems.powerEquation import PowerEquation
from problems.logEquation import LogEquation
from problems.exponentialEquation import ExponentialEquation
from problems.radicalEquation import RadicalEquation
from problems.radicalFractionEquation import RadicalFractionEquation
from problems.functionRange import FunctionRange

app = FastAPI()

# Engedélyezzük, hogy a React (frontend) kommunikálhasson a Pythonnal
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Fejlesztéshez minden engedélyezett
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Itt tároljuk a memóriában a generált feladatokat (session alapján)
sessions = {}

class AnswerData(BaseModel):
    session_id: str
    student_answer: str

@app.get("/generate/{problem_type}")
def generate_task(problem_type: str):
    session_id = str(uuid.uuid4())
    
    # A te Tkinteres logikád alapján példányosítjuk a megfelelő osztályt
    if problem_type == "fractionSimplification":
        prob = FractionSimplification()
        prob.generateTask()
    elif problem_type == "fractionCombination":
        prob = FractionCombination()
        prob.generateTask()
    elif problem_type == "powerSimplification":
        prob = PowerSimplification()
        prob.generateTask()
    elif problem_type == "radicalRationalization":
        prob = RadicalRationalization()
        prob.generateTask()
    elif problem_type == "linearEquation":
        prob = LinearEquation()
        prob.generateTask()
    elif problem_type == "intervalProblem":
        prob = IntervalProblem()
        prob.generateTask()
    elif problem_type == "linearSystem":
        prob = LinearSystem()
        prob.generateTask()
    elif problem_type == "arithmeticSequence":
        prob = ArithmeticSequence()
        prob.generateTask()
    elif problem_type == "geometricSequence":
        prob = GeometricSequence()
        prob.generateTask()
    elif problem_type == "priceChange":
        prob = PriceChange()
        prob.generateTask()
    elif problem_type == "linearFunction":
        prob = LinearFunction()
        prob.generateTask()
    elif problem_type == "wordLinearSystem":
        prob = WordLinearSystem()
        prob.generateTask()
    elif problem_type == "powerEquation":
        prob = PowerEquation()
        prob.generateTask()
    elif problem_type == "logEquation":
        prob = LogEquation()
        prob.generateTask()
    elif problem_type == "exponentialEquation":
        prob = ExponentialEquation()
        prob.generateTask()
    elif problem_type == "radicalEquation":
        prob = RadicalEquation()
        prob.generateTask()
    elif problem_type == "radicalFractionEquation":
        prob = RadicalFractionEquation()
        prob.generateTask()
    elif problem_type == "functionRange":
        prob = FunctionRange()
        prob.generateTask()
    else:
        raise HTTPException(status_code=400, detail="Ismeretlen feladattípus")

    # Mentsük el a feladat példányát az ellenőrzéshez
    sessions[session_id] = {
        "type": problem_type,
        "instance": prob
    }
    
    # Használjuk a te meglévő get_latex() függvényeidet[cite: 1, 2, 3, 4]
    instruction, latex_str = prob.get_latex()
    
    return {
        "session_id": session_id,
        "type": problem_type,
        "instruction": instruction,
        "latex": latex_str,
        "text": prob.get_text() if hasattr(prob, "get_text") else None,
        "answer_format": (
            prob.get_answer_format()
            if hasattr(prob, "get_answer_format")
            else None
        ),
        "answer_fields": (
            prob.get_answer_fields()
            if hasattr(prob, "get_answer_fields")
            else None
        ),
    }

@app.post("/validate")
def validate_answer(data: AnswerData):
    if data.session_id not in sessions:
        raise HTTPException(status_code=404, detail="Feladat nem található vagy lejárt")
    
    task_data = sessions[data.session_id]
    prob_instance = task_data["instance"]
    
    # Meghívjuk a te saját validáló függvényedet[cite: 1, 2, 3, 4]
    try:
        is_correct = prob_instance.validateSolution(data.student_answer)
        return {"is_correct": is_correct}
    except Exception as e:
        return {"is_correct": False, "error": str(e)}

@app.get("/solution/{session_id}")
def get_solution(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Feladat nem található vagy lejárt")
    
    task_data = sessions[session_id]
    prob_instance = task_data["instance"]
    prob_type = task_data["type"]
    
    # Get the solution depending on what type it is
    try:
        import sympy as sp
        solution = prob_instance.getSolution()
        
        if prob_type == "powerSimplification":
            _, exponent = solution.as_base_exp()
            ans_latex = rf"x^{{{sp.latex(exponent)}}}"
        elif prob_type == "fractionSimplification":
            ans_latex = sp.latex(solution)
        elif prob_type == "priceChange":
            ans_latex = prob_instance.get_solution_latex()
        elif prob_type == "radicalFractionEquation":
            ans_latex = r"\varnothing"
        elif prob_type in (
            "powerEquation",
            "logEquation",
            "exponentialEquation",
            "radicalEquation",
        ):
            ans_latex = rf"x = {sp.latex(solution)}"
        elif prob_type == "functionRange":
            domain, value_range = solution
            ans_latex = (
                rf"\text{{Értelmezési tartomány: }}{domain},\quad "
                rf"\text{{Értékkészlet: }}{value_range}"
            )
        elif prob_type == "wordLinearSystem":
            first_price, second_price = solution
            first_label = prob_instance.item_a.capitalize()
            second_label = prob_instance.item_b.capitalize()
            ans_latex = (
                rf"\text{{{first_label} ára}} = {sp.latex(first_price)}, \quad "
                rf"\text{{{second_label} ára}} = {sp.latex(second_price)}"
            )
        elif "linearEquation" in prob_type:
            # Csak egy szám
            ans_latex = rf"x = {str(solution).rstrip('0').rstrip('.') if '.' in str(solution) else solution}"
        elif prob_type == "linearSystem":
            x, y = solution
            # x, y formázása, tizedesek eltávolítása, ha integer
            sx = str(x).rstrip('0').rstrip('.') if '.' in str(x) else x
            sy = str(y).rstrip('0').rstrip('.') if '.' in str(y) else y
            ans_latex = rf"x = {sx}, \quad y = {sy}"
        elif prob_type == "arithmeticSequence":
            first, second = solution
            ans_latex = rf"a_{{19}} = {sp.latex(first)}, \quad d = {sp.latex(second)}"
        elif prob_type in ("geometricSequence",):
            ans_latex = sp.latex(solution)
        elif prob_type == "intervalProblem":
            ans_latex = sp.latex(solution)
        else:
            ans_latex = sp.latex(solution)
            
        return {"solution_latex": ans_latex}
    except Exception as e:
        return {"error": str(e)}