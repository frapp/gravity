#!/usr/bin/env python3
#Gravity's Rainbow: A post-modern rocket simulator!
import math
import sys
import random
import time
import readline

def main():
    target = random.randint(500, 3000)                #creates target distance
    drawLogo()
    #target = 500                                    #angle 50, vel 67
    play(target)


def play(targetDist):
    clear(50)
    diffSet = setDiff()

    while diffSet[0] > 0:

        print("Your target distance is: {0:d}" .format(targetDist))
        print("You have {0:d} rockets.\n" .format(diffSet[0]))

        while True:                                                    #user input angle and confirms if it's between 1 and 90
            try:
                playerAngle = float(input("Input your angle:"))

                if (playerAngle > 0 and playerAngle < 91):
                    break
                else:
                    print("Enter a value between 1 and 90")
                    continue
            except ValueError:
                print("Enter a number.")

        while True:                                                    #user input velocity and confirms it it's 1 and 500
            try:
                playerVelocity = float(input("Input your velocity:"))
                if (playerVelocity > 0 and playerVelocity < 501):
                    break
                else:
                    print("Enter a value between 1 and 500")
                    continue
            except ValueError:
                print("Enter a number.")


        shotDist = calcDist(playerAngle, playerVelocity)
        diffSet[0] = diffSet[0] -1
        if round(shotDist[0], 0) == 0:
            print("The rocket returned down on the launchpad after {0} minutes, killing everyone.\n" .format(round(shotDist[1], 2)))
            stillPlay = input("Do you want to start another game? Y/N? : ").lower()
            if playAgain(stillPlay) is True:
                main()

        print("\nYour rocket flew {0:.2f} miles in {1:.2f} minutes" .format(round(shotDist[0], 2), round(shotDist[1], 2)))
        print("You have {0} rockets left" .format(diffSet[0]))

        if diffSet[0] == 0:                                            #tests if rockets is 0, exits
            print("You ran out of rockets.")
            stillPlay = input("Do you want to start another game? Y/N? : ").lower()
            if playAgain(stillPlay) is True:
                main()

        if calcHit(shotDist[0], targetDist, diffSet[1]) is True:                #Calculates whether or not rocket hit target, generates score, prints eval and asks user if they want to play another game
            userScore = getScore(diffSet[0], shotDist[0], targetDist, diffSet[2])
            print("Your score is: {0:.0f}" .format(userScore))
            evalScore(userScore)
            stillPlay = input("Do you want to start another game? Y/N? : ").lower()
            if playAgain(stillPlay) is True:
                main()

        elif calcHit(shotDist[0], targetDist, diffSet[1]) is False:
            print("You missed.\n")
            #stillPlay = input("Do you still want to play? Y/N? : ").lower()
            #if playAgain(stillPlay) is True:
            #    continue
    else:
        print("Exiting")
        exit()



def calcHit(dist, targetDist, diffRange):
    if (round(dist, 0) > (targetDist - diffRange) and round(dist, 0) < (targetDist + diffRange)):
        return True
    else:
        return False




def calcDist(plyrAngl,plyrVel):
    gravity = 9.81                #gravity 9.81 m/s^2
    velInitX = plyrVel * math.cos(math.radians(plyrAngl))    #creates Vix
    velInitY = plyrVel * math.sin(math.radians(plyrAngl))    #creates Viy
    timeInAir = 2 * (velInitY / gravity)              #solves for time
    distanceX = velInitX * timeInAir                #solves for distance
    return (distanceX, timeInAir)                    #returns horizontal distance, time in air


def playAgain(stillPlay):
    valid = {'y', 'ye', 'yes', 'n', 'no' }
    validY = {'ye', 'y', 'yes'}
    validN = { 'n', 'no'}

    while True:
            if stillPlay in valid:
                if stillPlay in validN:
                    print("Exiting")
                    exit()
                elif stillPlay in validY:
                    break
            else:
                print("Please enter Y/N")
                continue
    return True

def getScore(rocketsLeft, rcktDist, trgtDist, difficulty):
    playerScore = difficulty * ((rocketsLeft * 1000) - (abs(rcktDist) - trgtDist))
    playerScore = round(playerScore)
    return playerScore

def evalScore(playerScore):

    clear(100)
    hscore = open('highscore.txt')
    data = hscore.readlines()
    hscore.close()
    hscore = open('highscore.txt')

    for n in range(10):
        fileLine = hscore.readline()
        score = fileLine.split('-')

        if playerScore > int(score[1]):
            drawHit()
            print("Success! You hit the target")
            print("You'd make Tyrone Slothrop proud with a score of {0:.0f}.\n" .format(playerScore))
            userName = input("Enter your name: ")
            newScore = ('%s-%s\n' % (userName, playerScore))
            hscore.close()

            hscore = open('highscore.txt', 'w')
            data.insert(n, newScore)
            data.pop(10)
            hscore.writelines(data)
            hscore.close()

            break

        else:
            continue
    hscore.close()


def setDiff():
    valid = {'e', 'm', 'h', '?'    }

    while True:
        print("Enter your difficulty:\n (e)asy, (m)edium, (h)ard.\n")
        getDiff = input(": ").lower()
        if getDiff in valid:
            if getDiff == 'e':
                return [99, 300, 1]
                break
            elif getDiff == 'm':
                return [50, 150, 3]
                break
            elif getDiff == 'h':
                return [10, 50, 10]
                break
            elif getDiff == '?':
                print("Easy: 99 rockets, 600 miles of tolerance.\nMedium: 50 rockets, 300 miles of tolerance.\nHard: 10 rockets, 100 miles of tolerance.\n")
                continue
        else:
            print("Enter e, m or h.")
            continue


def drawLogo():

    logo = open('logo.art')
    logoDraw = logo.read()

    for n in range(50):
        clear(100)
        print(logoDraw)
        print('\n' *  n)
        print("Gravity's Rainbow: A post-modern rocket simulator!")
        time.sleep(.05)
    logo.close()


def drawHit():
    f = open('hit.art')
    offset = 1486

    for r in range(7):
        #line = f.readlines(1485)
        #for n in range(24):
        #    print(line[n].rstrip())
        #time.sleep(.5)

        f.seek(offset * r)
        line = f.readlines(1485)
        for n in range(24):
            print(line[n].rstrip())

        time.sleep(.5)
        clear(55)
    f.close()


def clear(lines):
    print(' \n' * lines)

main()
