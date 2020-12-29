import numpy as np
import os
import math
from math import gcd
from collections import Counter
import collections
from sympy.core.numbers import mod_inverse

def create_equations(ainput,binput,m,elem):             #Creating list for a, b, m
    ainput.append(int(elem[0]))
    binput.append(int(elem[1]))
    m.append(int(elem[2]))

def primeFactors(n):                                    #Finding prime factorization (with powers) of numbers 
    m=[]
    while n % 2 == 0:  
        m.append(int(2))
        n = n / 2
    for i in range(3,int(math.sqrt(n))+1,2): 
        while n % i== 0: 
            m.append(int(i))
            n = n / i 
    if n > 2: 
        m.append(int(n))
    count=Counter(m)
    return count

def gcd(p,q):                                           # Finding GCD of two numbers
    while q != 0:
        p, q = q, p%q
    return p

def is_coprime(x, y):                                   # Check if numbers are coprime
    return gcd(x, y) == 1

def check_conditions_form(a,m,no_of_eqs):               # Checking if m's are coprime and reducing equations if possible
                                                            # x=a mod m1 x=b mod m2 (a-b)|gcd(m1,m2)
    flag2=1
    for i in range(0,no_of_eqs-1):
        flag=0
        for j in range(i+1,no_of_eqs):
            if(is_coprime(m[i],m[j])==False):
                num=a[i]-a[j]
                if(num%gcd(m[i],m[j])==0):
                    if(m[i]>=m[j] and m[i]%m[j]==0):
                        m.remove(m[j])
                        a.remove(a[j])
                    elif(m[i]<m[j] and m[j]%m[i]==0):
                        m.remove(m[i])
                        a.remove(a[i])
                    flag2=-1
                    return flag2
                else:
                    raise Exception("Solutions does not exist")
    return flag2
                    
def check_conditions_forb(ainput,binput,m,no_of_eqs):               # Checking gcd(a,m) divides b for equation ax ~ b (mod m)
    for i in range(0,no_of_eqs):
        g=gcd(ainput[i],m[i])
        if(binput[i]%g!=0):
            raise Exception('GCD of '+str(ainput[i])+ ' and ' +str(m[i])+' does not divide '+ str(binput[i])+' not able to find solution using CRT')


def process_eq(a,m,no_of_eqs):                                      # Processing equations if m's are not coprime and then trying to apply CRT 
    flag=0
    for i in range(0,no_of_eqs-1):
        for j in range(i+1,no_of_eqs):
            if(is_coprime(m[i],m[j])==False):
                flag=1
    if(flag==1):
        anew=[]
        mnew=[]
        count={}
        for i in range(no_of_eqs):
            count=primeFactors(m[i])
            for j in count:
                anew.append(a[i])
                mnew.append(pow(j,count[j]))
        return anew,mnew
    else:
        return a,m 


if __name__ == '__main__':
    ainput=[]
    binput=[]
    m=[]
    dirname = os.getcwd()
    filename = os.path.join(dirname,'input.txt')                        # Reading input equations from input.txt file
    with open(filename,'r') as f:
        lines = f.readlines()
        no_of_eqs=int(lines[0])
    for i in range(1,no_of_eqs+1):
        elem = lines[i].split()
        create_equations(ainput,binput,m, elem)

    print("Original Equations "+"\n")
    for i in range(no_of_eqs):
        print(str(ainput[i])+"x ~ "+str(binput[i])+" (mod "+str(m[i])+")")
    print("\n")

    check_conditions_forb(ainput,binput,m,no_of_eqs)                    # Calling function to check conditions on 'b'
    
    a=[]
    for i in range(0,no_of_eqs):
        a.append((mod_inverse(ainput[i],m[i])*binput[i])%m[i])          # Converting equation to x ~ a (mod m)
    
    flag2=-1                                                            # Checking if m are coprime and reducing equations if possible
    while(flag2==-1):
        flag2=check_conditions_form(a,m,no_of_eqs)
        if(flag2==-1):
            no_of_eqs-=1


    no_of_eqs=len(m)
    a,m=process_eq(a,m,no_of_eqs)                                       # Updating equations (breaking a into its prime factors)

    no_of_eqs=len(m)                                                    # Checking if m are coprime and reducing equations if possible
    flag2=-1
    while(flag2==-1):
        flag2=check_conditions_form(a,m,no_of_eqs)
        if(flag2==-1):
            no_of_eqs-=1

    print("Updated Equations "+"\n")
    for i in range(no_of_eqs):
        print("x ~ "+str(a[i])+" (mod "+str(m[i])+")")
    print("\n")

    M=np.prod(m)                                                        # Product of all m's

    b=[]                                                                # Calculating b[i]'s needed for finding solution later
    for i in range(0,no_of_eqs):
        temp1=1
        for j in range(0,no_of_eqs):
            if(j!=i):
                temp1=temp1*m[j]    
        temp=mod_inverse(temp1,m[i])
        b.append(temp)

    x=0
    for i in range(0,no_of_eqs):                                        # Finding x using CRT algorithm
        temp1=1
        for j in range(0,no_of_eqs):
            if(j!=i):
                temp1=temp1*m[j]
        x=x+(temp1*b[i]*a[i])
    x=x%M
    print("Solution of congruence equations is = " + str(int(x))+" mod "+str(M))