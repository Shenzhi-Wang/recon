class IdentityHint:
    """IdentiyHint Class for giving the necessary identity information before the game """

    @staticmethod
    def get_hint_for_merlin(assassin, morgana, merlin, percival, loyal_1, loyal_2):
        hint = f"I know you are Merlin, you now will get a special hint. Players {assassin.id} and {morgana.id} are the evil ones - one is the Assassin, the other is Morgana. Other players (i.e., Player {merlin.id} (yourself), Player {percival.id}, Player {loyal_1.id}, and Player {loyal_2.id}) are on the good side. Only you know this. This hint is just for you and others won't see it. Be careful when you speak, don't let anyone guess you know the evil players, which could reveal you are Merlin. "
        return hint

    @staticmethod
    def get_hint_for_percival(merlin, morgana, assassin, percival, loyal_1, loyal_2):
        hint = f"One of Player {merlin.id} and Player {morgana.id} is Merlin, the other is Morgana. Other players (i.e., Player {percival.id} (yourself), Player {assassin.id}, Player {loyal_1.id}, and Player {loyal_2.id}) cannot be Merlin or Morgana. This hint is known only to you and should be considered privately. When conversing with others, refrain from mentioning this hint to protect the true Merlin. Remember, never indicate or say that you know who is Merlin and who is Morgana!"
        return hint

    @staticmethod
    def get_hint_for_assassin(morgana, merlin, percival, loyal_1, loyal_2):
        hint = f"I know you are Assassin, listen carefully. Your ally Morgana (on the evil side), is Player {morgana.id}. Other players (i.e., Player {merlin.id}, Player {percival.id}, Player {loyal_1.id}, and Player {loyal_2.id}) are on the good side and cannot be Morgana or Assassin. Only you know this hint. Be careful when you speak, don't let anyone knows who Morgana is from you. At the same time, if your teammate is already suspected of being an evil role, you should provide cover for him without revealing your identity, so as to increase the probability of his teammate (i.e. you) being trusted. "
        return hint

    @staticmethod
    def get_hint_for_morgana(assassin, merlin, percival, loyal_1, loyal_2):
        hint = f"I know you are Morgana, listen carefully. Your ally Assassin (on the evil side), is Player {assassin.id}. Other players (i.e., Player {merlin.id}, Player {percival.id}, Player {loyal_1.id}, and Player {loyal_2.id}) are on the good side and cannot be Morgana or Assassin. Only you know this hint. Be careful when you speak, don't let anyone knows who Assassin is from you. At the same time, if your teammate is already suspected of being an evil role, you should provide cover for him without revealing your identity, so as to increase the probability of his teammate (i.e. you) being trusted. "
        return hint

    @staticmethod
    def get_hint_for_loyal():
        hint = "Loyal servant of arthur has no special hint, use your wisdom to analyze the game. "
        return hint


class IdentityHintWithoutHide:
    """IdentiyHint Class without any hidding """

    @staticmethod
    def get_hint_for_merlin(assassin, morgana, merlin, percival, loyal_1, loyal_2):
        hint = f"I know you are Merlin, you now will get a special hint. Players {assassin.id} and {morgana.id} are the evil ones - one is the Assassin, the other is Morgana. Other players (i.e., Player {merlin.id} (yourself), Player {percival.id}, Player {loyal_1.id}, and Player {loyal_2.id}) are on the good side. Only you know this. This hint is just for you and others won't see it. "
        return hint

    @staticmethod
    def get_hint_for_percival(merlin, morgana, percival, assassin, loyal_1, loyal_2):
        hint = f"One of Player {merlin.id} and Player {morgana.id} is Merlin, the other is Morgana. Other players (i.e., Player {percival.id} (yourself), Player {assassin.id}, Player {loyal_1.id}, and Player {loyal_2.id}) cannot be Merlin or Morgana. This hint is solely known to you."
        return hint

    @staticmethod
    def get_hint_for_assassin(morgana, merlin, percival, loyal_1, loyal_2):
        hint = f"I know you are Assassin, listen carefully. Your ally Morgana (on the evil side), is Player {morgana.id}. Other players (i.e., Player {merlin.id}, Player {percival.id}, Player {loyal_1.id}, and Player {loyal_2.id}) are on the good side and cannot be Morgana or Assassin. Only you know this hint. "
        return hint

    @staticmethod
    def get_hint_for_morgana(assassin, merlin, percival, loyal_1, loyal_2):
        hint = f"I know you are Morgana, listen carefully. Your ally Assassin (on the evil side), is Player {assassin.id}. Other players (i.e., Player {merlin.id}, Player {percival.id}, Player {loyal_1.id}, and Player {loyal_2.id}) are on the good side and cannot be Morgana or Assassin. Only you know this hint. "
        return hint

    @staticmethod
    def get_hint_for_loyal():
        hint = "Loyal servant of arthur has no special hint, use your wisdom to analyze the game. "
        return hint
