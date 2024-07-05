# %%
import pulp as pl

# %%
# Define the decision variables
hired = [pl.LpVariable(f"x_H{i}", lowBound=0, cat=pl.LpInteger) for i in range(1, 7)]
fired = [pl.LpVariable(f"x_F{i}", lowBound=0, cat=pl.LpInteger) for i in range(1, 7)]

# %%
# Number of available pilots for every month
avail_pilots = [120]
for i in range(6):
    avail_pilots.append(avail_pilots[i] + hired[i] - fired[i])
avail_pilots = avail_pilots[1:]

# %%
# Define the problem and add the objective function
prob = pl.LpProblem("PilotStaffing", pl.LpMinimize)
prob += pl.lpSum(4 * avail_pilots[i] + 5 * hired[i] + 3 * fired[i] for i in range(6))

# %%
# Add the remaining constraints
lower_bounds = [100, 110, 115, 140, 110, 200]
for n, l in zip(avail_pilots, lower_bounds):
    prob += n >= l

# %%
# Solve the problem
prob.solve(pl.PULP_CBC_CMD(msg=False))
status = pl.LpStatus[prob.status]
assert status == "Optimal", "Could not find the optimal solution"

# %%
min_cost = int(pl.value(prob.objective))
print(f"Minimum cost = {min_cost}")

# %%
num_months = sum(pl.value(n) > l for n, l in zip(avail_pilots, lower_bounds))
print(f"Number of months with more pilots than the minimum = {num_months}")

# %%
hired_4 = int(pl.value(hired[3]))  # pyright: ignore
print(f"Number of pilots to hire in month 4 = {hired_4}")
