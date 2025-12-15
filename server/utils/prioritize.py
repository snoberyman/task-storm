import replicate
import json
import os

def prioritize_tasks_stream(tasks):
    # --- 1. Define Prompts (Optimized for Llama 3 Instruct) ---
    # Moved the role instructions to the dedicated system_prompt
    system_prompt = (
        "You are an AI that assigns priorities to tasks. "
        "Rules: HIGH = important + urgent, MEDIUM = important but not urgent, "
        "LOW = optional or trivial. "
        "Respond with JSON ONLY. "
        "The output MUST be a JSON array, for example: "
        "[ { \"id\": \"1\", \"priority\": \"HIGH\" }, { \"id\": \"2\", \"priority\": \"MEDIUM\" } ]"
    )

    # The user prompt is just the data to process
    user_prompt = f"Tasks to prioritize:\n{json.dumps(tasks, indent=2)}"

    full_output = [] # Initialize a list to collect the streamed tokens

    # --- 2. Use replicate.stream() ---
    print("Streaming response from Replicate...")
    
    # We use a standard system_prompt and prompt input structure,
    # letting the Replicate client handle the Llama 3 chat template automatically.
    stream_iterator = replicate.stream(
        "meta/meta-llama-3-8b-instruct",
        input={
            "prompt": user_prompt,
            "system_prompt": system_prompt, # Use the dedicated system_prompt field
            "temperature": 0.3,
            "top_p": 0.9,
            # We remove the custom prompt_template here for simplicity/robustness
            "json": True, # Recommended for JSON output
        }
    )

    # --- 3. Collect the Output ---
    for token in stream_iterator:
        # Print the token as it arrives (optional, but shows the streaming effect)
        print(token, end="", flush=True) 
        full_output.append(token)
    
    # Print a newline after the stream is complete
    print() 

    # --- 4. Process the Full Output ---
    output_text = "".join(full_output)

    try:
        # Tries to find and extract the JSON array using index/rindex
        start = output_text.index("[")
        end = output_text.rindex("]") + 1
        return json.loads(output_text[start:end])
    except Exception as e:
        raise ValueError(
            f"Failed to parse JSON.\nOutput was:\n{output_text}"
        ) from e

# Example Usage (You will need to run this in an environment with your REPLICATE_API_TOKEN set):
# tasks_list = [
#     {"id": "1", "description": "Fix critical bug reported by CEO"}, 
#     {"id": "2", "description": "Clean up old documentation"}, 
#     {"id": "3", "description": "Design a new login screen"}
# ]
# result = prioritize_tasks_stream(tasks_list)
# print("\n--- Final Structured Output ---")
# print(json.dumps(result, indent=2))