import replicate
import json
import os

def prioritize_tasks(tasks):
    # The dedicated system prompt contains the instructions for the model
    system_prompt = (
        "You are an AI that assigns priorities to tasks. "
        "Rules: HIGH = important + urgent, MEDIUM = important but not urgent, "
        "LOW = optional or trivial. "
        "Respond with JSON ONLY. "
        "The output MUST be a JSON array, for example: "
        "[ { \"id\": \"1\", \"priority\": \"HIGH\" }, { \"id\": \"2\", \"priority\": \"MEDIUM\" } ]"
    )

    # The user prompt contains the data to be processed
    user_prompt = f"Tasks to prioritize:\n{json.dumps(tasks, indent=2)}"

    # --- Use the synchronous replicate.run() method ---
    # This is the correct method for Replicate Python Client v0.20.0
    output = replicate.run(
        "meta/meta-llama-3-8b-instruct",
        input={
            "prompt": user_prompt,
            "system_prompt": system_prompt, # Cleanly passes the instructions
            "temperature": 0.3,
            "top_p": 0.9,
            "json": True, # Recommended for JSON output
            # No need for the problematic replicate.stream() or complex prompt_template
        }
    )

    # Replicate.run() returns a list of strings when used with Llama-3-instruct models, 
    # which must be joined to reconstruct the JSON string.
    if isinstance(output, list):
        output_text = "".join(output)
    else:
        output_text = str(output)

    # --- JSON Post-Processing ---
    try:
        # Tries to find and extract the JSON array using index/rindex
        start = output_text.index("[")
        end = output_text.rindex("]") + 1
        return json.loads(output_text[start:end])
    except Exception as e:
        # Provides debugging output if the JSON fails to parse
        raise ValueError(
            f"Failed to parse JSON.\nOutput was:\n{output_text}"
        ) from e

# NOTE: Ensure the function you are importing in tasks_graphql.py 
# is named 'prioritize_tasks' to match this definition.