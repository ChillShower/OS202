
# TD1

`pandoc -s --toc README.md --css=./github-pandoc.css -o README.html`





## lscpu

```
coller ici les infos *utiles* de lscpu. 
```
CPU(s):                             12
Thread(s) per core:                 2
Core(s) per socket:                 6
Socket(s):                          1
Model name:                         Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz
L1d cache:                          192 KiB
L1i cache:                          192 KiB
L2 cache:                           1.5 MiB
L3 cache:                           12 MiB

*Des infos utiles s'y trouvent : nb core, taille de cache*



## Produit matrice-matrice

./TestProductMatrix.exe 1023
Test passed
Temps CPU produit matrice-matrice naif : 1.41747 secondes
MFlops -> 1510.57

./TestProductMatrix.exe 1024
Test passed
Temps CPU produit matrice-matrice naif : 3.51473 secondes
MFlops -> 610.996

./TestProductMatrix.exe 1025
Test passed
Temps CPU produit matrice-matrice naif : 1.39084 secondes
MFlops -> 1548.55

### Permutation des boucles

*Expliquer comment est compilé le code (ligne de make ou de gcc) : on aura besoin de savoir l'optim, les paramètres, etc. Par exemple :*

`make TestProduct.exe && ./TestProduct.exe 1024`


  ordre           | time    | MFlops  | MFlops(n=2048) 
------------------|---------|---------|----------------
i,j,k (origine)   | 2.73764 | 782.476 | crash          
j,i,k             | 4.03349 | 532.413 | crash
i,k,j             | 19.6747 | 109.15  | crash
k,i,j             | 19.9865 | 107.447 | crash 
j,k,i             | 0.779407| 2755.28 | 1877.43
k,j,i             | 0.972266| 2208.74 | 1730.74


*Discussion des résultats*



### OMP sur la meilleure boucle 

`make TestProduct.exe && OMP_NUM_THREADS=8 ./TestProduct.exe 1024`

  OMP_NUM         | MFlops  | MFlops(n=2048) | MFlops(n=512)  | MFlops(n=4096)
------------------|---------|----------------|----------------|---------------
1                 |         |
2                 |         |
3                 |         |  
4                 |         |
5                 |         |
6                 |         |
7                 |         |  
8                 |         |




### Produit par blocs

`make TestProduct.exe && ./TestProduct.exe 1024`

  szBlock         | MFlops  | MFlops(n=2048) | MFlops(n=512)  | MFlops(n=4096)
------------------|---------|----------------|----------------|---------------
origine (=max)    |  |
32                |  |
64                |  |
128               |  |
256               |  |
512               |  | 
1024              |  |




### Bloc + OMP



  szBlock      | OMP_NUM | MFlops  | MFlops(n=2048) | MFlops(n=512)  | MFlops(n=4096)|
---------------|---------|---------|-------------------------------------------------|
A.nbCols       |  1      |         |                |                |               |
512            |  8      |         |                |                |               |
---------------|---------|---------|-------------------------------------------------|
Speed-up       |         |         |                |                |               |
---------------|---------|---------|-------------------------------------------------|



### Comparaison with BLAS


# Tips 

```
	env 
	OMP_NUM_THREADS=4 ./produitMatriceMatrice.exe
```

```
    $ for i in $(seq 1 4); do elap=$(OMP_NUM_THREADS=$i ./TestProductOmp.exe|grep "Temps CPU"|cut -d " " -f 7); echo -e "$i\t$elap"; done > timers.out
```
