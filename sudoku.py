#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import itertools
import math
import sys
import os
"""Sudoku"""

def var(i,j,k):
    """Return the literal Xijk.
    """
    return (1,i,j,k)

def neg(l):
    """Return the negation of the literal l.
    """
    (s,i,j,k) = l
    return (-s,i,j,k)

def initial_configuration():
    """Return the initial configuration of the example in td6.pdf
    
    >>> cnf = initial_configuration()
    >>> [(1, 1, 4, 4)] in cnf
    True
    >>> [(1, 2, 1, 2)] in cnf
    True
    >>> [(1, 2, 3, 1)] in cnf
    False
    """
    return [[var(1,4,4)],[var(2,1,2)],[var(3,2,1)],[var(4,3,1)]]

def at_least_one(L):
    """Return a cnf that represents the constraint: at least one of the
    literals in the list L is true.
    
    >>> lst = [var(1, 1, 1), var(2, 2, 2), var(3, 3, 3)]
    >>> cnf = at_least_one(lst)
    >>> len(cnf)
    1
    >>> clause = cnf[0]
    >>> len(clause)
    3
    >>> clause.sort()
    >>> clause == [var(1, 1, 1), var(2, 2, 2), var(3, 3, 3)]
    True
    """
    return [[i for i in L]] # à compléter

def at_most_one(L):
    """Return a cnf that represents the constraint: at most one of the
    literals in the list L is true
    
    >>> lst = [var(1, 1, 1), var(2, 2, 2), var(3, 3, 3)]
    >>> cnf = at_most_one(lst)
    >>> len(cnf)
    3
    >>> cnf[0].sort()
    >>> cnf[1].sort()
    >>> cnf[2].sort()
    >>> cnf.sort()
    >>> cnf == [[neg(var(1,1,1)), neg(var(2,2,2))], \
    [neg(var(1,1,1)), neg(var(3,3,3))], \
    [neg(var(2,2,2)), neg(var(3,3,3))]]
    True
    """
    l = []
    for x in itertools.combinations(L, 2):
        l += [[neg(a) for a in x]]
    return l # à compléter

def assignment_rules(N):
    """Return a list of clauses describing the rules for the assignment (i,j) -> k.
    """
    cnf = []
    for i in range(1,N+1):
        for j in range(1,N+1):
            tmp = [var(i,j,k) for k in range(1,N+1)]
            cnf.extend(at_least_one(tmp))
            cnf.extend(at_most_one(tmp))
            # add clauses to cnf saying that (i,j) contains 
            # *exactly* one of the digits k=1..N
            # à compléter
    return cnf

def row_rules(N):
    """Return a list of clauses describing the rules for the rows.
    """
    cnf = []
    for i in range(1, N+1):
        for k in range(1, N+1):
            tmp = [var(i,j,k) for j in range(1, N+1)]
            cnf.extend(at_least_one(tmp))
            cnf.extend(at_most_one(tmp))
    return cnf # à compléter

def column_rules(N):
    """Return a list of clauses describing the rules for the columns.
    """
    cnf = []
    for j in range(1, N+1):
        for k in range(1, N+1):
            tmp = [var(i,j,k) for i in range(1,N+1)]
            cnf.extend(at_least_one(tmp))
            cnf.extend(at_most_one(tmp))
    return cnf # à compléter

def subgrid_rules(N):
    """Return a list of clauses describing the rules for the subgrids.
    """
    size_sub = int(math.sqrt(N))
    cnf = []
    for si in range(0, size_sub):
        for sj in range(0, size_sub):
            for k in range(1, N+1):
                tmp = [var(i,j,k) for i in range((size_sub*si) +1, (size_sub*(si+1)) + 1) for j in range((size_sub*sj) +1, (size_sub*(sj+1)) +1)]
                cnf.extend(at_least_one(tmp))
                cnf.extend(at_most_one(tmp))


    return cnf # à compléter

def generate_rules(N):
    """Return a list of clauses describing the rules of the game.
    """
    cnf = []    
    cnf.extend(assignment_rules(N))
    cnf.extend(row_rules(N))
    cnf.extend(column_rules(N))
    cnf.extend(subgrid_rules(N))
    return cnf

def literal_to_integer(l, N):
    """Return the external representation of the literal l.

    >>> literal_to_integer(var(1,2,3), 4)
    7
    >>> literal_to_integer(neg(var(3,2,1)), 4)
    -37
    >>> literal_to_integer(var(1,4,4), 4)
    16
    """
    s,i,j,k = l
    return int(s *(math.pow(N,2) * (i-1) + N * (j-1) + k)) # à compléter


def to_cnf_file(path, cnf, N):
    stri = "p cnf " + str(int(math.pow(N,3))) + " " + str(len(cnf)) + "\n"
    for clauses in cnf:
        stri += " ".join([str(literal_to_integer(clause, N)) for clause in clauses])
        stri += " 0\n"
    f = open(path,"w")
    f.write(stri)
    f.close()

def read_text(path):
    f = open(path,"r")
    lines = [l.rstrip().split(" ") for l in f.readlines()]
    N = int(lines[0][0])
    cnf = [[var(i,j+1,int(lines[i][j]))] for i in range(1, len(lines)) for j in range(len(lines[i])) if lines[i][j] != '0']
    cnf += generate_rules(N)
    to_cnf_file("sudoku.cnf", cnf, N)
    f.close()
    return N
    
def read_result(N):
    f = open("sudoku.out","r")
    lines = [l.rstrip().split(" ") for l in f.readlines()]
    if lines[0][0] == "UNSAT":
        return "no satisfactory answer could be found"
    else:
        ok = [v for v in lines[1] if int(v) > 0]
        count = 0
        stri = ""
        for i in ok:
            if int(i) % N == 0:
                stri += str(N) + " "
            else:
                stri += str(int(i) % N) + " "
            count += 1
            if count == N:
                count = 0
                stri += "\n"
        return stri


def main(path):
    import doctest
    doctest.testmod()
    N = read_text(path)
    print(len(subgrid_rules(4)))
    os.system("minisat sudoku.cnf sudoku.out > tmp.txt")
    print(read_result(N))



if __name__ == "__main__":
    main(sys.argv[1])
