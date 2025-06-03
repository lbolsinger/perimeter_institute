import numpy as np
from gurobipy import Model, GRB

# P(x=0) = 0.4, P(x=1) = 0.6
p = np.zeros((2, 2, 2))

#P(ab|x)
p[0, 0, 0] = 0.08/0.4
p[0, 0, 1] = 0.36/0.6
p[0, 1, 0] = 0.04/0.4
p[0, 1, 1] = 0.06/0.6

p[1, 0, 0] = 0.24/0.4
p[1, 0, 1] = 0.06/0.6
p[1, 1, 0] = 0.04/0.4
p[1, 1, 1] = 0.12/0.6

m = Model("New Model")
#Q(ab|xa#)
q = m.addMVar((2, 2, 2, 2), lb=0, ub=1)

# consistency
m.addConstrs(q[a, b, x, a] == p[a, b, x] for a in range(2) for b in range(2) for x in range(2))

# d-sep
m.addConstrs(sum(q[a0, b, 1, a_s] for a0 in range(2)) == sum(q[a1, b, 0, a_s] for a1 in range(2)) for b in range(2) for a_s in range(2))
m.addConstrs(sum(q[a, b, x, 0] for b in range(2)) == sum(q[a, b, x, 1] for b in range(2)) for a in range(2) for x in range(2))

# normalization
m.addConstrs(sum(q[a, b, x, a_s] for a in range(2) for b in range(2)) == 1 for a_s in range(2) for x in range(2))

m.setObjective(sum(q[a, 1, 0, 1] for a in range(2)), GRB.MINIMIZE)

m.optimize()

print(m.objVal)

for (a, b, x, a_s) in np.ndindex(q.x.shape):
    print(f"P(A={a}, B={b} | X={x}, A#={a_s}) = {float(q.x[a, b, x, a_s]):.2f}")
