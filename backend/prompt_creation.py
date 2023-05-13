
def parse_input(user_text):
    """ Parse input from user to get the location and the question. """

    prompt = f"""
    You will be given a user prompt delimited by <<< and >>>. Your output will be only a JSON object!!!

    There are three scenarios. Your first job is to read the text and determine what scenario the question fits - do not output this information, just store it for later use.

        1. In the first scenario the user will ask a question about something at a specific location in Slovenia. 
        2. In the second scenario the user will be asking you to give a recommendation of a location in Slovenia that fits the users' preferences.
        3. In the third scenario the user will be asking you something else, that has nothing to do with the first two scenarios.

    After determining the scenario, follow the instructions for the chosen scenario.

    You should only return a JSON object. What the JSON object looks like depends on our scenario. 

        First scenario: 
            You only need to return JSON. Use the following format:
                task: <"location_prediction">
                location: <user refering location - string> - extract from user prompt to what location is the user refering to.
                question: <generated question - string> - store a rewritten question that describes what information the user is 
                        asking about some location. You should reference the location as the picture. If the input is not a question
                        you should output "Describe the surroundings".

                        some examples for the question extraction in this scenario:
                            For example:
                                input: What is the weather like in london?
                                your output: What is the weather?
                                input: Is it cloudy or foggy in london?
                                your output: Is it cloudy or is it foggy?


        Second scenario:
            You only need to return JSON. Use the following format:
                task: <"location_recommendation">
                user_location: <coordinates - tuple> - get coordinates of the user location, in case it is not provided, give coordinates of Ljubljana
                distance: <maximum distance - int> - from user input determine the maximum distance the user is willing to travel if this information was provided
                prefered_weather: <weather - string> - from user input determine the weather the user prefers if this information was provided
                prefered_activity: <activity - string> - from user input determine the activity the user prefers if this information was provided

        Third scenario:
            You only need to return JSON. Use the following format:
                task: <"other">
                answer: <answer - string> - please provide an answer for the user question

    <<<{user_text}>>>
    """
    return prompt


def describe_location(location, response):
    # generate format
    chat_txt = ""

    loc_txt = str(location)+"-"
    for fact in response:
        loc_txt += fact[0]+","
    loc_txt = loc_txt[:-1]+";"
    chat_txt += loc_txt
    print(chat_txt)

    prompt = f"""

    You will be provided with text delimited by < and >.
    Text will be of format location-fact,...,fact;location-fact,...fact;...
    facts are based on the location at this moment.

    Generate text for each location, describe it based on facts about it in this moment. 
    Be short and do no overexaggerate in your answers.

    <{chat_txt}>
    """
    return prompt


def describe_location_general(task,locations):
    #generate format for general search (where is it sunny)
    if len(locations)>0:
        txt = locations[0][1]
    else:
        txt = "loc:None"

    txt += ";"+task.get("prefered_weather")+";"+str(task.get("distance"))
    prompt = f"""

    You will be provided with text delimited by < and >.
    Text will be of format location;weather;distance.

    Generate text  that is an answer to the previous user question. Be short.
    At the location is the user specified weather. The location is at most user specified distance away from the user location.
    If location is None, answer that no location statisfies the user preferences.

    <{txt}>
    """
    return prompt