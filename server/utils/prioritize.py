import replicate
import json
import os

def prioritize_tasks(tasks):
    prompt = f"""
You are an AI that assigns priorities to tasks.

Rules:
- HIGH = important + urgent
- MEDIUM = important but not urgent
- LOW = optional or trivial

Respond with JSON ONLY.
Format:
[
  {{ "id": "1", "priority": "HIGH" }},
  {{ "id": "2", "priority": "MEDIUM" }}
]

Tasks:
{json.dumps(tasks, indent=2)}
"""

    input = {
        "top_p": 0.9,
        "temperature": 0.3,
        "prompt": prompt,
        "prompt_template": (
            "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
            "You are a helpful assistant\n"
            "<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n"
            "{prompt}"
            "<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
        ),
    }

    output_text = ""

    for event in replicate.stream(
        "meta/meta-llama-3-8b-instruct",  # ✅ correct model
        input=input
    ):
        if isinstance(event, str):
            output_text += event
        elif isinstance(event, list):
            output_text += event[0]

    # Extract JSON safely
    try:
        start = output_text.index("[")
        end = output_text.rindex("]") + 1
        json_string = output_text[start:end]
        return json.loads(json_string)
    except Exception as e:
        raise ValueError(
            f"Failed to parse JSON.\nOutput:\n{output_text}"
        ) from e
