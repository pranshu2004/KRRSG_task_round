#!/usr/bin/env python
import rospy
from std_msgs.msg import String

class GameServer:
    def __init__(self):
        rospy.init_node('game_server')
        self.rate = rospy.Rate(10)  # Adjust the rate as per your requirements
        self.player_a_hitpoints = {'Fire': 300, 'Water': 400, 'Earth': 500}
        self.player_b_hitpoints = {'Rock': 300, 'Thunder': 400, 'Wind': 500}

        self.states = ['PLAYER_A_ATTACK', 'PLAYER_B_ATTACK', 'GAME_OVER']
        self.current_state = 'PLAYER_A_ATTACK'

        # ROS Publishers and Subscribers
        self.hitpoints_pub = rospy.Publisher('monster_hitpoints', String, queue_size=10)
        self.moves_sub = rospy.Subscriber('monster_moves', String, self.handle_moves)
        self.winner_pub = rospy.Publisher('winner/', String, queue_size=10)
        self.flag = 0
        self.round = 1

    def run(self):
        input('Press enter to start the game server ')
        print()
        rospy.loginfo("Game Server started!")
        while True:
            if self.current_state == 'PLAYER_A_ATTACK':
                self.send_hitpoints('A')
                while not self.flag: pass
                else: self.flag = 0
            elif self.current_state == 'PLAYER_B_ATTACK':
                self.send_hitpoints('B')
                while not self.flag: pass
                else: self.flag = 0
            elif self.current_state == 'GAME_OVER':
                self.end_game()
            self.rate.sleep()

    def send_hitpoints(self, player):
        hitpoints_msg = self.format_hitpoints_message()
        self.hitpoints_pub.publish(hitpoints_msg+player)

    def format_hitpoints_message(self):
        player_a_hp = ','.join(str(hp) for hp in self.player_a_hitpoints.values())
        player_b_hp = ','.join(str(hp) for hp in self.player_b_hitpoints.values())
        return 'PlayerA:' + player_a_hp + ';PlayerB:' + player_b_hp

    def handle_moves(self, move_msg):
        player, moves_str = move_msg.data.split(':')
        moves = moves_str.split(',')

        if self.current_state == 'PLAYER_A_ATTACK' and player == 'A':
            print(f"\nRound - {self.round}")
            self.process_moves('A', moves)
            self.current_state = 'PLAYER_B_ATTACK'
            self.check_game_end()
            self.flag = 1
        elif self.current_state == 'PLAYER_B_ATTACK' and player == 'B':
            self.process_moves('B', moves)
            self.current_state = 'PLAYER_A_ATTACK'
            self.check_game_end()
            self.flag = 1
            self.round+=1

    def process_moves(self, player, moves):
        if player == 'A':
            self.update_hitpoints_b(moves)
        elif player == 'B':
            self.update_hitpoints_a(moves)

    def check_game_end(self):
        if all(hp == 0 for hp in self.player_a_hitpoints.values()):
            self.current_state = 'GAME_OVER'
            rospy.loginfo("Winner: Player B")
            self.winner_pub.publish('02')
        elif all(hp == 0 for hp in self.player_b_hitpoints.values()):
            self.current_state = 'GAME_OVER'
            rospy.loginfo("Winner: Player A")
            self.winner_pub.publish('20')

    def end_game(self):
        rospy.loginfo("Game Over!")
        rospy.signal_shutdown("Game Over!")
        exit()

    def update_hitpoints_a(self, player_b_moves):
        player_a_hp = self.player_a_hitpoints

        #Rock's turn
        if player_b_moves[0]=="1":
            for i in player_a_hp:
                player_a_hp[i]-=30
                if player_a_hp[i]<0: player_a_hp[i]=0
            print("Rock attacked all")
        elif player_b_moves[0][0]=="2":
            attack_one = player_b_moves[0].split()
            player_a_hp[attack_one[1]]-=60
            if player_a_hp[attack_one[1]]<0:player_a_hp[attack_one[1]]=0
            print("Rock attacked",attack_one[1])
        else: pass

        #Thunder's turn
        if player_b_moves[1]=="1":
            for i in player_a_hp:
                player_a_hp[i]-=40
                if player_a_hp[i]<0: player_a_hp[i]=0
            print("Thunder attacked all")
        elif player_b_moves[1][0]=="2":
            attack_one = player_b_moves[1].split()
            player_a_hp[attack_one[1]]-=80
            if player_a_hp[attack_one[1]]<0:player_a_hp[attack_one[1]]=0
            print("Thunder attacked", attack_one[1])
        else: pass

        #Wind's turn
        if player_b_moves[2]=="1":
            for i in player_a_hp:
                player_a_hp[i]-=50
                if player_a_hp[i]<0: player_a_hp[i]=0
            print("Wind attacked all")
        elif player_b_moves[2][0]=="2":
            attack_one = player_b_moves[2].split()
            player_a_hp[attack_one[1]]-=100
            if player_a_hp[attack_one[1]]<0:player_a_hp[attack_one[1]]=0
            print("Wind attacked",attack_one[1])
        else: pass

        self.player_a_hitpoints = player_a_hp

    def update_hitpoints_b(self, player_a_moves):
        player_b_hp = self.player_b_hitpoints

        #Fire's turn
        if player_a_moves[0]=="1":
            for i in player_b_hp:
                player_b_hp[i]-=30
                if player_b_hp[i]<0: player_b_hp[i]=0
            print("Fire attacked all")
        elif player_a_moves[0][0]=="2":
            attack_one = player_a_moves[0].split()
            player_b_hp[attack_one[1]]-=60
            if player_b_hp[attack_one[1]]<0:player_b_hp[attack_one[1]]=0
            print("Fire attacked", attack_one[1])
        else: pass

        #Water's turn
        if player_a_moves[1] == "1":
            for i in player_b_hp:
                player_b_hp[i]-=40
                if player_b_hp[i]<0: player_b_hp[i]=0
            print("Water attacked all")
        elif player_a_moves[1][0]=="2":
            attack_one = player_a_moves[1].split()
            player_b_hp[attack_one[1]]-=80
            if player_b_hp[attack_one[1]]<0: player_b_hp[attack_one[1]]=0
            print("Water attacked", attack_one[1])
        else: pass

        #Earth's turn
        if player_a_moves[2] == "1":
            for i in player_b_hp:
                player_b_hp[i]-=50
                if player_b_hp[i]<0: player_b_hp[i]=0
            print("Earth attacked all")
        elif player_a_moves[2][0]=="2":
            attack_one = player_a_moves[2].split()
            player_b_hp[attack_one[1]]-=100
            if player_b_hp[attack_one[1]]<0:player_b_hp[attack_one[1]]=0
            print("Earth attacked", attack_one[1])
        else: pass

        self.player_b_hitpoints = player_b_hp

if __name__ == '__main__':
    server = GameServer()
    server.run()
