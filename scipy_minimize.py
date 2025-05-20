from scipy.optimize import minimize
from functools import partial
import numpy as np
import einops

xab = [0.08, 0.04, 0.24, 0.04,
       0.36, 0.06, 0.06, 0.12]

P_XAB = np.array(xab).reshape((2,2,2))
for (a,b,x) in np.ndindex(P_XAB.shape):
    print(f"P(A={a},B={b},X={x}) = {float(P_XAB[x, a, b])}")


def Q_XAB_giv_AS(vars: list) -> np.ndarray:
  return np.array(vars).reshape((2,2,2,2))
def Q_AB_giv_AS(vars: list) -> np.ndarray:
  return einops.reduce(Q_XAB_giv_AS(vars), 'X A AS B -> A AS B', 'sum')
def Q_XB_giv_AS(vars: list) -> np.ndarray:
  return einops.reduce(Q_XAB_giv_AS(vars), 'X A AS B -> X AS B', 'sum')
# def Q_XA_giv_AS(vars: list) -> np.ndarray:
#   return einops.reduce(Q_XAB_giv_AS(vars), 'X A AS B -> X A AS', 'sum')
# def Q_X_giv_AS(vars: list) -> np.ndarray:
#   return einops.reduce(Q_XAB_giv_AS(vars), 'X A AS B -> X AS', 'sum')
# def Q_A_giv_AS(vars: list) -> np.ndarray:
#   return einops.reduce(Q_XAB_giv_AS(vars), 'X A AS B -> A AS', 'sum')
def Q_B_giv_AS(vars: list) -> np.ndarray:
  return einops.reduce(Q_XAB_giv_AS(vars), 'X A AS B -> AS B', 'sum')
def Q_null_giv_AS(vars: list) -> np.ndarray:
  return einops.reduce(Q_XAB_giv_AS(vars), 'X A AS B -> AS', 'sum')




def objective(vars):
  # minimize Q(B = 1 | A# = 1)
  return Q_B_giv_AS(vars)[1,1]

def d_sep2(vars: list) -> np.ndarray:
  return Q_XB_giv_AS(vars)[0,:,:] - Q_XB_giv_AS(vars)[1,:,:]
def d_sep2_constraint(a_s: int, b: int) -> callable:
  return {'type':'eq', 'fun': (lambda vars: d_sep2(vars)[a_s, b])}

def consistency_constraint(x: int, a: int, b: int) -> callable:
  return {'type':'eq', 'fun': (lambda vars: Q_XAB_giv_AS(vars)[x, a, a, b] - P_XAB[x, a, b])}


def normalization(vars: list) -> np.ndarray:
  return Q_null_giv_AS(vars) - 1
def normalization_constraint(a_s: int) -> callable:
  return {'type':'eq', 'fun': (lambda vars: normalization(vars)[a_s])}

constraints = []
for a_s in range(2):
  for b in range(2):
    constraints.append(d_sep2_constraint(a_s, b))

for x in range(2):
  for a in range(2):
    for b in range(2):
      constraints.append(consistency_constraint(x, a, b))

for a_s in range(2):
  constraints.append(normalization_constraint(a_s))


initial = [0.1] * 16

bounds = [(0, 1)] * 16

result = minimize(objective, initial, method='trust-constr', constraints=constraints, bounds=bounds)

print()
print("Q(XAB|A#=0)         Q(XAB|A#=1)")
for i in range(4):
  for j in range(4):
    print(f'{result.x[i*4 + j]:.6f}', end="  ")
  print()
print()

print()
print("     Q(B=1|A#=1) ≥", result.fun)
print("      P(A=1,B=1) =", P_XAB[:,1,1].sum())
print(" Q(A=0,B=1|A#=1) =", Q_AB_giv_AS(result.x)[0, 1, 1])
print(" Q(A=1,B=1|A#=1) =", Q_AB_giv_AS(result.x)[1, 1, 1])
print("         Q(A#=1) =", Q_null_giv_AS(result.x)[1])
print("         Q(A#=0) =", Q_null_giv_AS(result.x)[0])
