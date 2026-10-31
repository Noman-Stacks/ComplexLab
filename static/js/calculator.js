/**
 * ComplexLab - Interactive Calculator Engine & Controller
 */

class CalculatorApp {
  constructor() {
    this.currentMode = 'expression'; // 'expression' or 'rectangular'
    this.currentCategory = 'arithmetic';
    this.currentOperation = 'multiply';
    this.currentResult = null;
    this.currentSteps = [];

    this.plane = null;
    this.historyManager = null;

    this.init();
  }

  init() {
    // Initialize Complex Plane Canvas
    if (window.ComplexPlane) {
      this.plane = new window.ComplexPlane('planeCanvas');
    }

    // Initialize History Manager
    if (window.HistoryManager) {
      this.historyManager = new window.HistoryManager('historyList');
      window.historyManager = this.historyManager;
    }

    this.bindEvents();
    this.updateOperationUI();

    // Load initial interesting calculation
    this.loadPreset('mult_demo');
  }

  bindEvents() {
    // Mode Switching
    document.querySelectorAll('.mode-tab').forEach(tab => {
      tab.addEventListener('click', (e) => {
        document.querySelectorAll('.mode-tab').forEach(t => t.classList.remove('active'));
        e.currentTarget.classList.add('active');
        this.currentMode = e.currentTarget.dataset.mode;
        this.switchInputMode(this.currentMode);
      });
    });

    // Category Tabs
    document.querySelectorAll('.cat-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
        e.currentTarget.classList.add('active');
        this.currentCategory = e.currentTarget.dataset.category;
        this.renderOperations(this.currentCategory);
      });
    });

    // Calculate Button
    const calcBtn = document.getElementById('btnCalculate');
    if (calcBtn) {
      calcBtn.addEventListener('click', () => this.calculate());
    }

    // Clear Button
    const clearBtn = document.getElementById('btnClear');
    if (clearBtn) {
      clearBtn.addEventListener('click', () => this.clearInputs());
    }

    // Swap Button
    const swapBtn = document.getElementById('btnSwap');
    if (swapBtn) {
      swapBtn.addEventListener('click', () => this.swapInputs());
    }

    // Enter key to calculate on inputs
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey && (e.target.classList.contains('math-input') || e.target.classList.contains('rect-input'))) {
        e.preventDefault();
        this.calculate();
      }
    });

    // Preset selector
    const presetSelect = document.getElementById('presetSelect');
    if (presetSelect) {
      presetSelect.addEventListener('change', (e) => {
        if (e.target.value) this.loadPreset(e.target.value);
      });
    }

    // Quick Symbol Buttons
    document.querySelectorAll('.sym-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const sym = e.currentTarget.dataset.symbol;
        this.insertSymbol(sym);
      });
    });

    // Copy Result Button
    const copyResBtn = document.getElementById('btnCopyResult');
    if (copyResBtn) {
      copyResBtn.addEventListener('click', () => {
        if (this.currentResult && window.copyToClipboard) {
          window.copyToClipboard(this.currentResult.formatted || this.currentResult);
        }
      });
    }

    // Copy LaTeX Button
    const copyLatexBtn = document.getElementById('btnCopyLatex');
    if (copyLatexBtn) {
      copyLatexBtn.addEventListener('click', () => {
        if (this.currentSteps.length > 0 && window.copyToClipboard) {
          const latexCode = this.currentSteps.map(s => `% ${s.title}\n${s.latex}`).join('\n\n');
          window.copyToClipboard(latexCode);
        }
      });
    }

    // Download Solution Button
    const dlBtn = document.getElementById('btnDownloadSolution');
    if (dlBtn) {
      dlBtn.addEventListener('click', () => this.downloadSolution());
    }

    // Toggle Steps Accordion Button
    const toggleStepsBtn = document.getElementById('btnToggleSteps');
    if (toggleStepsBtn) {
      toggleStepsBtn.addEventListener('click', () => {
        const stepsContainer = document.getElementById('stepsContainer');
        if (stepsContainer) {
          const isHidden = stepsContainer.style.display === 'none';
          stepsContainer.style.display = isHidden ? 'flex' : 'none';
          toggleStepsBtn.querySelector('.toggle-arrow').textContent = isHidden ? '▲' : '▼';
        }
      });
    }
  }

  switchInputMode(mode) {
    const exprSection = document.getElementById('expressionInputs');
    const rectSection = document.getElementById('rectangularInputs');

    if (mode === 'expression') {
      if (exprSection) exprSection.style.display = 'flex';
      if (rectSection) rectSection.style.display = 'none';
    } else {
      if (exprSection) exprSection.style.display = 'none';
      if (rectSection) rectSection.style.display = 'flex';
    }
  }

  renderOperations(category) {
    const opGrid = document.getElementById('operationGrid');
    if (!opGrid) return;

    const opsByCategory = {
      arithmetic: [
        { id: 'multiply', name: 'Multiply (×)' },
        { id: 'divide', name: 'Divide (/)' },
        { id: 'add', name: 'Add (+)' },
        { id: 'subtract', name: 'Subtract (−)' },
        { id: 'negate', name: 'Negation (−z)' },
        { id: 'equals', name: 'Equality (==)' },
        { id: 'sum_multiple', name: 'Sum Multiple' },
        { id: 'product_multiple', name: 'Product Multiple' },
      ],
      conjugate_modulus: [
        { id: 'conjugate', name: 'Conjugate (z̄)' },
        { id: 'double_conjugate', name: 'Double Conjugate' },
        { id: 'modulus', name: 'Modulus (|z|)' },
        { id: 'argument', name: 'Argument (θ)' },
        { id: 'reciprocal', name: 'Reciprocal (1/z)' },
        { id: 'verify_identities', name: 'Verify Identities' },
        { id: 'product_with_conjugate', name: 'z · z̄ = |z|²' },
        { id: 'real_part', name: 'Real Part Re(z)' },
        { id: 'imag_part', name: 'Imag Part Im(z)' },
      ],
      polar: [
        { id: 'to_polar', name: 'To Polar Form' },
        { id: 'to_exponential', name: 'To Exponential Form' },
        { id: 'to_trig', name: 'Trigonometric Form' },
        { id: 'polar_to_rect', name: 'Polar to Rectangular' },
        { id: 'deg_to_rad', name: 'Deg ↔ Radian' },
      ],
      powers_roots: [
        { id: 'power', name: 'Integer Power (zⁿ)' },
        { id: 'powers_of_i', name: 'Powers of i (iᵏ)' },
        { id: 'square_roots', name: 'Square Roots (√z)' },
        { id: 'nth_roots', name: 'N-th Roots' },
        { id: 'roots_of_unity', name: 'Roots of Unity' },
        { id: 'de_moivre', name: "De Moivre's Theorem" },
      ],
      advanced: [
        { id: 'linear_eq', name: 'Linear Eq (az + b = c)' },
        { id: 'quadratic_eq', name: 'Quadratic (az² + bz + c = 0)' },
        { id: 'distance', name: 'Distance d(z₁, z₂)' },
        { id: 'normalize', name: 'Normalize (Unit z)' },
        { id: 'verify_inverse', name: 'Verify z · z⁻¹ = 1' },
      ]
    };

    const ops = opsByCategory[category] || opsByCategory.arithmetic;
    opGrid.innerHTML = ops.map(op => `
      <button type="button" class="op-btn ${op.id === this.currentOperation ? 'active' : ''}" data-op="${op.id}">
        ${op.name}
      </button>
    `).join('');

    // Rebind op button clicks
    opGrid.querySelectorAll('.op-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        opGrid.querySelectorAll('.op-btn').forEach(b => b.classList.remove('active'));
        e.currentTarget.classList.add('active');
        this.currentOperation = e.currentTarget.dataset.op;
        this.updateOperationUI();
      });
    });
  }

  updateOperationUI() {
    const op = this.currentOperation;
    const isUnary = [
      'conjugate', 'double_conjugate', 'negate', 'reciprocal', 'modulus',
      'argument', 'normalize', 'verify_identities', 'verify_inverse',
      'product_with_conjugate', 'real_part', 'imag_part',
      'to_polar', 'to_exponential', 'to_trig', 'square_roots'
    ].includes(op);

    const isNthRoot = ['nth_roots', 'de_moivre', 'power'].includes(op);
    const isRootsOfUnity = op === 'roots_of_unity';
    const isPowersOfI = op === 'powers_of_i';
    const isEq = ['linear_eq', 'quadratic_eq'].includes(op);
    const isMulti = ['sum_multiple', 'product_multiple'].includes(op);

    const z2GroupExpr = document.getElementById('z2GroupExpr');
    const z2GroupRect = document.getElementById('z2GroupRect');
    const extraInputs = document.getElementById('extraInputs');
    const multiInputs = document.getElementById('multiInputs');
    const eqInputs = document.getElementById('eqInputs');
    const standardInputs = document.getElementById('standardInputs');

    // Reset visibility
    if (standardInputs) standardInputs.style.display = 'block';
    if (multiInputs) multiInputs.style.display = 'none';
    if (eqInputs) eqInputs.style.display = 'none';
    if (extraInputs) extraInputs.style.display = 'none';

    if (isMulti) {
      if (standardInputs) standardInputs.style.display = 'none';
      if (multiInputs) multiInputs.style.display = 'block';
    } else if (isEq) {
      if (standardInputs) standardInputs.style.display = 'none';
      if (eqInputs) eqInputs.style.display = 'block';
      const eqTitle = document.getElementById('eqTitle');
      if (eqTitle) eqTitle.textContent = op === 'linear_eq' ? 'Solve: a·z + b = c' : 'Solve: a·z² + b·z + c = 0';
    } else if (isUnary) {
      if (z2GroupExpr) z2GroupExpr.style.display = 'none';
      if (z2GroupRect) z2GroupRect.style.display = 'none';
    } else if (isPowersOfI || isRootsOfUnity || isNthRoot) {
      if (z2GroupExpr) z2GroupExpr.style.display = 'none';
      if (z2GroupRect) z2GroupRect.style.display = 'none';
      if (extraInputs) {
        extraInputs.style.display = 'block';
        const label = document.getElementById('extraInputLabel');
        if (label) {
          label.textContent = isPowersOfI ? 'Exponent k (for iᵏ):' : 'Root Degree n:';
        }
      }
    } else {
      if (z2GroupExpr) z2GroupExpr.style.display = 'block';
      if (z2GroupRect) z2GroupRect.style.display = 'block';
    }
  }

  insertSymbol(sym) {
    // Find active or last focused input
    let target = document.activeElement;
    if (!target || (!target.classList.contains('math-input') && !target.classList.contains('rect-input'))) {
      target = document.getElementById('inputZ1') || document.querySelector('.math-input');
    }
    if (!target) return;

    const start = target.selectionStart || target.value.length;
    const end = target.selectionEnd || target.value.length;
    const text = target.value;
    target.value = text.substring(0, start) + sym + text.substring(end);
    target.focus();
    target.selectionStart = target.selectionEnd = start + sym.length;
  }

  clearInputs() {
    document.querySelectorAll('.math-input, .rect-input').forEach(inp => inp.value = '');
    const resultCard = document.getElementById('resultCard');
    const stepsCard = document.getElementById('stepsCard');
    if (resultCard) resultCard.style.display = 'none';
    if (stepsCard) stepsCard.style.display = 'none';
    if (this.plane) this.plane.clear();
    if (window.showToast) window.showToast('Calculator inputs cleared.', 'info');
  }

  swapInputs() {
    if (this.currentMode === 'expression') {
      const z1El = document.getElementById('inputZ1');
      const z2El = document.getElementById('inputZ2');
      if (z1El && z2El) {
        const tmp = z1El.value;
        z1El.value = z2El.value;
        z2El.value = tmp;
      }
    } else {
      const r1 = document.getElementById('rectZ1Real');
      const i1 = document.getElementById('rectZ1Imag');
      const r2 = document.getElementById('rectZ2Real');
      const i2 = document.getElementById('rectZ2Imag');
      if (r1 && r2 && i1 && i2) {
        const tr = r1.value; r1.value = r2.value; r2.value = tr;
        const ti = i1.value; i1.value = i2.value; i2.value = ti;
      }
    }
    if (window.showToast) window.showToast('Inputs swapped.', 'info');
  }

  loadPreset(presetKey) {
    const presets = {
      mult_demo: { op: 'multiply', cat: 'arithmetic', z1: '3 + 4i', z2: '2 - i' },
      div_demo: { op: 'divide', cat: 'arithmetic', z1: '3 + 4i', z2: '1 - 2i' },
      power_demo: { op: 'power', cat: 'powers_roots', z1: '1 + i', n: 8 },
      power_i_demo: { op: 'powers_of_i', cat: 'powers_roots', k: 105 },
      roots_unity_demo: { op: 'roots_of_unity', cat: 'powers_roots', n: 5 },
      quadratic_demo: { op: 'quadratic_eq', cat: 'advanced', a: '1', b: '-2', c: '5' },
      linear_demo: { op: 'linear_eq', cat: 'advanced', a: '2 + i', b: '3', c: '4 - i' },
      conj_identities: { op: 'verify_identities', cat: 'conjugate_modulus', z1: '3 - 4i' },
      sqrt_demo: { op: 'square_roots', cat: 'powers_roots', z1: '-4 + 3i' }
    };

    const p = presets[presetKey];
    if (!p) return;

    // Set category & op
    this.currentCategory = p.cat;
    this.currentOperation = p.op;

    document.querySelectorAll('.cat-btn').forEach(b => {
      b.classList.toggle('active', b.dataset.category === p.cat);
    });
    this.renderOperations(p.cat);
    this.updateOperationUI();

    // Set inputs
    if (p.z1) {
      const z1El = document.getElementById('inputZ1');
      if (z1El) z1El.value = p.z1;
    }
    if (p.z2) {
      const z2El = document.getElementById('inputZ2');
      if (z2El) z2El.value = p.z2;
    }
    if (p.n || p.k) {
      const extraInp = document.getElementById('inputExtraN');
      if (extraInp) extraInp.value = p.n || p.k;
    }
    if (p.a && p.b && p.c) {
      const eqA = document.getElementById('eqA');
      const eqB = document.getElementById('eqB');
      const eqC = document.getElementById('eqC');
      if (eqA) eqA.value = p.a;
      if (eqB) eqB.value = p.b;
      if (eqC) eqC.value = p.c;
    }

    // Auto calculate preset
    this.calculate();
  }

  loadFromHistory(item) {
    if (!item) return;
    this.currentOperation = item.operation;
    this.updateOperationUI();

    const z1El = document.getElementById('inputZ1');
    const z2El = document.getElementById('inputZ2');
    if (z1El && item.z1) z1El.value = item.z1;
    if (z2El && item.z2) z2El.value = item.z2;

    this.calculate();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  async calculate() {
    const calcBtn = document.getElementById('btnCalculate');
    if (calcBtn) {
      calcBtn.disabled = true;
      calcBtn.innerHTML = '<span class="spinner"></span> Calculating...';
    }

    try {
      const op = this.currentOperation;

      // 1. Equations endpoint
      if (['linear_eq', 'quadratic_eq'].includes(op)) {
        await this.handleEquation(op === 'linear_eq' ? 'linear' : 'quadratic');
        return;
      }

      // 2. Roots endpoint
      if (['square_roots', 'nth_roots', 'roots_of_unity', 'de_moivre'].includes(op)) {
        await this.handleRoots(op);
        return;
      }

      // 3. Conversions endpoint
      if (['to_polar', 'to_exponential', 'to_trig'].includes(op)) {
        await this.handleConversion(op);
        return;
      }

      // 4. Standard Calculate endpoint
      await this.handleStandardCalculation(op);

    } catch (err) {
      console.error('Calculation error:', err);
      if (window.showToast) window.showToast(err.message || 'Error occurred during calculation.', 'error');
    } finally {
      if (calcBtn) {
        calcBtn.disabled = false;
        calcBtn.innerHTML = 'Calculate Result';
      }
    }
  }

  getPayload(includeZ2 = true) {
    const payload = { operation: this.currentOperation };

    if (this.currentMode === 'expression') {
      payload.z1 = document.getElementById('inputZ1')?.value.trim();
      if (includeZ2) payload.z2 = document.getElementById('inputZ2')?.value.trim();
    } else {
      payload.z1_real = document.getElementById('rectZ1Real')?.value.trim();
      payload.z1_imag = document.getElementById('rectZ1Imag')?.value.trim();
      if (includeZ2) {
        payload.z2_real = document.getElementById('rectZ2Real')?.value.trim();
        payload.z2_imag = document.getElementById('rectZ2Imag')?.value.trim();
      }
    }

    // Check extra input for power or powers of i
    const extraVal = document.getElementById('inputExtraN')?.value.trim();
    if (extraVal) {
      payload.n = parseInt(extraVal, 10);
      payload.exponent = parseInt(extraVal, 10);
      payload.k = parseInt(extraVal, 10);
    }

    return payload;
  }

  async handleStandardCalculation(op) {
    let payload;
    if (['sum_multiple', 'product_multiple'].includes(op)) {
      payload = {
        operation: op,
        numbers: document.getElementById('inputMultiNumbers')?.value.trim()
      };
    } else {
      payload = this.getPayload();
    }

    const response = await fetch('/api/calculate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await response.json();
    if (!data.success) {
      throw new Error(data.error || 'Calculation failed.');
    }

    this.displayResult(data);
  }

  async handleRoots(rootType) {
    const payload = { type: rootType };
    if (this.currentMode === 'expression') {
      payload.z = document.getElementById('inputZ1')?.value.trim() || '1';
    } else {
      payload.z_real = document.getElementById('rectZ1Real')?.value.trim() || '1';
      payload.z_imag = document.getElementById('rectZ1Imag')?.value.trim() || '0';
    }

    const extraVal = document.getElementById('inputExtraN')?.value.trim() || '3';
    payload.n = parseInt(extraVal, 10);

    const response = await fetch('/api/roots', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await response.json();
    if (!data.success) throw new Error(data.error || 'Roots calculation failed.');

    this.displayRootsResult(data);
  }

  async handleConversion(convOp) {
    const payload = { mode: 'rectangular_to_all' };
    if (this.currentMode === 'expression') {
      payload.z = document.getElementById('inputZ1')?.value.trim();
    } else {
      payload.z_real = document.getElementById('rectZ1Real')?.value.trim();
      payload.z_imag = document.getElementById('rectZ1Imag')?.value.trim();
    }

    const response = await fetch('/api/convert', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await response.json();
    if (!data.success) throw new Error(data.error || 'Conversion failed.');

    this.displayConversionResult(data);
  }

  async handleEquation(eqType) {
    const payload = {
      type: eqType,
      a: document.getElementById('eqA')?.value.trim(),
      b: document.getElementById('eqB')?.value.trim(),
      c: document.getElementById('eqC')?.value.trim()
    };

    const response = await fetch('/api/equation/solve', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await response.json();
    if (!data.success) throw new Error(data.error || 'Failed to solve equation.');

    this.displayEquationResult(data);
  }

  displayResult(data) {
    const res = data.result;
    this.currentResult = res;
    this.currentSteps = data.steps || [];

    // Show result card
    const resultCard = document.getElementById('resultCard');
    if (resultCard) resultCard.style.display = 'flex';

    // Populate representations
    document.getElementById('resultMain').textContent = res.formatted ?? res.value ?? (data.result_str ?? '0');
    document.getElementById('repRect').textContent = res.formatted ?? 'N/A';
    document.getElementById('repPolar').textContent = res.polar ?? 'N/A';
    document.getElementById('repExp').textContent = res.exponential ?? 'N/A';
    document.getElementById('repTrig').textContent = res.trigonometric ?? 'N/A';

    // Render Steps with MathJax
    this.renderSteps(this.currentSteps);

    // Update Plane Visualization
    if (this.plane) {
      const z1Data = data.inputs?.z1;
      const z2Data = data.inputs?.z2;

      this.plane.updateElements({
        z1: z1Data ? { real: z1Data.real, imag: z1Data.imaginary } : null,
        z2: z2Data ? { real: z2Data.real, imag: z2Data.imaginary } : null,
        result: (res.real !== undefined && res.imaginary !== undefined) ? { real: res.real, imag: res.imaginary } : null,
        conjugate: data.operation === 'conjugate' ? { real: res.real, imag: res.imaginary } : null,
        roots: []
      });
    }

    // Save to History
    if (this.historyManager) {
      this.historyManager.addEntry({
        operation: data.operation,
        z1: document.getElementById('inputZ1')?.value || data.inputs?.z1?.formatted,
        z2: document.getElementById('inputZ2')?.value || data.inputs?.z2?.formatted,
        result: res.formatted || res.value || data.result_str,
        steps: this.currentSteps
      });
    }

    if (window.showToast) window.showToast('Calculation complete!', 'success');
  }

  displayRootsResult(data) {
    const rootsInfo = data.result.roots;
    this.currentSteps = data.steps || [];

    const resultCard = document.getElementById('resultCard');
    if (resultCard) resultCard.style.display = 'flex';

    const firstRoot = rootsInfo[0];
    document.getElementById('resultMain').textContent = firstRoot.formatted;
    document.getElementById('repRect').textContent = `Total Roots: ${rootsInfo.length}`;
    document.getElementById('repPolar').textContent = `Root Radius: ${data.result.root_radius || data.result.modulus_root}`;
    document.getElementById('repExp').textContent = `Spacing: ${data.result.angular_spacing_deg ?? 180}°`;
    document.getElementById('repTrig').textContent = rootsInfo.map(r => r.formatted).join('; ');

    this.renderSteps(this.currentSteps);

    // Update Plane with polygon and roots
    if (this.plane) {
      const inputZ = data.result.input;
      this.plane.updateElements({
        z1: inputZ ? { real: inputZ.real, imag: inputZ.imaginary } : null,
        z2: null,
        result: null,
        conjugate: null,
        roots: rootsInfo.map(r => ({ real: r.real, imag: r.imaginary, k: r.k }))
      });
    }

    if (window.showToast) window.showToast(`Calculated ${rootsInfo.length} distinct roots.`, 'success');
  }

  displayConversionResult(data) {
    const res = data.result;
    const resultCard = document.getElementById('resultCard');
    if (resultCard) resultCard.style.display = 'flex';

    document.getElementById('resultMain').textContent = res.rectangular;
    document.getElementById('repRect').textContent = res.rectangular;
    document.getElementById('repPolar').textContent = res.polar;
    document.getElementById('repExp').textContent = res.exponential;
    document.getElementById('repTrig').textContent = res.trigonometric;

    const steps = [
      { step: "1", title: "Rectangular Form", latex: `z = ${res.rectangular}` },
      { step: "2", title: "Modulus r", latex: `r = \\sqrt{${res.real}^2 + ${res.imaginary}^2} = ${res.modulus}` },
      { step: "3", title: "Principal Argument θ", latex: `\\theta = ${res.argument_radians ?? 0}\\text{ rad} (${res.argument_degrees ?? 0}^\\circ)` },
      { step: "4", title: "Polar / Exponential Representations", latex: `z = ${res.polar} = ${res.exponential}` }
    ];
    this.renderSteps(steps);

    if (this.plane) {
      this.plane.updateElements({
        z1: { real: res.real, imag: res.imaginary },
        z2: null,
        result: null,
        roots: []
      });
    }
  }

  displayEquationResult(data) {
    const res = data.result;
    const resultCard = document.getElementById('resultCard');
    if (resultCard) resultCard.style.display = 'flex';

    let mainText = 'No solution';
    if (res.solution) mainText = res.solution.formatted;
    else if (res.roots && res.roots.length > 0) mainText = res.roots.map(r => r.formatted).join(', ');

    document.getElementById('resultMain').textContent = mainText;
    document.getElementById('repRect').textContent = res.equation;
    document.getElementById('repPolar').textContent = res.infinite_solutions ? 'Infinite Solutions' : 'Solvable';
    document.getElementById('repExp').textContent = res.is_repeated ? 'Repeated Root' : 'Distinct Roots';
    document.getElementById('repTrig').textContent = res.explanation || mainText;

    this.renderSteps(data.steps || []);

    if (this.plane) {
      if (res.solution) {
        this.plane.updateElements({ z1: null, z2: null, result: { real: res.solution.real, imag: res.solution.imaginary }, roots: [] });
      } else if (res.roots) {
        this.plane.updateElements({ z1: null, z2: null, result: null, roots: res.roots.map((r, i) => ({ real: r.real, imag: r.imaginary, k: i })) });
      }
    }
  }

  renderSteps(steps) {
    const stepsCard = document.getElementById('stepsCard');
    const stepsList = document.getElementById('stepsList');
    if (!stepsCard || !stepsList) return;

    if (!steps || steps.length === 0) {
      stepsCard.style.display = 'none';
      return;
    }

    stepsCard.style.display = 'block';
    stepsList.innerHTML = steps.map((s, idx) => `
      <div class="step-item">
        <div class="step-header">
          <span class="step-num">${s.step || idx + 1}</span>
          <span>${s.title}</span>
        </div>
        <div class="step-latex">$$${s.latex}$$</div>
      </div>
    `).join('');

    // Trigger MathJax re-render
    if (window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise([stepsList]).catch(err => console.error('MathJax error:', err));
    }
  }

  downloadSolution() {
    if (!this.currentResult) {
      alert('No calculation to download.');
      return;
    }

    let text = `ComplexLab Mathematical Solution\n`;
    text += `Generated: ${new Date().toLocaleString()}\n`;
    text += `Operation: ${this.currentOperation}\n`;
    text += `Result: ${document.getElementById('resultMain').textContent}\n\n`;
    text += `Representations:\n`;
    text += `  Rectangular:   ${document.getElementById('repRect').textContent}\n`;
    text += `  Polar:         ${document.getElementById('repPolar').textContent}\n`;
    text += `  Exponential:   ${document.getElementById('repExp').textContent}\n`;
    text += `  Trigonometric: ${document.getElementById('repTrig').textContent}\n\n`;

    if (this.currentSteps.length > 0) {
      text += `Step-by-Step Solution:\n`;
      this.currentSteps.forEach(s => {
        text += `  [Step ${s.step}] ${s.title}\n`;
        text += `    Formula: ${s.latex}\n\n`;
      });
    }

    const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ComplexLab_Solution_${Date.now()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  }
}

// Instantiate on DOM load
document.addEventListener('DOMContentLoaded', () => {
  window.calculatorApp = new CalculatorApp();
});
