# ⚽ Premier League Games Simulator
This is a simple football match simulator using historical data provided by Football-Data API. The simulator estimates match results based on the historical performance of the teams involved in the match.

# Features
Simulates match results based on historical football data.
Estimates goals scored, possession, and shots on target for both teams.
Uses recent match data (last 5 matches) to calculate team strength.
Customizable with a graphical user interface (GUI) built using Tkinter.

# Requirements
Before running the project, you will need to install the following Python libraries:
requests (for fetching the historical football data)
pandas (for handling the data)
numpy (for statistical calculations)
tkinter (for creating the graphical user interface)

# Install them using pip:
pip install requests pandas numpy tk

# How It Works
Data Collection:
The historical football data for the English Premier League is downloaded from a given URL. The data is then saved locally with the current date as the filename.

Team Strength Calculation:
The simulator calculates the strength of a team based on their performance in the last few matches:
Goals scored and conceded (home or away).
Possession estimation based on shots attempted.
Shots on target.

# Match Simulation:
The simulator runs 5000 simulations for a match between two teams and returns average:
Predicted score for both teams.
Possession percentage for each team.
Number of shots on target for both teams.

# User Interface:
The application provides a simple graphical interface where you can select two teams, click "Simulate", and view the predicted results (score, possession, and shots on target).

# Usage
Run the script by executing:
python match_simulator.py
The window will open with drop-down lists for selecting a home and away team.
After selecting both teams, click the Simulate button.
The match simulation will display below, showing:
Predicted score (home team vs away team).
Possession percentage for both teams.
Shots on target for both teams.

# Example Output
After selecting two teams (e.g., "Manchester United" and "Chelsea"), clicking Simulate will display:
Manchester United vs Chelsea
Score: 2-1
Possession: 53.2% - 46.8%
Shots on target: 4 - 3

# A few predicted matches
| Date       | Home Team     | Away Team    | Predicted Score | Predicted Possession | Predicted Shots on Target | Actual Score | Actual Possession | Actual Shots on Target |
|------------|---------------|--------------|-----------------|----------------------|---------------------------|--------------|--------------------|------------------------|
| 25.02.2025 | Brighton      | Bournemouth  | 2-1             | 54.2%-45.8%          | 5-7                       | 2-1          | 44%-56%            | 4-5                    |
| 25.02.2025 | Crystal Palace| Aston Villa  | 1-1             | 44.7%-55.3%          | 9-4                       | 4-1          | 36%-64%            | 6-2                    |
| 25.02.2025 | Wolves        | Fulham       | 1-2             | 47.9%-52.1%          | 5-6                       | 1-2          | 60%-40%            | 5-5                    |
| 25.02.2025 | Chelsea       | Southampton  | 3-0             | 58.8%-41.2%          | 11-4                      | 4-0          | 60%-40%            | 10-2                   |

# License
This project is licensed under the MIT License - see the LICENSE file for details.
