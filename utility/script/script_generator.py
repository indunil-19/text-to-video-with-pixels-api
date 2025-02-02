import os
from openai import OpenAI
import json

# Check for Groq API key and initialize the client accordingly
if os.environ.get("GROQ_API_KEY") and len(os.environ.get("GROQ_API_KEY")) > 30:
    from groq import Groq
    model = "mixtral-8x7b-32768"
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )
else:
    OPENAI_API_KEY = os.getenv('OPENAI_KEY')
    if not OPENAI_API_KEY:
        raise ValueError("Missing OpenAI API Key in environment variables.")
    model = "gpt-4o"
    client = OpenAI(api_key=OPENAI_API_KEY)

def generate_script(topic):
    """
    Generate a concise, engaging script for a YouTube Shorts-style facts video.
    
    Args:
        topic (str): The topic for the facts video (e.g., 'weird facts').
    
    Returns:
        str: The generated script.
    """
    # Prompt for the AI
    prompt = (
        """You are a seasoned content writer for a YouTube Shorts channel, specializing in facts videos. 
        Your facts shorts are concise, each lasting less than 120 seconds (approximately 300 words). 
        They are incredibly engaging and original. When a user requests a specific type of facts short, you will create it.

        For instance, if the user asks for:
        Weird facts
        You would produce content like this:

        Weird facts you don't know:
        - Bananas are berries, but strawberries aren't.
        - A single cloud can weigh over a million pounds.
        - There's a species of jellyfish that is biologically immortal.
        - Honey never spoils; archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still edible.
        - The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after 38 minutes.
        - Octopuses have three hearts and blue blood.
        - The world is crazier than we can imagine. Stay curious!

        You are now tasked with creating the best short script based on the user's requested type of 'facts'.

        Keep it brief, highly interesting, and unique.

        Strictly output the script in a JSON format like below, and only provide a parsable JSON object with the key 'script'.

        # Output
        {"script": "Here is the script ..."}
        """
    )

    try:
        # Call the AI model for script generation
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": topic}
            ]
        )
        
        # Parse the response content as JSON
        content = response.choices[0].message.content
        
        # Clean the content by removing unexpected control characters
        content = content.replace("\n", "\\n").replace("\r", "")
        
        # Attempt to load the content as JSON
        script = json.loads(content)["script"]
        return script
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Raw response content: {content}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise
