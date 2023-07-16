#!/usr/bin/env python
import rospy
from std_msgs.msg import String

class PlayerA:
    def __init__(self):
        rospy.init_node('player_a')
        self.hitpoints_sub = rospy.Subscriber('monster_hitpoints', String, self.update_hitpoints)
        self.winner_sub = rospy.Subscriber('winner/', String, self.win_check)
        self.move_pub = rospy.Publisher('monster_moves', String, queue_size=10)
        self.hitpoints = {}
        self.flag = 0
        self.round = 1
        self.check_winner = 1

    def update_hitpoints(self, hitpoints_msg):
        hitpoints_data = hitpoints_msg.data
        if hitpoints_data[-1] == 'A':
            hitpoints_data = hitpoints_data[:-1:]
            player_a_data = hitpoints_data.split(';')[0]
            player_a_hitpoints = [int(x) for x in player_a_data.split(':')[1].split(',')]
            player_b_data = hitpoints_data.split(';')[1]
            player_b_hitpoints = [int(x) for x in player_b_data.split(':')[1].split(',')]
            self.hitpoints = {
                'Fire': player_a_hitpoints[0],
                'Water': player_a_hitpoints[1],
                'Earth': player_a_hitpoints[2]
            }
            print(f"\nCurrent State @ Round {self.round} = ")
            print(f"Fire : {player_a_hitpoints[0]}\nWater : {player_a_hitpoints[1]}\nEarth : {player_a_hitpoints[2]}")
            print(f"Rock : {player_b_hitpoints[0]}\nThunder : {player_b_hitpoints[1]}\nWind : {player_b_hitpoints[2]}\n")
            self.flag = 1
            self.round+=1

    def take_moves_input(self):

        if self.hitpoints['Fire'] != 0:
            fire_move = input("Enter Player A's move for Fire: ")
        else:
            fire_move = '0'

        if self.hitpoints['Water'] != 0:
            water_move = input("Enter Player A's move for Water: ")
        else:
            water_move = '0'

        if self.hitpoints['Earth'] != 0:
            earth_move = input("Enter Player A's move for Earth: ")
        else:
            earth_move = '0'

        moves_str = fire_move+','+water_move+','+earth_move

        move_msg = 'A:' + moves_str
        self.move_pub.publish(move_msg)

    def win_check(self, d):
        data = d.data
        if data[0] == '0' : self.check_winner = 0
        elif data[0] == '2' : self.check_winner = 2

if __name__ == '__main__':
    player_a = PlayerA()
    while player_a.check_winner == 1:
        if player_a.flag:
            player_a.take_moves_input()
            player_a.flag = 0    
    if not player_a.check_winner: print("Player B has won :((")
    else: print("You have won the game!!")
    print("Terminating the program now...")