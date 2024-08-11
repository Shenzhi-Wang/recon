import api_config

config = dict(
    model_name='gpt3.5',
    temperature=1,
    short_memory=True,
    only_attitude_without_public_history=False,
    short_context_model=api_config.gpt_3_5_model,
    long_context_model=api_config.gpt_3_5_long_context_model,
    short_model_context=api_config.gpt_3_5_short_model_context,
    
    temp_model_name='gpt4',
    temp_long_context_model=api_config.gpt_4_long_context_model,
    temp_short_context_model=api_config.gpt_4_model,
    temp_short_model_context=api_config.gpt_4_short_model_context,

    # for baseline
    is_revision_think_speak=True,
    is_first_think_then_speak=True,
    other_player_analysis=True,
    add_player_attitude=True,
    revision_add_history=False,
    
    # for tot
    breadth = None,
    seed = None, 
    tot=False,
    
    # for without cot
    without_cot = False,
)
