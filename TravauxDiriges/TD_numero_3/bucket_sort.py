import numpy as np
from mpi4py import MPI
import time as t
import random

#génération d'un tableau

dim=10000 #arbitraire à modifier

tab=np.array([random.randint(1,dim) for _ in range(dim)])##création d'un tableau aléatoire de valeur

#print(tab)

t_init=t.time()
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
comm_size = comm.Get_size()

nb_elt_per_process= dim//comm_size

a=rank*nb_elt_per_process #rang du premier élément
if rank!=comm_size-1:
    b= a+nb_elt_per_process #dernière colonne
else:
    b=dim

local_array=tab[a:b] #array spécifique au processus

## algorithme de tri pour mon tableau
for i in range(1, len(local_array)):
    key = local_array[i]
    j = i - 1
    while j >= 0 and local_array[j] > key:
        local_array[j + 1] = local_array[j]
        j -= 1
    local_array[j + 1] = key

results= comm.gather(local_array,root=0) #renvoi des données en 0

if (rank==0):
    sorted=np.empty(dim)
    ind_list=[0 for _ in range(comm_size)] #liste des indices initialement 0
    size_list=[np.size(results[i]) for i in range(comm_size)]#liste des tailles des listes
    tot_ind=0
    print(results)
    while ind_list !=size_list:
        cur=dim+2
        best_process=-1
        for i in range(comm_size):
            cur_ind=ind_list[i]
            if cur_ind!=size_list[i]:
                if results[i][cur_ind]<cur:
                    best_process=i
                    cur=results[i][cur_ind]
        if best_process!=-1:
            sorted[tot_ind]=cur
            ind_list[best_process]+=1
            tot_ind+=1
        else:
            break
    final_time=t.time()
    #print(sorted)
    #print(len(sorted))
    #print(sorted[99])
    print("temps total= "+str(final_time-t_init))


