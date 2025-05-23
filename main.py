import os
import pandas as pd
import tkinter as tk
import requests
import numpy as np
from tkinter import ttk
from datetime import datetime

# Collecting data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(SAVE_DIR, exist_ok=True)

today_date = datetime.now().strftime("%d-%m-%Y")
save_path = os.path.join(SAVE_DIR, f"{today_date}.csv")

if not os.path.exists(save_path):
    url = "https://www.football-data.co.uk/mmz4281/2425/E0.csv"
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            file.write(response.content)
        print(f"File saved as {save_path}")
    else:
        print("Error while downloading file")
else:
    print(f"Todays file ({save_path}) already exist; skipping download.")

# Reading data
if os.path.exists(save_path):
    df = pd.read_csv(save_path)
    print("Data read properly.")
else:
    print("Error while reading file.")

# Sort teams
teams = sorted(df['HomeTeam'].unique().tolist())

def calculate_team_strength(team_name, df, is_home=True, last_matches=5):
    home_weight = 1.2 
    away_weight = 0.9

    if is_home:
        matches = df[df['HomeTeam'] == team_name].tail(last_matches)
        weight = home_weight
    else:
        matches = df[df['AwayTeam'] == team_name].tail(last_matches)
        weight = away_weight
    
    # Avg scored and conceded
    goals_scored = matches['FTHG' if is_home else 'FTAG'].mean() * weight
    goals_conceded = matches['FTAG' if is_home else 'FTHG'].mean() * weight
    
    # Estimate possession based on shots
    total_shots = matches['HS'].sum() + matches['AS'].sum()
    possession = matches['HS'].sum() / total_shots if total_shots > 0 else 0.5
    possession *= weight
    
    # Cap possession to max 100%
    possession = max(0, min(1, possession))
    
    # Estimate shots on target
    chances = matches['HST' if is_home else 'AST'].mean() * weight
    
    
    return {
        'goals_scored': goals_scored,
        'goals_conceded': goals_conceded,
        'possession': possession,
        'chances': chances,
    }

def simulate_match(home_team, away_team, df, simulations=5000):
    home_goals_list = []
    away_goals_list = []
    home_possession_list = []
    away_possession_list = []
    home_chances_list = []
    away_chances_list = []

    for _ in range(simulations):
        home_strength = calculate_team_strength(home_team, df)
        away_strength = calculate_team_strength(away_team, df, is_home=False)

        # Simulate goals
        home_goals = max(0, min(5, (home_strength['goals_scored'] + away_strength['goals_conceded']) / 2 + np.random.normal(0, 0.1)))
        away_goals = max(0, min(5, (away_strength['goals_scored'] + home_strength['goals_conceded']) / 2 + np.random.normal(0, 0.1)))

        # Simulate possession
        home_possession = home_strength['possession']
        away_possession = away_strength['possession']

        # Normalization of possession so that the sum is 100% and no team is biased
        total_possession = home_possession + away_possession

        if total_possession == 0:
            home_possession = 0.5
            away_possession = 0.5
        else:
            # Calculate normalized possession based on total possession
            home_possession = (home_possession / total_possession) * 0.5 + 0.5
            away_possession = (away_possession / total_possession) * 0.5 + 0.5

            # Ensure the sum is 100% by adjusting proportionally
            if home_possession + away_possession != 1:
                correction = 1 - (home_possession + away_possession)
                home_possession += correction / 2
                away_possession += correction / 2



        # Simulate shots on target
        home_chances = home_strength['chances'] + np.random.normal(0, 0.1)
        away_chances = away_strength['chances'] + np.random.normal(0, 0.1)


        home_goals_list.append(home_goals)
        away_goals_list.append(away_goals)
        home_possession_list.append(home_possession)
        away_possession_list.append(away_possession)
        home_chances_list.append(home_chances)
        away_chances_list.append(away_chances)

    # Return avg value
    return (
        round(np.mean(home_goals_list)),
        round(np.mean(away_goals_list)),
        np.mean(home_possession_list) * 100,
        np.mean(away_possession_list) * 100,
        round(np.mean(home_chances_list)),
        round(np.mean(away_chances_list))
    )

# UI
root = tk.Tk()
root.title("Match Simulator")
root.geometry("500x500")
root.configure(bg='black')

font_style = ("Arial", 14)

home_team_var = tk.StringVar()
away_team_var = tk.StringVar()

ttk.Label(root, text="Home:", background='black', foreground='white', font=font_style).pack()
home_team_combobox = ttk.Combobox(root, textvariable=home_team_var, values=teams, font=font_style)
home_team_combobox.pack()

ttk.Label(root, text="Away:", background='black', foreground='white', font=font_style).pack()
away_team_combobox = ttk.Combobox(root, textvariable=away_team_var, values=teams, font=font_style)
away_team_combobox.pack()

def predict():
    try:
        home_team = home_team_var.get()
        away_team = away_team_var.get()
        result = simulate_match(home_team, away_team, df)
        result_label.config(text=f"{home_team} vs {away_team}\nScore: {result[0]}-{result[1]}\nPossession: {result[2]:.1f}% - {result[3]:.1f}%\nShots on target: {result[4]} - {result[5]}")
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")

ttk.Button(root, text="Simulate", command=predict).pack()
result_label = ttk.Label(root, text="", background='black', foreground='white', font=font_style)
result_label.pack()

root.mainloop()
