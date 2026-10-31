# ComplexLab

> **Explore Complex Numbers. Solve with Confidence.**

ComplexLab is a production-quality, responsive web application and mathematical learning platform for exploring, solving, and visualizing operations on complex numbers. It combines exact and numerical computation, step-by-step pedagogical explanations, an interactive Argand plane visualization, an extensive learning center, and interactive practice exercises.

---

## 🌟 Key Features

### 1. Mathematical Calculation Engine
- **Basic Arithmetic:** Addition, subtraction, multiplication, division, negation, equality comparison, multi-number sums, and multi-number products.
- **Conjugates & Modulus:** Complex conjugate ($\bar{z} = a - bi$), double conjugate identity ($\bar{\bar{z}} = z$), modulus ($|z| = \sqrt{a^2 + b^2}$), principal argument ($\text{Arg}(z) \in (-\pi, \pi]$), and reciprocal ($z^{-1} = 1/z$).
- **Identities Verification:** Verifies $z + \bar{z} = 2\text{Re}(z)$, $z - \bar{z} = 2i\text{Im}(z)$, and $z\bar{z} = |z|^2$.
- **Polar & Exponential:** Seamless conversion between Rectangular ($a + bi$), Polar ($r, \theta$), Exponential ($r e^{i\theta}$), and Trigonometric ($r(\cos\theta + i\sin\theta)$) representations.
- **Powers & Roots:** Arbitrary integer powers, cyclically reduced powers of $i$ ($i^k$), principal square roots, all $n$ distinct $n$-th roots, De Moivre's theorem expansions, and roots of unity.
- **Advanced Operations:** Complex linear equation solver ($az + b = c$), complex quadratic solver ($az^2 + bz + c = 0$), distance between numbers ($|z_1 - z_2|$), normalization to unit modulus ($z / |z|$), and multiplicative inverse verification.

### 2. Step-by-Step Pedagogical Explanations
- Every calculation produces understandable algebraic derivations rendered via MathJax LaTeX.
- Demonstrates application of distributive properties, substitution of $i^2 = -1$, realization of denominators using conjugates, discriminant evaluations, and angle calculations.

### 3. Interactive Complex Plane Visualization
- Built with HTML5 Canvas with HiDPI / Retina device pixel ratio scaling.
- Renders real and imaginary axes, grid lines, vector arrows with arrowheads, coordinate ticks, and hover tooltips showing $a + bi$, $|z|$, and $\theta$.
- Plots $n$-th roots as regular polygons inscribed inside circles of radius $r^{1/n}$.
- Interactive panning (click & drag), zooming (mouse wheel or buttons), and auto-scaling reset.

### 4. Learning Center
- 20 comprehensive, original lessons with definitions, formulas, worked examples, common pitfalls, and "Try in Calculator" presets.

### 5. Interactive Practice & Quizzes
- Dynamic question generation across multiple topics and difficulty tiers (Beginner, Intermediate, Advanced).
- Evaluates answers using component-wise numerical tolerance ($\varepsilon < 0.05$) to avoid false rejections due to formatting differences.
- Provides progressive hints, revealed worked solutions, and persistent score/streak counters.

### 6. Calculation History & Theme Persistence
- Browser-local calculation history stored in `localStorage` without external tracking.
- Re-open past calculations, copy results, copy LaTeX, and export calculation logs as `.txt` files.
- Light and Dark theme modes with instant switching.

---

## 🛠️ Technology Stack

- **Backend:** Python 3.11+ (Flask 3.1, SymPy 1.14, NumPy 2.4, Python standard `cmath` & `math`).
- **Parsing:** Safe AST parser with strict token whitelisting (zero `eval()` usage).
- **Frontend:** Semantic HTML5, CSS3 with responsive custom properties, Vanilla JavaScript (ES6+).
- **Math Rendering:** MathJax v3 for TeX/LaTeX formulas.
- **Testing:** pytest 9.1 with 56 automated unit and integration tests.

---

## 📁 Project Structure

```
ComplexLab/
│
├── app.py                     # Main Flask server and REST API routes
├── requirements.txt           # Python package dependencies
├── README.md                  # Project documentation and guide
├── .gitignore                 # Git ignore rules
├── pytest.ini                 # Pytest configuration
│
├── src/                       # Backend calculation engine
│   ├── __init__.py
│   ├── complex_engine.py      # Core ComplexNum class and algebraic operations
│   ├── parser.py              # Safe AST parser for mathematical expressions
│   ├── formatter.py           # Mathematical formatting, LaTeX, fractions
│   ├── explanations.py        # Step-by-step mathematical explanation generators
│   ├── conversions.py         # Rectangular, polar, exponential, angle conversions
│   ├── roots.py               # Square roots, nth roots, roots of unity, De Moivre
│   ├── equations.py           # Linear (az+b=c) and quadratic (az^2+bz+c=0) solvers
│   └── practice.py            # Practice question generator and answer checker
│
├── templates/                 # Jinja2 HTML templates
│   ├── base.html              # Base layout with navbar, theme toggle, and MathJax
│   ├── index.html             # Calculator and interactive complex plane page
│   ├── learn.html             # 20-lesson mathematics learning center
│   ├── practice.html          # Interactive practice and quiz system
│   └── about.html             # Mathematical conventions and guide
│
├── static/                    # Frontend static assets
│   ├── css/
│   │   ├── style.css          # Design system, themes, navbar, buttons, toast
│   │   ├── calculator.css     # Calculator grid, inputs, plane canvas styles
│   │   └── responsive.css     # Mobile and tablet responsive rules
│   │
│   └── js/
│       ├── theme.js           # Light/dark mode toggle and localStorage sync
│       ├── visualization.js   # HTML5 Canvas interactive complex plane
│       ├── calculator.js      # Calculator controller, inputs, and API caller
│       ├── history.js         # Calculation history manager and export
│       ├── practice.js        # Practice questions and quiz controller
│       └── app.js             # Global utilities and toast notifications
│
└── tests/                     # Automated test suite (pytest)
    ├── test_parser.py         # AST parser tests and security checks
    ├── test_arithmetic.py     # Basic arithmetic and modulus identities
    ├── test_conjugate.py      # Conjugate operations and identities
    ├── test_modulus_argument.py # Modulus, argument, and inverse tests
    ├── test_powers_roots.py   # Powers, roots, and De Moivre tests
    ├── test_conversions.py    # Polar/rectangular/degree-radian conversions
    ├── test_equations.py      # Linear and quadratic solvers
    ├── test_api.py            # Flask endpoints, validation, and status codes
    └── test_practice.py       # Practice question generation and answer verification
```

---

## 🚀 Installation & Local Setup

### 1. Clone or Open the Project
Navigate to the project root directory in PowerShell:
```powershell
cd ComplexLab
```

### 2. Create and Activate a Virtual Environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Run the Flask Server
```powershell
python app.py
```

The application will start on:
**[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🧪 Running Automated Tests

Run the complete test suite with `pytest`:
```powershell
python -m pytest -v
```

All 56 tests covering parser safety, mathematical operations, identities, roots, equations, conversions, and API routes will execute.

---

## 🔌 API Endpoint Documentation

| Method | Endpoint | Description | Sample Payload |
|---|---|---|---|
| `GET` | `/api/health` | Health status and metadata | N/A |
| `POST` | `/api/calculate` | Perform arithmetic and unary operations | `{"operation": "multiply", "z1": "3+4i", "z2": "2-i"}` |
| `POST` | `/api/convert` | Convert rectangular, polar, or angles | `{"mode": "rectangular_to_all", "z": "1+i"}` |
| `POST` | `/api/roots` | N-th roots, square roots, De Moivre | `{"type": "nth_roots", "z": "16", "n": 4}` |
| `POST` | `/api/equation/solve` | Solve complex linear or quadratic | `{"type": "quadratic", "a": "1", "b": "-2", "c": "5"}` |
| `POST` | `/api/practice/generate` | Generate random verified question | `{"topic": "arithmetic", "difficulty": "beginner"}` |
| `POST` | `/api/practice/check` | Verify user answer with tolerance | `{"question": {...}, "answer": "10+5i"}` |

---

## 🔣 Supported Input Formats

The parser safely processes the following notations without using Python's `eval()`:
- Standard complex numbers: `3 + 4i`, `3 - 4i`, `-2 + 5i`
- Imaginary unit notation: accepts both `i` and `j` (e.g. `3 + 4j`, `7j`, `-j`)
- Pure imaginary numbers: `7i`, `-7i`, `i`, `-i`
- Pure real numbers: `5`, `-3`, `0`, `0 + 0i`
- Decimals and fractions: `1.5 + 2.75i`, `1/2 + 3/4i`, `3/4i`
- Parentheses and compound expressions: `(2 - 3i) * (1 + i)`
- Mathematical constants: `pi`, `e`

---

## 📐 Mathematical Conventions

1. **Standard Form:** Complex numbers are defined as $z = a + bi$ where $a = \text{Re}(z) \in \mathbb{R}$, $b = \text{Im}(z) \in \mathbb{R}$, and $i^2 = -1$.
2. **Principal Argument:** $\text{Arg}(z) \in (-\pi, \pi]$ radians. The argument for $z = 0$ is undefined.
3. **Branch Cuts:** Standard branch cut along the negative real axis $(-\infty, 0]$ for square roots and complex logarithm.
4. **Division & Inverse:** Multiplicative inverse $z^{-1} = 1/z$ exists for all $z \neq 0$. Zero denominator requests return HTTP 422 with a descriptive error.

---

## ⚠️ Known Limitations
- General complex-base powers ($z_1^{z_2}$) calculate the principal branch value $\exp(z_2 \text{Ln}(z_1))$.
- Root degrees $n$ are constrained to $1 \le n \le 100$ to ensure crisp canvas rendering.
