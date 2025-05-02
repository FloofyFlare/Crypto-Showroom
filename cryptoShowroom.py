import numpy as np
import re
import os

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
        print(userinput)
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

def oneTime():
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
      oneTime()
    case "3":
      print("You can become a backend developer")
    case _:
      cryptoShowroom()

print("Welcome to the cryptography showroom")
# use BouncyCastle for pivate public key encryption
cryptoShowroom()