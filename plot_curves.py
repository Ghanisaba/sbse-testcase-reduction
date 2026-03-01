import pandas as pd
import matplotlib.pyplot as plt


def main():
    # Load median convergence curves
    random_curve = pd.read_csv("curve_random.csv", header=None).iloc[:, 0]
    elitist_curve = pd.read_csv("curve_elitist.csv", header=None).iloc[:, 0]

    # Create plot
    plt.figure(figsize=(8, 5))
    plt.plot(random_curve, label="A) Pure Random Sampling (Median Best-So-Far)")
    plt.plot(elitist_curve, label="C) Elitist Random Search (Median Best-So-Far)")

    plt.xlabel("Fitness Evaluations")
    plt.ylabel("Median Best-So-Far Fitness")
    plt.title("Convergence Comparison (30 Independent Seeds)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Save plot
    plt.savefig("convergence.png", dpi=300)
    print("Saved convergence.png successfully.")


if __name__ == "__main__":
    main()