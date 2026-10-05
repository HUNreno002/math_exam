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
        "instruction": instruction,
        "latex": latex_str
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
        elif "linearEquation" in prob_type:
            # Csak egy szám
            ans_latex = rf"x = {str(solution).rstrip('0').rstrip('.') if '.' in str(solution) else solution}"
        elif prob_type == "linearSystem":
            x, y = solution
            # x, y formázása, tizedesek eltávolítása, ha integer
            sx = str(x).rstrip('0').rstrip('.') if '.' in str(x) else x
            sy = str(y).rstrip('0').rstrip('.') if '.' in str(y) else y
            ans_latex = rf"x = {sx}, \quad y = {sy}"
        elif prob_type == "intervalProblem":
            ans_latex = sp.latex(solution)
        else:
            ans_latex = sp.latex(solution)
            
        return {"solution_latex": ans_latex}
    except Exception as e:
        return {"error": str(e)}