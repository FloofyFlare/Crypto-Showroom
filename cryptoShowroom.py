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
  print(f"your message '{userinput}' encrypted by one-time pad is")
  ciphertext = bxor_numpy(bytes(userinput, 'utf-8'),key)
  print(f"{ciphertext}")
  input("Press enter to decrypt")
  decoded_ciphertext = str(bxor_numpy(ciphertext,key))
  print(f"{decoded_ciphertext}")
  print("Do the same vulnerabilities in Vigenère exist here? (Anwser no)")

# I did some research on how to make good encryption functions with PyCryptodome via AI
# just to keep transparency since I've never worked with this libary before
def encrypt_message(message, key):
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv  # Store the IV
    encrypted = cipher.encrypt(pad(message.encode(), AES.block_size))
    return iv, encrypted  # Return both IV & encrypted data

def decrypt_message(encrypted, key, iv):
    decipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted = unpad(decipher.decrypt(encrypted), AES.block_size).decode()
    return decrypted

def numeric_key() -> int:
  userinput = ""
  while True:
        userinput = input("Provide a provide a numeric (int) as your private key" \
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
        userinput = input("Whats your reponse?\n 1) yes its still avaliable \n 2) no its not avaliable \n:")
        userinput = userinput.replace(" ","")
        userinput = userinput.lower()
        if userinput[0] == "1":
           return (True, "yes its still avaliable")
        if userinput[0] == "2":
           return (False, "no its not avaliable")
        print("Your message does not follow yes or no (y/n) format")

def secure_convo():
  #Using Diffie Hellman
  # Example usage
  print("#############################################")
  print("Diffie Hellman with Rose for verification")
  pubprime = get_random_prime(10, 200)
  pubroot = np.random.randint(1,400)
  print(f"The public key you and Rose decided was prime number {pubprime} and primitive root {pubroot}")
  userpriv = numeric_key()
  x = power(pubroot, userpriv, pubprime)
  rosepriv = np.random.randint(1,400)
  y = power(pubroot, rosepriv, pubprime)
  usersk = power(y,userpriv,pubprime)
  rosesk = power(x,rosepriv,pubprime)
  print(usersk,rosesk)
  print("You recieved the shared secret key:", usersk)
  print("#############################################")
  print("Senario: As a real estate owner you're in a chat with Rose a prospective home buyer")
  key = get_key_from_secret(rosesk)
  rosemsg = "Hello i'm looking for a house is the house in CA avaliable?"
  iv1, encrypted1 = encrypt_message(rosemsg, key)
  print(f"Rose: {encrypted1.hex()}")
  input("press enter to decrypt the message with the shared key")
  decrypted1 = decrypt_message(encrypted1, key, iv1)
  print(f"Rose: {decrypted1}\n")
  w,s = yes_or_no()
  if w:
    ivy, yourenc = encrypt_message(s, key)
    print(f"Your response encrypted: {yourenc}\n")
    rosemsg2 = "Great! lets get on a call and talk more about it"
    iv2, encrypted2 = encrypt_message(rosemsg2, key)
    print(f"Rose: {encrypted2.hex()}")
    input("press enter to decrypt Rose's response with the shared key")
    decrypted2 = decrypt_message(encrypted2, key, iv2)
    print(f"Rose: {decrypted2}")
  else:
    ivy, yourenc = encrypt_message(s, key)
    print(f"Your response encrypted: {yourenc}\n")
    rosemsg2 = "Ok thanks, let me know if anything changes"
    iv2, encrypted2 = encrypt_message(rosemsg2, key)
    print(f"Rose: {encrypted2.hex()}")
    input("press enter to decrypt Rose's response with the shared key")
    decrypted2 = decrypt_message(encrypted2, key, iv2)
    print(f"Rose: {decrypted2}")

  




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