"""
NOTE: You need to use your own api keys.
"""
gpt_api_key = "Your OpenAI API key"
claude_api_key = "Your Anthropic API key"

"""
NOTE: 
    The following models are used by ourselves in our paper. 
    You can change these models to meet your requirements.
"""

tokens_left_for_answer = 1500

gpt_3_5_model = "gpt-3.5-turbo-0613"
gpt_3_5_long_context_model = "gpt-3.5-turbo-16k-0613"
gpt_3_5_short_model_context = 4000 - tokens_left_for_answer

gpt_4_model = "gpt-4-0613"
gpt_4_long_context_model = "gpt-4-32k-0613"
gpt_4_short_model_context = 8000 - tokens_left_for_answer

claude_model = "claude-2.0"
claude_short_model_context = 128000 - tokens_left_for_answer

"""
NOTE: If you have your own api_base_url, you can change the following urls to yours.
"""
gpt_api_base_url = "https://api.openai.com/v1/chat/completions"
claude_api_base_url = "https://api.anthropic.com/v1/messages"
