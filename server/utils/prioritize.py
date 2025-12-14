import replicate
import json
import os

client = replicate.Client(api_token=os.environ["REPLICATE_API_TOKEN"])

def prioritize_tasks(tasks):
    prompt = f"""
You are an AI that assigns priorities to tasks.

Rules:
- HIGH = important + urgent
- MEDIUM = important but not urgent
- LOW = optional or trivial

⚠️ IMPORTANT:
Respond with JSON ONLY.
No explanations.
Output must be a single JSON array like:

[
  {{ "id": "1", "priority": "HIGH" }},
  {{ "id": "2", "priority": "MEDIUM" }},
  {{ "id": "3", "priority": "LOW" }}
]

Tasks:
{json.dumps(tasks, indent=2)}
"""

    output = client.run(
        "meta/llama-3-8b-instruct:latest",
        input={
            "prompt": prompt,
            "temperature": 0.3,
            "max_new_tokens": 512,
            "top_p": 0.9,
        }
    )

    # Replicate returns a list of strings
    text = "".join(output).strip()

    try:
        start = text.index("[")
        end = text.rindex("]") + 1
        priorities = json.loads(text[start:end])
        return priorities
    except Exception as e:
        raise ValueError(
            f"Failed to parse JSON from AI output:\n{text}\nError: {e}"
        )
