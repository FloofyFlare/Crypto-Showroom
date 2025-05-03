import numpy as np
import re
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import sympy
import random

def get_random_prime(start, end):
    primes = list(sympy.primerange(start, end))
    return random.choice(primes)

def power(a, b, p):
    if b == 1:
        return a
    else:
        return pow(a, b) % p
  # Got implementation from geeksforgeeks

def bxor_numpy(b1, b2):
    n_b1 = np.frombuffer(b1, dtype='uint8')
    n_b2 = np.frombuffer(b2, dtype='uint8')

    return (n_b1 ^ n_b2).tobytes()
    ##Got implementation from https://tutorial.eyehunts.com/python/python-xor-bytes/

def is_alpha(str):
  return bool(re.fullmatch(r'[a-zA-Z]+', str))

def validmsg() -> str:
  userinput = ""
  while True:
        userinput = input("Provide a provide a message in the set [Aa-Zz] " \
        "to encode \n message: ")
        userinput = userinput.replace(" ","")
        userinput = userinput.lower()
        if is_alpha(userinput):
          break
        print("Your message does not follow the [a-zA-Z] set")
        
  return userinput

def classical():
  print("\n#############################################")
  print("Which classical cipher would you like to try: \n" \
  "   Ceasar(1)\n" \
  "   Vigenère(2)")
  userinput = input("enter choice here: ")
  
  encoded = ""
  frequencytable = {}
  match userinput:
    case "1":
      randKey = np.random.randint(1,27)
      print(f"KEY: {randKey}")
      userinput = validmsg()
      for c in userinput:
        cint = ((ord(c) - 97 + randKey ) % 27) + 97
        encoded += chr(cint)
        original = frequencytable.get((c,chr(cint)))
        frequencytable[c, chr(cint)] = frequencytable.get((c,chr(cint)), 0) + 1
      print(f"encoded result: {encoded}")
      print("frequency analysis:")
      print(frequencytable)
    case "2":
      randKey = ""
      for i in range(1,19):
        randKey += chr(97 + np.random.randint(1,27))
      print(f"{randKey} is the key with length 19")
      userinput = validmsg()
      counter = 0
      for c in userinput:
        cint = ((ord(c) - ord(randKey[counter % 18])) % 27) + 97
        encoded += chr(cint)
        original = frequencytable.get((c,chr(cint)))
        frequencytable[c, chr(cint)] = frequencytable.get((c,chr(cint)), 0) + 1
        counter += 1
      print(f"before encoding: {userinput}\nencoded result:  {encoded}")
      print("frequency analysis:")
      print(frequencytable)
      print("the weekness lies in reapeated common words with the same mapping try \n" \
      " 'the cat went with Will the manager'. You'll see that the encoding for 'the' is used twice neat right?")
    case _:
      classical()

def one_time():
  print("\n#############################################")
  userinput = input("Provide a message of your choice to encrypt \n" \
  "enter here: ")
  key = os.urandom(len(userinput))
  print(f"KEY: {key}")
  print(f"your message '{userinput}' encrypted is")
  ciphertext = bxor_numpy(bytes(userinput, 'utf-8'),key)
  print(f"your message XOR key = {ciphertext}")
  input("Press enter to decrypt")
  decoded_ciphertext = str(bxor_numpy(ciphertext,key))
  print(f"Your ciphertext XOR key = {decoded_ciphertext}")
  print("Do the same vulnerabilities in Vegengère exist here? (Anwser no)")

def numeric_key() -> int:
  userinput = ""
  while True:
        userinput = input("Provide a provide a numeric (int) for you private key" \
        " to encode messages: ")
        userinput = userinput.replace(" ","")
        if userinput.isnumeric():
          break
        print("Your provided private key is not an integer!")
        
  return int(userinput)

def get_key_from_secret(secret):
    return hashlib.sha256(str(secret).encode()).digest()

def yes_or_no():
  while True:
        userinput = input("Respond y or n:")
        userinput = userinput.replace(" ","")
        userinput = userinput.lower()
        if userinput[0] == "y":
           return True
        if userinput[0] == "n":
           return False
        print("Your message does not follow yes or no (y/n)format")

def secure_convo():
  #Using Diffie Hellman
  # Example usage
  print("#############################################")
  print("Diffie Hellman with Rose for verification")
  pubprime = get_random_prime(10, 200)
  pubroot = np.random.randint(1,400)
  input(f"The public key you and Rose decided was prime number {pubprime} and primitive root {pubroot} \n"\
         "press enter to continue")
  userpriv = numeric_key()
  x = power(pubroot, userpriv, pubprime)
  rosepriv = np.random.randint(1,400)
  y = power(pubroot, rosepriv, pubprime)
  usersk = power(y,userpriv,pubprime)
  rosesk = power(x,rosepriv,pubprime)
  print("You recieved the shared secret key:", usersk)
  print("#############################################")
  print("As a real estate agent your in a chat with Rose a prospective home owner")
  key = get_key_from_secret(rosesk)
  cipher = AES.new(key, AES.MODE_CBC)  # Initialize AES in CBC mode
  iv = cipher.iv
  rosemsg = "Hello i'm looking for a house is the house in CA avaliable?"
  encrypted_msg = cipher.encrypt(pad(rosemsg.encode(), AES.block_size))
  print(f"Rose: {encrypted_msg.hex()}")
  input("decript?")
  key = get_key_from_secret(usersk)
  decipher = AES.new(key, AES.MODE_CBC, iv=iv)
  decrypted_msg = unpad(decipher.decrypt(encrypted_msg), AES.block_size).decode()
  print(f"Rose: {decrypted_msg}")
  if yes_or_no :
    rosemsg = "Great! lets get on a call and talk more about it"
    encrypted_msg = cipher.encrypt(pad(rosemsg.encode(), AES.block_size))
    print(f"Rose: {encrypted_msg.hex()}")
    input("decript?")
    key = get_key_from_secret(usersk)
    decipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted_msg = unpad(decipher.decrypt(encrypted_msg), AES.block_size).decode()
    print(f"Rose: {decrypted_msg}")
  else:
    rosemsg = "Ok thanks, let me konw if anything changes"
    encrypted_msg = cipher.encrypt(pad(rosemsg.encode(), AES.block_size))
    print(f"Rose: {encrypted_msg.hex()}")
    input("decript?")
    key = get_key_from_secret(usersk)
    decipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted_msg = unpad(decipher.decrypt(encrypted_msg), AES.block_size).decode()
    print(f"Rose: {decrypted_msg}")

  




def cryptoShowroom():
  print("Would you like to try: \n" \
  "   classical ciphers(1)\n" \
  "   one-time pad(2)\n" \
  "   A public-key conversation(3)")
  userinput = input("enter choice here: ")
  match userinput:
    case "1":
      classical()
    case "2":
      one_time()
    case "3":
      secure_convo()
    case _:
      cryptoShowroom()

print("Welcome to the cryptography showroom")
# use BouncyCastle for pivate public key encryption
cryptoShowroom()