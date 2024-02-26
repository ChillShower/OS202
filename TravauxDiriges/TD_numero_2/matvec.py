# Produit matrice-vecteur v = A.u
import numpy as np
from mpi4py import MPI
import time as t

# Dimension du problème (peut-être changé)
dim = 120
# Initialisation de la matrice
A = np.array([[(i+j) % dim+1. for i in range(dim)] for j in range(dim)])
#print(f"A = {A}")

# Initialisation du vecteur u
u = np.array([i+1. for i in range(dim)])
#print(f"u = {u}")

# Produit matrice-vecteur
"""
t_init= t.time()
v = A.dot(u)
t_final=t.time()

print(f"v = {v}")
print ("temps non parrallélisé ="+str(t_final-t_init))"""

## question 1
"""
t_init=t.time()
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
comm_size = comm.Get_size()

nb_col_per_process= dim//comm_size

a=rank*nb_col_per_process #première colonne
if rank!=comm_size-1:
    b= a+nb_col_per_process #dernière colonne
else:
    b=dim

localresult=A[a:b,:].dot(u) #calcul dans un processus

results= comm.gather(localresult,root=0)#renvoie des résultats

if rank==0:
    v=np.hstack(results) #stackage des résultats
    t_final= t.time()
    print("temps parallélisation colonne="+str(t_final-t_init))"""

#question 2:

t_init=t.time()
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
comm_size = comm.Get_size()

nb_col_per_process= dim//comm_size

a=rank*nb_col_per_process #première colonne
if rank!=comm_size-1:
    b= a+nb_col_per_process #dernière colonne
else:
    b=dim

localresult=A[:,a:b].dot(u[a:b]) #calcul dans un processus

results= comm.gather(localresult,root=0)#renvoie des résultats

if rank==0:
    v=results[0]
    for k in range(1,comm_size):
        v+= results[k]
    t_final= t.time()
    print(v)
    print("temps parallélisation ligne="+str(t_final-t_init))


