# This is for prompt Template.

output_array_system_message = "Your output should be json. List, start with [ and end with ]. Do not include any other text in your output except for the array."
output_json_system_message = "Your output should be json. Do not include any other text in your output except for the json."
output_text_system_message = "Do not include any other text except for the required output text."

def synopsis_prompt_gen(prompt, synopsis, degree, info):
    return f"""
        You are a novel synopsis writer. Your task is improve the original synopsis. 

        Below, inside ``` is a instruction for the novel.
        ```
        {info}
        ```

        ORIGINAL_SYNOPSIS: {synopsis}

        And I want to get fixed synopsis by following the instruction below
        INSTRUCTION: {prompt}

        Preserve the original synopsis by the following float: {degree} (0: do not care about origin Synopsis, 1: Leave the original content intact.)
        In the original synopsis, between [ and ] is a instruction for what should be generated in that location.
    """
