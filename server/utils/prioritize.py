import requests
import json

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
  {{ "id": "2", "priority": "MEDIUM" }}
  {{ "id": "3", "priority": "LOW" }}
]

Tasks:
{json.dumps(tasks, indent=2)}
"""

    response = requests.post(
        "http://127.0.0.1:5000/v1/chat/completions",  # <- chat endpoint
        json={
            "model": "mistral-7b-instruct-v0.2.Q4_K_M.gguf",
            "messages": [{"role": "user", "content": prompt}],
            
            "temperature": 0,
            "do_sample": False
        }
    )

    res_json = response.json()
    print("Model response:", res_json)
    try:
        text = res_json["choices"][0]["message"]["content"]
        
    except (KeyError, IndexError):
        raise ValueError(f"No content returned from model: {res_json}")

    text = text.strip()

    # Find JSON array start
    try:
        start_index = text.index('[')
        json_string = text[start_index:]
    except ValueError:
        raise ValueError(f"Could not find start of JSON array in model output:\n{text}")

    try:
        priorities = json.loads(json_string)
    except json.JSONDecodeError:
        raise ValueError(f"Failed to parse JSON from model output:\n{json_string}")

    return priorities
