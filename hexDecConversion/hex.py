import random
last_number = 0
generated_number = 0
while True:
    print("hex to bin")
    while generated_number == last_number:
        generated_number = random.randrange(1, 16)
    
    print(hex(generated_number))
    guess = 0
    while guess != generated_number:
        guess = 0
        s = str(input())
        guess = int(s, 2)
    print("")

    last_number = generated_number
    print("bin to hex")
    nn = random.randrange(10, 16)
    print(bin(nn)[2:])
    guess = 0
    while guess != nn:
        s = str(input())
        guess = int(s, 16)
    
    print("")
