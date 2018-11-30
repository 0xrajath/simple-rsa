Simple RSA
-----------------------------------------------

A simple RSA implementation.

How is it different from a regular RSA implementation?
- This uses small integers in order to avoid the precise arithmetic involved in using long integers.
- This uses the inbuilt 'random' function to help in generating random bits. Ideally we would want good random number generation.
- This uses a fairly simple hash function.
- Decryption will not involve nonces.

Steps to run:
`python3 simple_rsa.py`


