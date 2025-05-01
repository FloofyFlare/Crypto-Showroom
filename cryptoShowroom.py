def classical():
  print("Which classical cipher would you like to try")
  
def cryptoShowroom():
  print("Would you like to try: \n" \
  "   classical ciphers(1)\n" \
  "   one-time pad(2)\n" \
  "   A public-key conversation(3)")
  userinput = input("enter choice here: ")
  match userinput:
    case "1":
      print("You can become a web developer.")
    case "2":
      print("You can become a Data Scientist")
    case "3":
      print("You can become a backend developer")
    case _:
      cryptoShowroom()

print("Welcome to the cryptography showroom")
# use BouncyCastle for pivate public key encryption
cryptoShowroom()