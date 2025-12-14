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
    input = {
        "top_p": 0.9,
        "prompt": prompt,
        "temperature": 0.6,
    }

    for event in replicate.stream(
        "meta/meta-llama-3-70b-instruct",
        input=input
    ):

        # Replicate often returns a string or list
        print(event, end="")
        event = event if isinstance(event, str) else event[0]
        event = event.strip()

    # Extract JSON array from model output
    try:
        start_idx = event.index("[")
        json_string = event[start_idx:]
        priorities = json.loads(json_string)
    except Exception as e:
        raise ValueError(f"Failed to parse JSON from model output: {e}\nOutput was:\n{event}")
    return priorities
