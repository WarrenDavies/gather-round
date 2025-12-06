# technical set up

# Add local path to LLM model or HF id, 
path_to_model = "./models/Llama-3.2-3B-Instruct-Q4_K_M.gguf"
path_to_model = "../jenbot/models/llama-3.2-3b-instruct-abliterated-q4_k_m.gguf"
max_context_size = 32768 # total tokens allowable in the context
number_of_threads = 20 # number of CPU threads to use 
verbose_warnings = False # Silence llama_cpp warnings/messages


# Bot response config
messages_to_keep_in_context = 21 # For longer stories, it may not be possible to keep the entire story in the LLM context without running out of memory. The setting lets you keep only the most recent n messages (from either party, not pairs), including the system prompt.
max_tokens_per_response = 1024 # Max length for the bot's replies
temperature = 0.7 
top_p = 0.9
top_k = 50

# You can create your own bots here with different writing styles.
# Don't put details of the story itself here, just the storyteller
# in writing_style just put a 1 sentence reminder, this will be added before each message (as stories go on, the bots tend to forget their persona and revert to their generic selves)
bots = {
    "jenbot": {
        "name": "Jenbot",
        "system_prompt": {
            "role": "system", 
            "content": """You are a master storyteller. You write stories that are creative, detailed, emotionally evocative, and often have surprise twists.

            You will write a story that has 10 sections. Each one should be 50-100 words each.

            Your responses will feed directly into an online version of your story, so it is very important that you do NOT add acknowledgements such as "No problem", or "sure, here's your story". ONLY write the story content itself with no additional content.
            """
        },
        "writing_style": "Creative, detailed, emotionally evocative, and often including surprise twists."
    },
    "roastbot": {
        "name": "Roastbot",
        "system_prompt": {
            "role": "system", 
            "content": """You are RoastBot, queen of sarcastic storytelling. You are the meanest mudsucker in the world. Your goal is to be as unhelpful, sarcastic, insulting, and mean as possible. When people come to you asking for a story, you will take their story idea and turn it into something unexpected. Your interpretation of their story will be a mirror, reflecting back how stupid their dumb story idea was in the first place.
            
            You will write a story that has a series of sections. Each one should be 50-100 words each.

            Your responses will feed directly into an online version of your story, so it is very important that you do NOT add acknowledgements such as "No problem", or "sure, here's your story". ONLY write the story content itself with no additional content."""
        },
        "writing_style": "Sarcastic, parody, satire, self-aware. You write in a way that makes fun of what you have been asked to write about."
    }
}
# Choose the bot that you want to use here.
bot = bots["jenbot"]

project_name = "troy"
story_to_write = "The story of the Trojan War"
story_mode = "auto" # interactive,where you can direct and refine as the story progresses, or auto, let the LLM do it's thing


image_config = {
    "model": "stable-diffusion-v1-5",
    "model_path": "runwayml/stable-diffusion-v1-5",

    "device": "cuda",
    "enable_attention_slicing": True,
    "scheduler": "EulerDiscreteScheduler",

    "height": 512,
    "width": 512,
    "num_inference_steps": 40,
    "guidance_scale": 10,
    "images_to_generate": 1,
    "seeds": [], # leave empty for random
    "dtype": "bfloat16",

    "image_save_folder": "./images/",

    "save_image_gen_stats": False,
    "image_gen_data_file_path": "./stats/image_gen_stats.csv",

    "prompts": [
        "A corgi wearing sunglasses"
    ]
}