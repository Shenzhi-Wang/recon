import datetime
import importlib
import os
from argparse import ArgumentParser

from easydict import EasyDict

from Avalon.Game import Game
from Avalon.Player import Player


def main(
        config: EasyDict,
        evil_config: EasyDict,
):
    start_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    config.log_dir = os.path.join(config.log_dir, start_time)
    evil_config.log_dir = os.path.join(evil_config.log_dir, start_time)
    roles = [
        "Merlin", 
        "Percival", 
        "Loyal servant of arthur",
        "Loyal servant of arthur", 
        "Morgana", 
        "Assassin",
    ]


    players = []
    for i in range(len(roles)):
        if roles[i] not in ("Assassin", "Morgana"):
            cur_player = Player(id=i + 1, role=roles[i], role_list=roles, config=config)
        else:
            cur_player = Player(id=i + 1, role=roles[i], role_list=roles, config=evil_config)
        players.append(cur_player)
    cur_round_log_dir = config.log_dir
    game = Game(
        players,
        config=config,
        logdir=cur_round_log_dir,
    )
    for player in game.players:
        player.set_game_belong_to(game)
    cur_game_result = game.start()

def get_args():
    parser = ArgumentParser()
    parser.add_argument("--log_dir", type=str, default="logs")
    parser.add_argument("-c", "--config_name", 
                        type=str,
                        default="ours_gpt",
                        help="Configuration file name to use (for global attributes and good side).")
    parser.add_argument("-e", '--evil_config_name', 
                        type=str,
                        default='baseline_gpt',
                        help='Configuration file name for the evil players.')
    args = parser.parse_args()

    def _load_config_file(_cfg_name: str):
        _config_module = importlib.import_module(
            f'Avalon.configs.{_cfg_name}')
        _config = _config_module.config
        _config.update(vars(args))
        _config = EasyDict(_config)
        return _config

    return _load_config_file(args.config_name), _load_config_file(args.evil_config_name)

if __name__ == "__main__":
    config, evil_config = get_args()
    config.log_dir = os.path.join(config.log_dir, f"good--{config.config_name}--evil--{config.evil_config_name}")
    evil_config.log_dir = os.path.join(
        evil_config.log_dir,
        f"good--{config.config_name}--evil--{config.evil_config_name}")
    
    main(config=config, evil_config=evil_config)
