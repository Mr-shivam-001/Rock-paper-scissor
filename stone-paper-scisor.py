import random

com = random.randint(1,3)

HScount = 0
CScount = 0


while True:
    print(f"Scores are ===>>> Human {HScount} and Computer {CScount}")
    user = int(input("1 = Stone, 2 = Paper, 3 = Scisor Choose your :- "))

    if user == 1 and com == 3:
        print("Congrass! You Won 👍\n")
        HScount += 1

    elif user == 2 and com == 1:
        print("Congrass! You Won 👍\n")
        HScount += 1

    elif user == 3 and com == 2:
        print("Congrass! You Won 👍\n")
        HScount += 1

    elif user == com:
        print("Match Draw 😮‍💨\n")

    else:
        print("Computer won 🤖\n")
        CScount += 1


    if HScount == 5:
        print("You Won this Match 😎🥳")
        break
    elif CScount == 5:
        print("Computer Won This Match 🤖👾")
        break
