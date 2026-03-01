# Test Suite Reduction via Random Search  
_Search-Based Software Engineering (SBSE) Assignment_

---

## Overview

This project formulates **test suite reduction** as a Search-Based Software Engineering (SBSE) optimization problem and implements two variants of Random Search:

- **A) Pure Random Sampling**
- **C) Elitist Random Search**

The objective is to select a subset of tests that:

- Achieves **maximum structural coverage**
- Minimizes **total execution time**
- Enforces **full coverage as a constraint**

---

##  Repository Structure
Implementation/
│
├── main.py
├── tests.csv
├── coverage.csv
├── curve_random.csv
├── curve_elitist.csv
├── plot_curves.py
└── README.md


---

## Dataset

The dataset consists of:

### 01.tests.csv

Columns:

- 30 tests (t1–t30)
- Each test has an execution time

---

### 2️⃣ coverage.csv

Columns:

- Binary coverage matrix (0/1)
- 20 structural elements
- A value of 1 indicates coverage

---

## 🧠 Problem Formulation

### Encoding

A solution is represented as a binary vector:

\[
x \in \{0,1\}^{30}
\]

Where:
- `1` → test selected
- `0` → test excluded

Search space size:
\[
2^{30}
\]

---

### Fitness Function

\[
F(x) = r(x) - \alpha \hat{T}(x) - \lambda m(x)
\]

Where:

- \(r(x)\) = coverage ratio  
- \(\hat{T}(x)\) = normalized execution time  
- \(m(x)\) = missing coverage ratio  

Parameters:
- α = 0.15
- λ = 3.0

Full coverage is enforced via penalty.

---

## 🔄 Operators

1. **Single-bit flip**
   - Flips one test selection
   - Local mutation

2. **Two-bit flip**
   - Flips two selections
   - Moderate exploration

---

## 🚀 Algorithms Implemented

### A) Pure Random Sampling

- Independent random solutions
- Keeps best-so-far

### C) Elitist Random Search

- Mutates incumbent best solution
- Accepts only improvements

---

## 🧪 Experimental Setup

- Evaluation budget: 10,000
- 30 independent seeds
- Fixed random seeds for reproducibility
- Median best-so-far fitness tracked

---

## 📈 Results

Final fitness distribution (min / median / max):

| Algorithm | Min | Median | Max |
|------------|------|--------|------|
| Pure Random | 0.7398 | 0.7451 | 0.7507 |
| Elitist RS | 0.7612 | 0.7629 | 0.7669 |

Elitist Random Search consistently outperforms Pure Random Sampling.

---

## 📊 Convergence Curves

Median convergence curves are saved as:

- `curve_random.csv`
- `curve_elitist.csv`

To generate a plot:

convergence.png


### 1️⃣ Install Dependencies
## ▶️ How to Run

### 1️⃣ Install Dependencies


python -m pip install numpy pandas matplotlib

### 2️⃣ Run Experiment


python main.py


Output:


Final fitness distribution (min/median/max):

Saved median convergence curves to curve_random.csv and curve_elitist.csv

## 📌 Key Observations

- Elitist Random Search achieves higher median fitness.
- Penalty-based constraint handling effectively enforces full coverage.
- Even simple random search benefits from exploitation mechanisms.

## 📎 Author: Saba Ghani

SBSE Assignment – FAST NUCES  
Test Suite Reduction via Random Search

