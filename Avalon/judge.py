class Judge:
    """
    This Class is to obtain the identity of each key role
    """

    @staticmethod
    def get_assassin(players):
        """Get the player with the 'Assassin' role."""
        for player in players:
            if player.role == "Assassin":
                return player  # This is a GPTPlayer instance
        return None  # If no player is the assassin

    @staticmethod
    def get_merlin(players):
        """Get the player with the 'Merlin' role."""
        for player in players:
            if player.role == "Merlin":
                return player
        return None

    @staticmethod
    def get_percival(players):
        """Get the player with the 'Merlin' role."""
        for player in players:
            if player.role == "Percival":
                return player
        return None

    @staticmethod
    def get_morgana(players):
        """Get the player with the 'Morgana' role."""
        for player in players:
            if player.role == "Morgana":
                return player
        return None

    @staticmethod
    def get_loyals(players):
        loyals = []
        for player in players:
            if player.role == 'Loyal servant of arthur':
                loyals.append(player)
        return loyals
