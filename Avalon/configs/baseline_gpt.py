import api_config

config = dict(
    model_name='gpt3.5',
    short_model_context=api_config.gpt_3_5_short_model_context,
    temperature=1,
    short_memory=True,
    only_attitude_without_public_history=False,
    short_context_model=api_config.gpt_3_5_model,
    long_context_model=api_config.gpt_3_5_long_context_model,

    # for baseline
    is_revision_think_speak=False,
    is_first_think_then_speak=False,
    other_player_analysis=False,
    add_player_attitude=False,
    revision_add_history=False,
    
    # for tot
    breadth = None,
    seed = None, 
    tot=False,
    
    # for without cot
    without_cot = False,
)