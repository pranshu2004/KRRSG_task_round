#!/usr/bin/env python
import rospy
from std_msgs.msg import String

class PlayerB:
    def __init__(self):
        rospy.init_node('player_b')
        self.hitpoints_sub = rospy.Subscriber('monster_hitpoints', String, self.update_hitpoints)
        self.winner_sub = rospy.Subscriber('winner/', String, self.win_check)
        self.move_pub = rospy.Publisher('monster_moves', String, queue_size=10)
        self.hitpoints = {}
        self.flag = 0
        self.round = 1
        self.check_winner = 1

    def update_hitpoints(self, hitpoints_msg):
        hitpoints_data = hitpoints_msg.data
        if hitpoints_data[-1] == 'B':
            hitpoints_data = hitpoints_data[:-1:]
            player_a_data = hitpoints_data.split(';')[0]
            player_a_hitpoints = [int(x) for x in player_a_data.split(':')[1].split(',')]
            player_b_data = hitpoints_data.split(';')[1]
            player_b_hitpoints = [int(x) for x in player_b_data.split(':')[1].split(',')]
            self.hitpoints = {
                'Rock': player_b_hitpoints[0],
                'Thunder': player_b_hitpoints[1],
                'Wind': player_b_hitpoints[2]
            }
            print(f"\nCurrent State @ Round {self.round} = ")
            print(f"Fire : {player_a_hitpoints[0]}\nWater : {player_a_hitpoints[1]}\nEarth : {player_a_hitpoints[2]}")
            print(f"Rock : {player_b_hitpoints[0]}\nThunder : {player_b_hitpoints[1]}\nWind : {player_b_hitpoints[2]}\n")
            self.flag = 1
            self.round+=1

    def take_moves_input(self):

        if self.hitpoints['Rock'] != 0:
            rock_move = input("Enter Player B's move for Rock: ")
        else:
            rock_move = '0'

        if self.hitpoints['Thunder'] != 0:
            thunder_move = input("Enter Player B's move for Thunder: ")
        else:
            thunder_move = '0'

        if self.hitpoints['Wind'] != 0:
            wind_move = input("Enter Player B's move for Wind: ")
        else:
            wind_move = '0'

        moves_str = rock_move+','+thunder_move+','+wind_move

        move_msg = 'B:' + moves_str
        self.move_pub.publish(move_msg)

    def win_check(self, d):
        data = d.data
        if data[1] == '0' : self.check_winner = 0
        elif data[1] == '2' : self.check_winner = 2
        

if __name__ == '__main__':
    player_b = PlayerB()
    while player_b.check_winner == 1:
        if player_b.flag:
            player_b.take_moves_input()
            player_b.flag = 0
    if not player_b.check_winner: print("Player A has won :((")
    else: print("You have won the game!!")
    print("Terminating the program now...")