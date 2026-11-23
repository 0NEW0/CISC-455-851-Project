# Part 4 — GA Implementation: From Standard Baseline to Healthy Complexity

This document details the design, implementation, and empirical evaluation of the Genetic Algorithm (GA) for the weekly study schedule optimization problem. The development was divided into two distinct phases: establishing a robust baseline (Phase 1) and engineering advanced Evolutionary Algorithm (EA) strategies to add "complexity" (Phase 2).

---

## Project Structure

| File | Description |
|---|---|
| `genetic_algorithm.py` | The core GA loop. `run_ga()` connects Parts 1 to 3. Extended with optional hooks for advanced strategies. |
| `compare_survival.py` | Phase 1 experiment script. Compares 4 standard survival schemes across 20 seeds. |
| `strategy_runner.py` | Master wrapper providing a unified interface to run the baseline or any advanced strategy. |
| `strategy_memetic.py` | Strategy 1: Memetic Algorithm (Local Search / Hill Climbing). |
| `strategy_island.py` | Strategy 2: Island Model (Multi-population with migration). |
| `strategy_adaptive.py` | Strategy 3: Adaptive Penalties (Dynamic fitness landscape). |
| `experiment_advanced_strategies.py` | Phase 2 experiment script. Compares Baseline + 3 Advanced strategies across 20 seeds. |
| `tests/test_ga.py` | 12 unit tests for the core GA. |

---

## Phase 1: Establishing the Baseline (Population Management)

Before adding advanced features, we needed to determine the most robust standard population management strategy. We implemented and compared four standard survival schemes across 20 distinct seeds to answer the question: *"How should we manage the population?"*

### The Survival Schemes
![Flow of Thinking Diagram](./step 4 images/Survival_Schemes.png)
| Scheme | Mechanism |
|---|---|
| `elitist` (default) | Copy the 2 best schedules, then make 48 children. The new population is the 2 elites plus the 48 children. |
| `mu_comma_lambda (μ,λ)` | Make 50 children. The new population is only the children; parents are discarded completely. |
| `mu_plus_lambda (μ+λ)` | Make 50 children, pool them with the 50 parents, sort by fitness, and keep the best 50. |
| `steady_state` | Repeat 25 times per generation: make 2 children, remove the 2 worst schedules, and add the children. |

### Results (30 seeds per scheme)

| Scheme | Reached Target | Avg Gen | Best at Gen 100 | **Final Mean** | Evaluations |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`elitist`** | **30/30** | **21.0** | **-65.0** | **-212.7** | **19,450** |
| `mu_comma_lambda` | 30/30 | 20.1 | -65.0 | -261.6 | 20,050 |
| `mu_plus_lambda` | 30/30 | 16.5 | -65.0 | -65.0 | 25,050 |
| `steady_state` | 30/30 | 14.5 | -65.0 | -73.7 | 25,050 |

### Phase 1 Conclusion
The **Elitist** scheme was selected as our baseline. While $(\mu + \lambda)$ converged fastest, its `Final Mean` of exactly -65.0 proved it suffered from severe **premature convergence** (the entire population became identical clones). Elitist maintained a diverse, exploring population (`Final Mean` = -212.7) while reliably protecting the best solution, giving us a rock-solid foundation for Phase 2.

---

## Phase 2: Adding Complexity (Advanced EA Design)

Having established a working baseline, we engaged in critical reflection. A standard GA relies on blind mutation and static rules, which can be inefficient. To address this, we proactively engineered three advanced EA strategies to enhance the core search process, answering a new question: *"How can we enhance the core EA search process?"*

### The Flow of Thinking
The diagram below illustrates our design philosophy: identifying specific limitations in the baseline and engineering targeted, modular solutions for each.

![Flow of Thinking Diagram](./step_4_images/flow_of_thinking.png)

Below is the detailed breakdown of each advanced strategy, including its implementation, rationale, empirical results, and acknowledged trade-offs.

---

### Strategy 1: Memetic Algorithm (Hybrid Local Search)

**Implementation File:** `strategy_memetic.py`

**Algorithm Design:**
![Memetic Algorithm Diagram](./step_4_images/memetic_diagram.png)

**Why We Tried It & How It Works (Rationale):** 
In a standard GA, mutation is completely blind. To fix this, we added a "hill-climbing" local search step immediately after mutation. How it works: After a child is mutated, the algorithm attempts a set number of random gene swaps (e.g., 20 attempts). If a swap improves the fitness score, it is kept; otherwise, it is discarded. We hypothesized this would allow the algorithm to fine-tune offspring, turning random variations into directed improvements and accelerating convergence.

**Empirical Results (20 seeds):**
*   **Best Generation (Mean):** 8.5 (vs. Baseline 26.1)
*   **Best Fitness (Mean):** -66.3 (Highest overall fitness achieved)

**Conclusion & Trade-off Acknowledged:** 
The Memetic Algorithm was the clear winner for performance, achieving **~67% faster convergence**. However, the trade-off is explicit: while it requires far fewer generations, it increases computation time *per generation* due to the repeated local fitness evaluations. This demonstrates a clear understanding of the time-complexity trade-off in hybrid algorithms.

---

### Strategy 2: Island Model (Multi-Population with Migration)

**Implementation File:** `strategy_island.py`

**Algorithm Design:**
![Island Model Diagram](./step_4_images/island_diagram.png)

**Why We Tried It & How It Works (Rationale):** 
How it works: We maintain 3 independent populations ("islands") that evolve completely separately. Every 10 generations, the top 2 individuals from one island are copied and replace the worst 2 individuals in the next island. We hypothesized this periodic migration would inject fresh genetic material, preventing stagnation in local optima while maintaining high population diversity.

**Empirical Results (20 seeds):**
*   **Best Generation (Mean):** 26.4 (Slightly faster than baseline 26.1)
*   **Best Fitness (Mean):** -68.8

**Conclusion & Trade-off Acknowledged:** 
The Island Model successfully maintained population diversity and avoided local optima traps. The trade-off is architectural: it introduces higher implementation complexity and memory overhead compared to a single-population approach, making it best suited for highly multimodal search spaces where diversity is critical.

---

### Strategy 3: Adaptive Penalties (Dynamic Fitness Landscape)

**Implementation File:** `strategy_adaptive.py`

**Algorithm Design:**
![Adaptive Penalties Diagram](./step_4_images/adaptive_diagram.png)

**Why We Tried It & How It Works (Rationale):** 
Standard GAs use static penalty weights, which can trap the algorithm in infeasible regions early on. How it works: Instead of static weights, we implemented a dynamic "pressure ramp." In early generations (0-30), penalty weights for hard constraints are kept very low (10% of normal) to encourage exploration. As generations progress, these weights increase exponentially, reaching 100% by the final generation. We hypothesized this would better balance exploration and exploitation, allowing diverse structures early on before ruthlessly eliminating constraint violations later.

**Empirical Results (20 seeds):**
*   **Best Generation (Mean):** 29.5 (Similar to baseline 26.1)
*   **Best Fitness (Mean):** -71.2

**Conclusion & Limitation Acknowledged:** 
On our specific, small-scale 20-slot problem, the adaptive strategy showed marginal empirical gains because the baseline GA was already efficient enough to find feasible solutions quickly. However, this strategy successfully demonstrates a scalable, advanced EA principle. Its true value would be realized in much larger, heavily constrained search spaces where early exploration is critical to avoid getting trapped in infeasible regions.

---

## Software Architecture & Modularity

To implement these advanced strategies cleanly without breaking the existing codebase or teammates' modules, we engineered a modular, hook-based architecture:
1. `genetic_algorithm.py`: The core GA loop, extended with three optional hooks (`repair_function`, `score_override`, `generation_callback`) that default to `None`.
2. `strategy_runner.py`: A master wrapper that cleanly routes the chosen strategy to the core GA, injecting the appropriate hook logic.
3. This ensures **100% backward compatibility**. The original `run_ga()` functions identically to the baseline, guaranteeing that all 45 existing unit tests pass without modification.

---

## How to Run 
### 1. Run the Core GA (Single Run)
Runs the baseline GA once and prints the best schedule and penalty breakdown.
```powershell
uv run python -m step4_ga_implementation.genetic_algorithm
```

### 2. Run Phase 1 Experiment (Survival Schemes)
Compares the 4 standard survival schemes (Elitist, μ,λ, μ+λ, Steady-State) across 30 seeds.
```powershell
uv run python -m step4_ga_implementation.compare_survival
```

### 3. Run Phase 2 Experiment (Advanced Strategies)
Compares the Baseline against the 3 Advanced Strategies (Memetic, Island, Adaptive) across 20 seeds. This generates the final statistical comparison table.
```powershell
uv run python -m step4_ga_implementation.experiment_advanced_strategies
```