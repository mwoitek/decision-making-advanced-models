# %%
import pulp as pl

# %%
# Define the decision variables
c1 = pl.LpVariable("C_1", lowBound=600, cat=pl.LpInteger)
c2 = pl.LpVariable("C_2", cat=pl.LpInteger)
t1 = pl.LpVariable("T_1", lowBound=300, cat=pl.LpInteger)
t2 = pl.LpVariable("T_2", cat=pl.LpInteger)

# %%
# Define the problem and add the objective function
prob = pl.LpProblem("CarManufacturing", pl.LpMinimize)
prob += 700 * c1 + 750 * c2 + 1100 * t1 + 1350 * t2 - 360000

# %%
# Add the remaining constraints
prob += c1 + t1 <= 1000
prob += c2 + t2 <= 1000
prob += 2 * c1 - 3 * t1 >= 0
prob += 2 * c2 - 3 * t2 >= 0
prob += c1 + 2 * t1 <= 1500
prob += c2 + 2 * t2 <= 1500
prob += c1 + c2 >= 900
prob += t1 + t2 >= 600

# %%
# Solve the problem
prob.solve(pl.PULP_CBC_CMD(msg=False))
status = pl.LpStatus[prob.status]
assert status == "Optimal", "Could not find the optimal solution"

# %%
# Print the optimal solution
for decision_var in [c1, t1, c2, t2]:
    print(f"{decision_var.name} = {int(pl.value(decision_var))}")  # pyright: ignore

# %%
# Print the minimum cost
min_cost = int(pl.value(prob.objective))
print(f"Minimum cost = ${min_cost}")

# %%
# How much steel needs to be purchased every month
s1 = int(c1.varValue + 2 * t1.varValue)  # pyright: ignore
s2 = int(c2.varValue + 2 * t2.varValue)  # pyright: ignore
print(f"S_1 = {s1}")
print(f"S_2 = {s2}")
