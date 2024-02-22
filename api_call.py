import pandas as pd
import json
from openai import OpenAI
from prompt_templates import prompt_templates


# Extract and format student code
def get_code(instance, codeLanguage="C#"):
    studentCode = f"\n## Student code\n\n```{codeLanguage}\n"
    studentCode += instance['file_content']
    studentCode += "\n```\n\n"

    return studentCode


# Extract and format the error list
def get_errors(instance):
    errorList = json.loads(instance['error_list'])

    errors = "## Errors\n"
    for index, item in enumerate(errorList):
        errors += f"\n- {item['type']} `{item['id']}` on line `{item['line']}` with the following message: `{item['message']}`"

        # Break after processing 3 items
        if index >= 2:
            break

    return errors


def get_history(history, codeLanguage="C#"):
    prompt_history = prompt_templates['history']

    history = history.sort_values(by="upload_date")
    for i, row in history.iterrows():
        prompt_history += f"\n## Submission on {row['upload_date']}"
        prompt_history += get_code(row, codeLanguage=codeLanguage)
        prompt_history += get_errors(row)

    return prompt_history


# Create the full prompt for a single instance
def create_prompt(instance, history=None, language="English", codeLanguage="C#"):
    prompt = prompt_templates['header'].format(language=language)

    if history is not None:
        prompt += "\n\n"
        prompt += get_history(history, codeLanguage=codeLanguage)

    prompt += "\n\n# Latest submission for feedback\n"
    prompt += get_code(instance, codeLanguage=codeLanguage)
    prompt += get_errors(instance)

    return prompt


def query_openai(model, prompt, client, language="English", codeLanguage="C#", **kwargs):
    messages = [
            {
                "role": "system",
                "content": f"You are a well-trained Computer Science Education expert who is knowledgeable about best tutoring practices. Please respond in a similar way to a StackOverflow reply to help with a {codeLanguage} programming assignment. Communicate only in {language}. Your responses should always be properly formatted in markdown.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ]

    response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,
            # max_tokens=4096,
            top_p=0.1,
            # frequency_penalty=0,
            # presence_penalty=0,
            **kwargs,
        )

    return response


def make_api_call(
    instance,
    history=None,
    model = "gpt-4-0125-preview",
    key:str = "",
    api_seed: int = 42,
    language = "English",
    codeLanguage = "C#",
):
    """
    Some `model` options:
    - gpt-3.5-turbo-0125
    - gpt-4-0125-preview
    """
    client = OpenAI(
        api_key=key,
        )

    prompt = create_prompt(instance, history, language=language, codeLanguage=codeLanguage)

    response = query_openai(
                model,
                prompt,
                client,
                seed=api_seed,
            )

    return response, prompt
