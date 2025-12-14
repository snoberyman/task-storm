import replicate
import json
import os

# Create client using environment variable
client = replicate.Client(api_token=os.environ["REPLICATE_API_TOKEN"])

def prioritize_tasks(tasks):
    prompt = f"""
You are an AI that assigns priorities to tasks.
Rules:
- HIGH = important + urgent
- MEDIUM = important but not urgent
- LOW = optional or trivial

⚠️ IMPORTANT: Respond with JSON only, no explanations.
Output must be a single JSON array like this one:
[
  {{ "id": "1", "priority": "HIGH" }},
  {{ "id": "2", "priority": "MEDIUM" }},
  {{ "id": "3", "priority": "LOW" }}
]

Tasks:
{json.dumps(tasks, indent=2)}
"""

    # Call Replicate model
    output = client.run(
        "mistralai/mistral-7b-instruct:latest",  # Replace with your chosen model
        input={
            "input": prompt,
            "temperature": 0,
            "max_output_tokens": 300
        }
    )

    # Replicate often returns a string or list
    text = output if isinstance(output, str) else output[0]
    text = text.strip()

    # Extract JSON array from model output
    try:
        start_idx = text.index("[")
        json_string = text[start_idx:]
        priorities = json.loads(json_string)
    except Exception as e:
        raise ValueError(f"Failed to parse JSON from model output: {e}\nOutput was:\n{text}")

    return priorities
