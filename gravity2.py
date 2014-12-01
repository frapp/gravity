#!/usr/bin/env python3
#Gravity's Rainbow: A post-modern rocket simulator!
import math
import sys
import random
import time
import readline

def main():
    target = random.randint(500, 3000)
    clear(55)                #creates target distance
    draw('logo.art',257)
    #target = 500                                    #angle 50, vel 67
    play(target)


def play(target_dist):
    clear(50)
    diff_set = set_diff()

    while diff_set[0] > 0:

        print("Your target distance is: {0:d}" .format(target_dist))
        print("You have {0:d} rockets.\n" .format(diff_set[0]))

        while True:                                                    #user input angle and confirms if it's between 1 and 90
            try:
                player_angle = float(input("Input your angle:"))

                if (player_angle > 0 and player_angle < 91):
                    break
                else:
                    print("Enter a value between 1 and 90")
                    continue
            except ValueError:
                print("Enter a number.")

        while True:                                                    #user input velocity and confirms it it's 1 and 500
            try:
                player_velocity = float(input("Input your velocity:"))
                if (player_velocity > 0 and player_velocity < 501):
                    break
                else:
                    print("Enter a value between 1 and 500")
                    continue
            except ValueError:
                print("Enter a number.")


        shot_dist = calc_dist(player_angle, player_velocity)
        diff_set[0] = diff_set[0] -1
        if round(shot_dist[0], 0) == 0:
            print("The rocket returned down on the launchpad after {0} minutes, killing everyone.\n" .format(round(shot_dist[1], 2)))
            still_play = input("Do you want to start another game? Y/N? : ").lower()
            if play_again(still_play) is True:
                main()

        print("\nYour rocket flew {0:.2f} miles in {1:.2f} minutes" .format(round(shot_dist[0], 2), round(shot_dist[1], 2)))
        print("You have {0} rockets left" .format(diff_set[0]))

        if diff_set[0] == 0:                                            #tests if rockets is 0, exits
            print("You ran out of rockets.")
            still_play = input("Do you want to start another game? Y/N? : ").lower()
            if play_again(still_play) is True:
                main()

        if calc_hit(shot_dist[0], target_dist, diff_set[1]) is True:                #Calculates whether or not rocket hit target, generates score, prints eval and asks user if they want to play another game
            user_score = get_score(diff_set[0], shot_dist[0], target_dist, diff_set[2])
            print("Your score is: {0:.0f}" .format(user_score))
            eval_score(user_score)
            still_play = input("Do you want to start another game? Y/N? : ").lower()
            if play_again(still_play) is True:
                main()

        elif calc_hit(shot_dist[0], target_dist, diff_set[1]) is False:
            print("You missed.\n")
            #still_play = input("Do you still want to play? Y/N? : ").lower()
            #if play_again(still_play) is True:
            #    continue
    else:
        print("Exiting")
        exit()



def calc_hit(dist, target_dist, diff_range):
    if (round(dist, 0) > (target_dist - diff_range) and round(dist, 0) < (target_dist + diff_range)):
        return True
    else:
        return False




def calc_dist(plyr_angl,plyr_vel):
    gravity = 9.81                #gravity 9.81 m/s^2
    vel_init_x = plyr_vel * math.cos(math.radians(plyr_angl))    #creates Vix
    vel_init_y = plyr_vel * math.sin(math.radians(plyr_angl))    #creates Viy
    time_in_air = 2 * (vel_init_y / gravity)              #solves for time
    distance_x = vel_init_x * time_in_air                #solves for distance
    return (distance_x, time_in_air)                    #returns horizontal distance, time in air


def play_again(still_play):
    valid = {'y', 'ye', 'yes', 'n', 'no' }
    valid_y = {'ye', 'y', 'yes'}
    valid_n = { 'n', 'no'}

    while True:
        if still_play in valid:
            if still_play in valid_n:
                print("Exiting")
                exit()
            elif still_play in valid_y:
                break
        else:
            print("Please enter Y/N")
            continue
    return True

def get_score(rockets_left, rckt_dist, trgt_dist, difficulty):
    player_score = difficulty * ((rockets_left * 1000) - (abs(rckt_dist) - trgt_dist))
    player_score = round(player_score)
    return player_score

def eval_score(player_score):

    clear(100)
    hscore = open('highscore.txt')
    data = hscore.readlines()
    hscore.close()
    hscore = open('highscore.txt')

    for rank in range(10):
        file_line = hscore.readline()
        score = file_line.split('-')

        if player_score > int(score[1]):
            draw('hit.art',1486)
            print("Success! You hit the target")
            print("You'd make Tyrone Slothrop proud with a score of {0:.0f}.\n" .format(player_score))
            user_name = input("Enter your name: ")
            new_score = ('%s-%s\n' % (user_name, player_score))
            hscore.close()

            hscore = open('highscore.txt', 'w')
            data.insert(rank, new_score)
            data.pop(10)
            hscore.writelines(data)
            hscore.close()

            break

        else:
            continue
    hscore.close()


def set_diff():
    valid = {'e', 'm', 'h', '?'    }

    while True:
        print("Enter your difficulty:\n (e)asy, (m)edium, (h)ard.\n")
        get_diff = input(": ").lower()
        if get_diff in valid:
            if get_diff == 'e':
                return [99, 300, 1]
                break
            elif get_diff == 'm':
                return [50, 150, 3]
                break
            elif get_diff == 'h':
                return [10, 50, 10]
                break
            elif get_diff == '?':
                print("Easy: 99 rockets, 600 miles of tolerance.\nMedium: 50 rockets, 300 miles of tolerance.\nHard: 10 rockets, 100 miles of tolerance.\n")
                continue
        else:
            print("Enter e, m or h.")
            continue


#def drawLogo():

#    logo = open('logo.art')
#    logoDraw = logo.read()

#    for n in range(50):
#        clear(100)
#        print(logoDraw)
#        print('\n' *  n)
#        print("Gravity's Rainbow: A post-modern rocket simulator!")
#        time.sleep(.05)
#    logo.close()


#def drawHit():
#    f = open('hit.art')
#    offset = 1486

#    for r in range(7):
        #line = f.readlines(1485)
        #for n in range(24):
        #    print(line[n].rstrip())
        #time.sleep(.5)

#        f.seek(offset * r)
#        line = f.readlines(1485)
#        for n in range(24):
#            print(line[n].rstrip())

#        time.sleep(.5)
#        clear(55)
#    f.close()

def draw(file, offset):                         #draw() function
    f = open(file)                              #draw(<filename.art>,offset)
    frames = int((f.seek(0,2))/(offset -1))     #frame = x chars per frame, offset = chars per frame +1
    f.seek(0)                                   #frame height = 24 lines to fit with 25x50 term window
    for r in range(frames):    

        f.seek((offset * r))
        
        line = f.readlines(offset)
        for n in range(24):
            print(line[n].rstrip())
        time.sleep(.5)
        clear(55)

    f.close()



def clear(lines):
    print(' \n' * lines)

main()
