from games_id import GamesId
from current_plays import CurrentPlays
import pandas as pd
from win_probability_calculation import WinProbabilityCalculator

momentum_chart = {
    # Positive offensive plays
    "Home Run": 8,
    "Triple": 7,
    "Double": 6,
    "Single": 2,
    "Walk": 2,
    "Intent Walk": 2,
    "Hit By Pitch": 2,
    "Stolen Base": 2,
    "Sac Fly": 4,
    "Sac Bunt": 2,
    "Field Error": 4,
    "Catcher Interference": 1,

    # Neutral or slightly negative
    "Out": 0,
    "Forceout": 0,
    "Fielders Choice": 1,
    "Fielders Choice Out": 0,
    "Bunt Groundout": 0,
    "Pop Out": 0,
    "Flyout": 0,
    "Groundout": 0,
    "Lineout": 0,
    "Strikeout": -1,

    # Strong defensive plays
    "Double Play": -3,
    "Grounded Into DP": -3,
    "Triple Play": -6,

    # Negative base-running
    "Caught Stealing 2B": -2,
    "Caught Stealing 3B": -2,
    "Caught Stealing Home": -3,
    "Caught Stealing 1B": -1,  # rare but possible
    "Pickoff": -2,

    # Wild or rare events
    "Wild Pitch": 1,
    "Passed Ball": 1,
    "Unknown Event": 0,
}


GamesId = GamesId()
games_id = GamesId.get_games_id()
current_plays = CurrentPlays(games_id)
df = pd.DataFrame(current_plays.get_current_plays())
wp_calc = WinProbabilityCalculator()

# 1) Momentum per event (already did this)
df['momentum_raw'] = df['event'].map(momentum_chart).fillna(0)

# 2) Assign positive momentum only to the batting team
df['home_delta'] = df.apply(
    lambda r: r['momentum_raw'] if not r['top_inning'] else 0,
    axis=1
)
df['away_delta'] = df.apply(
    lambda r: r['momentum_raw'] if r['top_inning'] else 0,
    axis=1
)

# 3) Cumulative positive sums
df['home_cumulative'] = df.groupby('gamePk')['home_delta'].cumsum()
df['away_cumulative'] = df.groupby('gamePk')['away_delta'].cumsum()

df['momentum_diff'] = df['home_cumulative'] - df['away_cumulative']

df['home_win_prob'] = df.apply(
    lambda r: wp_calc.weighted_win_probability(r['momentum_diff'], r['inning']),
    axis=1
)

df['away_win_prob'] = 1 - df['home_win_prob']

print(df.head(50))