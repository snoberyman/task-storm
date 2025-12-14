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

    output = replicate.run(
        "meta/meta-llama-3-8b-instruct",
        input={
            "prompt": prompt,
            "temperature": 0.3,
            "top_p": 0.9,
            "prompt_template": (
                "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
                "You are a helpful assistant\n"
                "<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n"
                "{prompt}"
                "<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
            ),
        }
    )

    # Replicate may return list or string
    if isinstance(output, list):
        output_text = "".join(output)
    else:
        output_text = str(output)

    try:
        start = output_text.index("[")
        end = output_text.rindex("]") + 1
        return json.loads(output_text[start:end])
    except Exception as e:
        raise ValueError(
            f"Failed to parse JSON.\nOutput was:\n{output_text}"
        ) from e
