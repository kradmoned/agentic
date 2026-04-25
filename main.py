from google import genai
from google.genai import types
import os
import argparse
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT
from call_function import available_functions
from call_function import call_function
def main():
    # create an argument parser object
    parser = argparse.ArgumentParser()
    # Create an argument that will be passed to it
    parser.add_argument("user_prompt", type = str , help = "User prompt")
    parser.add_argument("--verbose", action="store_true", help = "Enable verbose output")
    args = parser.parse_args()
    prompt = args.user_prompt
    # Load the dot env file from project directory into enviromental variables of the system
    load_dotenv()
    #get api key, from system enviroment variable such as $path is env variable
    api_key = os.environ.get("GEMINI_API_KEY")
    #In case there is no api key
    if api_key == None:
        raise RuntimeError("Gemini API key not found, Create a .env in project and add GEMINI_API_KEY = yourkey")
    # Create a new instance of gemini client
    client = genai.Client(api_key=api_key)
    # get the response
    message = [types.Content(role="user", parts=[types.Part(text = prompt)])]
    # types.GenerateContentConfig -- takes a list of Tool objects via the tools parameter, alongside other config like system_instruction.
    config = types.GenerateContentConfig(system_instruction= SYSTEM_PROMPT, tools=[available_functions])
    response = None
    try : 
        # clients.model is a sub object that contains the contains the method generate content that can either take a string prompt
        # or it can take a types.content list where each types.content can be thought as a single message between user and model
        # Types.content has two fields one is role other is "parts" which is a list of part because each message can contain multiple part such as an image and text
        #print([fd.name for fd in available_functions.function_declarations])
        response = client.models.generate_content(model = "gemini-3.1-flash-lite-preview",contents = message, config= config)
    except Exception as e:
        print(e)
    # Each response has some meta data attached to it
    if response == None:
        raise RuntimeError("No response")
    usage_metadata = response.usage_metadata
    # If metadata data is none then api request failed
    if usage_metadata == None:
        raise RuntimeError("Failed Api Request")
    if args.verbose == True:
        print(f"User prompt: {prompt}")
        # howing the number of tokens in the prompt that was sent to the model
        print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
        # showing the number of tokens in the model's response.
        print(f"Response tokens: {usage_metadata.candidates_token_count}")
    function_call_results  = []
    if response.function_calls:
        for function_call in response.function_calls:
            function_call_result : types.Content = call_function(function_call, verbose= args.verbose)
            if not function_call_result.parts:
                raise Exception("Function call response has no parts")
            if not function_call_result.parts[0].function_response:
                raise Exception("call_function return has no function Response")
            if not function_call_result.parts[0].function_response.response:
                raise Exception("Call function return has no funtion response.response")
            function_call_results.append(function_call_result.parts[0])
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
        
    else:
        ("Response:")
        (response.text)
    

if __name__ == "__main__":
    main()
