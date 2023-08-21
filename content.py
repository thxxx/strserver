from setting import generate
from prompt import synopsis_prompt_gen, output_array_system_message, output_text_system_message, output_json_system_message
from setting import translate
import json
import re

def topic_generate(originalList, prompt, type, info, chosenKeywords, brainDump):
    if type == "re":
        topic_prompt = f"""
            You are a best-seller web novel writer. Your task is give a novel writer creative possible topics for new novel.

            Below, inside ``` is what a writer written for his new web novel.
            ```
            {brainDump}
            ```
            These are writer's additional preference of new novel : {chosenKeywords}
            This is current topics : {originalList}

            Your task is to generate new possible topics by following below INSTRUCION.
            INSTRUCTION : {prompt}
            
            The output should be json dictionary with the following key: value pairs
            - ideas: list (length 4) of creative ideas. this should be one simple sentence. Do not include any other text except for the list.

            Based on the above information, write 4 possible interesting settings that could be included in this web novel.
        """
    else:
        topic_prompt = f"""
            You are a best-seller web novel writer. Your task is give a novel writer creative possible topics for new novel.

            Below, inside ``` is what a writer written for his new web novel.
            ```
            {brainDump}
            ```
            These are writer's additional preference of new novel : {chosenKeywords}

            The output should be json dictionary with the following key: value pairs
            - ideas: list (length 4) of creative ideas. this should be one simple sentence. Do not include any other text except for the list.

            Based on the above information, write 4 possible interesting settings that could be included in this web novel.
        """

    output = generate(topic_prompt, systemMessage=output_array_system_message, model="chatgpt", keys=['ideas'])
    aa = [
        translate(output['data']['ideas'][0]),
        translate(output['data']['ideas'][1]),
        translate(output['data']['ideas'][2]),
        translate(output['data']['ideas'][3]),
    ]
    output['data'] = aa
    
    return output

def synopsis_generate(prompt, synopsis, info, type):
    synop_prompt = f"""
        You are a best-seller novel writer having published highest-grossing books. Do not include any other text except for the plot.
        Write a plot summary.
        Below, inside ``` is a information of novel.
        ```
        {info}
        ```

        Please make unique and creative plot of a Web novel that can be used when you write a Webnovel based on the above information.
        <Instructions>
        - plot is a summary of whole story of a web novel including the prologue and ending.
        - It would be good to add some unique and very creative stories.
        - Please make unique and creative plot of a Web novel that can be used when you write a Webnovel based on the above information.
        - Feel free to think outside the box. You can combine several unique elements.
    """
    if type == "re":
        synop_prompt = f"""
            You are a best-seller novel writer having published highest-grossing books. Do not include any other text in your output except for the plot.
            Below, inside ``` is a information of novel.
            ```
            {info}
            ```

            Below, inside ''' is current synopsis of a novel written by a writer.
            ORIGINAL_SYNOPSIS : '''
            {synopsis}
            '''

            In the above original synopsis, a text between [ and ] is a instruction for what should be generated in that place.
        """
        if prompt:
            synop_prompt += f"""
            \n\n
                Modify above synopsis(plot summary) by following INSTRUCTION below and return plot summary.
                INSTRUCTION: {prompt}
            """


    output = generate(synop_prompt, systemMessage=output_text_system_message, model="chatgpt")
    output['data'] = translate(output['data'])

    return output

def plan_generate(dump, keywords):
    plan_prompt = f"""
        You are a best-seller writer having published highest-grossing books.
        Below, inside ``` is what a writer wrote for planning a novel.
        INFORMATION : ```{dump}```
        These are important elements of a novel : {keywords}

        By using above INFORMATION, organize below elements. Each element should be more than 1 and less than 4 sentences.
        - background: What is the concept and setting of the background world of this novel?
        - intention: What is the core theme consciousness and planning intention of the novel?
        - growth: How does the main character change as the novel progresses?
        - ending: What is the ending of this novel?
        - interest: What is the key elements that makes readers interested in novels?
        - event: What is the main events of this novel?

        Your output should be json dictionary with below key:value pairs.
        - background
        - intention
        - growth 
        - event
        - ending
        - interest
    """

    output = generate(plan_prompt, model="chatgpt", keys=["background, intention, growth, event, ending, interest"])
    # response_body = {
    #     'data': res,
    #     "prompt_tokens": response['usage']['prompt_tokens'],
    #     "completion_tokens": response['usage']['completion_tokens'],
    #     "total_tokens": response['usage']['total_tokens']
    # }
    output['data'] = {
        "background": translate(output['data']['background']),
        "intention": translate(output['data']['intention']),
        "growth": translate(output['data']['growth']),
        "event": translate(output['data']['event']),
        "ending": translate(output['data']['ending']),
        "interest": translate(output['data']['interest']),
    }

    return output

def first_generate(info:str):
    first_prompt = f"""
        You are a best-seller writer having published highest-grossing books.
        Your task is to plan the first chapter of a novel, which is short story. What should be written in the first chapter? return the detail desciptions, not whole novel.
        Do not include any other text except for the json.

        The book description of the entire novel is described below delimited by ```
        ```
        [[Book Description]]:
        {info}
        ```

        Please create an engaging first chapter for a web novel, ensuring it includes the following key elements as part of a json dictionary. and generate in this order:
        - event : Detail an extreme event that takes place in the first chapter. It has to be a big impact on the main character, usually positive. Include descriptions for the reader to understand the story and protagonist's behavior, thoughts, decision, story.
        - end : Conclude the first chapter with a cliffhanger that entices readers to continue the novel. Do not include explanations, just the novel's content.
        - start : Describe the beginning of the first chapter, introducing the main character without any special events.
        - descriptions : list (length 2 to 5). Include What should be fully explained to the reader to understand the story and protagonist's behavior, thoughts, decision, story.

        Bear in mind the following instructions when crafting the chapter:

        1. Include detailed descriptions of the characters, their backgrounds, the protagonist's introduction, and their surrounding circumstances.
        2. Keep in mind these popular keywords: "The main character who happens to get a very good opportunity," "A very powerful main character from the start," and "provocative, high-tension story."
        3. Avoid vague expressions in the start, descriptions, event, and end segments, opting for detailed scenes and plausibility from novels.
        4. If romance is involved, do not let characters fall in love at first sight.
        5. The first chapter should not span more than one day. This is short story.

        To ensure quality, make sure to:

        - Provide context for the character's actions, the reasons behind an event, and the emotional connections between characters.
        - Offer enough explanations for a character's behavior.
        - Include descriptions explaining why the character made a certain decision.
        - Prioritize plausibility throughout the chapter.
        - If a character realize something, add detail descriptions about why and how the character realize it.
    """

    output = generate(first_prompt, model="chatgpt")

    return output

def character_generate(info:str):
    char_prompt = f"""
        You are a best-seller writer having published highest-grossing books.
        Your task is to write about characters in the novel.
        Do not include any other text except for the json.

        The book description of the entire novel is described below delimited by ```
        ```
        {info}
        ```

        The output should be json dictionary with the following key: value pairs
        - characters: 2-4 most important characters including protagonists and antagonists.
    """

    output = generate(char_prompt, model="chatgpt")

    return output

def character_nudge_generate(info:str, characters:str):
    cn_prompt = f"""
        You are a best-seller writer having published highest-grossing books.
        You are a assistant for writers. Your task is giving them good questions, nudge or guide to help them. Is stimulates the creativity of writers.
        Give 3 good questions, which is important things When planning characters in a novel, for people who is writing about characters descriptions in his novel. every question should be simple one sentence.
        Do not include any other text except for the json.

        The book description of the entire novel is described below.
        INFORMATION : 
        '''
        {info}
        '''

        Below, inside ``` is what is written about characters in novel until now.
        ```
        {characters}
        ```

        The output should be json dictionary with the following key: value pairs
        - nudges: list (length 3) of creative ideas. this should be one simple sentence. Do not include any other text except for the list.

        Give 3 good questions for people who is writing about characters descriptions in his novel. every question should be simple one sentence.
        """
    
    output = generate(cn_prompt, systemMessage=output_json_system_message, model="chatgpt", keys=['nudges'])
    aa = [
        translate(output['data']['nudges'][0]),
        translate(output['data']['nudges'][1]),
        translate(output['data']['nudges'][2]),
    ]
    output['data'] = aa
    
    return output


def synop_nudge_generate(info:str, synopsis:str):
    cn_prompt = f"""
        You are a best-seller writer having published highest-grossing books.
        You are a assistant for writers. Your task is giving them good nudge questions, nudge or guide to help them. Is stimulates the creativity of writers.
        Give 3 good nudge questions, which is important things When writing synopsis, plot summary of a novel, for people who is writing about synopsis, plot summary of novel. every question should be simple one sentence.
        Do not include any other text except for the json.

        The book description of the entire novel is described below.
        INFORMATION : 
        '''
        {info}
        '''

        Below, inside ``` is what is written about synopsis, plot of novel in novel until now.
        ```
        {synopsis}
        ```

        The output should be json dictionary with the following key: value pairs
        - nudges: list (length 3) of creative ideas. this should be one simple sentence. Do not include any other text except for the list.

        Give 3 good nudge questions for people who is writing about synopsis, plot summary of novel. every question should be simple one sentence.
        """
    
    output = generate(cn_prompt, systemMessage=output_json_system_message, model="chatgpt", keys=['nudges'])
    aa = [
        translate(output['data']['nudges'][0]),
        translate(output['data']['nudges'][1]),
        translate(output['data']['nudges'][2]),
    ]
    output['data'] = aa
    
    return output

def first_nudge_generate(info:str, first:str):
    fn_prompt = f"""
        You are a best-seller writer having published highest-grossing books.
        You are a assistant for writers. Your task is giving them good nudge questions, nudge or guide to help them. Is stimulates the creativity of writers.
        Give 3 good nudge questions, which is important things When writing the first chapter, of a novel, for people who is writing about  the first chapter of novel. every question should be simple one sentence.
        Do not include any other text except for the json.

        The book description of the entire novel is described below.
        INFORMATION : 
        '''
        {info}
        '''

        Below, inside ``` is what is written about the first chapter of novel in novel until now. start is the start of novel, event is the main event in the first chapter.
        ```
        {first}
        ```

        The output should be json dictionary with the following key: value pairs
        - nudges: list (length 3) of creative ideas. this should be one simple sentence. Do not include any other text except for the list.

        Give 3 good nudge questions for people who is writing about the first chapter of novel. every question should be simple one sentence.
    """

    output = generate(fn_prompt, systemMessage=output_json_system_message, model="chatgpt", keys=['nudges'])
    aa = [
        translate(output['data']['nudges'][0]),
        translate(output['data']['nudges'][1]),
        translate(output['data']['nudges'][2]),
    ]
    output['data'] = aa
    
    return output

def brain_nudge_generate(info:str, brainDump:str):
    bn_prompt = f"""
        You are a best-seller writer having published highest-grossing books.
        You are a assistant for writers. Your task is giving them good nudge questions, nudge or guide to help them. Is stimulates the creativity of writers.
        Do not include any other text except for the json.

        """
    
def brain_generate(info:str, brainDump:str, prompt:str):
    b_prompt = f"""
        You are a best-seller writer having published highest-grossing books.
        Your task is helping a writer who is trying to write a novel.

        Below, inside ``` is what a writer is writing now.
        INFORMATION : ```
        {brainDump}
        ```

        Based on the above information, follow the below instruction.
        INSTRUCTION: {prompt}
    """

    output = generate(b_prompt, systemMessage=output_text_system_message, model="chatgpt")
    output['data'] = re.sub(r'\n', '<br />', output['data'])
    output['data'] = translate(output['data'])

    return output