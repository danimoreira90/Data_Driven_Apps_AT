from langchain.tools import tool
from langchain.chains import LLMChain
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


from soccer_stats.competitions import get_matches
from soccer_stats.matches import get_lineups
import json
import yaml


def get_match_details(match_id: int) -> dict:
    """
    Get the details of a specific match using the match ID.
    Args:
        match_id (int): The unique identifier of the match.
        
    Returns:
        dict: The details of the match.
    """
    

def filter_starting_xi(line_ups: str) -> dict:
    """
    Filter the starting XI players from the provided lineups.
    
    Args:
        line_ups (str): The JSON string containing the lineups of the teams.
        
    Returns:
    
    """
    line_ups_dict = json.loads(line_ups)
    filter_starting_xi =  {}
    for team, team_line_up in line_ups_dict.items():
        filter_starting_xi[team] = []
        for player in sorted(team_line_up, key= lambda x: x["jersey_number"]):
            try:
                positions = player["positions"]["positions"]
                if positions[0].get("start_reason") == "Starting XI":
                    filter_starting_xi[team].append({
                        "player": player["player_name"],
                        "position": positions[0].get('position'),
                        "jersey_number": player["jersey_number"]
                    })
            except (KeyError, IndexError):
                continue
    return filter_starting_xi


def get_sport_specialist_comments_about_match(match_details: str, line_ups: str) -> str:
    """
    Returns the comments of a sports specialist about a specific match.
    The comments are generated based on match details and lineups.
    """
    
    line_ups = filter_starting_xi(line_ups)
    
    agent_prompt = """
    You are a sports commentator with expertise in football (soccer). Respond as
    if you are delivering an engaging analysis for a TV audience. Here is the
    information to include:

    Instructions:
    1. Game Overview:
        - Describe the importance of the game (league match, knockout, rivalry, etc.).
        - Specify when and where the game took place.
        - Provide the final result.
    3. Analysis of the Starting XI:
        - Evaluate the starting lineups for both teams.
        - Highlight key players and their roles.
        - Mention any surprising decisions or notable absences.
    3.  Contextual Insights:
        - Explain the broader implications of the match (rivalry, league standings, or storylines).
    4. Engaging Delivery:
        - Use a lively, professional, and insightful tone, making the commentary
        appealing to fans of all knowledge levels.
    
    The match details are provided by the provided as follow: 
    {match_details}
    
    The team lineups are provided here:
    {lineups}
    
    Provide the expert commentary on the match as you are in a sports broadcast.
    Start your analysis now and engage the audience with your insights.
    
    Say: "Hello everyone, I've watched to the match between [Home Team] and [Away Team]..."
    """
    llm = GoogleGenerativeAI(model="gemini-pro")
    input_variables={"match_details": yaml.dump(match_details),
                     "lineups": yaml.dump(line_ups)}
    prompt = PromptTemplate.from_template(agent_prompt)
    chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
    return chain.run(
        **input_variables
    )


def retrieve_match_details(action_input:str) -> str:
    """
    Get the details of a specific match 
    
    Args:
        - action_input(str): The input data containing the match_id.
          format: {
              "match_id": 12345
              "competition_id": 123,
                "season_id": 02
            }
    """
    match_id = json.loads(action_input)["match_id"]
    competition_id = json.loads(action_input)["competition_id"]
    season_id = json.loads(action_input)["season_id"]
    matches = json.loads(get_matches(competition_id, season_id))
    match_details= next(
        (match for match in matches if match["match_id"] == int(match_id)),
        None
    )
    return match_details

@tool
def get_match_details(action_input:str) -> str:
    """
    Get the details of a specific match 
    
    Args:
        - action_input(str): The input data containing the match_id.
          format: {
              "match_id": 12345
              "competition_id": 123,
                "season_id": 02
            }
    """
    return yaml.dump(retrieve_match_details(action_input))
    

@tool
def get_specialist_comments(action_input:str) -> str:
    """
    Provide an overview of the match and the match details.
    Provide comments of a sports specialist about a specific match.
    The specialist knows match details and lineups.
    
    Args:
        - action_input(str): The input data containing the competition_id, season_id and match_id.
          format: {
              "competition_id": 123,
              "season_id": 02,
              "match_id": 12345
            }
    """
    match_details = retrieve_match_details(action_input)
    line_ups = get_lineups(match_details["match_id"])
    return get_sport_specialist_comments_about_match(match_details, line_ups)