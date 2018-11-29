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
            found_mult_inverse = False
            if ri==1:
                found_mult_inverse = True
                while ti < 0: # Normalizing Multiplicative Inverse
                    ti = ti + bigger_num


            return ti,ri,found_mult_inverse #Return (Multiplicative Inverse, GCD, Yes/No Multiplicative Inverse)

        qi = int(ri/ri_1)
        ri_2 = ri%ri_1

        i+=1
        ri = ri_1
        ri_1 = ri_2


# Function to generate RSA Keys. Public Key: (n,e) ; Private Key: (n,d)
def generate_rsa_keys():
    found_e = False

    while not found_e: # In the rare case that an e was not found
        #Calculating p and q
        p = -1
        q = -1
        
        #Assigning p
        while True:
            n = random_num_7bit()
            if is_prime(n):
                p = n
                break
        
        #Assigning q
        while True:
            n = random_num_7bit()
            if is_prime(n):
                q = n
                if q != p: #Checking that p and q are not equal
                    break
        
        #Calculating n
        n = p*q
        #Calculating phi(n)
        phi_n = (p-1)*(q-1)

        e = 3 #Starting to check with e=3
        d = -1
        found_mult_inverse = False

        while (not found_mult_inverse) and e < phi_n:
            mult_inv,gcd,found_mult_inverse = extended_euclidean_algorithm(phi_n,e)

            if not found_mult_inverse:
                e+=1
            else: # Found Multiplicative Inverse as GCD = 1
                found_e = True
                d = mult_inv

    return p,q,n,e,d
    
    


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
    
    #Assigning q
    while True:
        n = random_num_7bit()
        if is_prime(n):
            q = n
            if q != p: #Checking that p and q are not equal
                break
    
    #Calculating n
    n = p*q

    #Calculating phi(n)
    phi_n = (p-1)*(q-1)


    # Line 162: Finding e and d
    print("line:162")

    e = 3 #Starting to check with e=3
    d = -1
    found_mult_inverse = False

    while not found_mult_inverse:
        print("e = "+str(e))
        # Extended Euclidean Algorithm
        ri = phi_n
        ri_1 = e
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
                
                if ri==1:
                    found_mult_inverse = True
                    while ti < 0: # Normalizing Multiplicative Inverse
                        ti = ti + phi_n
                    d = ti

                print(str(i)+" |  |"+str(ri)+" |  |  |"+str(si)+" |"+str(ti))
                break

            qi = int(ri/ri_1)
            ri_2 = ri%ri_1
            print(str(i)+" |"+str(qi)+" |"+str(ri)+" |"+str(ri_1)+" |"+str(ri_2)+" |"+str(si)+" |"+str(ti))

            i+=1
            ri = ri_1
            ri_1 = ri_2

        if not found_mult_inverse:
            e+=1


    # Empty Line
    print()


    # Line 173: Printing d
    print("line:173")
    print("d = "+str(d))


    # Empty Line
    print()


    # Line 177: Printing Alice's Keys
    print("line:177")
    print("p = "+str(p)+", q = "+str(q)+", n = "+str(n)+", e = "+str(e)+", d = "+str(d))
    print("p = "+format(p, '032b'))
    print("q = "+format(q, '032b'))
    print("n = "+format(n, '032b'))
    print("e = "+format(e, '032b'))
    print("d = "+format(d, '032b'))


    # Empty Line
    print()


    # Line 185: Printing Trent's Keys
    print("line:185")
    pt,qt,nt,et,dt = generate_rsa_keys()
    print("p = "+str(pt)+", q = "+str(qt)+", n = "+str(nt)+", e = "+str(et)+", d = "+str(dt))
    print("p = "+format(pt, '032b'))
    print("q = "+format(qt, '032b'))
    print("n = "+format(nt, '032b'))
    print("e = "+format(et, '032b'))
    print("d = "+format(dt, '032b'))


    # Empty Line
    print()





if __name__ == "__main__":
    main()