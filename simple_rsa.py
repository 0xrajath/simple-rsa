import random

# Function to get random bit
def random_bit():
    rand_num = random.randint(0,4294967295) # Random number between 0 and 2^32-1
    bin_rand_num = format(rand_num, '032b') # 32-bit binary representation of Random number
    lsb_bit = rand_num & 1 # LSB bit of Random number

    return lsb_bit,bin_rand_num,rand_num


def main():

    #Printing random number
    print("line:124")
    final_rand_num = 1 # b_7
    final_rand_num = final_rand_num << 1 # Bit shift by 1 to left
    
    for i in range(5,0,-1):
        rand_bit,bin_rand_num,rand_num = random_bit()

        final_rand_num = final_rand_num + rand_bit #Adding new random bit to final random number
        final_rand_num = final_rand_num << 1 # Bit shift by 1 to left

        print("b_"+str(i)+"|"+bin_rand_num+"|"+str(rand_bit))
    
    final_rand_num = final_rand_num + 1 #b_0
    print("Number|"+str(final_rand_num)+"|"+format(final_rand_num, '032b'))



if __name__ == "__main__":
    main()