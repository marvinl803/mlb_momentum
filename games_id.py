from datetime import date
import requests

class GamesId:
    
    def get_games_id(self):
        """
        Get the games id for today from the MLB API.
        """ 
        today = date.today()
        url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2025-05-10"
        response = requests.get(url)
        games = response.json()
        todays_games = []

        # Check if there are games today
        if games['dates']:
            for game in games['dates'][0]['games']:
                todays_games.append(game['gamePk'])
        else:
            return ("No games found for today.")
        return todays_games
        