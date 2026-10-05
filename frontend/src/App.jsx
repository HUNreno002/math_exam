import React, { useState, useRef, useEffect } from 'react';
import 'katex/dist/katex.min.css';
import { BlockMath } from 'react-katex';
import 'mathlive';

function App() {
  const [problemType, setProblemType] = useState('fractionSimplification');
  const [taskData, setTaskData] = useState(null);
  const [feedback, setFeedback] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [solutionInfo, setSolutionInfo] = useState('');
  
  // A MathLive beviteli mező hivatkozása
  const mfRef = useRef(null);

  const generateTask = async () => {
    setIsLoading(true);
    setFeedback('');
    setSolutionInfo('');
    try {
      const response = await fetch(`http://localhost:8000/generate/${problemType}`);
      const data = await response.json();
      setTaskData(data);
      if (mfRef.current) {
        mfRef.current.value = ''; // Mező ürítése új feladatnál
      }
    } catch (error) {
      setFeedback('Hiba a szerverhez való csatlakozáskor.');
    }
    setIsLoading(false);
  };

  const checkAnswer = async () => {
    if (!taskData) return;
    
    const studentAnswer = mfRef.current.getValue('ascii-math'); 
    
    try {
      const response = await fetch('http://localhost:8000/validate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: taskData.session_id,
          student_answer: studentAnswer
        })
      });
      
      const result = await response.json();
      if (result.is_correct) {
        setFeedback('✓ HELYES!');
      } else {
        setFeedback('✗ HELYTELEN. Próbáld újra!');
      }
    } catch (error) {
      setFeedback('Hiba történt az ellenőrzés során.');
    }
  };

  const getSolution = async () => {
    if (!taskData) return;
    try {
      const response = await fetch(`http://localhost:8000/solution/${taskData.session_id}`);
      const result = await response.json();
      if (result.solution_latex) {
        setSolutionInfo(result.solution_latex);
      } else {
        setFeedback('Hiba történt a megoldás lekérésekor.');
      }
    } catch (error) {
      setFeedback('Hiba történt a hálózati kapcsolat során.');
    }
  };

  useEffect(() => {
    const mf = mfRef.current;
    
    const handleKeyDown = (e) => {
      if (e.key.length === 1 && !e.ctrlKey && !e.metaKey && !e.altKey) {
        let allowedChars = "";
        if (problemType === 'intervalProblem') {
          allowedChars = "0123456789()[]Uu-rR,";
        } else {
          allowedChars = "0123456789xyzXYZ+-*/=.,><()^";
        }
        
        e.preventDefault();
        e.stopImmediatePropagation();
        
        if (allowedChars.includes(e.key)) {
          mf.insert(e.key === '*' ? '\\times' : e.key);
        }
      }
    };

    if (mf) {
      mf.mathVirtualKeyboardPolicy = "auto";
      mf.smartFence = false;
      mf.smartMode = false;
      mf.smartSuperscript = true;
      mf.inlineShortcuts = {};
      mf.addEventListener("keydown", handleKeyDown, { capture: true });
    }

    if (window.mathVirtualKeyboard) {
      if (problemType === 'intervalProblem') {
        window.mathVirtualKeyboard.layouts = [
          {
            label: 'Intervallum',
            rows: [
              [
                { class: 'tex', label: '[', key: '[' },
                { class: 'tex', label: ']', key: ']' },
                { class: 'action', label: '7', key: '7' },
                { class: 'action', label: '8', key: '8' },
                { class: 'action', label: '9', key: '9' },
                { class: 'tex', label: '∞', insert: '\\infty' }
              ],
              [
                { class: 'tex', label: '(', key: '(' },
                { class: 'tex', label: ')', key: ')' },
                { class: 'action', label: '4', key: '4' },
                { class: 'action', label: '5', key: '5' },
                { class: 'action', label: '6', key: '6' },
                { class: 'tex', label: '∪', insert: '\\cup' }
              ],
              [
                { class: 'tex', label: 'ℝ', insert: '\\mathbb{R}' },
                { class: 'tex', label: '', key: '' },
                { class: 'action', label: '1', key: '1' },
                { class: 'action', label: '2', key: '2' },
                { class: 'action', label: '3', key: '3' },
                { class: 'tex', label: '∅', insert: '\\emptyset' },
              ],
              [
                { class: 'tex', label: '', key: '' },
                { class: 'tex', label: '', key: '' },
                { class: 'action', label: '0', key: '0' },
                { class: 'action', label: ',', insert: ',' },
                { class: 'tex', label: '-', key: '-' },
                { class: 'tex', label: '', key: '' }
              ]
            ]
          }
        ];
      } else {
        window.mathVirtualKeyboard.layouts = [
          {
          label: 'Matek',
          rows: [
            [
              { class: 'tex', label: '(□)', insert: '\\left(#0\\right)', variants: ['\\left(#0\\right)', '(', ')'] },
              { 
                class: 'tex',
                label: problemType === 'powerSimplification' ? 'x^□' : '□²',
                insert: problemType === 'powerSimplification' ? '^{#?}' : '^2',
                variants: problemType === 'powerSimplification' ? ['^{#?}', '^2'] : ['^2', '^{#?}']
              },
              { class: 'action', label: '7', key: '7' },
              { class: 'action', label: '8', key: '8' },
              { class: 'action', label: '9', key: '9' },
              { class: 'tex', label: '÷', insert: '\\div' }
            ],
            [
              { class: 'tex', label: '□/□', insert: '\\frac{#0}{#?}' },
              { class: 'tex', label: '√□', insert: '\\sqrt{#0}', variants: ['\\sqrt{#0}', '\\sqrt[#?]{#0}'] },
              { class: 'action', label: '4', key: '4' },
              { class: 'action', label: '5', key: '5' },
              { class: 'action', label: '6', key: '6' },
              { class: 'tex', label: '×', insert: '\\times' }
            ],
            [
              { class: 'tex', label: '', key: '' },
              { class: 'tex', label: 'x', insert: 'x', variants: ['x', 'y', 'z'] },
              { class: 'action', label: '1', key: '1' },
              { class: 'action', label: '2', key: '2' },
              { class: 'action', label: '3', key: '3' },
              { class: 'tex', label: '-', key: '-' }
            ],
            [
              { class: 'tex', label: '', insert: '' },
              { class: 'tex', label: '', insert: '' },
              { class: 'action', label: '0', key: '0' },
              { class: 'tex', label: ',', insert: ',' },
              { class: 'tex', label: '=', key: '=' },
              { class: 'tex', label: '+', key: '+' }
            ]
          ]
        }
      ];      }    }

    return () => {
      if (mf) {
        mf.removeEventListener("keydown", handleKeyDown, { capture: true });
      }
    };
  }, [taskData, problemType]);
  
  return (
    <div className="app-layout">
      {/* Címsáv felül */}
      <header className="top-navbar">
        <h1 className="navbar-title">Matek gyakorló</h1>
      </header>
      
      <main className="main-content">
        {/* Vezérlők */}
        <div className="toolbar">
          <div className="select-wrapper">
            <select 
              className="clean-select"
              value={problemType} 
              onChange={(e) => setProblemType(e.target.value)}
            >
              <option value="fractionSimplification">Egyszerűsítés</option>
              <option value="fractionCombination">Tört kifejezések összevonása</option>
              <option value="powerSimplification">Tört kitevős hatványok</option>
              <option value="radicalRationalization">Nevező gyöktelenítése</option>
              <option value="linearEquation">Lineáris egyenlet</option>
              <option value="intervalProblem">Intervallum</option>
              <option value="linearSystem">Egyenletrendszer</option>
            </select>
          </div>
          <button 
            className="btn btn-primary" 
            onClick={generateTask} 
            disabled={isLoading}
          >
            {isLoading ? 'Generálás...' : 'Új feladat'}
          </button>
        </div>

        {/* Feladat doboza */}
        {taskData && (
          <div className="task-card">
            <h2 className="task-instruction">{taskData.instruction}</h2>
            
            <div className="math-display">
              <BlockMath math={taskData.latex} />
            </div>

            <div className="input-section">
              <label className="input-label">Írd be a megoldásod:</label>
              <div className="math-field-wrapper">
                <math-field ref={mfRef}></math-field>
              </div>
            </div>

            <div className="action-buttons">
              <button className="btn btn-primary" onClick={checkAnswer}>
                Ellenőrzés
              </button>
              <button className="btn btn-outline" onClick={getSolution}>
                Megoldás mutatása
              </button>
            </div>

            {feedback && (
              <div className={`feedback-banner ${feedback.includes('HELYES') && !feedback.includes('HELYTELEN') ? 'success' : 'error'}`}>
                {feedback}
              </div>
            )}

            {solutionInfo && (
              <div className="solution-panel">
                <span className="solution-badge">Helyes megoldás</span>
                <div className="solution-math">
                  <BlockMath math={solutionInfo} />
                </div>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;