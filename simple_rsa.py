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


# Fast Exponentiation
def fast_exponentiation(n,a,x):
    k = len(bin(x))-3
    y = 1

    j=2
    for i in range(k,-1,-1):
        xi = bin(x)[j] # Getting xi binary number
        y = (y*y)%n
        if xi=='1':
            y = (y*a)%n
        j+=1

    return y

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


# XOR between two bytes of data
def byte_xor(a,b):
    s0 = str(int(a[0])^int(b[0]))
    s1 = str(int(a[1])^int(b[1]))
    s2 = str(int(a[2])^int(b[2]))
    s3 = str(int(a[3])^int(b[3]))
    s4 = str(int(a[4])^int(b[4]))
    s5 = str(int(a[5])^int(b[5]))
    s6 = str(int(a[6])^int(b[6]))
    s7 = str(int(a[7])^int(b[7]))
    
    return s0 + s1 + s2 + s3 + s4 + s5 + s6 + s7


# Simple hash function that XOR's byte-by-byte and returns respective int value
def hash_simple(bit_string):
    byte_list = []

    for i in range(0,len(bit_string),8):
        byte_list.append(bit_string[i:i+8])

    while len(byte_list) > 1:
        byte_list[1] = byte_xor(byte_list[0],byte_list[1])
        byte_list = byte_list[1:]

    return int(byte_list[0], 2)


# Decrypting or Signing 'h' with Private Key (n,d)
def sign_w_priv_key(n,d,h):
    return fast_exponentiation(n,h,d)


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


    # Using The representation for 'Alice' = 32(Space),65(A),108(l),105(i),99(c),101(e)
    Alice = "001000000100000101101100011010010110001101100101"
    bytes_1_6 = Alice
    bytes_7_10 = format(n, '032b')
    bytes_11_14 = format(e, '032b')

    r = bytes_1_6 +bytes_7_10 + bytes_11_14
    h_r = hash_simple(r)
    s = sign_w_priv_key(nt,dt,h_r) # Signing with Trent's Private Key (nt,dt)
    
    # Line 207 : Alice Digital Certificate
    print("line:207")
    print("r = "+r)
    print("h(r) = "+format(h_r, '032b'))
    print("s = "+format(s, '032b'))


    # Empty Line
    print()

    # Line 209 : Alice Digital Certificate
    print("line:209")
    print("h(r) = "+str(h_r)+", s = "+str(s))





if __name__ == "__main__":
    main()