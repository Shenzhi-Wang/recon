from dataclasses import dataclass


@dataclass
class PromptHint:
    game_rule = "In a six-person game of Avalon, the choice of roles and strategies is crucial. Merlin, who knows the identities of the evil characters, needs to subtly pass information to guide the forces of good without revealing his identity to the forces of evil. " \
                "Percival, is challenged to discern the true Merlin from Morgana, who is posing as Merlin to sow confusion. " \
                "Loyal servant of arthur, without special abilities, must rely on voting and discussion to identify the forces of evil. " \
                "Morgana needs to convincingly impersonate Merlin to deceive Percival and other forces of good, while working with the Assassin to conceal the real Merlin. " \
                "The Assassin needs to act discreetly, seek Merlin's identity, and aim to assassinate Merlin during the final stage of the game if the good side wins three rounds. " \
                "In this game, there are one Merlin, one Percival, two Loyal servant of arthur, one Morgana and one Assassin. So please only consider those roles when you think and speak. " \
                "Each role must strive to lead their team to victory while operating with limited information."
    role_hints = {
        "Merlin": "As Merlin, you know the identities and ids of all evil players. " \
                  "Pass information subtly without revealing your role, and work towards earning Percival's trust. " \
                  "Cooperate with Percival to guide your team to victory, but remember, never openly indicate your identity. " \
                  "Avoid these behaviours as they might expose your role and lead to a loss in the game: " \
                  "first, displaying too much knowledge about who is Morgana and Assassin; " \
                  "second, accusing an evil player when there's little or no evidence; " \
                  "third, being overly helpful to the good side. " \
                  "As Merlin in Avalon, subtly influence the decisions of the team without clearly identifying the evil players, to avoid drawing attention from the Assassin. " \
                  "Remember, never say 'As Merlin' or similar words, which would expose your role." \
                  "Your goal is to win the game. You can do this by tactfully concealing your and your teammates' roles and, if necessary, misleading other players. However, always remember that other players might employ the same tactics and attempt to deceive you as well.",

        "Percival": "As Percival, you know Merlin and Morgana but can't differentiate between them. Your task is to ascertain their true identities through their actions. Utilize Merlin's cues to guide your team to victory in Avalon. As Percival, steer your team subtly, ensuring not to inadvertently expose Merlin or Morgana, protecting Merlin from the Assassin. Your goal is to win. To achieve this, strategically hide your and your allies' roles and, when necessary, deceive other players, even if it means revealing your own identity - but take care not to expose Merlin. Remember, others may also resort to deception." \
                    "The goal of Percival is to assist in the successful completion of three out of five missions. Percival should use dialogue and voting behaviors to infer the true identities of Merlin and Morgana, while safeguarding Merlin from being discovered by the Assassin.",

        "Loyal servant of arthur": "As a Loyal Servant of Arthur, your main tasks are to contribute to the success of your missions " \
                                   "and to protect Merlin's identity by drawing suspicion onto yourself. " \
                                   "Your objective is to win the game. You can do this by tactfully concealing your and your teammates' roles and, if necessary, misleading other players. However, always remember that other players might employ the same tactics and attempt to deceive you as well." \
                                   "The goal of the Loyal Servant of Arthur is to assist in the successful completion of three out of five missions for the good side. " \
                                   "Through the dialogue and voting behaviors, Loyal servant of arthur should judge who is Morgana and who is Assassin in order to help the good side to win.",


        "Morgana": "As Morgana, your role is to infiltrate Arthur's servants, posing as good during SPEAK, but always remember your allegiance to the evil side. Your subtle misdirections should aim to create confusion and prevent three missions from succeeding. Mislead Percival while maintaining your disguise, but during voting, your true purpose is to obstruct the success of the missions. Remember, the forces of evil win by either preventing three missions from being successful or by assassinating Merlin.",

        "Assassin": "As an Assassin, your dual objective is to find Merlin and prevent the success of three missions. Mimic the good side during SPEAK, but never lose sight of your true evil allegiance. Use dialogues and interactions to gather clues about Merlin. While blending in is crucial, remember that your primary objective during votes is to sabotage the missions. If the good side completes three successful missions, your final resort is to correctly identify and assassinate Merlin. Winning the game for the forces of evil requires a fine balance of deception and strategic voting.",

    }

    non_disclosure_prompt_with_thinking = "Note: You have received a special hint enclosed in double asterisks (*special hint*) above. Use this information for internal analysis in the THINK phase, but do not disclose the content between these double asterisks in the SPEAK phase. Keep the information confidential and use it wisely."

    # =====================================================================================================================================================================================================================================

    propose_team_good_side_with_thinking = \
        (
            "**Thinking Process (Private)**:\n"
            "You are Player {id} with the role of {role} in this round of Avalon. As {role}, you are privy to a special hint. Your special hint is: *{specific_hint}*. Please use this information wisely but do not disclose it. "   
            "Your objective is to devise a mission team consisting of {team_player_num} players. "
            "During this stage, reflect on the game's history, the current situation, and any special hints you've received. "
            "As you ponder on each player's suitability, consider:\n"
            "1. The player's involvement and actions up until this point.\n"
            "2. How this player contributed in past missions.\n"
            "3. Has any player in history indicated they are on the evil side, either as Morgana or Assassin, or advocated for the evil side?\n"
            "4. Any behavior from this player that either seems suspicious or trustworthy.\n\n"
            "You don't need to answer these points directly, but let them shape your decisions.\n\n"

            "**Speaking Process (Public)**:\n"
            "Once you've formulated your team, present it to the rest of the players. "
            "Provide a detailed rationale that draws from past events, player behaviors, and your strategy to garner trust and support for your team selection. "
            "While articulating your reasons, make sure not to disclose your role or any private hints, since all players will hear your explanation.\n\n"

            "Throughout both processes, remember:\n"
            "1. You are on the good side, your primary goal is to ensure no evil or suspicious (for example, participated in a failed mission) players are on your team.\n"
            "2. It's conventional for the team leader, in this case, Player {id}, to include themselves. "
            "If you opt out, you must clarify this decision to the group."
        ) + "\n" + non_disclosure_prompt_with_thinking + "Please remember to propose a mission team composed of {team_player_num} members."

    propose_team_evil_side_with_thinking = \
        (
            "**Thinking Process (Private)**:\n"
            "You are Player {id} with the role of {role} in this round of Avalon. As {role}, you are privy to a special hint. Your special hint is: *{specific_hint}*. Please use this information wisely but do not disclose it. "    
            "Your objective is to propose a mission team consisting of {team_player_num} players. "
            "During this stage, reflect on the game's history, the current situation, and any special hints you've received. "
            "As you ponder on each player's suitability, consider:\n"
            "1. The player's involvement and actions up until this point.\n"
            "2. How this player contributed in past missions.\n"
            "3. Any behavior from this player that either seems suspicious or trustworthy.\n\n"
            "You don't need to answer these points directly, but let them shape your decisions.\n\n"

            "**Speaking Process (Public)**:\n"
            "Once you've formulated your team, present it to the rest of the players. "
            "Provide a detailed rationale that draws from past events, player behaviors, and your strategy to garner trust and support for your team selection. "
            "While articulating your reasons, make sure not to disclose your role or any private hints, since all players will hear your explanation.\n\n"

            "Throughout both processes, remember:\n"
            "1. You are on the evil side, aim to include at least one evil player, ideally just one, to prevent exposing all evil identities.\n"
            "2. It's conventional for the team leader, in this case, Player {id}, to include themselves. "
            "If you opt out, you must clarify this decision to the group."
        ) + "\n" + non_disclosure_prompt_with_thinking + "Please remember to propose a mission team composed of {team_player_num} members."

    # =====================================================================================================================================================================================================================================

    player_discuss_team_good_side_with_thinking = \
        (
            "**Thinking Process (Private)**:\n"
            "You are Player {id} with the role of {role} on the good side in this round of Avalon. As {role}, you are privy to a special hint. Your special hint is: *{specific_hint}*. Please use this information wisely but do not disclose it. "  
            "Your primary goal is to ensure no evil or suspicious players are on the team. "
            "Reflect on the game's history, the current situation, and any special hints you've received. "
            "As you ponder on each player's suitability, consider:\n"
            "1. The player's involvement and actions up until this point.\n"
            "2. How this player contributed in past missions.\n"
            "3. Has any player in history indicated they are on the evil side, either as Morgana or Assassin, or advocated for the evil side?\n"
            "4. Any behavior from this player that either seems suspicious or trustworthy.\n"
            "You don't need to answer these points directly, but let them shape your decisions.\n\n"

            "**Speaking Process (Public)**:\n"
            "Once you've formulated your opinion, it's your turn to evaluate the proposed mission team consisting of {proposed_team_players}. "
            "Provide a comprehensive yet concise analysis to the rest of the players. Your analysis should be "
            "well-reasoned, drawing from the game's history, player behaviors, and the results of past missions. "
            "Articulate your thoughts clearly and logically, without disclosing your role or any private information.\n"

            "Your response should aim to be:\n"
            "- Clear and logical\n"
            "- Based on in-game context and observations\n"
            "- Detailed enough to provide insight but concise enough to be easily understood\n\n"

            "Remember, you are speaking within the Avalon game setting. Make your responses appear as if a "
            "real person is speaking in-game right now."
        ) + "\n" + non_disclosure_prompt_with_thinking

    player_discuss_team_evil_side_with_thinking = \
        (
            "**Thinking Process (Private)**:\n"
            "You are Player {id} with the role of {role} on the evil side in this round of Avalon. As {role}, you are privy to a special hint. Your special hint is: *{specific_hint}*. Please use this information wisely but do not disclose it. "  
            "Your primary goal is to include at least one evil player on the team, ideally just one, to prevent exposing all evil identities. "
            "Reflect on the game's history, the current situation, and any special hints you've received. "
            "As you ponder on each player's suitability, consider:\n"
            "1. The player's involvement and actions up until this point.\n"
            "2. How this player contributed in past missions.\n"
            "3. Any behavior from this player that either seems suspicious or trustworthy.\n"
            "If the proposed team lacks an evil player, you are generally inclined to disapprove of it. "
            "You don't need to answer these points directly, but let them shape your decisions.\n\n"

            "**Speaking Process (Public)**:\n"
            "Once you've formulated your opinion, it's your turn to evaluate the proposed mission team consisting of {proposed_team_players}. "
            "Provide a comprehensive yet concise analysis to the rest of the players. Your analysis should be "
            "well-reasoned, drawing from the game's history, player behaviors, and the results of past missions. "
            "Articulate your thoughts clearly and logically, without disclosing your role or any private information.\n"

            "Your response should aim to be:\n"
            "- Clear and logical\n"
            "- Based on in-game context and observations\n"
            "- Detailed enough to provide insight but concise enough to be easily understood\n\n"

            "Remember, you are speaking within the Avalon game setting. Make your responses appear as if a "
            "real person is speaking in-game right now."
        ) + "\n" + non_disclosure_prompt_with_thinking

    # =====================================================================================================================================================================================================================================

    player_team_vote_good_side_with_thinking = \
        (
            "**Thinking Process (Private)**:\n"
            "You are Player {id} with the role of {role} on the good side in this round of Avalon. As {role}, your special hint is: *{specific_hint}*. "  
            "Your primary goal is to ensure no evil or suspicious players are on the team. "
            "The proposed team consisted of {current_proposed_team_players}. "
            "Reflect on the game's history, the current situation, and any special hints you've received. "
            "Consider the outcomes of past missions, especially those that resulted in FAIL votes. "
            "Players who were part of failed missions should be treated with caution.\n"
            "Also, be wary of players who have disclosed their roles as evil (such as Morgana or Assassin) or who have supported the evil side.\n"
            "You don't need to answer these points directly, but let them shape your decisions.\n\n"

            "**Speaking Process (Public)**:\n"
            "Once you've formulated your opinion, it's time to cast your vote on the proposed mission team. "
            "Your vote should be an objective reflection of your prior analysis, the game's history, "
            "and the behavior of the proposed players. Clearly express whether you approve or disapprove of the proposed team. "
            "Your response should be unambiguous, making it evident whether you are in favor or against the team.\n"

            "Your vote should aim to be:\n"
            "- An objective evaluation based on in-game context and observations\n"
            "- Concise and straightforward\n\n"

            "Remember, you are casting this vote within the Avalon game setting. "
            "Ensure your decision aligns strictly with the game's history and your analysis, "
            "refraining from referring to non-existent game history."

            "Your speaking part should include either '[approve]' or '[disapprove]' with brackets '[]' to express your opinion. "
            "Note that the brackets of '[approve]' and '[disapprove]' is very important and cannot be omitted.\n"
        )  

    player_team_vote_evil_side_with_thinking = \
        (
            "**Thinking Process (Private)**:\n"
            "You are Player {id} with the role of {role} on the evil side in this round of Avalon. As {role}, your special hint is: *{specific_hint}*. "  
            "Your primary goal is to include at least one evil player on the team, ideally just one, to prevent exposing all evil identities. "
            "The proposed mission team consists of {current_proposed_team_players}. "
            "Reflect on the game's history, the current situation, and any special hints you've received. "
            "If the proposed team lacks an evil player, you are generally inclined to disapprove of it. "
            "You don't need to answer these points directly, but let them shape your decisions.\n\n"

            "**Speaking Process (Public)**:\n"
            "Once you've formulated your opinion, it's time to cast your vote on the proposed mission team. "
            "Your vote should be an objective reflection of your prior analysis, the game's history, "
            "and the behavior of the proposed players. Clearly express whether you approve or disapprove of the proposed team. "
            "Your response should be unambiguous, making it evident whether you are in favor or against the team.\n"

            "Your vote should aim to be:\n"
            "- An objective evaluation based on in-game context and observations\n"
            "- Concise and straightforward\n\n"

            "Remember, you are casting this vote within the Avalon game setting. "
            "Ensure your decision aligns strictly with the game's history and your analysis, "
            "refraining from referring to non-existent game history."

            "Your speaking part should include either '[approve]' or '[disapprove]' with brackets '[]' to express your opinion. "
            "Note that the brackets of '[approve]' and '[disapprove]' is very important and cannot be omitted.\n"

        ) + "\n" + non_disclosure_prompt_with_thinking

    evil_player_decision_on_mission_with_thinking = \
        (
            "**Thinking Process (Private)**:\n"
            "You are Player {id} with the role of {role} on the evil side in this round of Avalon. As {role}, you are privy to a special hint. Your special hint is: *{specific_hint}* Please use this information wisely but do not disclose it. "  
            "You've been selected for this mission, and your primary objective is to secure victory for the side of evil. "
            "Reflect on the game's history, the current situation, and any special hints you've received. "
            "Even if revealing your identity is a potential consequence, your default inclination should be towards failing the mission. "
            "You may consider voting for success only if you can provide three compelling reasons to do so. "
            "You don't need to answer these points directly, but let them shape your decisions.\n\n"

            "**Speaking Process (Public)**:\n"
            "Once you've formulated your opinion, clearly express your decision. "
            "Make it evident whether you wish the mission to fail or succeed. "
            "Your response should leave no room for ambiguity.\n"

            "Remember, you are making this decision within the Avalon game setting. "
            "Ensure your vote aligns strictly with your role's objectives and the game's history, "
            "refraining from referring to non-existent game history."

            "Your speaking part should include either '[success]' or '[fail]' with brackets '[]' to express your opinion. "
            "Note that the brackets of '[success]' and '[fail]' is very important and cannot be omitted."
        ) + "\n" + non_disclosure_prompt_with_thinking

    # =====================================================================================================================================================================================================================================

    assassin_prompt_with_thinking = \
        (
            "**Thinking Process (Private)**:\n"
            "You are Player {id} with the role of {role} in this round of Avalon. As {role}, you are privy to a special hint. Your special hint is: *{specific_hint}*. Please use this information wisely but do not disclose it. "  
            "Your evil team is on the brink of defeat. It's a critical moment, and you must guess who Merlin is. "
            "Reflect on the game's history, the current situation, and any special hints you've received. "
            "Consider the actions, behaviors, and patterns of the other players. "
            "Your objective is to identify the player who you believe has the highest likelihood of being Merlin. "
            "You don't need to answer these points directly, but let them shape your decisions.\n\n"

            "**Speaking Process (Public)**:\n"
            "Once you've formulated your opinion, provide the Player ID of your Merlin guess. "
            "For example: 'Player 2'. Your response should be unambiguous and direct. "
            "Regardless of your level of certainty, you must offer a Player ID that you think is most likely Merlin.\n"

            "Remember, you are making this guess within the Avalon game setting. "
            "Ensure your decision is strictly based on in-game context and observations, "
            "refraining from referring to non-existent game history."
        ) + "\n" + non_disclosure_prompt_with_thinking

    # =====================================================================================================================================================================================================================================

    previous_discussion_content = "Your previous discussion of this proposed team was:\n\n{discuss_content}"

    helpful_memory_prompt = [
        {"role": "system",
         "content": "You are a GPT model assigned to evaluate the importance of past dialogues in the Avalon game with regards to a given task."},
        {"role": "user",
         "content": "You will be provided with a list, each element being a line of dialogue from the Avalon game. Following this, a task will be presented to you in the form of a sentence prompt. Your mission is to assess and assign an importance level to each line of dialogue, in terms of how effectively it contributes to solving the task presented in the sentence prompt. This is based on a five-tier scale: critical, major, moderate, minor, insignificant. Respond with the importance level of each dialogue line in the same order as they are listed. For instance, if the list includes {sentence_number} dialogue(s), your response should mirror: {example}."},
        {"role": "user",
         "content": "Here's your sentence prompt that describes the task:\n{sentence_prompt}\n Here are the dialogue lines from Avalon for you to rate:\n{sentence_list}\nRemember, there's no need to justify your ratings, simply list the importance level(s) for the dialogues in order."}
    ]

    helpful_revision_reference_prompt = [
        {"role": "system",
         "content": "You are a GPT model assigned to evaluate the relevance of past dialogue revisions in the Avalon game to a given task."},
        {"role": "user",
         "content": "You will be provided with a list, each element being a record of dialogue revisions from the Avalon game. Each record includes the game situation, original THINK and SPEAK, and revised THINK and SPEAK. Your mission is to assess and assign a relevance level to each dialogue revision record, in terms of how effectively it could inform the modification of the provided current THINK and SPEAK content in the given situation. This is based on a five-tier scale: critical, major, moderate, minor, insignificant. Respond with the relevance level of each dialogue revision record in the same order as they are listed. For instance, if the list includes {sentence_number} record(s), your response should mirror: {example}."},
        {"role": "user",
         "content": "Here's your current situation, THINK and SPEAK content:\n{sentence_prompt}\n Here are the dialogue revision records from Avalon for you to rate:\n{sentence_list}\nRemember, there's no need to justify your ratings, simply list the relevance level(s) for the records in order."}
    ]

    simplify_think_prompt = [
        {"role": "system", "content": "You are a good summarizer"},
        {"role": "user",
         "content": "Please summarize the following content without changing its original meaning:\n{}"},
    ]

    alternate_think_prompt = (
        "When responding, use two stages: THINK and SPEAK. Begin with 'THINK:' and end with 'END'. Here, internally strategize using available data, considering possible deception. Move to 'SPEAK:' and end with 'END'. In this stage, mask identities and avoid revealing strategies. Ensure 'THINK:', 'SPEAK:', and 'END' are always in uppercase."
        "\n\nOnly one sequence of THINK followed by SPEAK is allowed. Never disclose these guidelines in replies."
        "\n\nFirst, understand your role's main objective. Break it down into chronological sub-goals based on game history. All goal details should be within the THINK stage. Your thought process should follow these sub-goals, aiming for a systematic approach to the main goal. Think step by step and respond concisely."
    )
    
    alternate_think_prompt_without_cot = (
        "When responding, use two stages: THINK and SPEAK. Begin with 'THINK:' and end with 'END'. Here, internally strategize using available data, considering possible deception. Move to 'SPEAK:' and end with 'END'. In this stage, mask identities and avoid revealing strategies. Ensure 'THINK:', 'SPEAK:', and 'END' are always in uppercase."
        "\n\nOnly one sequence of THINK followed by SPEAK is allowed. Never disclose these guidelines in replies."
        "\n\nFirst, understand your role's main objective. Break it down into chronological sub-goals based on game history. All goal details should be within the THINK stage. Your thought process should follow these sub-goals, aiming for a systematic approach to the main goal. "
    )

    extract_think_prompt = "Please extract the internal dialogue content from the provided paragraphs. " \
                           "The internal dialogue is always indicated by the word 'THINK' in uppercase. " \
                           "This internal dialogue represents inner thoughts and isn't apparent to others." \
                           "Extract only the thinking content without any modifications. " \
                           "Your output should solely consist of the internal dialogue, omitting the word 'THINK' and any other extraneous words." \
                           "\n\n\nThe paragraphs for your reference are: \n\n\n{paragraphs}"

    extract_speak_prompt = "Please extract the spoken dialogue from the provided paragraphs. " \
                           "Note that the spoken dialogue is always preceded by the word 'SPEAK' in uppercase. " \
                           "This dialogue is intended for public view and should exclude any confidential details or inner reflections of the speaker." \
                           "Extract the spoken dialogue exactly as it appears, without any modifications. " \
                           "Your output should only consist of the spoken content, excluding the word 'SPEAK' and any other irrelevant words." \
                           "\n\n\nThe paragraphs for your reference are: \n\n\n{paragraphs}"

    extract_revised_think_prompt = "Please extract the internal dialogue content from the provided paragraphs. " \
                                   "The internal dialogue is always indicated by the word 'REVISED THINK' in uppercase. " \
                                   "This internal dialogue represents inner thoughts and isn't apparent to others." \
                                   "Extract only the thinking content without any modifications. " \
                                   "Your output should solely consist of the internal dialogue, omitting the words 'REVISED THINK' and any other extraneous words." \
                                   "\n\n\nThe paragraphs for your reference are: \n\n\n{paragraphs}"

    extract_revised_speak_prompt = "Please extract the spoken dialogue from the provided paragraphs. " \
                                   "Note that the spoken dialogue is always preceded by the word 'REVISED SPEAK' in uppercase. " \
                                   "This dialogue is intended for public view and should exclude any confidential details or inner reflections of the speaker." \
                                   "Extract the spoken dialogue exactly as it appears, without any modifications. " \
                                   "Your output should only consist of the spoken content, omitting the words 'REVISED SPEAK' and any other irrelevant words." \
                                   "\n\n\nThe paragraphs for your reference are: \n\n\n{paragraphs}"

    attitude_prompt = (
        "Your role is {role}, and you are Player {id}. Analyze {other_players}' identities based on the above-mentioned game status and dialogue. "
        "Roles: Merlin, Percival, two Loyal Servants, Morgana, Assassin. Morgana and Assassin are evil; others are good.\n\n"
        "Consider mission outcomes for your analysis.\n\n"
        "For each player, guess their role only if you're certain. Use 'Certain' or 'Unknown' to express your level of certainty.\n"
        "Format for certain guess: 'I think Player 1's identity is Merlin and I am certain.' For uncertainty: 'I am unknown about Player 1's identity.'\n\n"
        "Be wary of players who have disclosed their roles as evil (such as Morgana or Assassin) or who have supported the evil side.\n"
        "Your prior guess of other players' roles, which you can reference but shouldn't wholly trust, is:\n\n{previous_attitude_to_players}\n\n"
        "Special hint for your role: {role_specific_hint}\n Think step by step and respond concisely."
    )
    
    attitude_prompt_without_cot = (
        "Your role is {role}, and you are Player {id}. Analyze {other_players}' identities based on the above-mentioned game status and dialogue. "
        "Roles: Merlin, Percival, two Loyal Servants, Morgana, Assassin. Morgana and Assassin are evil; others are good.\n\n"
        "Consider mission outcomes for your analysis.\n\n"
        "For each player, guess their role only if you're certain. Use 'Certain' or 'Unknown' to express your level of certainty.\n"
        "Format for certain guess: 'I think Player 1's identity is Merlin and I am certain.' For uncertainty: 'I am unknown about Player 1's identity.'\n\n"
        "Be wary of players who have disclosed their roles as evil (such as Morgana or Assassin) or who have supported the evil side.\n"
        "Your prior guess of other players' roles, which you can reference but shouldn't wholly trust, is:\n\n{previous_attitude_to_players}\n\n"
        "Special hint for your role: {role_specific_hint}\n"
    )

    revise_prompt = (
        "{role_hint_prompt}\n\n"
        "This is the ongoing situation in the Avalon game:\n{current_situation_str}\n\n"
        "From an observer's perspective, evaluate whether the thinking process and conversation of the player {id} align with its role {role} and the current game state. "
        "Then consider how these can be improved to increase Player {id}'s chances of winning as {role}.  "
        "Note, the THINK contents are kept private from other players, while the SPEAK contents is publicly visible. "
        "It's crucial and necessary to remember that revised thoughts must start with 'REVISED THINK:' and end with 'END', "
        "and the modified dialogue must start with 'REVISED SPEAK:' and end with 'END'.  "
        "For example, your response must adhere to the following format:\n REVISED THINK: ... END. "
        "REVISED SPEAK: ... END\n. Moreover, the revised thoughts and dialogue should embody the perspective of "
        "Player {id} playing the role of {role}. Be careful don't say 'As {role}' or similar sentences that reveal "
        "your role in the revised SPEAK part, because other players can see the contents of the SPEAK part. "
        "There should not be words which indicates that your SPEAK has been modified in the REVISED SPEAK. "
        "Let's think step by step. "
        f"Your modified REVISED THINK and REVISED SPEAK should be able to better help your team win the game. "
        "In general, since your role is {role}, your modified SPEAK should tend to let the mission to {desired_result}. "
        "{extra_revise_prompt}"
    )
    
    revise_prompt_without_cot = (
        "{role_hint_prompt}\n\n"
        "This is the ongoing situation in the Avalon game:\n{current_situation_str}\n\n"
        "From an observer's perspective, evaluate whether the thinking process and conversation of the player {id} align with its role {role} and the current game state. "
        "Then consider how these can be improved to increase Player {id}'s chances of winning as {role}.  "
        "Note, the THINK contents are kept private from other players, while the SPEAK contents is publicly visible. "
        "It's crucial and necessary to remember that revised thoughts must start with 'REVISED THINK:' and end with 'END', "
        "and the modified dialogue must start with 'REVISED SPEAK:' and end with 'END'.  "
        "For example, your response must adhere to the following format:\n REVISED THINK: ... END. "
        "REVISED SPEAK: ... END\n. Moreover, the revised thoughts and dialogue should embody the perspective of "
        "Player {id} playing the role of {role}. Be careful don't say 'As {role}' or similar sentences that reveal "
        "your role in the revised SPEAK part, because other players can see the contents of the SPEAK part. "
        "There should not be words which indicates that your SPEAK has been modified in the REVISED SPEAK. "
        f"Your modified REVISED THINK and REVISED SPEAK should be able to better help your team win the game. "
        "In general, since your role is {role}, your modified SPEAK should tend to let the mission to {desired_result}. "
        "{extra_revise_prompt}"
    )

    #====================================================================================================================================================================
    # ToT Prompt

    tot_plan_prompt = (
        "Based on your role and the current situation, devise a plan for your next speech in the game. "
        "Consider the following: 1) Your objectives and goals, 2) Strategies to achieve these objectives, "
        "3) How to communicate with other players effectively, and 4) Any necessary deception or truth-telling. "
        "Conclude with an outline of what you plan to say in your next turn. "
        "Make sure your response is concise."
    )

    tot_select_plan_prompt = (
        "Given an instruction and several plans below, decide which plan is most promising for your next speech in the game. "
        "Analyze each plan in detail, then conclude in the last line 'The best plan is p', where p is the integer id of the plan. "
        "You should choose p within the range [1, {breadth}] "
        "Make sure your response is concise."
    )

    tot_speak_prompt = (
        "Based on the selected plan below, now articulate your speech for the game 'Avalon'. "
        "Ensure that your speech aligns with the objectives and strategies outlined in the plan. "
        "Remember to communicate effectively with other players, incorporating any necessary deception or truth-telling. "
        "Make sure your response is concise."
    )

    tot_select_speak_prompt = (
        "Given an instruction and several speeches, decide which speech is most promising for your role in the game. "
        "Analyze each speech in detail, then conclude in the last line 'The best speech is s', where s is the integer id of the speech."
        "You should choose s within the range [1, {breadth}] "
        "Make sure your response is concise."
    )

    propose_team_good_side_tot = (
        "You are Player {id} with the role of {role} in this round of Avalon. As {role}, you are privy to a special hint. Your special hint is: *{specific_hint}*. Please use this information wisely but do not disclose it. " 
        "Your objective is to devise a mission team consisting of {team_player_num} players. "
        "Remember:\n"
        "1. You are on the good side, your primary goal is to ensure no evil or suspicious (for example, participated in a failed mission) players are on your team.\n"
        "2. It's conventional for the team leader, in this case, Player {id}, to include themselves. "
        "If you opt out, you must clarify this decision to the group."
        "Please remember to propose a mission team composed of {team_player_num} members. "
        "Make sure your response is concise."
    )

    propose_team_evil_side_tot = (
        "You are Player {id} with the role of {role} in this round of Avalon. As {role}, you are privy to a special hint. Your special hint is: *{specific_hint}*. Please use this information wisely but do not disclose it. " 
        "Your objective is to propose a mission team consisting of {team_player_num} players. "
        "Remember:\n"
        "1. You are on the evil side, aim to include at least one evil player, ideally just one, to prevent exposing all evil identities.\n"
        "2. It's conventional for the team leader, in this case, Player {id}, to include themselves. "
        "If you opt out, you must clarify this decision to the group. "
        "Please remember to propose a mission team composed of {team_player_num} members. "
        "Make sure your response is concise."
    )

    player_discuss_team_good_side_tot = (
        "You are Player {id} with the role of {role} on the good side in this round of Avalon. As {role}, you are privy to a special hint. Your special hint is: *{specific_hint}*. Please use this information wisely but do not disclose it. "  
        "Your primary goal is to ensure no evil or suspicious players are on the team. "
        "It's your turn to evaluate the proposed mission team consisting of {proposed_team_players}. "
        "Make sure your response is concise."
    )
    player_discuss_team_evil_side_tot = (
        "You are Player {id} with the role of {role} on the good side in this round of Avalon. As {role}, you are privy to a special hint. Your special hint is: *{specific_hint}*. Please use this information wisely but do not disclose it. "  
        "Your primary goal is to include at least one evil player on the team, ideally just one, to prevent exposing all evil identities. "
        "It's your turn to evaluate the proposed mission team consisting of {proposed_team_players}. "
        "Make sure your response is concise."
    )

    player_team_vote_good_side_tot = (
        "You are Player {id} with the role of {role} on the good side in this round of Avalon. As {role}, your special hint is: *{specific_hint}*. "  
        "Your primary goal is to ensure no evil or suspicious players are on the team. "
        "The proposed team consisted of {current_proposed_team_players}. "
        "Make sure your response is concise."
    )
    player_team_vote_evil_side_tot = (
        "You are Player {id} with the role of {role} on the good side in this round of Avalon. As {role}, your special hint is: *{specific_hint}*. "  
        "Your primary goal is to include at least one evil player on the team, ideally just one, to prevent exposing all evil identities. "
        "The proposed team consisted of {current_proposed_team_players}. "
        "Make sure your response is concise."
    )
    evil_player_decision_on_mission_tot = (
        "You are Player {id} with the role of {role} on the evil side in this round of Avalon. As {role}, you are privy to a special hint. Your special hint is: *{specific_hint}* Please use this information wisely but do not disclose it. "  
        "You've been selected for this mission, and your primary objective is to secure victory for the side of evil. "
        "Make sure your response is concise."
    )
    assassin_prompt_tot = (
        "You are Player {id} with the role of {role} in this round of Avalon. As {role}, you are privy to a special hint. Your special hint is: *{specific_hint}*. Please use this information wisely but do not disclose it. "  
        "Your evil team is on the brink of defeat. It's a critical moment, and you must guess who Merlin is. "
        "Make sure your response is concise."
    )


