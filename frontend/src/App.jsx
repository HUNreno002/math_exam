import React, { useState, useRef, useEffect } from 'react';
import 'katex/dist/katex.min.css';
import { BlockMath, InlineMath } from 'react-katex';
import 'mathlive';

function App() {
  const [problemType, setProblemType] = useState('fractionSimplification');
  const [taskData, setTaskData] = useState(null);
  const [feedback, setFeedback] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [solutionInfo, setSolutionInfo] = useState('');
  
  // A MathLive beviteli mező hivatkozása
  const answerRefs = useRef([]);

  const renderTaskText = (text) => text.split(/(-?\d+\/\d+)/g).map((part, index) => {
    const fraction = part.match(/^(-?)(\d+)\/(\d+)$/);
    if (!fraction) return <React.Fragment key={index}>{part}</React.Fragment>;

    const [, sign, numerator, denominator] = fraction;
    return (
      <React.Fragment key={index}>
        <InlineMath math={`${sign === '-' ? '-' : ''}\\frac{${numerator}}{${denominator}}`} />
      </React.Fragment>
    );
  });

  const htmlTaskTypes = [
    'arithmeticSequence',
    'geometricSequence',
    'priceChange',
    'linearFunction',
    'wordLinearSystem',
  ];

  const plainAnswerLabelTypes = [
    'functionRange',
  ];

  const generateTask = async () => {
    setIsLoading(true);
    setFeedback('');
    setSolutionInfo('');
    try {
      const response = await fetch(`http://localhost:8000/generate/${problemType}`);
      const data = await response.json();
      setTaskData(data);
      answerRefs.current.forEach((field) => {
        if (field) field.value = '';
      });
    } catch (error) {
      setFeedback('Hiba a szerverhez való csatlakozáskor.');
    }
    setIsLoading(false);
  };

  const checkAnswer = async () => {
    if (!taskData) return;
    
    const fieldCount = taskData.answer_fields ? taskData.answer_fields.length : 1;
    const studentAnswer = answerRefs.current.slice(0, fieldCount)
      .map((field) => field?.getValue('ascii-math') || '')
      .join(', ');
    
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
    const handleKeyDown = (e) => {
      if (e.key.length === 1 && !e.ctrlKey && !e.metaKey && !e.altKey) {
        let allowedChars = "";
        if (problemType === 'intervalProblem' || problemType === 'functionRange') {
          allowedChars = "0123456789()[]Uu-rR,";
        } else if (problemType === 'priceChange') {
          allowedChars = "0123456789%-,";
        } else {
          allowedChars = "0123456789xyzXYZ+-*/=.,><()^";
        }
        
        e.preventDefault();
        e.stopImmediatePropagation();
        
        if (allowedChars.includes(e.key)) {
          e.currentTarget.insert(e.key === '*' ? '\\times' : e.key);
        }
      }
    };

    const fields = answerRefs.current.filter(Boolean);
    fields.forEach((mf) => {
      mf.mathVirtualKeyboardPolicy = "auto";
      mf.smartFence = false;
      mf.smartMode = false;
      mf.smartSuperscript = true;
      mf.inlineShortcuts = {};
      mf.addEventListener("keydown", handleKeyDown, { capture: true });
    });

    if (window.mathVirtualKeyboard) {
      if (problemType === 'intervalProblem' || problemType === 'functionRange') {
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
      } else if (problemType === 'priceChange') {
        window.mathVirtualKeyboard.layouts = [
          {
            label: 'Százalék',
            rows: [
              [
                { class: 'action', label: '7', key: '7' },
                { class: 'action', label: '8', key: '8' },
                { class: 'action', label: '9', key: '9' },
                { class: 'tex', label: '%', key: '%' }
              ],
              [
                { class: 'action', label: '4', key: '4' },
                { class: 'action', label: '5', key: '5' },
                { class: 'action', label: '6', key: '6' },
                { class: 'tex', label: ',', key: ',' }
              ],
              [
                { class: 'action', label: '1', key: '1' },
                { class: 'action', label: '2', key: '2' },
                { class: 'action', label: '3', key: '3' },
                { class: 'tex', label: '-', key: '-' }
              ],
              [
                { class: 'action', label: '0', key: '0' },
                { class: 'tex', label: '', key: '' },
                { class: 'tex', label: '', key: '' },
                { class: 'action', label: '⌫', command: 'deleteBackward' }
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
      fields.forEach((mf) => {
        mf.removeEventListener("keydown", handleKeyDown, { capture: true });
      });
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
              <option value="arithmeticSequence">Számtani sorozat</option>
              <option value="geometricSequence">Mértani sorozat</option>
              <option value="priceChange">Százalékos árváltozás</option>
              <option value="linearFunction">Lineáris függvény két pontból</option>
              <option value="wordLinearSystem">Szöveges egyenletrendszer</option>
              <option value="powerEquation">Hatványazonosságos egyenlet</option>
              <option value="logEquation">Logaritmusos egyenlet</option>
              <option value="exponentialEquation">Exponenciális egyenlet</option>
              <option value="radicalEquation">Gyökös egyenlet</option>
              <option value="radicalFractionEquation">Gyökös tört-egyenlet</option>
              <option value="functionRange">Függvény ÉT és ÉK</option>
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
            
            <div className={`math-display ${htmlTaskTypes.includes(taskData.type) ? 'text-display' : ''}`}>
              {htmlTaskTypes.includes(taskData.type) ? (
                <p>{renderTaskText(taskData.text)}</p>
              ) : (
                <BlockMath math={taskData.latex} />
              )}
            </div>

            <div className="input-section">
              <label className="input-label">Írd be a megoldásod:</label>
              {taskData.answer_fields ? (
                <div className="structured-answer">
                  {taskData.answer_fields.map((field, index) => (
                    <div className="structured-answer-row" key={field.name}>
                      {field.label && (
                        <span className="answer-label">
                          {taskData.type === 'wordLinearSystem' || plainAnswerLabelTypes.includes(taskData.type) ? (
                            field.label
                          ) : (
                            <InlineMath math={field.label} />
                          )}
                        </span>
                      )}
                      <div className="math-field-wrapper">
                        <math-field
                          ref={(element) => {
                            answerRefs.current[index] = element;
                          }}
                        ></math-field>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="math-field-wrapper">
                  <math-field
                    ref={(element) => {
                      answerRefs.current[0] = element;
                    }}
                  ></math-field>
                </div>
              )}
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