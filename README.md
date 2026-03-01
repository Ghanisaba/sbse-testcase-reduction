Test Suite Reduction via Random Search

Search-Based Software Engineering (SBSE) Assignment

📘 Assignment Introduction

This assignment investigates Test Suite Reduction as a combinatorial optimization problem within the domain of Search-Based Software Engineering (SBSE). The goal is to model regression test selection mathematically and apply stochastic search techniques to minimize execution cost while preserving structural coverage. Two variants of Random Search are implemented and experimentally evaluated to analyze their convergence behavior and solution quality under a fixed evaluation budget.

📌 Project Overview

This project formulates the test suite reduction problem as an optimization task and implements two baseline random-search algorithms:

A) Pure Random Sampling

C) Elitist Random Search

The objective is to select a subset of regression tests that:

Maximizes structural coverage

Minimizes total execution time

Enforces full coverage as a constraint

📂 Repository Structure
Implementation/
│
├── main.py
├── tests.csv
├── coverage.csv
├── curve_random.csv
├── curve_elitist.csv
├── plot_curves.py
└── README.md
📊 Dataset Description

The dataset consists of:

1️⃣ tests.csv
test_id,time

30 regression tests (t1–t30)

Each test has an associated execution time

2️⃣ coverage.csv
test_id,e1,e2,...,e20

Binary coverage matrix (0/1 values)

20 structural program elements

A value of 1 indicates coverage

🧠 Problem Formulation
🔹 Solution Encoding

A candidate solution is represented as a binary vector:

𝑥
∈
{
0
,
1
}
30
x∈{0,1}
30

Where:

x_i = 1 → test 
𝑡
𝑖
t
i
	​

 is selected

x_i = 0 → test 
𝑡
𝑖
t
i
	​

 is excluded

Search space size:

2
30
2
30
🔹 Fitness Function

The scalar fitness function is defined as:

𝐹
(
𝑥
)
=
𝑟
(
𝑥
)
−
𝛼
𝑇
^
(
𝑥
)
−
𝜆
𝑚
(
𝑥
)
F(x)=r(x)−α
T
^
(x)−λm(x)

Where:

𝑟
(
𝑥
)
r(x) = coverage ratio

𝑇
^
(
𝑥
)
T
^
(x) = normalized execution time

𝑚
(
𝑥
)
m(x) = missing coverage ratio

Parameters:

𝛼
=
0.15
α=0.15 (time trade-off weight)

𝜆
=
3.0
λ=3.0 (constraint penalty weight)

Full structural coverage is enforced via penalty-based constraint handling.

🔄 Search Operators

Two mutation operators are implemented:

1️⃣ Single-Bit Flip

Flips one randomly selected test decision

Local search move (Hamming distance = 1)

2️⃣ Two-Bit Flip

Flips two randomly selected test decisions

Moderately disruptive move (Hamming distance = 2)

🚀 Algorithms Implemented
A) Pure Random Sampling

Independently samples new candidate solutions

Tracks best-so-far solution

Serves as baseline without exploitation

C) Elitist Random Search

Maintains incumbent best solution

Applies mutation operators

Accepts only improving solutions

Introduces exploitation of promising regions

🧪 Experimental Setup

Evaluation budget: 10,000 fitness evaluations

Independent runs: 30 seeds per algorithm

Fixed random seeds for reproducibility

Median best-so-far fitness recorded

Convergence curves generated

📈 Experimental Results

Final fitness distribution (min / median / max):

Algorithm	Min	Median	Max
Pure Random	0.7398	0.7451	0.7507
Elitist RS	0.7612	0.7629	0.7669
🔍 Key Observation

Elitist Random Search consistently outperforms Pure Random Sampling, demonstrating the advantage of exploitation in stochastic optimization.

📊 Convergence Curves

Median convergence curves are stored as:

curve_random.csv

curve_elitist.csv

To generate the convergence plot:

python plot_curves.py

This produces:

convergence.png
▶️ How to Run
1️⃣ Install Dependencies
python -m pip install numpy pandas matplotlib
2️⃣ Execute Experiment
python main.py

Example Output:

Final fitness distribution (min/median/max):
A_pure_random: 0.7398 / 0.7451 / 0.7507
C_elitist: 0.7612 / 0.7629 / 0.7669
Saved median convergence curves to curve_random.csv and curve_elitist.csv
