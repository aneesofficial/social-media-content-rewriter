import os

def load_prompt(prompt_name: str) -> str:
    """
    Loads a prompt template from the prompts directory.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompt_path = os.path.join(base_dir, 'prompts', f'{prompt_name}_prompt.txt')
    
    try:
        with open(prompt_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Prompt template '{prompt_name}_prompt.txt' not found.")
