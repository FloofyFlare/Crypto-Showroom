import numpy as np
import re

def is_alpha(str):
  return bool(re.fullmatch(r'[a-zA-Z]+', str))

def classical():
  print("#############################################")
  print("Which classical cipher would you like to try: \n" \
  "   Ceasar(1)\n" \
  "   Vigenère(2)")
  userinput = input("enter choice here: ")
  
  encoded = ""
  frequencytable = {}
  match userinput:
    case "1":
      randKey = np.random.randint(1,27)
      print(f"{randKey} is the key")
      while True:
        userinput = input("Provide a provide a message in the set [Aa-Zz] " \
        "for the ceasar cipher \n message: ")
        userinput.lower()
        if is_alpha(userinput):
          break
      for c in userinput:
        cint = ((ord(c) - 97 + randKey ) % 27) + 97
        encoded += chr(cint)
        original = frequencytable.get((c,chr(cint)))
        frequencytable[c, chr(cint)] = frequencytable.get((c,chr(cint)), 0) + 1
      print(f"encoded result: {encoded}")
      print("frequency analysis:")
      print(frequencytable)
    case "2":



      
      userinput = input("Provide a number for the Vigenère cipher: ")
    case _:
      classical()

  
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
      print("You can become a Data Scientist")
    case "3":
      print("You can become a backend developer")
    case _:
      cryptoShowroom()

print("Welcome to the cryptography showroom")
# use BouncyCastle for pivate public key encryption
cryptoShowroom()