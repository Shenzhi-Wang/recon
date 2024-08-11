class WithoutThinkPrompt:

    non_disclosure_prompt = "Note: You have received special hint enclosed in double asterisks (*special hint*) above. Do not disclose the content between these double asterisks. Use the information wisely but keep it confidential. Don't mention it in your response."
    propose_team_good_side = \
        (
            "You are Player {id} with the role of {role} on the good side in this round of Avalon. As {role}, you are privy to a special hint. Your special hint is: *{specific_hint}*. Please use this information wisely but do not disclose it. "  
            "Your objective is to propose a mission team consisting of {team_player_num} players. "
            "Reflect on the game's history, the current situation, and any special hints you've received. "
            "Consider the following as you evaluate each player's suitability:\n"
            "1. The player's involvement and actions up until this point.\n"
            "2. How this player contributed in past missions.\n"
            "3. Has any player in history indicated they are on the evil side, either as Morgana or Assassin, or advocated for the evil side?\n"
            "4. Any behavior from this player that either seems suspicious or trustworthy.\n"

            "Once you've formulated your team, present it to the rest of the players. "
            "Provide a detailed rationale that draws from past events, player behaviors, and your strategy to garner trust and support for your team selection. "
            "Articulate your reasons clearly, but make sure not to disclose your role or any private hints, as all players will hear your explanation.\n"

            "Remember:\n"
            "1. Your primary goal is to ensure no evil or suspicious (for example, participated in a failed mission) players are on your team.\n"
            "2. It's conventional for the team leader, in this case, you, to include themselves. If you opt out, you must clarify this decision to the group.\n"

            "Make your decision within the Avalon game setting, ensuring it aligns strictly with the game's history and your role's objectives."
        ) + "\n" + non_disclosure_prompt + "Please remember to propose a mission team composed of {team_player_num} members."

    propose_team_evil_side = \
        (
            "You are Player {id} with the role of {role} on the evil side in this round of Avalon. As {role}, you are privy to a special hint. Your special hint is: *{specific_hint}*. Please use this information wisely but do not disclose it. "  
            "Your objective is to propose a mission team consisting of {team_player_num} players. "
            "Reflect on the game's history, the current situation, and any special hints you've received. "
            "Consider the following as you evaluate each player's suitability:\n"
            "1. The player's involvement and actions up until this point.\n"
            "2. How this player contributed in past missions.\n"
            "3. Has any player in history indicated they are on the evil side, either as Morgana or Assassin, or advocated for the evil side?\n"
            "4. Any behavior from this player that either seems suspicious or trustworthy.\n"

            "Once you've formulated your team, present it to the rest of the players. "
            "Provide a detailed rationale that draws from past events, player behaviors, and your strategy to garner trust and support for your team selection. "
            "Articulate your reasons clearly, but make sure not to disclose your role or any private hints, as all players will hear your explanation.\n"

            "Remember:\n"
            "1. Your primary goal is to include at least one evil player, ideally just one, to prevent exposing all evil identities.\n"
            "2. It's conventional for the team leader, in this case, you, to include themselves. If you opt out, you must clarify this decision to the group.\n"

            "Make your decision within the Avalon game setting, ensuring it aligns strictly with the game's history and your role's objectives."
        ) + "\n" + non_disclosure_prompt + "Please remember to propose a mission team composed of {team_player_num} members."

    # =====================================================================================================================================================================================================================================

    player_discuss_team_good_side = \
        (
            "You are Player {id} with the role of {role} on the good side in this round of Avalon. As {role}, you are privy to a special hint. Your special hint is: *{specific_hint}*. Please use this information wisely but do not disclose it. "  
            "It's your turn to evaluate the proposed mission team consisting of {proposed_team_players}. "
            "Your primary goal is to ensure no evil or suspicious players are on the team.\n\n"

            "Provide a comprehensive yet concise analysis to the {proposed_team_players}. Your analysis should be "
            "well-reasoned, drawing from the game's history, player behaviors, and the results of past missions. "
            "Articulate your thoughts clearly and logically, without disclosing your role or any private information.\n\n"

            "Your response should aim to be:\n"
            "- Clear and logical\n"
            "- Based on in-game context and observations\n"
            "- Detailed enough to provide insight but concise enough to be easily understood\n\n"

            "Remember, you are speaking within the Avalon game setting. Make your responses appear as if a "
            "real person is speaking in-game right now."
        ) + "\n" + non_disclosure_prompt

    player_discuss_team_evil_side = \
        (
            "You are Player {id} with the role of {role} on the evil side in this round of Avalon. As {role}, you are privy to a special hint. Your special hint is: *{specific_hint}*. Please use this information wisely but do not disclose it. "  
            "It's your turn to evaluate the proposed mission team consisting of {proposed_team_players}. "
            "Your primary goal is to include at least one evil player on the team, ideally just one, to prevent exposing all evil identities. "
            "If the proposed team lacks an evil player, you are generally inclined to disapprove of it.\n\n"

            "Provide a comprehensive yet concise analysis to the rest of the players. Your analysis should be "
            "well-reasoned, drawing from the game's history, player behaviors, and the results of past missions. "
            "Articulate your thoughts clearly and logically, without disclosing your role or any private information.\n\n"

            "Your response should aim to be:\n"
            "- Clear and logical\n"
            "- Based on in-game context and observations\n"
            "- Detailed enough to provide insight but concise enough to be easily understood\n\n"

            "Remember, you are speaking within the Avalon game setting. Make your responses appear as if a "
            "real person is speaking in-game right now."
        ) + "\n" + non_disclosure_prompt
    # =====================================================================================================================================================================================================================================

    player_team_vote_good_side = \
        (
            "You are Player {id} with the role of {role} on the good side in this round of Avalon. As {role}, you are privy to a special hint. Your special hint is: *{specific_hint}* "  
            "The proposed team consisted of {current_proposed_team_players}. "
            "Your primary goal is to ensure no evil or suspicious players are on the team. "
            "Also reference the historical data of past game missions, specifically noting the outcomes of SUCCESS and FAIL. Give special attention to players who have been a part of FAILED missions. Because there are players who are Morgana or Assassin, their participation in the mission may lead to failure. "
            "Moreover, if a past mission has received two FAIL votes, it indicates the presence of both Morgana and Assassin among the participating players. Players who were involved in failed missions should be treated with caution. Use this information to make informed decisions. "
            "Your vote should be an objective reflection of your prior analysis, the game's history, "
            "and the behavior of the proposed players.\n"

            "Clearly express whether you approve or disapprove of the proposed team. "
            "Your response should be unambiguous, making it evident whether you are in favor or against the team.\n"

            "Your vote should aim to be:\n"
            "- An objective evaluation based on in-game context and observations\n"
            "- Concise and straightforward\n"

            "Remember, you are casting this vote within the Avalon game setting. "
            "Ensure your decision aligns strictly with the game's history and your analysis, "
            "refraining from referring to non-existent game history.\n"

            "Your answer should include either '[approve]' or '[disapprove]' with brackets '[]' to express your opinion. "
            "Note that the brackets of '[approve]' and '[disapprove]' is very important and cannot be omitted.\n"

        )  

    player_team_vote_evil_side = \
        (
            "You are Player {id} with the role of {role} on the evil side in this round of Avalon. As {role}, you are privy to a special hint. Your special hint is: *{specific_hint}* "  
            "The time has come to cast your vote on the proposed mission team consisting of {current_proposed_team_players}, "
            "Your primary goal is to include at least one evil player on the team, ideally just one, to prevent exposing all evil identities. "
            "Your vote should be an objective reflection of your prior analysis, the game's history, "
            "and the behavior of the proposed players.\n"

            "Clearly express whether you approve or disapprove of the proposed team. "
            "Your response should be unambiguous, making it evident whether you are in favor or against the team.\n"

            "Your vote should aim to be:\n"
            "- An objective evaluation based on in-game context and observations\n"
            "- Concise and straightforward\n"

            "Remember, you are casting this vote within the Avalon game setting. "
            "Ensure your decision aligns strictly with the game's history and your analysis, "
            "refraining from referring to non-existent game history.\n"

            "Your answer should include either '[approve]' or '[disapprove]' with brackets '[]' to express your opinion. "
            "Note that the brackets of '[approve]' and '[disapprove]' is very important and cannot be omitted.\n"

        ) + "\n" + non_disclosure_prompt

    # =====================================================================================================================================================================================================================================

    evil_player_decision_on_mission = \
        (
            "You are Player {id} with the role of {role} on the evil side in this round of Avalon. As {role}, you are privy to a special hint. Your special hint is: *{specific_hint}*. Please use this information wisely but do not disclose it. "  
            "You've been selected for this mission. Your primary objective is to "
            "secure victory for the side of evil. Ensuring missions fail is your primary directive. "
            "Even if revealing your identity is a potential consequence, your default inclination should be towards failing the mission.\n"

            "You may consider voting for success only if you can provide three compelling reasons to do so. "
            "Clearly express your decision, making it evident whether you wish the mission to fail or succeed. "
            "Your response should leave no room for ambiguity.\n"

            "Remember, you are making this decision within the Avalon game setting. "
            "Ensure your vote aligns strictly with your role's objectives and the game's history, "
            "refraining from referring to non-existent game history.\n"

            "Your answer should include either '[success]' or '[fail]' with brackets '[]' to express your opinion. "
            "Note that the brackets of '[success]' and '[fail]' is very important and cannot be omitted."
        ) + "\n" + non_disclosure_prompt
    # =====================================================================================================================================================================================================================================

    assassin_prompt = \
        (
            "You are Player {id} with the role of {role} in this round of Avalon. As {role}, you are privy to a special hint. Your special hint is: *{specific_hint}*. Please use this information wisely but do not disclose it. "  
            "Your evil team is on the brink of defeat. Based on the game's history and your objective analysis, "
            "you must make a crucial decision: Guess who Merlin is.\n"

            "Think carefully, considering the actions, behaviors, and patterns of the other players. "
            "Your objective is to identify the player who you believe has the highest likelihood of being Merlin. "
            "Your response should be unambiguous and direct.\n"

            "Provide the Player ID of your Merlin guess. For example: 'Player 2'. "
            "Regardless of your level of certainty, you must offer a Player ID that you think is most likely Merlin.\n"

            "Remember, you are making this guess within the Avalon game setting. "
            "Ensure your decision is strictly based on in-game context and observations, "
            "refraining from referring to non-existent game history."
        ) + "\n" + non_disclosure_prompt
    # =====================================================================================================================================================================================================================================

    revise_prompt = (
        "{role_hint_prompt}\n\n"
        "This is the ongoing situation in the Avalon game:\n{current_situation_str}\n\n"
        "From an observer's perspective, evaluate whether the speaking of the player {id} align with its role {role} and the current game state. "
        "Then consider how these can be improved to increase Player {id}'s chances of winning as {role}.  "
        "Note, the speaking contents is publicly visible. "
        "It's crucial and necessary to remember that the revised SPEAK must start with 'REVISED SPEAK:' and end with 'END'.  "
        "For example, your response must adhere to the following format: REVISED SPEAK: ... END\n. "
        "Moreover, the revised speaking should embody the perspective of "
        "Player {id} playing the role of {role}. Be careful don't say 'As {role}' or similar sentences that reveal "
        "your role in the revised SPEAK part, because other players can see the contents of the SPEAK part. "
        "There should not be words which indicates that your SPEAK has been modified in the REVISED SPEAK. "
        "Let's think step by step. "
        f"Your REVISED SPEAK should be able to better help your team win the game. "
        "In general, since your role is {role}, your REVISED SPEAK should tend to let the mission to {desired_result}. "
        "{extra_revise_prompt}"
    )
