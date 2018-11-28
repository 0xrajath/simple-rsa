import random

# Function to get random bit
def random_bit():
    rand_num = random.randint(0,4294967295) # Random number between 0 and 2^32-1
    bin_rand_num = format(rand_num, '032b') # 32-bit binary representation of Random number
    lsb_bit = rand_num & 1 # LSB bit of Random number

    return lsb_bit,bin_rand_num,rand_num

# Function to get 7-bit random number
def random_num_7bit():
    rand_num = 1 # b_7
    rand_num = rand_num << 1 # Bit shift by 1 to left
    
    for i in range(5,0,-1):
        rand_bit,_,_ = random_bit()
        rand_num = rand_num + rand_bit #Adding new random bit to final random number
        rand_num = rand_num << 1 # Bit shift by 1 to left
    
    rand_num = rand_num + 1 #b_0
    return rand_num

# Function to get 'a' for Miller-Rabin
def get_a(n):
    return random.randint(1,n-1)

# Miller-Rabin Primality Testing
def primality_testing(n,a):
    x = n-1
    k = len(bin(x))-3
    y = 1

    j=2
    for i in range(k,-1,-1):
        z = y
        xi = bin(x)[j] # Getting xi binary number
        y = (y*y)%n
        if y==1 and z!=1 and z!=n-1:
            # Bad Square Root: n is not prime
            return False 
        if xi=='1':
            y = (y*a)%n
        j+=1

    if y!=1:
        # Bad final value
        return False
    else:
        return True

# Function to check if Prime using 20 rounds of Miller-Rabin
def is_prime(n):
    for i in range(20):
        a = get_a(n)
        if not primality_testing(n,a):
            # It is not Prime if it fails Miller-Rabin Primality Test
            return False
    # It is Prime if it passes for 20 a's
    return True

# Extended Euclidean Algorithm to get Multiplicative Inverse and GCD
def extended_euclidean_algorithm(bigger_num, smaller_num):
    ri = bigger_num
    ri_1 = smaller_num
    ri_2 = -1

    qi = -1
    qi_1 = -1
    qi_2 = -1

    si = -1
    si_1 = -1
    si_2 = -1

    ti = -1
    ti_1 = -1
    ti_2 = -1

    i = 1

    while True:
        if i == 1:
            si_2 = 1
            si = 1

            ti_2 = 0
            ti = 0
        elif i == 2:
            qi_1 = qi

            si_1 = 0
            si = 0

            ti_1 = 1
            ti = 1
        else:
            qi_2 = qi_1
            qi_1 = qi

            si = si_2 - (qi_2*si_1)
            si_2 = si_1
            si_1 = si

            ti = ti_2 - (qi_2*ti_1)
            ti_2 = ti_1
            ti_1 = ti

        if ri_1 == 0:
            return ti,ri #Return (Multiplicative Inverse, GCD)

        qi = int(ri/ri_1)
        ri_2 = ri%ri_1

        i+=1
        ri = ri_1
        ri_1 = ri_2


def main():

    # Line 124: Printing random number
    print("line:124")
    rand_num = 1 # b_7
    rand_num = rand_num << 1 # Bit shift by 1 to left
    
    for i in range(5,0,-1):
        rand_bit,bin_rand_num,_ = random_bit()

        rand_num = rand_num + rand_bit #Adding new random bit to final random number
        rand_num = rand_num << 1 # Bit shift by 1 to left

        print("b_"+str(i)+"|"+bin_rand_num+"|"+str(rand_bit))
    
    rand_num = rand_num + 1 #b_0
    print("Number|"+str(rand_num)+"|"+format(rand_num, '032b'))


    # Empty Line
    print()


    #Line 139: Failed Miller-Rabin Primality Test
    n = -1
    a = -1
    print("line:139")

    #Finding n and a for which n is not prime
    while True:
        n = random_num_7bit()
        a = get_a(n)
        if not primality_testing(n,a):
            break

    print("n = "+str(n)+", a = "+str(a))
    print("i |xi |z |y |y ")

    #Miller-Rabin Primality Testing
    x = n-1
    k = len(bin(x))-3
    y = 1

    j=2
    for i in range(k,-1,-1):
        z = y
        xi = bin(x)[j] # Getting xi binary number
        y = (y*y)%n
        #if y==1 and z!=1 and z!=n-1:
            # Bad Square Root: n is not prime

        if xi=='1':
            y_new = (y*a)%n
        else:
            y_new = y
        j+=1
        print(str(i)+" |"+xi+" |"+str(z)+" |"+str(y)+" |"+str(y_new))
        y = y_new

    if y!=1:
        # Bad final value
        print(str(n)+" is not a prime because "+str(a)+"^"+str(x)+" mod "+str(n)+" != 1") #22 is not a prime because 7^21 mod 22 != 1
    else:
        print(str(n)+" is perhaps a prime")
    

    # Empty Line
    print()


    #Line 145: Passed Miller-Rabin Primality Test
    n = -1
    a = -1
    print("line:145")

    #Finding n and a for which n is prime
    while True:
        n = random_num_7bit()
        a = get_a(n)
        if primality_testing(n,a):
            break

    print("n = "+str(n)+", a = "+str(a))
    print("i |xi |z |y |y ")

    #Miller-Rabin Primality Testing
    x = n-1
    k = len(bin(x))-3
    y = 1

    j=2
    for i in range(k,-1,-1):
        z = y
        xi = bin(x)[j] # Getting xi binary number
        y = (y*y)%n
        #if y==1 and z!=1 and z!=n-1:
            # Bad Square Root: n is not prime

        if xi=='1':
            y_new = (y*a)%n
        else:
            y_new = y
        j+=1
        print(str(i)+" |"+xi+" |"+str(z)+" |"+str(y)+" |"+str(y_new))
        y = y_new

    if y!=1:
        # Bad final value
        print(str(n)+" is not a prime because "+str(a)+"^"+str(x)+" mod "+str(n)+" != 1") #22 is not a prime because 7^21 mod 22 != 1
    else:
        print(str(n)+" is perhaps a prime")

    
    # Empty Line
    print()


    #Calculating p and q
    p = -1
    q = -1
    #Assigning p
    if is_prime(n):
        p = n
    else: #For the case that earlier calculated prime n is not actually a prime after testing for 20 a's
        while True:
            n = random_num_7bit()
            if is_prime(n):
                p = n
                break
    
    print("p:",p)
    #Assigning q
    while True:
        n = random_num_7bit()
        if is_prime(n):
            q = n
            if q != p: #Checking that p and q are not equal
                break
    
    print("q",q)
    #Calculating n
    n = p*q
    print("n:",n)
    #Calculating phi(n)
    phi_n = (p-1)*(q-1)
    print("phi(n):",phi_n)


    # Extended Euclidean Algorithm
    ri = 5904
    ri_1 = 5
    ri_2 = -1

    qi = -1
    qi_1 = -1
    qi_2 = -1

    si = -1
    si_1 = -1
    si_2 = -1

    ti = -1
    ti_1 = -1
    ti_2 = -1

    i = 1

    print("i |qi |r |ri+1 |ri+2 |si |ti")
    while True:
        if i == 1:
            si_2 = 1
            si = 1

            ti_2 = 0
            ti = 0
        elif i == 2:
            qi_1 = qi

            si_1 = 0
            si = 0

            ti_1 = 1
            ti = 1
        else:
            qi_2 = qi_1
            qi_1 = qi

            si = si_2 - (qi_2*si_1)
            si_2 = si_1
            si_1 = si

            ti = ti_2 - (qi_2*ti_1)
            ti_2 = ti_1
            ti_1 = ti

        if ri_1 == 0:
            print(str(i)+" |  |"+str(ri)+" |  |  |"+str(si)+" |"+str(ti))
            break

        qi = int(ri/ri_1)
        ri_2 = ri%ri_1
        print(str(i)+" |"+str(qi)+" |"+str(ri)+" |"+str(ri_1)+" |"+str(ri_2)+" |"+str(si)+" |"+str(ti))

        i+=1
        ri = ri_1
        ri_1 = ri_2


    print()
    mi,gcd = extended_euclidean_algorithm(4620,13)
    print(mi,gcd)




if __name__ == "__main__":
    main()