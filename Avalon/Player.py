import copy
import re
from typing import Callable, Dict, List, Tuple

from easydict import EasyDict

from Avalon.Game import Game
from Avalon.prompt.game_prompt import PromptHint
from Avalon.prompt.without_thinking_prompt import WithoutThinkPrompt
from Avalon.utils import (
    call_api,
    extract_plan_id,
    extract_speak_id,
    extract_think_speak,
    extract_think_speak_in_revision,
    judge_contents_valid,
    mark_memory_position,
)


class Player:

    combined_scores = []
    combined_grades = []
    evaluate_retrieved_count = 0
    evaluate_abandoned_count = 0

    def __init__(
            self,
            id: int,
            role: str,
            role_list: List[str],
            config: EasyDict,
    ):
        self.id = id
        self.role = role
        self.role_list = [_ for _ in role_list if _ != self.role]
        self.propose_count = [2, 3, 4, 3, 4]
        self.game_belong_to: Game = None
        self.config: EasyDict = config
        self.discuss_content = ""
        self.private_game_history = []
        self.private_memory_dict_list = []

        self.description_str = "The game state corresponding to the following history dialogue is:\n" \
                               "{current_round}\n\n\n" \
                               "{current_proposed_team_players}\n\n\n" \
                               "{current_mission_results}\n\n\n"  # \

        self.general_game_status = "So far the game status is as follows:\n\n\n" \
                                   "{current_round}\n\n\n" \
                                   "{current_proposed_team_players}\n\n\n" \
                                   "{current_mission_results}\n"

        self.special_status_propose = "So far the game status is as follows:\n\n\n" \
                                      "{current_round}\n\n\n" \
                                      "{current_mission_results}\n"

        self.private_description_str = "The game state corresponding to the following history dialogue is:\n" \
                                       "{current_round}\n" \
                                       "{current_proposed_team_players}\n" \
                                       "{current_mission_results}\n" \
                                       f"The inner dialogue of you (Player {self.id} with role {self.role}) is:\n"

        self.attitude_player: str = "Empty. "

        self.attitude_prompt: str = None  # Left to be set in set_game_belong_to()

        self.revision_history_file_header = ['situation', 'original THINK', 'original SPEAK',
                                             'revised THINK', 'revised SPEAK', 'complete response',
                                             'perspective analysis', 'active flag', 'revision quality']

        self.compare_dict = {}
        self.latest_input_messages = None
        self.latest_revision_results = None
        self.perspective_analysis_response = "Empty. "

    def _get_temp_config(self):
        temp_config = copy.deepcopy(self.config)
        if self.config['temp_model_name'] is not None:
            temp_config['model_name'] = self.config['temp_model_name']
            temp_config['long_context_model'] = self.config['temp_long_context_model']
            temp_config['short_context_model'] = self.config['temp_short_context_model']
            temp_config['short_model_context'] = self.config['temp_short_model_context']
        # if self.config['temp_model_name'] == 'gpt4':
        #     temp_config['model_name'] = "gpt4"
        #     temp_config['long_context_model'] = "gpt-4-32k-0613"
        #     temp_config['short_context_model'] = "gpt-4-0613"
        #     temp_config['short_model_context'] = 7900
        # elif self.config['temp_model_name'] == 'claude':
        #     temp_config['model_name'] = "claude"
        else:
            raise ValueError(f"Invalid temp_model_name: {self.config['temp_model_name']}")
        return temp_config

    def set_game_belong_to(self, game: Game):
        self.game_belong_to = game

        other_players = ', '.join([f'Player {_}' for _ in range(1, 7) if _ != self.id])
        attitude_prompt = PromptHint.attitude_prompt if not self.config['without_cot'] else PromptHint.attitude_prompt_without_cot
        self.attitude_prompt: str = attitude_prompt.format(
            role=self.role,
            id=self.id,
            other_players=other_players,
            role_specific_hint=self.game_belong_to.role_hints_without_hide[self.role],
            previous_attitude_to_players="{previous_attitude_to_players}",
        )

    def get_game_history_dict_list(self, ):
        game_history_dict_list = []
        history_str = ""
        for i, (subject, message) in enumerate(self.game_belong_to.get_full_history_list()):
            if subject == f'Player {self.id}':
                history_str += f"Public history {i}: {subject} (yourself): {message}\n\n\n"
            else:
                if self.config['short_memory'] and message == self.game_belong_to.discussion_round_begin_sign:
                    history_str = ""
                history_str += f"Public history {i}: {subject}: {message}\n\n\n"
        game_history_dict_list.append({'role': 'user', 'content': history_str})
        return game_history_dict_list

    def discuss_proposed_team(self, ):
        cur_proposed_team = ', '.join([
            f'player {_}' if _ != self.id else f'player {_} (yourself)' for _ in self.game_belong_to.proposed_team])
        
        if not self.config['tot']:
            if self.config['is_first_think_then_speak']:
                if self.role in ["Morgana", "Assassin"]:
                    prompt = PromptHint.player_discuss_team_evil_side_with_thinking.format(
                        id=self.id, role=self.role,
                        specific_hint=self.game_belong_to.role_hints.get(self.role),
                        proposed_team_players=cur_proposed_team)
                else:
                    prompt = PromptHint.player_discuss_team_good_side_with_thinking.format(
                        id=self.id, role=self.role,
                        specific_hint=self.game_belong_to.role_hints.get(self.role),
                        proposed_team_players=cur_proposed_team)
            else:
                if self.role in ["Morgana", "Assassin"]:
                    prompt = WithoutThinkPrompt.player_discuss_team_evil_side.format(
                        id=self.id, role=self.role,
                        specific_hint=self.game_belong_to.role_hints.get(self.role),
                        proposed_team_players=cur_proposed_team)
                else:
                    prompt = WithoutThinkPrompt.player_discuss_team_good_side.format(
                        id=self.id, role=self.role,
                        specific_hint=self.game_belong_to.role_hints.get(self.role),
                        proposed_team_players=cur_proposed_team)
        else:
            if self.role in ["Morgana", "Assassin"]:
                prompt = PromptHint.player_discuss_team_evil_side_tot.format(
                    id=self.id, role=self.role,
                    specific_hint=self.game_belong_to.role_hints.get(self.role),
                    proposed_team_players=cur_proposed_team)
            else:
                prompt = PromptHint.player_discuss_team_good_side_tot.format(
                    id=self.id, role=self.role,
                    specific_hint=self.game_belong_to.role_hints.get(self.role),
                    proposed_team_players=cur_proposed_team)
            
        retrieved_history = []
        
        latest_game_info = self.game_belong_to.memory_dict_list[-1]
        current_situation_str = self.general_game_status.format(
            current_round=latest_game_info['current_round'],
            current_proposed_team_players=latest_game_info['current_proposed_team_players'],
            current_mission_results=latest_game_info['current_mission_results'],
        )

        retrieved_history.append(dict(
            role='user',
            content=current_situation_str
        ))

        retrieved_history_without_public_history = copy.deepcopy(retrieved_history)

        retrieved_history.extend(self.retrieve_memory(
            get_history_fn=self.get_game_history_dict_list))

        retrieved_history.append(dict(
            role='user',
            content='The above dialogues are the histories of the current discussion round of Avalon games.'))

        retrieved_history = self._use_and_update_player_attitude(
            message_list=retrieved_history,
            output_message_list=retrieved_history_without_public_history if self.config[
                'only_attitude_without_public_history'] else None
        )
        
        if self.config['tot']:
            retrieved_history.append(dict(role='user', content=prompt))
            _, selected_speak_content = self.execute_tot(retrieved_history=retrieved_history, PromptHint=PromptHint)
            return selected_speak_content
        if self.config['is_first_think_then_speak']:
            retrieved_history.append(
                dict(role='user', content=PromptHint.alternate_think_prompt if not self.config['without_cot'] else PromptHint.alternate_think_prompt_without_cot))
        retrieved_history.append(dict(role='user', content=prompt))
        num_original_discuss_revision = 0
        while True:
            action = self.player_call_api(
                input_messages=retrieved_history, config=self.config)
            think_content, speak_content = extract_think_speak(action, config=self.config)
            if judge_contents_valid(think_content, speak_content,
                                    is_first_think_then_speak=self.config['is_first_think_then_speak']):
                break
            else:
                num_original_discuss_revision += 1
                if num_original_discuss_revision > 5:
                    raise RuntimeError("Too many discuss team calls in original explain team")
                if num_original_discuss_revision > 1:
                    retrieved_history = retrieved_history[:-1]
                if self.config['is_first_think_then_speak']:
                    retrieved_history.append(
                        dict(role='user',
                             content=f"Your previous response is:\n{action}\n\nYour previous response does not meet my format requirements. Start your response with the label THINK:, followed by your detailed thoughts on the matter, which should end with 'END'. After that, use the label SPEAK:, and provide your attitude for the proposed team {self.game_belong_to.proposed_team}, based on your prior THINK thoughts, which also should be end with 'END'. Ensure you strictly adhere to this format."))
                else:
                    retrieved_history.append(
                        dict(role='user',
                             content=f"Your previous response is:\n{action}\n\nYour previous response does not meet my format requirements. Start your response with the label 'SPEAK:', and provide your attitude for the proposed team {self.game_belong_to.proposed_team}, which should end with 'END. Ensure you strictly adhere to this format."))

        think_content, speak_content = self.revise_think_speak(
            thinking=think_content,
            speaking=speak_content,
        )

        self.append_private_game_history(
            f"In round {self.game_belong_to.round}, the Player {self.game_belong_to.leader.id} propose the team "
            f"{self.game_belong_to.proposed_team}, my internal thought is:\n{think_content}"
        )
        if self.config['is_first_think_then_speak']:
            self.discuss_content = f"I thought: {think_content}\n I spoke: {speak_content}"
        else:
            self.discuss_content = f"I spoke: {speak_content}"

        return speak_content

    def execute_tot(self, retrieved_history, PromptHint) -> Tuple[str, str]:
        plans_list = []
        speaking_contents_list = []
        # Generate plans
        for i in range(self.config['breadth']):
            plan_prompt = PromptHint.tot_plan_prompt  
            retrieved_history_with_plan_prompt = copy.deepcopy(retrieved_history)
            retrieved_history_with_select_plan_prompt = copy.deepcopy(retrieved_history)
            retrieved_history_with_plan_prompt.append({
                'role': "user",
                "content": plan_prompt,
            })
            cur_plan = self.player_call_api(input_messages=retrieved_history_with_plan_prompt, config=self.config)
            plans_list.append(f"Plan {i+1}: {cur_plan}")
        # choose one plan
        try_num = 0
        while True:
            try_num += 1
            try:
                select_plans_prompt = PromptHint.tot_select_plan_prompt.format(breadth=self.config['breadth'])  # 创建选择计划的提示
                select_plans_prompt += "\n\n".join(plans_list)
                retrieved_history_with_select_plan_prompt.append({
                    'role': "user", 
                    "content": select_plans_prompt
                })
                selected_plan = self.player_call_api(input_messages=retrieved_history_with_select_plan_prompt, config=self.config)
                plan_id = extract_plan_id(selected_plan)
                selected_plan = plans_list[plan_id]
            except:
                if try_num < 5:
                    continue
                else:
                    raise ValueError("Too much try num for selecting plans.")
            break
        for i in range(self.config['breadth']):
            speak_prompt = PromptHint.tot_speak_prompt
            speak_prompt = speak_prompt + selected_plan  
            retrieved_history_with_speak_prompt = copy.deepcopy(retrieved_history)
            retrieved_history_with_speak_prompt.append({
                'role': "user",
                "content": speak_prompt,
            })
            cur_speak = self.player_call_api(input_messages=retrieved_history_with_speak_prompt, config=self.config)
            speaking_contents_list.append(f"Speak {i+1}: {cur_speak}")
        try_num = 0
        while True:
            try_num += 1
            try:
                select_speak_prompt = PromptHint.tot_select_speak_prompt.format(breadth=self.config['breadth']) 
                select_speak_prompt += "\n\n".join(speaking_contents_list)
                retrieved_history_with_speak_prompt.append({
                    'role': "user", 
                    "content": select_speak_prompt,
                })
                selected_speak = self.player_call_api(input_messages=retrieved_history_with_speak_prompt, config=self.config)
                speak_id = extract_speak_id(selected_speak)
                selected_speak = speaking_contents_list[speak_id]
            except:
                if try_num < 5:
                    continue
                else:
                    raise ValueError("Too much try num for selecting speak.")
            break
        return selected_plan, selected_speak
    
    def append_private_game_history(self, think_content: str) -> None:
        if not self.config['is_first_think_then_speak']:
            return
        self.private_game_history.append(think_content)
        memory_status = mark_memory_position(
            round_info=self.game_belong_to.round,
            team_info=self.game_belong_to.proposed_team,
            mission_results_info=self.game_belong_to.round_result,
            mission_vote_results=self.game_belong_to.round_vote_result,
            previous_mission_player=self.game_belong_to.previous_player_team_list,
            previous_mission_leader=self.game_belong_to.previous_leader_list,
        )
        self.private_memory_dict_list.append(memory_status)

    def propose_team(self):
        
        def summarize_proposed_team_players(
            _previous_think_content: str,
            _previous_speak_content: str,
            _current_propose_count: int,
        ):
            """
            return: if return None, it means that the proposed team players are invalid; 
                    else, the integeer indices of the proposed team players are returned.
            """
            _proposed_team_str = self.player_call_api(
                input_messages=[{
                    'role': 'user',
                    'content': f'''\n\nPrevious thinking content:\n\n''' + _previous_think_content + f'''Previous speaking content: {_previous_speak_content}\n\n\nBased on your previous thinking and speaking contents above, summarize which players you want to include in the mission team. You are Player {self.id}, so when referring to 'I', 'myself', 'me', and similar terms in previous thinking and speaking, they all relate to Player {self.id}. Your response format should be "{', '.join([f'Player id{i+1}' for i in range(_current_propose_count)])}" where {', '.join([f'id{i+1}' for i in range(_current_propose_count)])} are the player numbers you want on the team, ranging from 1 to 6.'''
                }],
                config=self.config,
            )

            _matches = re.findall(r'\d', _proposed_team_str)
            _proposed_team = list(set(int(_match) for _match in _matches))

            if len(_proposed_team) != _current_propose_count:
                return None

            _has_invalid_player = False
            for _player in _proposed_team:
                if _player not in range(1, 7):
                    _has_invalid_player = True
                    break
            if _has_invalid_player:
                return None
            
            return _proposed_team
        
        round = self.game_belong_to.round
        if not self.config['tot']:
            if self.config['is_first_think_then_speak']:
                assert self.game_belong_to.round - 1 >= 0
                if self.role in ["Morgana", "Assassin"]:
                    prompt = PromptHint.propose_team_evil_side_with_thinking.format(
                        id=self.id, 
                        role=self.role,
                        specific_hint=self.game_belong_to.role_hints.get(self.role),
                        team_player_num=self.game_belong_to.propose_count[self.game_belong_to.round - 1])
                else:
                    prompt = PromptHint.propose_team_good_side_with_thinking.format(
                        id=self.id, 
                        role=self.role,
                        specific_hint=self.game_belong_to.role_hints.get(self.role),
                        team_player_num=self.game_belong_to.propose_count[self.game_belong_to.round - 1])
            else:
                if self.role in ["Morgana", "Assassin"]:
                    prompt = WithoutThinkPrompt.propose_team_evil_side.format(
                        id=self.id, 
                        role=self.role,
                        specific_hint=self.game_belong_to.role_hints.get(self.role),
                        team_player_num=self.game_belong_to.propose_count[self.game_belong_to.round - 1])
                else:
                    prompt = WithoutThinkPrompt.propose_team_good_side.format(
                        id=self.id, 
                        role=self.role,
                        specific_hint=self.game_belong_to.role_hints.get(self.role),
                        team_player_num=self.game_belong_to.propose_count[self.game_belong_to.round - 1])
        else:
            if self.role in ["Morgana", "Assassin"]:
                prompt = PromptHint.propose_team_evil_side_tot.format(
                    id=self.id, 
                    role=self.role,
                    specific_hint=self.game_belong_to.role_hints.get(self.role),
                    team_player_num=self.game_belong_to.propose_count[self.game_belong_to.round - 1])
            else:
                prompt = PromptHint.propose_team_good_side_tot.format(
                    id=self.id, 
                    role=self.role,
                    specific_hint=self.game_belong_to.role_hints.get(self.role),
                    team_player_num=self.game_belong_to.propose_count[self.game_belong_to.round - 1])

        retrieved_history = []
        latest_game_info = self.game_belong_to.memory_dict_list[-1]
        current_situation_str = self.special_status_propose.format(
            current_round=latest_game_info['current_round'],
            current_mission_results=latest_game_info['current_mission_results']
        )
        retrieved_history.append(dict(
            role='user',
            content=current_situation_str
        ))

        retrieved_history_without_public_history = copy.deepcopy(retrieved_history)
        retrieved_history.extend(self.retrieve_memory(
            get_history_fn=self.get_game_history_dict_list))

        retrieved_history.append(dict(
            role='user',
            content='The above dialogues are the histories of the current discussion round to your current situation. '))

        retrieved_history = self._use_and_update_player_attitude(
            message_list=retrieved_history,
            output_message_list=retrieved_history_without_public_history if self.config[
                'only_attitude_without_public_history'] else None,
        )

        if self.config['tot']:
            retrieved_history.append(dict(role='user', content=prompt))
            try_num = 0
            while True:
                try_num += 1
                selected_plan_content, selected_speak_content = self.execute_tot(retrieved_history=retrieved_history, PromptHint=PromptHint)
                selected_players_indices = summarize_proposed_team_players(
                    _previous_think_content=selected_plan_content,
                    _previous_speak_content=selected_speak_content,
                    _current_propose_count=self.game_belong_to.propose_count[self.game_belong_to.round - 1],
                )
                if selected_players_indices is not None:
                    return selected_players_indices, selected_speak_content
                elif try_num >= 5:
                    raise ValueError(f"Too many try_num in propose_team!")
            
        if self.config['is_first_think_then_speak']:
            retrieved_history.append(
                dict(role='user', content=PromptHint.alternate_think_prompt if not self.config['without_cot'] else PromptHint.alternate_think_prompt_without_cot))
        retrieved_history.append(dict(role='user', content=prompt))

        num_original_propose_revision = 0
        while True:
            num_original_propose_revision += 1
            if num_original_propose_revision > 6:
                raise RuntimeError("Too many propose team calls")
            analysis = self.player_call_api(
                input_messages=retrieved_history, config=self.config)
            think_content, speak_content = extract_think_speak(analysis, config=self.config)
            if num_original_propose_revision > 1:
                retrieved_history = retrieved_history[:-1]
            if not judge_contents_valid(think_content, speak_content,
                                        is_first_think_then_speak=self.config["is_first_think_then_speak"]):
                if self.config["is_first_think_then_speak"]:
                    retrieved_history.append(
                        dict(role='user',
                             content=f"Your previous response is:\n{analysis}\n\nYour previous response does not meet my format requirements. Start your response with the label THINK:, followed by your detailed thoughts on the matter. The thoughts should end with 'END'. After that, use the label SPEAK:, and provide the Players that you want to propose for the mission, based on your prior thoughts. The speaking should also end with 'END'. Ensure you strictly adhere to this format. ")
                    )
                    continue
                else:
                    retrieved_history.append(
                        dict(role='user',
                             content=f"Your previous response is:\n{analysis}\n\nYour previous response does not meet my format requirements. Start your response with the label SPEAK:, and provide the Players that you want to propose for the mission. Your response should end with 'END'. Ensure you strictly adhere to this format.")
                    )
                    continue

            current_propose_count = self.game_belong_to.get_team_size()
            think_content, speak_content = self.revise_think_speak(
                thinking=think_content,
                speaking=speak_content,
                specific_prompt=f"The prompt for {'original THINK and SPEAK' if self.config['is_first_think_then_speak'] else 'original SPEAK'} is as follows, which you also need to follow in revised THINK and SPEAK:\n\n{prompt}"
            )
            
            previous_think_content = f"Previous thinking content: \n\n{think_content}\n\n\n" if self.config[
                'is_first_think_then_speak'] else ''
            proposed_team_str = self.player_call_api(
                input_messages=[{
                    'role': 'user',
                    'content': previous_think_content + f'''Previous speaking content: {speak_content}\n\n\nBased on your previous thinking and speaking contents above, summarize which players you want to include in the mission team. You are Player {self.id}, so when referring to 'I', 'myself', 'me', and similar terms in previous thinking and speaking, they all relate to Player {self.id}. Your response format should be "{', '.join([f'Player id{i}' for i in range(current_propose_count)])}" where {', '.join([f'id{i}' for i in range(current_propose_count)])} are the player numbers you want on the team, ranging from 1 to 6.'''
                }],
                config=self.config,
            )

            matches = re.findall(r'\d', proposed_team_str)
            proposed_team = list(set(int(match) for match in matches))

            if len(proposed_team) != self.propose_count[round - 1]:
                continue

            has_invalid_player = False
            for player in proposed_team:
                if player not in range(1, 7):
                    break
            if has_invalid_player:
                continue
            break

        print(f'Player {self.id} proposed team: {proposed_team}')
        self.append_private_game_history(
            f"In round {self.game_belong_to.round}, I propose the team{proposed_team}, because my internal thought is:\n{think_content}")
        return proposed_team, speak_content

    def vote_on_team(self, ) -> bool:
        def summarize_vote_on_team(
            _previous_think_content: str,
            _previous_speak_content: str,
        ) -> bool:
            """
            return: if return None, it means that the proposed team players are invalid; 
                    else, the integeer indices of the proposed team players are returned.
            """
            _vote_on_team_str = self.player_call_api(
                input_messages=[{
                    'role': 'user',
                    'content': f'''\n\nPrevious thinking content:\n\n''' + _previous_think_content + f'''\n\nPrevious speaking content:\n\n{_previous_speak_content}\n\n\nBased on your previous thinking and speaking contents above, summarize your vote on the proposed team. Kindly utilize only one word, either [approve] or [disapprove] with bracket. No additional words should be included.'''
                }],
                config=self.config,
            )
            _vote_on_team_str_lower = _vote_on_team_str.lower()
            disapprove_flag = ('[disapprove]' in _vote_on_team_str_lower \
                            or '["disapprove"]' in _vote_on_team_str_lower or "['disapprove']" in _vote_on_team_str_lower)
            approve_flag = ('[approve]' in _vote_on_team_str_lower \
                            or '["approve"]' in _vote_on_team_str_lower or "['approve']" in _vote_on_team_str_lower)

            if disapprove_flag and not approve_flag:
                return False
            elif approve_flag and not disapprove_flag:
                return True
            else:
                return None

        retrieved_history = [
            dict(role='user',
                 content=PromptHint.previous_discussion_content.format(discuss_content=self.discuss_content))
        ]

        cur_proposed_team = ', '.join([f'player {_}' for _ in self.game_belong_to.proposed_team])

        if not self.config['tot']:
            if self.config['is_first_think_then_speak']:
                if self.role in ["Morgana", "Assassin"]:
                    prompt = PromptHint.player_team_vote_evil_side_with_thinking.format(
                        id=self.id, 
                        role=self.role,
                        specific_hint=self.game_belong_to.role_hints_without_hide.get(self.role),
                        current_proposed_team_players=cur_proposed_team)
                else:
                    prompt = PromptHint.player_team_vote_good_side_with_thinking.format(
                        id=self.id, 
                        role=self.role,
                        specific_hint=self.game_belong_to.role_hints_without_hide.get(self.role),
                        current_proposed_team_players=cur_proposed_team)
            else:
                if self.role in ["Morgana", "Assassin"]:
                    prompt = WithoutThinkPrompt.player_team_vote_evil_side.format(
                        id=self.id, role=self.role,
                        specific_hint=self.game_belong_to.role_hints_without_hide.get(self.role),
                        current_proposed_team_players=cur_proposed_team)
                else:
                    prompt = WithoutThinkPrompt.player_team_vote_good_side.format(
                        id=self.id, role=self.role,
                        specific_hint=self.game_belong_to.role_hints_without_hide.get(self.role),
                        current_proposed_team_players=cur_proposed_team)
        else:
            if self.role in ["Morgana", "Assassin"]:
                prompt = PromptHint.player_team_vote_evil_side_tot.format(
                    id=self.id,
                    role=self.role,
                    specific_hint=self.game_belong_to.role_hints_without_hide.get(self.role),
                    current_proposed_team_players=cur_proposed_team,
                )
            else:
                prompt = PromptHint.player_team_vote_good_side_tot.format(
                    id=self.id,
                    role=self.role,
                    specific_hint=self.game_belong_to.role_hints_without_hide.get(self.role),
                    current_proposed_team_players=cur_proposed_team,
                )

        latest_game_info = self.game_belong_to.memory_dict_list[-1]
        current_situation_str = self.general_game_status.format(
            current_round=latest_game_info['current_round'],
            current_proposed_team_players=latest_game_info['current_proposed_team_players'],
            current_mission_results=latest_game_info['current_mission_results']
        )
        retrieved_history.append(dict(
            role='user',
            content=current_situation_str
        ))

        retrieved_history_without_public_history = copy.deepcopy(retrieved_history)
        retrieved_history.extend(self.retrieve_memory(
            get_history_fn=self.get_game_history_dict_list))

        retrieved_history.append(dict(
            role='user',
            content='The above dialogues are the histories of the current discussion round. '))

        retrieved_history = self._use_and_update_player_attitude(
            message_list=retrieved_history,
            output_message_list=retrieved_history_without_public_history if self.config[
                'only_attitude_without_public_history'] else None,
        )
                
        retrieved_history.append(dict(role='user', content=prompt))
        if self.config['tot']:
            try_num = 0
            while True:
                try_num += 1
                selected_think_content, selected_speak_content = self.execute_tot(retrieved_history=retrieved_history, PromptHint=PromptHint)
                vote = summarize_vote_on_team(
                    _previous_think_content=selected_think_content,
                    _previous_speak_content=selected_speak_content,
                )
                if vote is not None:
                    return vote
                else:
                    if try_num >= 5:
                        raise ValueError(f"Too many try_num in vote_on_team!")

        if self.config['is_first_think_then_speak']:
            retrieved_history.append(
                dict(role='user', content=PromptHint.alternate_think_prompt if not self.config['without_cot'] else PromptHint.alternate_think_prompt_without_cot))
        num_original_team_revision = 0
        num_revised_team_revision = 0

        generate_revise_loop_continue = True
        while generate_revise_loop_continue:
            generate_revise_loop_continue = False
            while True:
                action = self.player_call_api(
                    input_messages=retrieved_history, config=self.config)
                think_content, speak_content = extract_think_speak(action, config=self.config)
                if judge_contents_valid(think_content, speak_content,
                                        is_first_think_then_speak=self.config['is_first_think_then_speak']):
                    break
                else:
                    num_original_team_revision += 1
                    if num_original_team_revision > 5:
                        raise RuntimeError("Too many revision calls in original vote on team")
                    if num_revised_team_revision > 1:
                        retrieved_history = retrieved_history[:-1]
                    if self.config['is_first_think_then_speak']:
                        retrieved_history.append(
                            dict(role='user',
                                 content=f"Your previous response is:\n{action}\n\nYour previous response does not meet my format requirements. Start your response with the label 'THINK:', followed by your detailed thoughts on the matter, and add 'END' at the end of your thoughts. After that, use the label SPEAK:, and provide the response, either [approve] or [disapprove] with bracket [] based on your prior thoughts, and add 'END' at the end of your speaking. For example: 'SPEAK: [approve] END' or 'SPEAK: [disapprove] END'. Ensure you strictly adhere to this format. "))
                    else:
                        retrieved_history.append(
                            dict(role='user',
                                 content=f"Your previous response is:\n{action}\n\nYour previous response does not meet my format requirements. Start your response with the label SPEAK:, and provide the response, either [approve] or [disapprove] with bracket [], which should be end with 'END'. For example: SPEAK: [approve] END. You must add END in the end of your speak phase! Ensure you strictly adhere to this format. "))

            specific_prompt = [
                "In the REVISED SPEAK phase, to articulate your vote, kindly utilize only one word, either [approve] or [disapprove] with brackets []. Note that brackets of [approve] or [disapprove] is very important and cannot be omitted. No additional words should be included. "]
            while True:
                think_content, speak_content = self.revise_think_speak(
                    thinking=think_content,
                    speaking=speak_content,
                    specific_prompt='\n\n'.join(specific_prompt),
                    is_role_hint_no_hide=True,
                )

                self.append_private_game_history(
                    f"In round {self.game_belong_to.round}, For the proposed team {self.game_belong_to.proposed_team}, my internal thought is:\n{think_content}")
                speak_content_lower = speak_content.lower()
                disapprove_flag = ("[disapprove]" in speak_content_lower \
                                   or "['disapprove']" in speak_content_lower or '["disapprove"]' in speak_content_lower)
                approve_flag = ("[approve]" in speak_content_lower \
                                or "['approve']" in speak_content_lower or '["approve"]' in speak_content_lower)

                if disapprove_flag and not approve_flag:  
                    return False
                elif approve_flag and not disapprove_flag:  
                    return True
                else:
                    num_revised_team_revision += 1
                    if num_revised_team_revision > 5:
                        raise RuntimeError(f'Too many revision calls in revised vote on team.')
                    if num_revised_team_revision > 1:
                        specific_prompt = specific_prompt[:-1]
                    specific_prompt.append(
                        f"\nYour previous response is:\n{speak_content}\n\nYour previous response does not meet my format requirements. I want you to only give a word [approve] or [disapprove] with bracket [] in the revised speak phase to express whether you approve this proposed team or not.\n")

                    if self.config["is_revision_think_speak"]:
                        continue
                    else:
                        generate_revise_loop_continue = True
                        break

    def vote_on_mission(self):
        def summarize_vote_on_mission(
            _previous_think_content: str,
            _previous_speak_content: str,
        ):
            """
            return: if return None, it means that the proposed team players are invalid; 
                    else, the integeer indices of the proposed team players are returned.
            """
            _vote_on_mission_str = self.player_call_api(
                input_messages=[{
                    'role': 'user',
                    'content': f'''\n\nPrevious thinking content:\n\n''' + _previous_think_content + f'''\n\nPrevious speaking content:\n\n{_previous_speak_content}\n\n\nBased on your previous thinking and speaking contents above, summarize your vote on this mission. Kindly utilize only one word, either [success] or [fail] with bracket. No additional words should be included.'''
                }],
                config=self.config,
            )
            _vote_on_team_str_lower = _vote_on_mission_str.lower()
            fail_flag = ('[fail]' in _vote_on_team_str_lower \
                            or '["fail"]' in _vote_on_team_str_lower or "['fail']" in _vote_on_team_str_lower)
            success_flag = ('[success]' in _vote_on_team_str_lower \
                            or '["success"]' in _vote_on_team_str_lower or "['success']" in _vote_on_team_str_lower)

            if fail_flag and not success_flag:
                return "Fail"
            elif success_flag and not fail_flag:
                return "Success"
            else:
                return None

        """In Mission vote"""
        if self.role in ['Loyal servant of arthur', 'Merlin', 'Percival']:
            return 'Success'

        if not self.config['tot']:
            if self.config['is_first_think_then_speak']:
                prompt = PromptHint.evil_player_decision_on_mission_with_thinking.format(
                    id=self.id, role=self.role,
                    specific_hint=self.game_belong_to.role_hints.get(self.role))
            else:
                prompt = WithoutThinkPrompt.evil_player_decision_on_mission.format(
                    id=self.id, role=self.role,
                    specific_hint=self.game_belong_to.role_hints.get(self.role))
        else:
            prompt = PromptHint.evil_player_decision_on_mission_tot.format(
                id=self.id,
                role=self.role,
                specific_hint=self.game_belong_to.role_hints.get(self.role),
            )

        retrieved_history = []
        latest_game_info = self.game_belong_to.memory_dict_list[-1]
        current_situation_str = self.general_game_status.format(
            current_round=latest_game_info['current_round'],
            current_proposed_team_players=latest_game_info['current_proposed_team_players'],
            current_mission_results=latest_game_info['current_mission_results']
        )

        retrieved_history.append(dict(
            role='user',
            content=current_situation_str
        ))

        retrieved_history_without_public_history = copy.deepcopy(retrieved_history)
        retrieved_history.extend(self.retrieve_memory(
            get_history_fn=self.get_game_history_dict_list))

        retrieved_history.append(dict(
            role='user',
            content='The above dialogues are the histories of the current discussion round. '))

        retrieved_history = self._use_and_update_player_attitude(
            message_list=retrieved_history,
            output_message_list=retrieved_history_without_public_history if self.config[
                'only_attitude_without_public_history'] else None,
        )
        
        if self.config['tot']:
            retrieved_history.append(dict(role='user', content=prompt))
            try_num = 0
            while True:
                try_num += 1
                selected_plan_content, selected_speak_content = self.execute_tot(retrieved_history=retrieved_history, PromptHint=PromptHint)
                vote = summarize_vote_on_mission(
                    _previous_think_content=selected_plan_content,
                    _previous_speak_content=selected_speak_content)
                if vote is not None:
                    return vote
                elif try_num >= 5:
                    raise ValueError(f"Too many try_num in propose_team!")
        
        if self.config['is_first_think_then_speak']:
            retrieved_history.append(
                dict(role='user', content=PromptHint.alternate_think_prompt if not self.config['without_cot'] else PromptHint.alternate_think_prompt_without_cot))
        retrieved_history.append(dict(role='user', content=prompt))
        retrieved_history.append(dict(role='user',
                                      content="In the SPEAK section, to articulate your vote, kindly utilize only one word, either [success] or [fail] with bracket. No additional words should be included."))

        generate_revise_loop_continue = True
        num_original_mission_revision = 0
        while generate_revise_loop_continue:
            generate_revise_loop_continue = False
            while True:
                decision = self.player_call_api(
                    input_messages=retrieved_history, config=self.config)
                think_content, speak_content = extract_think_speak(decision, config=self.config)
                if judge_contents_valid(think_content, speak_content,
                                        is_first_think_then_speak=self.config['is_first_think_then_speak']):
                    break
                else:
                    num_original_mission_revision += 1
                    if num_original_mission_revision > 5:
                        raise RuntimeError("Too many original mission calls in vote on mission")
                    if num_original_mission_revision > 1:
                        retrieved_history = retrieved_history[:-1]
                    if self.config['is_first_think_then_speak']:
                        retrieved_history.append(dict(role='user',
                                                      content=f"Your previous response is:\n{decision}\n\nYour previous response does not meet my format requirements. Start your response with the label THINK:, followed by your detailed thoughts on the matter, which should end with 'END'. After that, use the label SPEAK:, and provide a one-word response, either [success] or [fail] with bracket [] based on your prior THINK thoughts, which also should end with 'END'. Ensure you strictly adhere to this format."))
                    else:
                        retrieved_history.append(dict(role='user',
                                                      content=f"Your previous response is:\n{decision}\n\nYour previous response does not meet my format requirements. Start your response with the label SPEAK:, and provide a one-word response, either [success] or [fail] with bracket [], which should end with 'END'. Ensure you strictly adhere to this format."))
                    continue
            num_mission_revision = 0
            if self.config['is_first_think_then_speak']:
                specific_prompt = [
                    f"The original think and speak you get now were generated based on this prompt:\n\n{prompt}\n\nPlease also base on this prompt when you revise, try not to change [fail] to [success] in the REVISED SPEAK section. To articulate your vote, kindly utilize only one word, either [success] or [fail] with brakcet. No additional words should be included. "]
            else:
                specific_prompt = [
                    f"The original speak you get now were generated based on this prompt:\n\n{prompt}\n\nPlease also base on this prompt when you revise, try not to change [fail] to [success] in the REVISED SPEAK section. To articulate your vote, kindly utilize only one word, either [success] or [fail] with brakcet. No additional words should be included. "]

            while True:
                think_content, speak_content = self.revise_think_speak(
                    thinking=think_content,
                    speaking=speak_content,
                    specific_prompt='\n\n'.join(specific_prompt)
                )

                self.append_private_game_history(
                    f"In round {self.game_belong_to.round}, I am included in this round mission with team {self.game_belong_to.proposed_team}, my internal thought is:\n{think_content}")

                speak_content_lower = speak_content.lower()
                fail_flag = ('[fail]' in speak_content_lower \
                             or '["fail"]' in speak_content_lower or "['fail']" in speak_content_lower)
                success_flag = ('[success]' in speak_content_lower \
                                or '["success"]' in speak_content_lower or "['success']" in speak_content_lower)

                if fail_flag and not success_flag:
                    return "Fail"
                elif success_flag and not fail_flag:
                    return "Success"
                else:
                    num_mission_revision += 1
                    if num_mission_revision > 6:
                        raise RuntimeError(f'Too many revision calls.')
                    if num_mission_revision > 1:
                        specific_prompt = specific_prompt[:-1]
                    specific_prompt.append(
                        f"\nYour previous response is:\n{speak_content}\n\nYour previous response does not meet my format requirements. I want you to only give a word [success] or [fail] with bracket [] in the revised speak phase to express whether you want the mission to fail or succeed.\n")

                    if self.config["is_revision_think_speak"]:
                        continue
                    else:
                        generate_revise_loop_continue = True
                        break

    def guess_merlin(self, ) -> int:
        
        def summarize_guessed_merlin(_speak_content: str) -> int:
            _guess_int = re.findall('\d', _speak_content)
            _guess_int = list(set(_guess_int))
            if len(_guess_int) == 1:
                _guess_int = _guess_int[0]
                _guess_int = int(_guess_int)
                if _guess_int in [_ for _ in range(1, 7)]:
                    return _guess_int

            # If contains more than one number, use gpt to summarize it.
            _propose_merlin = self.player_call_api(
                input_messages=[{
                    'role': 'user',
                    'content': f'''This is a previous speaking content from a player who is playing Avalon game as role 'Assassin': {_speak_content}\n Based on the Assassin's previous statements, can you sum it up for me, who the assassin thinks is Merlin. Your response should be formatted as follows: "Player X is Merlin," where X is an integer ranging from 1 to 6. Only respond in this specified format without any extra contents.'''
                }],
                config=self.config, 
            )
            _guess_int = re.findall('\d', _propose_merlin)
            _guess_int = list(set(_guess_int))
            if len(_guess_int) == 1:
                _guess_int = _guess_int[0]
                _guess_int = int(_guess_int)
                if _guess_int in [_ for _ in range(1, 7)]:
                    return _guess_int
            else:
                return None
        
        """Assassin has one chance to guess who Merlin is"""

        if not self.config['tot']:
            if self.config['is_first_think_then_speak']:
                prompt = PromptHint.assassin_prompt_with_thinking.format(
                    id=self.id, 
                    role=self.role,
                    specific_hint=self.game_belong_to.role_hints_without_hide.get(self.role))
            else:
                prompt = WithoutThinkPrompt.assassin_prompt.format(
                    id=self.id, 
                    role=self.role,
                    specific_hint=self.game_belong_to.role_hints_without_hide.get(self.role))
        else:
            prompt = PromptHint.assassin_prompt_tot.format(
                id=self.id,
                role=self.role,
                specific_hint=self.game_belong_to.role_hints_without_hide.get(self.role)
            )

        retrieved_history = []

        latest_game_info = self.game_belong_to.memory_dict_list[-1]
        current_situation_str = self.general_game_status.format(
            current_round=latest_game_info['current_round'],
            current_proposed_team_players=latest_game_info['current_proposed_team_players'],
            current_mission_results=latest_game_info['current_mission_results']
        )
        retrieved_history.append(dict(
            role='user',
            content=current_situation_str
        ))
        retrieved_history_without_public_history = copy.deepcopy(retrieved_history)
        retrieved_history.extend(self.retrieve_memory(
            get_history_fn=self.get_game_history_dict_list))

        retrieved_history.append(dict(
            role='user',
            content='The above dialogues are the histories of the current discussion round. '))

        retrieved_history = self._use_and_update_player_attitude(
            message_list=retrieved_history,
            output_message_list=retrieved_history_without_public_history if self.config[
                'only_attitude_without_public_history'] else None,
        )
        retrieved_history.append(dict(role='user', content=prompt))
        
        if self.config['tot']:
            try_num = 0
            while True:
                try_num += 1
                _, selected_speak_content = self.execute_tot(retrieved_history=retrieved_history, PromptHint=PromptHint)
                guess_int = summarize_guessed_merlin(
                    _speak_content=selected_speak_content)
                if guess_int is not None:
                    return guess_int
                elif try_num >= 5:
                    raise ValueError(f"Too many try_num in propose_team!")
        
        
        if self.config['is_first_think_then_speak']:
            retrieved_history.append(
                dict(role='user', content=PromptHint.alternate_think_prompt if not self.config['without_cot'] else PromptHint.alternate_think_prompt_without_cot))

        generate_revise_loop_continue = True
        num_original_guess_revision = 0
        while generate_revise_loop_continue:
            generate_revise_loop_continue = False
            while True:
                guess_string = self.player_call_api(
                    input_messages=retrieved_history, config=self.config)
                think_content, speak_content = extract_think_speak(guess_string, config=self.config)
                if judge_contents_valid(think_content, speak_content,
                                        is_first_think_then_speak=self.config['is_first_think_then_speak']):
                    break
                else:
                    num_original_guess_revision += 1
                    if num_original_guess_revision > 5:
                        raise RuntimeError("Too many guess calls")
                    if num_original_guess_revision > 1:
                        retrieved_history = retrieved_history[:-1]
                    if self.config['is_first_think_then_speak']:
                        retrieved_history.append(dict(role='user',
                                                      content=f"Your previous response is:\n{speak_content}\n\nYour previous response does not meet my format requirements. Start your response with the label THINK:, followed by your detailed thoughts on the matter, which should end with 'END'. After that, use the label SPEAK:, and provide a Player id who you think is Merlin. For example, Player 2, which also should end with 'END'. Ensure you strictly adhere to this format."))
                    else:
                        retrieved_history.append(dict(role='user',
                                                      content=f"Your previous response is:\n{speak_content}\n\nYour previous response does not meet my format requirements. Start your response with the label SPEAK:, and provide a Player id who you think is Merlin. For example, Player 2, which should end with 'END'. Ensure you strictly adhere to this format."))

            num_guess_revised_revision = 0
            specific_prompt = [
                f"In the SPEAK section, please name one Player you think is Merlin. And respond only the Player number. For example: Player 2."]
            while True:
                think_content, speak_content = self.revise_think_speak(
                    thinking=think_content,
                    speaking=speak_content,
                    specific_prompt='\n\n'.join(specific_prompt),
                    allow_other_player_analysis=False, )

                guess_int = re.findall('\d', speak_content)
                guess_int = list(set(guess_int))
                if len(guess_int) == 1:
                    guess_int = guess_int[0]
                    guess_int = int(guess_int)
                    if guess_int in [_ for _ in range(1, 7)]:
                        break

                propose_merlin = self.player_call_api(
                    input_messages=[{
                        'role': 'user',
                        'content': f'''This is a previous speaking content from a player who is playing Avalon game as role 'Assassin': {speak_content}\n Based on the Assassin's previous statements, can you sum it up for me, who the assassin thinks is Merlin. Your response should be formatted as follows: "Player X is Merlin," where X is an integer ranging from 1 to 6. Only respond in this specified format without any extra contents.'''
                    }],
                    config=self.config,
                )
                guess_int = re.findall('\d', propose_merlin)
                guess_int = list(set(guess_int))
                num_guess_revised_revision += 1
                if len(guess_int) == 1:
                    guess_int = guess_int[0]
                    guess_int = int(guess_int)
                    if guess_int in [_ for _ in range(1, 7)]:
                        break
                else:
                    if num_guess_revised_revision > 5:
                        raise RuntimeError("Too many class in guessing merlin id")
                    if num_guess_revised_revision > 1:
                        specific_prompt = specific_prompt[:-1]
                    specific_prompt.append(
                        f"Your previous response is:\n{speak_content}\n\nYour previous response does not meet my format requirements. Provide a Player id who you think is Merlin in revised SPEAK phase. For example, Player 2. Regardless of your certainty, you must provide a Player ID that you believe has the highest likelihood of being Merlin.")

                    if self.config["is_revision_think_speak"]:
                        continue
                    else:
                        generate_revise_loop_continue = True
                        break
        return int(guess_int)

    def revise_think_speak(self, thinking: str, speaking: str, specific_prompt: str = None,
                           is_role_hint_no_hide: bool = False,
                           allow_other_player_analysis: bool = True):
        if not self.config['is_revision_think_speak']:
            return thinking, speaking

        latest_game_info = self.game_belong_to.memory_dict_list[-1]
        current_situation_str = self.description_str.format(
            current_round=latest_game_info['current_round'],
            current_proposed_team_players=latest_game_info['current_proposed_team_players'],
            current_mission_results=latest_game_info['current_mission_results']
        )
        role_str = ', '.join(self.role_list)
        if is_role_hint_no_hide:
            role_hint = self.game_belong_to.role_hints_without_hide[self.role]
        else:
            role_hint = self.game_belong_to.role_hints[self.role]
        if len(role_hint) > 0:
            role_hint = f"The hint for {self.role} is:\n{role_hint}\n\n"

        system_role_hint_prompt = self.game_belong_to.role_hints.get(self.role, "")
        input_messages = [
            {
                'role': 'system',
                'content': "You are an expert in Avalon game strategy. "
            },
            {
                'role': 'user',
                'content': f"The hint for {self.role} is:\n{system_role_hint_prompt}",
            }
        ]  

        if allow_other_player_analysis and self.config['other_player_analysis']:
            input_messages.append({
                'role': 'user',
                'content': f"I know that you are playing the role of {self.role}. {current_situation_str}\n\nBelow is your original SPEAK content:\n\n{speaking}\n\nPlease analyze how your original SPEAK might be interpreted by the other game roles, including {role_str}. Consider their perspectives one by one, and describe what you believe they would think. Then, reflect on your original SPEAK to determine whether it may inadvertently reveal your role, giving away any unique hints or clues that are specific to your role. Think step by step and respond concisely."
            })
            perspective_analysis_response = self.player_call_api(input_messages=input_messages,
                                                                 config=self._get_temp_config(), )
            self.perspective_analysis_response = perspective_analysis_response
            input_messages.append({
                'role': 'assistant',
                'content': perspective_analysis_response,
            })
        else:
            perspective_analysis_response = 'Empty'

        if self.config['revision_add_history']:
            assert self.config['short_memory'], f'Currently only support short memory!'
            input_messages.append(dict(
                role='user',
                content='The dialogues below are the histories of the current discussion round. '))
            input_messages.extend(self.retrieve_memory(
                get_history_fn=self.get_game_history_dict_list))

        revise_prompts = []

        if 'claude' in self.config['model_name']:
            if self.role not in ['Morgana', 'Assassin']:
                extra_revise_prompt = \
                    'Your revised SPEAK should not let any suspicious or evil players be included in the mission team.'
            else:
                extra_revise_prompt = 'Your revised SPEAK should let evil players be included in the mission team.'
        else:
            extra_revise_prompt = ''

        if self.config['is_first_think_then_speak']:
            revise_prompt = PromptHint.revise_prompt if not self.config['without_cot'] else PromptHint.revise_prompt_without_cot
            revise_prompts.append(
                revise_prompt.format(
                    role_hint_prompt=f"The information of role {self.role} is as follows:\n{role_hint}" if len(
                        role_hint) > 0 else '',
                    current_situation_str=current_situation_str,
                    id=self.id,
                    role=self.role,
                    desired_result='fail' if self.role in ['Morgana', 'Assassin'] else 'success',
                    extra_revise_prompt=extra_revise_prompt,
                )
            )
        else:
            revise_prompts.append(
                WithoutThinkPrompt.revise_prompt.format(
                    role_hint_prompt=f"The information of role {self.role} is as follows:\n{role_hint}" if len(
                        role_hint) > 0 else '',
                    current_situation_str=current_situation_str,
                    id=self.id,
                    role=self.role,
                    desired_result='fail' if self.role in ['Morgana', 'Assassin'] else 'success',
                    extra_revise_prompt=extra_revise_prompt,
                )
            )
        if specific_prompt is not None:
            revise_prompts.append(specific_prompt)
        for _ in revise_prompts:
            if _ is not None:
                input_messages.append({'role': "user", "content": _})
        if self.config['is_first_think_then_speak']:
            input_messages.append({
                'role': "user",
                "content": (f"The original THINK you generated before is:\n{thinking}\n\n and "
                            f"the original SPEAK you generated before is:\n{speaking}\n\n")
            })
        else:
            input_messages.append({'role': "user",
                                   "content": f"The original SPEAK you generated before is:\n{speaking}\n\n"})

        num_revision = 0
        while True:
            revision_results = self.player_call_api(
                input_messages=input_messages,
                config=self._get_temp_config(),
            )
            revised_think_contents, revised_speak_contents = extract_think_speak_in_revision(
                revision_results, config=self.config)

            if self.config['is_first_think_then_speak']:
                if len(revised_think_contents.strip()) > 0 and len(revised_speak_contents.strip()) > 0:
                    break
                else:
                    input_messages.append({'role': 'assistant', 'content': revision_results})
                    input_messages.append({'role': 'user',
                                           'content': 'Please note that your previous revision omitted the required markers. The content for "revised think" should begin with "REVISED THINK" in all uppercase letters and end with "END" in all uppercase letters. Similarly, the "revised speak" content should start with "REVISED SPEAK" in all uppercase letters and end with "END" in all uppercase letters. Your response must follow the format like: REVISED THINK: ... END. REVISED SPEAK: ... END. (... represents your generated text)'})
            else:
                if len(revised_speak_contents.strip()) > 0:
                    break
                else:
                    input_messages.append({'role': 'assistant', 'content': revision_results})
                    input_messages.append({'role': 'user',
                                           'content': 'Please note that your previous revision omitted the required markers. The "revised speak" content should start with "REVISED SPEAK" in all uppercase letters and end with "END" in all uppercase letters. Your response must follow the format like: REVISED SPEAK: ... END. (... represents your generated text)'})
            num_revision += 1
            if num_revision > 5:
                raise RuntimeError(f'Too many revision calls.')

        return revised_think_contents, revised_speak_contents

    def retrieve_memory(
            self,
            get_history_fn: Callable,
    ):
        game_history = get_history_fn()
        assert self.config['short_memory'] and get_history_fn == self.get_game_history_dict_list

        return game_history

    def player_call_api(self, input_messages, *args, **kwargs):
        system_identity_prompt = f"You are playing Avalon game like a real human. You are Player {self.id} and your role is {self.role}. There are 6 Players in the game."
        game_rule = PromptHint.game_rule

        prompts_at_the_beginning = [
            {'role': 'system',
             'content': system_identity_prompt},
        ]

        num_system_prompt_in_input_messages = 0
        for message in input_messages:
            if message['role'] == 'system':
                prompts_at_the_beginning.append(message)
                num_system_prompt_in_input_messages += 1
            else:
                break
        prompts_at_the_beginning.append(
            {'role': 'user',
             'content': (
                 f"\n\n\nThe rule of the Avalon game is:\n{game_rule}\n\n\n"
                 f"In the current mission, the proposed team should include {self.game_belong_to.get_team_size()} players.\n\n"
             )
             }
        )
        input_messages = input_messages[num_system_prompt_in_input_messages:]

        new_input_messages = prompts_at_the_beginning + input_messages

        ret = call_api(input_messages=new_input_messages, *args, **kwargs)
        return ret

    def _use_and_update_player_attitude(self, message_list: List[Dict], output_message_list: List[Dict] = None):
        if self.game_belong_to.round == 1:  # In the first round, we do not guess any player
            return message_list

        if output_message_list is None:
            output_message_list = message_list
        pure_history = copy.deepcopy(message_list)
        if self.config["add_player_attitude"]:
            pure_history.append(
                dict(
                    role='user',
                    content=self.attitude_prompt.format(previous_attitude_to_players=self.attitude_player),
                )
            )

            self.attitude_player = self.player_call_api(input_messages=pure_history, config=self._get_temp_config())
            if len(self.attitude_player) > 0:
                output_message_list.append(
                    dict(
                        role='user',
                        content=f"The following represents your current attitude towards other Players in the game:\n{self.attitude_player}.\n Analyze and consider this information.",
                    )
                )
                
        return output_message_list
