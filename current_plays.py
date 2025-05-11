import requests

class CurrentPlays:
    def __init__(self, games_id):
        self.games_id = games_id

    def get_current_plays(self):
            """
            Get the current plays for the given game IDs from the MLB API.
            """

            all_plays_data = []

            for gamePk in self.games_id:
                url = f"https://statsapi.mlb.com/api/v1.1/game/{gamePk}/feed/live"
                response = requests.get(url)

                if response.status_code != 200:
                    print(f"Error: Unable to fetch data for game {gamePk}")
                    continue
                
                game_data = response.json()
                if 'liveData' in game_data and 'plays' in game_data['liveData']:
                    all_plays = game_data['liveData']['plays'].get('allPlays', [])
                    home_team = game_data['gameData']['teams']['home']['name']
                    away_team = game_data['gameData']['teams']['away']['name']
                    for play in all_plays:
                        inning = play['about'].get('inning', 'Unknown Inning')
                        result = play.get('result', {})
                        event = result.get('event', 'Unknown Event')
                        top_inning = play['about'].get('isTopInning', 'Not Available')
                        description = result.get('description', 'No description available')
                        
                        all_plays_data.append({
                            "gamePk": gamePk,
                            "home_team": home_team,
                            "away_team": away_team,
                            "inning": inning,
                            "top_inning": top_inning,
                            "event": event,
                            "description": description
                        })
                else:
                    print(f"No play-by-play data found for game {gamePk}")

            return all_plays_data