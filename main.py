import random
import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Dict, List, Tuple

# -----------------------------
# Data loading
# -----------------------------
def load_dataset(tests_csv: str, coverage_csv: str):
    import pandas as pd
    import numpy as np

    tests = pd.read_csv(tests_csv)
    cov = pd.read_csv(coverage_csv)

    # Normalize IDs (fix spaces/case like "T1 " vs "t1")
    tests["test_id"] = tests["test_id"].astype(str).str.strip().str.lower()
    cov["test_id"] = cov["test_id"].astype(str).str.strip().str.lower()

    # Keep only e* columns from coverage
    element_cols = [c for c in cov.columns if c.startswith("e")]

    # If coverage has duplicates, OR them (max across rows)
    cov[element_cols] = cov[element_cols].apply(pd.to_numeric, errors="coerce").fillna(0).astype(int)
    cov = cov.groupby("test_id", as_index=False)[element_cols].max()

    # Merge (THIS replaces the assert)
    merged = tests.merge(cov, on="test_id", how="inner")

    # Print helpful warnings if something is missing
    missing_in_cov = sorted(set(tests["test_id"]) - set(cov["test_id"]))
    missing_in_tests = sorted(set(cov["test_id"]) - set(tests["test_id"]))

    if missing_in_cov:
        print("WARNING: tests.csv has test_id not in coverage.csv:", missing_in_cov)
    if missing_in_tests:
        print("WARNING: coverage.csv has test_id not in tests.csv:", missing_in_tests)

    # Sort for stable ordering
    merged = merged.sort_values("test_id").reset_index(drop=True)

    test_ids = list(merged["test_id"])
    times = merged["time"].to_numpy(dtype=float)
    C = merged[element_cols].to_numpy(dtype=int)

    return test_ids, times, C, element_cols

# -----------------------------
# Fitness
# -----------------------------
@dataclass
class FitnessConfig:
    alpha: float = 0.15     # time weight
    lam: float = 3.0        # missing coverage penalty weight

class TestSuiteProblem:
    def __init__(self, times: np.ndarray, C: np.ndarray, cfg: FitnessConfig):
        self.times = times
        self.C = C
        self.T, self.E = C.shape
        self.cfg = cfg
        self.Tmax = float(times.sum())

    def evaluate(self, x: np.ndarray) -> float:
        # x: {0,1}^T
        total_time = float((x * self.times).sum())
        time_norm = total_time / self.Tmax if self.Tmax > 0 else 0.0

        # union coverage
        covered = (x @ self.C) > 0       # shape (E,)
        cov_count = int(covered.sum())
        r = cov_count / self.E
        m = 1.0 - r

        # maximize
        F = (r) - (self.cfg.alpha * time_norm) - (self.cfg.lam * m)
        return float(F)

# -----------------------------
# Encoding + operators
# -----------------------------
def random_solution(T: int, rng: random.Random, p: float = 0.5) -> np.ndarray:
    return np.array([1 if rng.random() < p else 0 for _ in range(T)], dtype=int)

def op_flip_one(x: np.ndarray, rng: random.Random) -> np.ndarray:
    y = x.copy()
    i = rng.randrange(len(y))
    y[i] = 1 - y[i]
    return y

def op_flip_two(x: np.ndarray, rng: random.Random) -> np.ndarray:
    y = x.copy()
    i = rng.randrange(len(y))
    k = rng.randrange(len(y) - 1)
    if k >= i:
        k += 1
    y[i] = 1 - y[i]
    y[k] = 1 - y[k]
    return y

OPERATORS = [op_flip_one, op_flip_two]

# -----------------------------
# Random Search variants
# -----------------------------
def pure_random_sampling(problem: TestSuiteProblem, budget: int, seed: int, init_p: float = 0.5):
    rng = random.Random(seed)
    best_F = -1e18
    best_x = None
    best_curve = []

    for _ in range(budget):
        x = random_solution(problem.T, rng, p=init_p)
        F = problem.evaluate(x)
        if F > best_F:
            best_F = F
            best_x = x
        best_curve.append(best_F)

    return best_F, best_x, np.array(best_curve, dtype=float)

def elitist_random_search(problem: TestSuiteProblem, budget: int, seed: int, init_p: float = 0.5):
    rng = random.Random(seed)
    x_best = random_solution(problem.T, rng, p=init_p)
    F_best = problem.evaluate(x_best)
    best_curve = [F_best]

    for _ in range(budget - 1):
        op = rng.choice(OPERATORS)
        x_new = op(x_best, rng)
        F_new = problem.evaluate(x_new)
        if F_new > F_best:
            x_best, F_best = x_new, F_new
        best_curve.append(F_best)

    return F_best, x_best, np.array(best_curve, dtype=float)

# -----------------------------
# Experiment runner (>=30 seeds)
# -----------------------------
def run_experiment(tests_csv: str, coverage_csv: str,
                   budget: int = 10_000, seeds: int = 30,
                   alpha: float = 0.15, lam: float = 3.0, init_p: float = 0.5):

    test_ids, times, C, elements = load_dataset(tests_csv, coverage_csv)
    problem = TestSuiteProblem(times, C, FitnessConfig(alpha=alpha, lam=lam))

    algos = {
        "A_pure_random": pure_random_sampling,
        "C_elitist": elitist_random_search
    }

    results = {}
    curves = {}

    for name, algo in algos.items():
        final_F = []
        all_curves = []

        for s in range(seeds):
            seed = 1000 + s  # fixed, reproducible seed schedule
            F, x, curve = algo(problem, budget=budget, seed=seed, init_p=init_p)
            final_F.append(F)
            all_curves.append(curve)

        final_F = np.array(final_F, dtype=float)
        all_curves = np.stack(all_curves, axis=0)  # (seeds, budget)

        results[name] = {
            "min": float(np.min(final_F)),
            "median": float(np.median(final_F)),
            "max": float(np.max(final_F)),
            "all_final": final_F
        }

        curves[name] = {
            "median_curve": np.median(all_curves, axis=0),
            "all_curves": all_curves
        }

    return test_ids, elements, problem, results, curves

# -----------------------------
# Optional plotting (matplotlib only; no manual colors)
# -----------------------------
def plot_convergence(curves: Dict[str, Dict[str, np.ndarray]]):
    import matplotlib.pyplot as plt

    plt.figure()
    for name, obj in curves.items():
        plt.plot(obj["median_curve"], label=name)
    plt.xlabel("Fitness evaluations")
    plt.ylabel("Median best-so-far fitness")
    plt.title("Convergence (median over seeds)")
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Example run (edit paths as needed)
    test_ids, elements, problem, results, curves = run_experiment(
        tests_csv="tests.csv",
        coverage_csv="coverage.csv",
        budget=10_000,
        seeds=30,
        alpha=0.15,
        lam=3.0,
        init_p=0.5
    )

    print("Final fitness distribution (min/median/max):")
    for name, stats in results.items():
        print(f"{name}: {stats['min']:.4f} / {stats['median']:.4f} / {stats['max']:.4f}")

    plot_convergence(curves)  # uncomment if you want plots
    

np.savetxt("curve_random.csv", curves["A_pure_random"]["median_curve"], delimiter=",")
np.savetxt("curve_elitist.csv", curves["C_elitist"]["median_curve"], delimiter=",")
print("Saved median convergence curves to curve_random.csv and curve_elitist.csv")