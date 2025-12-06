from llama_cpp import Llama
import os
import shutil

from imagejenerator.models import registry
import config

project_name = "christmas"
template_name = "default"
project_path = f"public/{project_name}/"
section_path = f'src/templates/{template_name}/section.html'
footer_path = f'src/templates/{template_name}/footer.html'
story_path = project_path + "index.html"
number_of_sections = 8
sections = []
project_images_path = project_path + "images/"
config.image_config["image_save_folder"] = project_images_path
messages_system = [config.bot["system_prompt"]]
messages = [config.bot["system_prompt"]]
messages_all = [config.bot["system_prompt"]]

max_threads = os.cpu_count()
if config.number_of_threads > max_threads:
    config.number_of_threads = max_threads

def create_pipeline():
    llm = Llama(
        model_path=config.path_to_model,
        n_ctx=config.max_context_size,
        n_threads=config.number_of_threads,
        verbose=config.verbose_warnings,
    )
    return llm
llm = create_pipeline()


def generate_image(prompt):
    image_config = config.image_config
    image_config["prompts"][0] = prompt
    image_generator = registry.get_model_class(image_config)
    image_generator.generate_image()


def make_project_folders():
    os.makedirs(f"{project_path}/images/", exist_ok=True)
    shutil.copy(f'src/templates/{template_name}/header.html', project_path + "index.html")
make_project_folders()


def apply_replacements(content, replacement_text, image_path):
    content = content.replace("STORYTEXT", replacement_text)
    content = content.replace("IMAGE_PATH", image_path)
    
    return content


def add_section(replacement_text, image_path):
    with open(section_path, "r") as section_file, open(story_path, "a") as story_file:
        content = section_file.read()
        
        content = apply_replacements(content, replacement_text, image_path)

        story_file.write(content)
        story_file.write("\n")


def add_footer():
    with open(footer_path, "r") as footer_file, open(story_path, "a") as story_file:
        content = footer_file.read()
        story_file.write(content)


print("*** Starting story generation. ***")
for i in range(number_of_sections + 1):

    if i == 0:
        print(f"*** Generating plan for {number_of_sections} sections ***")
        user_input = f"Your story will have {number_of_sections} sections. The story you will write is: {config.story_to_write}. Take a moment to think about how you want to approach this story. And then write out a plan for what you will cover in each of the {number_of_sections} sections. Remember: your writing style is: {config.bot["writing_style"]}"
    else:
        print(f"*** Generating section {i}***")
        user_input = f"Now write up section {i} of your story, using 50-100 words. Remember, your writing style is: {config.bot["writing_style"]}. Do not include a title. And remember, respond ONLY with your story and no additional acknowledgement or confirmation. "

    # keep track of user input
    messages.append({"role": "user", "content": user_input})

    # call the LLM and generate response
    output = llm.create_chat_completion(
        messages=messages,
        max_tokens=config.max_tokens_per_response,
        temperature=config.temperature,
        top_p=config.top_p,
        top_k=config.top_k,
    )
    choice = output["choices"][0]["message"]
    output_text = (choice.get("content") or "").strip()
    if not output_text:
        output_text = "[No response generated.]"

    # keep track of bot responses
    messages.append({"role": "assistant", "content": output_text})

    # to keep responses faster, limit the number of messages we put in the context
    if len(messages) > config.messages_to_keep_in_context:
        if config.messages_to_keep_in_context == 0:
            messages = [config.bot["system_prompt"]]
        else:
            messages = [config.bot["system_prompt"]] + messages[-config.messages_to_keep_in_context:]
    
    if i == 0:
        continue

    #Image generation
    image_gen_prompt = f"You are an expert at turning creative writing into prompts that can be sent to AI image generators. You will be given a piece of writing. You must convert this into a prompt of comma-separated keywords. Focus on visual aspects only - appearance (if known), environment, and actions. Keep the prompt short - maximum 10 keywords. Your responses will feed directly into the image generator so it is very important that you do NOT add acknowledgements such as 'No problem', or 'sure, here's the prompt'. ONLY write the prompt, with no additional content. And remember, max 10 keywords. The writing that you must turn into a prompt is: {output_text}"
    image_prompt_output = llm.create_chat_completion(
        messages=[{"role": "system", "content": image_gen_prompt}],
        max_tokens=config.max_tokens_per_response,
        temperature=config.temperature,
        top_p=config.top_p,
        top_k=config.top_k,
    )
    image_prompt_choice = image_prompt_output["choices"][0]["message"]
    image_prompt_output_text = (image_prompt_choice.get("content") or "").strip()
    generate_image(image_prompt_output_text)
    images_generated = os.listdir(project_images_path)
    images_generated = sorted_files = sorted(images_generated)
    most_recent_image = images_generated[-1]
    image_path = "images/" + most_recent_image

    add_section(output_text, image_path)

add_footer()