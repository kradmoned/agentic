from google import genai
import os
from dotenv import load_dotenv


def main():
    # Load the dot env file from project directory into enviromental variables of the system
    load_dotenv()
    #get api key, from system enviroment variable such as $path is env variable
    api_key = os.environ.get("GEMINI_API_KEY")
    #In case there is no api key
    if api_key == None:
        raise RuntimeError("Gemini API key not found")
    # Create a new instance of gemini client
    client = genai.Client(api_key=api_key)
    # get the response
    try : 
        response = client.models.generate_content(model = "gemini-2.5-flash",contents = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")
    except Exception as e:
        print(Exception)
    # Each response has some meta data attached to it
    usage_metadata = response.usage_metadata
    # If metadata data is none then api request failed
    if usage_metadata == None:
        raise RuntimeError("Failed Api Request")
    # howing the number of tokens in the prompt that was sent to the model
    print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
    # showing the number of tokens in the model's response.
    print(f"Response tokens: {usage_metadata.candidates_token_count}")
    print("Response:")
    print(response.text)
    

if __name__ == "__main__":
    main()
