import copy
import csv
import os
import random
from typing import Dict, List, Tuple, Union

from Avalon.judge import Judge
from Avalon.prompt.identity_prompt import IdentityHint, IdentityHintWithoutHide
from Avalon.utils import log_decorator


class Game:
    def __init__(
            self,
            players: Union[List, Tuple],
            config: Dict,
            logdir: str = 'logs',
            logfile_name: str = 'game_history',
    ):
        self.players = players  # Store the player instances
        self.leader = None
        self.round_result = []
        self.round_vote_result = []
        self.previous_player_team_list = []
        self.previous_leader_list = []

        self.merlin = Judge.get_merlin(self.players)
        self.percival = Judge.get_percival(self.players)
        self.assassin = Judge.get_assassin(self.players)
        self.morgana = Judge.get_morgana(self.players)
        self.loyals = Judge.get_loyals(self.players)

        self.role_hints = dict()
        self.role_hints_without_hide = dict()
        self.total_leader_changes = 0
        self.round = 1
        self.propose_count = [2, 3, 4, 3, 4]
        self.config = config
        self.proposed_team = None
        self._full_history = []
        self._memory_dict_list = []

        # An integer to remember how many players have spoken in this discussion round
        self.discussion_round_begin_sign = 'A new discussion round begins.'

        self.logdir = logdir
        os.makedirs(self.logdir, exist_ok=False)

        self.logfile_name_csv = os.path.join(self.logdir, logfile_name + '.csv')

        self.role_hints["Merlin"] = IdentityHint.get_hint_for_merlin(
            assassin=self.assassin, morgana=self.morgana, merlin=self.merlin, percival=self.percival,
            loyal_1=self.loyals[0], loyal_2=self.loyals[1])
        self.role_hints["Percival"] = IdentityHint.get_hint_for_percival(
            merlin=self.merlin, morgana=self.morgana, assassin=self.assassin, percival=self.percival,
            loyal_1=self.loyals[0], loyal_2=self.loyals[1])
        self.role_hints["Assassin"] = IdentityHint.get_hint_for_assassin(
            morgana=self.morgana, merlin=self.merlin, percival=self.percival,
            loyal_1=self.loyals[0], loyal_2=self.loyals[1])
        self.role_hints["Morgana"] = IdentityHint.get_hint_for_morgana(
            assassin=self.assassin, merlin=self.merlin, percival=self.percival,
            loyal_1=self.loyals[0], loyal_2=self.loyals[1])
        self.role_hints["Loyal servant of arthur"] = IdentityHint.get_hint_for_loyal()

        self.role_hints_without_hide["Merlin"] = IdentityHintWithoutHide.get_hint_for_merlin(
            assassin=self.assassin, morgana=self.morgana, merlin=self.merlin, percival=self.percival,
            loyal_1=self.loyals[0], loyal_2=self.loyals[1])
        self.role_hints_without_hide["Percival"] = IdentityHintWithoutHide.get_hint_for_percival(
            merlin=self.merlin, morgana=self.morgana, assassin=self.assassin, percival=self.percival,
            loyal_1=self.loyals[0], loyal_2=self.loyals[1])
        self.role_hints_without_hide["Assassin"] = IdentityHintWithoutHide.get_hint_for_assassin(
            morgana=self.morgana, merlin=self.merlin, percival=self.percival,
            loyal_1=self.loyals[0], loyal_2=self.loyals[1])
        self.role_hints_without_hide["Morgana"] = IdentityHintWithoutHide.get_hint_for_morgana(
            assassin=self.assassin, merlin=self.merlin, percival=self.percival,
            loyal_1=self.loyals[0], loyal_2=self.loyals[1])
        self.role_hints_without_hide["Loyal servant of arthur"] = IdentityHintWithoutHide.get_hint_for_loyal()

    @property
    def full_history(self):
        return copy.deepcopy(self._full_history)

    @property
    def memory_dict_list(self):
        return copy.deepcopy(self._memory_dict_list)

    def memory_dict_list_append(self, item):
        return self._memory_dict_list.append(item)

    def get_full_history_list(self) -> list:
        ret = [(_[0], _[1]) for _ in self._full_history]
        return ret

    def start(self) -> bool:
        """
        return: True: the good side wins; False: the evil side wins.
        """
        print("Welcome to Avalon Game!")
        if self.round == 1:
            self._log("Game Start",
                      "Welcome to Avalon Game. This message signifies the start of a new game. "
                      "All previous information, such as completed tasks or team alignments, is reset. "
                      "The game history from this line onwards is the effective historical game history dialogue of this game!")
        
        """
        Before the game starts, players with special identities need to obtain certain special information
        """
        """Game Start"""
        while self.round < 6:
            # fail_counter is used to count the number of proposed team failures in each round
            fail_counter = 0
            if self.config['short_memory']:
                self._log(f'Voiceover', self.discussion_round_begin_sign)
            while True:
                # Leader proposes a team
                self.proposed_team, cur_leader_action = self.assign_leader()
                self._log(f"Player {self.total_leader_changes % len(self.players) + 1}",
                          f"I propose the team {', '.join([f'player {_}' for _ in self.proposed_team])}.")

                self._log(
                    f"Player {self.total_leader_changes % len(self.players) + 1}", cur_leader_action)

                # get the leader index
                leader_index = self.players.index(self.leader)

                # Rearrange the players list so that the next player after the leader is the first to speak in the list
                players_reordered = self.players[leader_index + 1:] + self.players[:leader_index]
                # Each player gets a chance to speak
                votes = [True]
                for player in players_reordered:
                    if fail_counter >= 3:
                        break
                    # Skip the leader in this loop
                    elif player == self.leader:
                        continue
                    else:
                        # Each player makes a statement
                        cur_action = player.discuss_proposed_team()
                        self._log(f"Player {player.id}", cur_action)

                votes_statements = []
                if fail_counter < 3:
                    for player in players_reordered:
                        vote = player.vote_on_team()
                        votes.append(vote)
                        statement = f"Player {player.id} votes: {'support' if vote else 'disagree'} with this team proposal."
                        votes_statements.append((player.id, statement))
                    # After all players have voted, log the statements
                    for player_id, statement in votes_statements:
                        self._log(f"Player {player_id}", statement)
                if fail_counter >= 3 or votes.count(True) > len(
                        self.players) / 2:  # If majority approves the team, go on the mission. Vote on mission only for players who are on the proposed team
                    self._log(
                        f"Voiceover", "The team proposal was approved by the majority. The mission start!")
                    print("Mission Start!")
                    self.previous_player_team_list.append([f'Player {_}' for _ in self.proposed_team])
                    self.previous_leader_list.append(f"Player {self.leader.id}")
                    mission_final_decision, mission_results = self.conduct_mission(
                        selected_players=[self.players[int(i) - 1] for i in self.proposed_team])
                    random.shuffle(mission_results)
                    self._log(f"Voiceover",
                              f"The mission result is {mission_final_decision}. The votes are: {mission_results}")
                    self.round_result.append(mission_final_decision)
                    self.round_vote_result.append(mission_results)
                    print(f"Mission Result:{mission_final_decision}")
                    print(f"Votes Result: {mission_results}")

                    if self.round_result.count('Success') >= 3:  # Check game result after each mission
                        print(
                            "Good side wins for now, moving on to assassination stage.")
                        self._log(
                            f"Voiceover", "Good side wins for now, moving on to assassination stage.")
                        game_result = self.start_assassin()  # transition to the assassination stage
                        print("Game is over")
                        self._log(f"Voiceover", "Game is over.")
                        return game_result  # end the game

                    elif self.round_result.count('Fail') >= 3:
                        print("Evil side has succeeded. ")
                        self._log(f"Voiceover", "Evil side has succeeded.")
                        print("Game is over")
                        self._log(f"Voiceover", "Game is over.")
                        return False  # end the game
                    self.round += 1
                    self.total_leader_changes += 1
                    break

                else:
                    fail_counter += 1
                    self.total_leader_changes += 1
                    self._log(f"Voiceover",
                              "The team proposal was rejected by the majority. Move on to the next leader.")
                    print("Team proposal was rejected. Move on to the next leader.")

    @log_decorator
    def _log(self, subject: str, message: str):
        assert len(self._full_history) == len(
            self._memory_dict_list), f"{len(self._full_history)=}, {len(self._memory_dict_list)=}"
        self._full_history.append([subject, message])
        f_csv = open(self.logfile_name_csv, 'w', encoding='utf-8')
        csv_writer = csv.writer(f_csv)
        role_assignment = f'Assigned roles:\n'
        for cur_player in self.players:
            role_assignment += f'Player {cur_player.id}: {cur_player.role}\n'
        csv_writer.writerow(['voiceover', role_assignment])

        for subject, message in self._full_history:
            csv_writer.writerow([subject, message])
        f_csv.close()

    def get_team_size(self):
        current_propose_count = self.propose_count[
            self.round - 1]  

        return current_propose_count

    def assign_leader(self):
        """ Leader is chosen based on the total number of leader changes """
        self.leader = self.players[self.total_leader_changes % len(self.players)]
        return self.leader.propose_team()

    def conduct_mission(self, selected_players):
        mission_results = []  # Initialize an empty list to collect mission results
        for player in selected_players:
            if player.role == "Morgana" or player.role == "Assassin":
                vote = player.vote_on_mission()
                mission_results.append(vote)
            else:
                mission_results.append("Success")
        # count the number of "fail" votes.
        fail_votes = mission_results.count('Fail')
        if fail_votes > 0:
            return 'Fail', mission_results
        else:
            return 'Success', mission_results

    def start_assassin(self):
        # Have the assassin guess who Merlin is
        guessed_merlin_id = self.assassin.guess_merlin()
        print(f"The Assassin guesses Player {guessed_merlin_id} is Merlin.")
        self._log(f"Assassin", f"I think Player {guessed_merlin_id} is Merlin")
        # Determine if the guess was correct
        for player in self.players:
            if player.role == "Merlin":
                real_merlin = player
                break

        if guessed_merlin_id == real_merlin.id:
            print("The guess is correct. Evil side wins!")
            self._log(f"Voiceover", "Evil side wins!")
            return False
        else:
            print("The guess is wrong. Good side wins finally!")
            self._log(f"Voiceover", "Good side wins finally!")
            return True

