import replicate
import json
import os

def prioritize_tasks(tasks):
    # --- 1. Define Prompts (Optimized for Llama 3 Instruct) ---
    system_prompt = (
        "You are an AI that assigns priorities to tasks. "
        "Rules: HIGH = important + urgent, MEDIUM = important but not urgent, "
        "LOW = optional or trivial. "
        "Respond with JSON ONLY. "
        "The output MUST be a JSON array, for example: "
        "[ { \"id\": \"1\", \"priority\": \"HIGH\" }, { \"id\": \"2\", \"priority\": \"MEDIUM\" } ]"
    )

    user_prompt = f"Tasks to prioritize:\n{json.dumps(tasks, indent=2)}"

    full_output = [] # Initialize a list to collect the streamed tokens

    # --- 2. Use replicate.stream() (This part is now working) ---
    print("Streaming response from Replicate...")
    
    stream_iterator = replicate.stream(
        "meta/meta-llama-3-8b-instruct",
        # NOTE: You must still use the full owner/name:version string here 
        # if your library version requires it (as per the last error).
        # We will assume you fixed that error, so I'll keep the simple name 
        # but be aware you may need the hash if the error returns.
        input={
            "prompt": user_prompt,
            "system_prompt": system_prompt,
            "temperature": 0.3,
            "top_p": 0.9,
            "json": True,
        }
    )

    # --- 3. CORRECTED: Collect the String Content ---
    for token_object in stream_iterator:
        # CONVERSION STEP: Convert the token object to a string.
        # This is typically handled by Python's built-in str() function
        # or by accessing a .text attribute if the library uses a custom object.
        token_string = str(token_object)
        
        # Print the token as it arrives
        print(token_string, end="", flush=True) 
        
        # Collect the string
        full_output.append(token_string)
    
    print() 

    # --- 4. Process the Full Output ---
    # Now this works because full_output is a list of strings
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