# %%
import pulp as pl

# %%
rates = [0.14, 0.13, 0.12, 0.125, 0.1]
probs = [0.1, 0.07, 0.03, 0.05, 0.02]

# %%
coeffs = [round(r * (1 - p) - p, ndigits=5) for r, p in zip(rates, probs)]
coeffs

# %%
" + ".join(f"{coeff} * x_{i}" for i, coeff in enumerate(coeffs, start=1))

# %%
# Define the decision variables
decision_vars = [pl.LpVariable(f"x_{i}", lowBound=0) for i in range(1, 6)]

# %%
# Define the problem and add the objective function
prob = pl.LpProblem("BankingLoan", pl.LpMaximize)
prob += pl.lpSum(c * x for c, x in zip(coeffs, decision_vars))

# %%
# Add the constraints
prob += pl.lpSum(decision_vars) <= 10
prob += pl.lpSum(c * x for c, x in zip([0.3, 0.3, 0.3, -0.7, -0.7], decision_vars)) <= 0
prob += pl.lpSum(c * x for c, x in zip([0.4, 0.4, -0.6], decision_vars[:3])) <= 0
prob += pl.lpSum(c * x for c, x in zip([0.06, 0.03, -0.01, 0.01, -0.02], decision_vars)) <= 0

# %%
# Solve the problem
prob.solve(pl.PULP_CBC_CMD(msg=False))
status = pl.LpStatus[prob.status]
assert status == "Optimal", "Could not find optimal solution"

# %%
max_return = pl.value(prob.objective)
print(f"Maximum net return (in $ millions): {max_return}")

# %%
loan_types = sum(pl.value(x) > 0 for x in decision_vars)  # pyright: ignore
print(f"Number of loan types: {loan_types}")

# %%
for t, x in zip(["Home", "Commercial"], [decision_vars[2], decision_vars[4]]):
    print(f"{t}: ${pl.value(x)} million")
