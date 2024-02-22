# %%
import pandas as pd
import keys
from api_call import make_api_call
from datetime import datetime

df = pd.read_excel('task_submit_deidentified.xlsx')

# Slice the dataframe while testing to keep costs low
df = df.iloc[:3]


# %%
# Set up the results dataframe
results_df = pd.DataFrame(
    columns=[
        "instance_id",
        "prompt",
        "response_full",
        "response_message",
        "response_id",
        "response_created",
        "response_model",
        "response_usage_completion_tokens",
        "response_usage_prompt_tokens",
        "response_usage_total_tokens",
    ]
)

for i, row in df.iterrows():
    print(f"{i+1}/{len(df)}")

    # Make the API call
    response, prompt = make_api_call(
        row,
        model = "gpt-3.5-turbo-0125",
        key = keys.api_key,
        api_seed = 42,
        language = "English",
        codeLanguage = "C#",
    )

    # Extract the data
    data = []
    data.append(
        {
            "instance_id": row.name,
            "prompt": prompt,
            "response_full": str(dict(response)),
            "response_message": response.choices[0].message.content.strip(),
            "response_id": response.id,
            "response_created": datetime.utcfromtimestamp(response.created).strftime("%Y-%m-%d_%H-%M-%S"),
            "response_model": response.model,
            "response_usage_completion_tokens": response.usage.completion_tokens,
            "response_usage_prompt_tokens": response.usage.prompt_tokens,
            "response_usage_total_tokens": response.usage.total_tokens,
        }
    )

    # Append the data to the results dataframe
    results_df = pd.concat([results_df, pd.DataFrame(data)])


# Convert columns to correct data types
    results_df = results_df.astype(
        {
            "response_usage_completion_tokens": "int",
            "response_usage_prompt_tokens": "int",
            "response_usage_total_tokens": "int",
        }
    )

# %%
