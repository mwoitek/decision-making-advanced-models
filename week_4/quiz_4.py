# %%
import pulp as pl

# %%
# Define the decision variables
decision_vars = [pl.LpVariable(f"x_{i}", lowBound=0, cat=pl.LpInteger) for i in range(1, 4)]

# %%
# Define the problem and add the objective function
prob = pl.LpProblem("ElectronicProducts", pl.LpMaximize)
prob += pl.lpSum(c * x for c, x in zip([75, 50, 35], decision_vars))

# %%
# Add the remaining constraints
all_coeffs = [
    [1, 1, 0],
    [1, 0, 0],
    [2, 2, 1],
    [1, 1, 0],
    [2, 1, 1],
]
upper_bounds = [450, 250, 800, 450, 600]
for coeffs, bound in zip(all_coeffs, upper_bounds):
    prob += pl.lpSum(c * x for c, x in zip(coeffs, decision_vars)) <= bound

# %%
# Solve the problem
prob.solve(pl.PULP_CBC_CMD(msg=False))
status = pl.LpStatus[prob.status]
assert status == "Optimal", "Could not find the optimal solution"

# %%
# Print the optimal solution
sol = []
for p, x in zip(["TVs", "Stereos", "Speakers"], decision_vars):
    val = int(pl.value(x))  # pyright: ignore
    sol.append(val)
    print(f"{p} = {val}")

# %%
# Unused inventory
parts = ["Chassis", "Picture Tube", "Speaker Cone", "Power Supply", "Electronics"]
unused = []
for coeffs, bound in zip(all_coeffs, upper_bounds):
    unused.append(bound - sum(c * x for c, x in zip(coeffs, sol)))
print("These parts will have unused inventory:")
for p, u in zip(parts, unused):
    if u > 0:
        print(p)

# %%
max_profit = int(pl.value(prob.objective))
print(f"Maximum profit = {max_profit}")
