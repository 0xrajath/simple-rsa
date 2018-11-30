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
def d_RSA(n,d,h):
    return fast_exponentiation(n,h,d)


# Encrypting or Verifying 'h' with Public Key (n,e)
def e_RSA(n,e,h):
    return fast_exponentiation(n,h,e)


def main():

    # Generating Alice's RSA Keys
    print("Generating Alice's RSA Keys")
    p_Alice,q_Alice,n_Alice,e_Alice,d_Alice = generate_rsa_keys()
    print("p = "+str(p_Alice)+", q = "+str(q_Alice)+", n = "+str(n_Alice)+", e = "+str(e_Alice)+", d = "+str(d_Alice))
    print("p = "+format(p_Alice, '032b'))
    print("q = "+format(q_Alice, '032b'))
    print("n = "+format(n_Alice, '032b'))
    print("e = "+format(e_Alice, '032b'))
    print("d = "+format(d_Alice, '032b'))


    # Empty Line
    print()


    # Generating Trent's Keys
    print("Generating Trent's RSA Keys")
    p_Trent,q_Trent,n_Trent,e_Trent,d_Trent = generate_rsa_keys()
    print("p = "+str(p_Trent)+", q = "+str(q_Trent)+", n = "+str(n_Trent)+", e = "+str(e_Trent)+", d = "+str(d_Trent))
    print("p = "+format(p_Trent, '032b'))
    print("q = "+format(q_Trent, '032b'))
    print("n = "+format(n_Trent, '032b'))
    print("e = "+format(e_Trent, '032b'))
    print("d = "+format(d_Trent, '032b'))


    # Empty Line
    print()
    print()
    print()



    # Creating Alice's Digital Certificate signed by Trent
    print("Creating Alice's Digital Certificate signed by Trent:")
    print("--------------------------------------------------------")
    print()

    # Using The representation for 'Alice' = 32(Space),65(A),108(l),105(i),99(c),101(e)
    Alice = "001000000100000101101100011010010110001101100101"
    bytes_1_6 = Alice
    bytes_7_10 = format(n_Alice, '032b')
    bytes_11_14 = format(e_Alice, '032b')

    r = bytes_1_6 +bytes_7_10 + bytes_11_14
    h_r = hash_simple(r)
    s = d_RSA(n_Trent,d_Trent,h_r) # Signing with Trent's Private Key (nt,dt)
    
    print("Alice's Digital Certificate signed by Trent")
    print("r = "+r)
    print("h(r) = "+format(h_r, '032b'))
    print("s = "+format(s, '032b'))


    # Empty Line
    print()

    print("Integer Representation of Alice's Digital Certificate signed by Trent")
    print("h(r) = "+str(h_r)+", s = "+str(s))


    # Empty Line
    print()
    print()
    print()




    # Authentication of Alice by Bob
    print("Authentication of Alice by Bob:")
    print("---------------------------------------------")
    print()

    # Generating common u among Alice and Bob
    print("Generating common u among Alice and Bob")
    k = len(bin(n_Alice)) - 3

    # Generating u which is cooperatively picked by Alice and Bob
    u = '1' # (k-1)th u
    for i in range(k-2):
        rand_bit,_,_ = random_bit()
        u = u+str(rand_bit)
    
    u = u+'1' # 0th u
    u = int(u, 2) #Converting from binary string to binary int

    h_u = hash_simple(format(u, '032b')) # Calculating h(u)

    print("k = "+str(k)+", u = "+str(u)+", h(u) = "+str(h_u))

    # Printing binary representatioin of u
    print("Binary representation of u and h(u)")
    print("u = ", format(u, '032b'))
    print("h(u) = ", format(h_u, '032b'))

    # Empty Line
    print()

    # Authentication of Alice by Bob
    print("Alice signing shared h(u)")
    v = d_RSA(n_Alice,d_Alice,h_u) # Alice signing/decrypting h(u)
    print("u = "+str(u)+", h(u) = "+str(h_u)+", v = "+str(v))
    print()

    print("Bob authenticating Alice")
    Ev = e_RSA(n_Alice,e_Alice,v) # Bob verifying Ev is equal to h(u) to authenticate Alice

    print("h(u) = "+str(h_u)+", v = "+str(v)+", Ev = "+str(Ev))
    print("Ev = h(u)")
    print("Alice authenticated by Bob!!")



if __name__ == "__main__":
    main()