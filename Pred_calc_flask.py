# Dependencies
from flask import Flask, render_template, request, redirect, url_for
import requests 
from collections import OrderedDict
from bs4 import BeautifulSoup
import io
from contextlib import redirect_stdout

app = Flask(__name__)

#URL = "https://www.pro-football-reference.com/boxscores/"
URL = "https://www.pro-football-reference.com/years/2025/week_7.htm"

MAX = 999
NFL_TEAMS = {"JAX" : "Jacksonville Jaguars",
             "CLE" : "Cleveland Browns",
             "BUF" : "Buffalo Bills",
             "WAS" : "Washington Commanders",
             "DET" : "Detroit Lions",
             "ATL" : "Atlanta Falcons",
             "PIT" : "Pittsburgh Steelers",
             "ARI" : "Arizona Cardinals",
             "GB" : "Green Bay Packers",
             "LAC" : "Los Angeles Chargers",
             "MIA" : "Miami Dolphins",
             "SF" : "San Francisco 49ers",
             "NYG" : "New York Giants",
             "DAL" : "Dallas Cowboys",
             "PHI" : "Philadelphia Eagles",
             "CAR" : "Carolina Panthers",
             "LAR" : "Los Angeles Rams",
             "MIN" : "Minnesota Vikings",
             "NO" : "New Orleans Saints",
             "SEA" : "Seattle Seahawks",
             "TB" : "Tampa Bay Buccaneers",
             "BAL" : "Baltimore Ravens",
             "CIN" : "Cincinnati Bengals",
             "DEN" : "Denver Broncos",
             "HOU" : "Houston Texans",
             "IND" : "Indianapolis Colts",   
             "KC" : "Kansas City Chiefs",
             "LVR" : "Las Vegas Raiders",
             "NE" : "New England Patriots",
             "NYJ" : "New York Jets",
             "TEN" : "Tennessee Titans",
             "CHI" : "Chicago Bears"
             }

# Dictionaries to keep scores
NFL_Game_Scores = {}
Jay_Game_Scores = {} 
J_Game_Scores = {}
T_Game_Scores = {}
B_Game_Scores = {}




def create_score_doc(): 
    score_doc = open(f"Week_Scores.txt", "w")
    return score_doc

def create_dict(file_name): # Creates a Dict from a file
    dict = {}
    file = open(f"{file_name}", "r")
    
    if file_name.startswith("Week"):
        for line in file:
            line = line[:-1]
            stuff = line.split(" ")
            name = stuff[0]
            first_num_index = 0
            sec_num_index=0
            for word in range(len(stuff)):
                if  stuff[word].isdigit() and first_num_index == 0:
                    first_num_index = word
                elif stuff[word].isdigit():
                    sec_num_index = word
                elif word > 0:
                    name = name + " " + stuff[word]
            dict[name] = [stuff[first_num_index], stuff[sec_num_index]]
    else:
        for line in file:
            line = line.rstrip()
            segments = line.partition("-")
            W_N_S = segments[0].split(" ")

            name = W_N_S[0]
            first_num = W_N_S[1]
            sec_num = segments[2]
            name = name.upper()
            name = change_name(name)
            dict[name] = [first_num, sec_num]
    file.close()
    return dict

def change_name(name): # Makes player prediction's readable
    full_name = (NFL_TEAMS.get(name))
    return full_name

def calc(actual, predicted1, predicted2, predicted3, predicted4):
    Jay_Score = 0
    J_Score = 0
    Ben_Score = 0
    Tre_Score = 0
    Jay_teams = ""
    J_teams = ""
    Ben_teams = ""
    Tre_teams = ""

    
    other_draw = ""
    
    for score in actual: # This is where we gonna keep the math
        if actual[score][0] == actual[score][1]: ## Tie detected
            if score == other_draw:
                continue
            score_list = list(actual.keys())
            draw_index = score_list.index(score)
            other_draw = score_list[draw_index+1]
            
            if score in predicted1: 
                if(predicted1[score][0]==predicted1[score][1]):
                   Jay_off = abs(int(actual[score][0]) - int(predicted1[score][0])) + abs(int(actual[score][1]) - int(predicted1[score][1])) 
                else:
                    Jay_off = MAX
            elif other_draw in predicted1:
                if(predicted1[other_draw][0]==predicted1[other_draw][1]):
                    Jay_off = abs(int(actual[other_draw][0]) - int(predicted1[other_draw][0])) + abs(int(actual[other_draw][1]) - int(predicted1[other_draw][1])) 
                else:
                    Jay_off = MAX

            if score in predicted2: 
                if(predicted2[score][0]==predicted2[score][1]):
                   J_off = abs(int(actual[score][0]) - int(predicted2[score][0])) + abs(int(actual[score][1]) - int(predicted2[score][1])) 
                else:
                    J_off = MAX
            elif other_draw in predicted2:
                if(predicted2[other_draw][0]==predicted2[other_draw][1]):
                    J_off = abs(int(actual[other_draw][0]) - int(predicted2[other_draw][0])) + abs(int(actual[other_draw][1]) - int(predicted2[other_draw][1])) 
                else:
                    J_off = MAX
            
            if score in predicted3: 
                if(predicted3[score][0]==predicted3[score][1]):
                   Ben_off = abs(int(actual[score][0]) - int(predicted3[score][0])) + abs(int(actual[score][1]) - int(predicted3[score][1])) 
                else:
                    Ben_off = MAX
            elif other_draw in predicted3:
                if(predicted3[other_draw][0]==predicted3[other_draw][1]):
                    Ben_off = abs(int(actual[other_draw][0]) - int(predicted3[other_draw][0])) + abs(int(actual[other_draw][1]) - int(predicted3[other_draw][1])) 
                else:
                    Ben_off = MAX

            if score in predicted4: 
                if(predicted4[score][0]==predicted4[score][1]):
                   Tre_off = abs(int(actual[score][0]) - int(predicted4[score][0])) + abs(int(actual[score][1]) - int(predicted4[score][1])) 
                else:
                    Tre_off = MAX
            elif other_draw in predicted4:
                if(predicted4[other_draw][0]==predicted4[other_draw][1]):
                    Tre_off = abs(int(actual[other_draw][0]) - int(predicted4[other_draw][0])) + abs(int(actual[other_draw][1]) - int(predicted4[other_draw][1])) 
                else:
                    Tre_off = MAX
        else:
            if score in predicted1:
                Jay_off = abs(int(actual[score][0]) - int(predicted1[score][0])) + abs(int(actual[score][1]) - int(predicted1[score][1]))
            else:
                Jay_off = MAX
            if score in predicted2:
                J_off = abs(int(actual[score][0]) - int(predicted2[score][0])) + abs(int(actual[score][1]) - int(predicted2[score][1]))
            else:
                J_off = MAX
            if score in predicted3:
                Ben_off = abs(int(actual[score][0]) - int(predicted3[score][0])) + abs(int(actual[score][1]) - int(predicted3[score][1]))
            else:
                Ben_off = MAX
            if score in predicted4:
                Tre_off = abs(int(actual[score][0]) - int(predicted4[score][0])) + abs(int(actual[score][1]) - int(predicted4[score][1]))
            else:
                Tre_off = MAX

        
        if min(Tre_off, Jay_off, Ben_off, J_off) == 0: # Only check for perfect scores if one is detected
            if Jay_off == 0:
                Jay_Score += 1
                Jay_teams = Jay_teams + score + "(Perfect), "
            if J_off == 0:
                J_Score += 1
                J_teams = J_teams + score + "(Perfect), "
            if Ben_off == 0:
                Ben_Score += 1
                Ben_teams = Ben_teams + score + "(Perfect), "
            if Tre_off == 0:
                Tre_Score += 1
                Tre_teams = Tre_teams + score + "(Perfect), "

        if min(Tre_off, Jay_off, Ben_off, J_off) != 999:
            if min(Tre_off, Jay_off, Ben_off, J_off) == Jay_off:
                Jay_Score += 1
                Jay_teams = Jay_teams + score + ", "
            if min(Tre_off, Jay_off, Ben_off, J_off) == J_off:
                J_Score += 1
                J_teams = J_teams + score + ", "
            if min(Tre_off, Jay_off, Ben_off, J_off) == Ben_off:
                Ben_Score += 1
                Ben_teams = Ben_teams + score + ", "
            if min(Tre_off, Jay_off, Ben_off, J_off) == Tre_off:
                Tre_Score += 1
                Tre_teams = Tre_teams + score + ", "
    print(f'Jay: {Jay_Score} [ {Jay_teams} ]\n J: {J_Score} [ {J_teams} ]\n Ben: {Ben_Score} [ {Ben_teams} ]\n Tre: {Tre_Score}  [ {Tre_teams} ]')
    return 0

def update_total_season(ben_score, j_score, jay_score, tre_score):
    # Read current total season scores
    with open("total_season.txt", "r") as f:
        lines = f.readlines()
        if len(lines) >= 2:
            scores = lines[1].strip().split("-")
            current_scores = list(map(int, scores))
            
            # Ask user if they want to update scores
            response = input("Do you want to update the total season scores? (y/n): ")
            if response.lower() == 'y':
                # Update scores
                new_scores = [
                    current_scores[0] + ben_score,  # Ben
                    current_scores[1] + j_score,    # J
                    current_scores[2] + jay_score,  # Jay
                    current_scores[3] + tre_score   # Tre
                ]
                
                # Write updated scores back to file
                with open("total_season.txt", "w") as f:
                    f.write("B-J-Jay-T\n")
                    f.write(f"{new_scores[0]}-{new_scores[1]}-{new_scores[2]}-{new_scores[3]}")
                
                # Print updated total_season.txt contents
                print("\nUpdated total season scores:")
                print(f"Ben: {new_scores[0]}")
                print(f"J: {new_scores[1]}")
                print(f"Jay: {new_scores[2]}")
                print(f"Tre: {new_scores[3]}")

def get_scores():
    response = requests.get(URL)
    parsed = BeautifulSoup(response.content, "html.parser")
    games = parsed.find_all("table", class_="teams")

    score_doc = create_score_doc()
    for game in games: 
        draws = game.find_all("tr", class_="draw")
        if len(draws) > 0:
            for draw in draws:
                W_N = draw.find("a")
                W_S = draw.find("td", class_="right")
                NFL_Game_Scores[W_N.text] = [W_S.text, W_S.text]
                score_doc.write(W_N.text + " " + W_S.text + " " + L_S.text + "\n")
        else:
            winner = game.find("tr", class_="winner")
            if winner: 
                W_N = winner.find("a")
                W_S = winner.find("td", class_="right")
                loser = game.find("tr", class_="loser")
                L_S = loser.find("td", class_="right")
                NFL_Game_Scores[W_N.text] = [W_S.text, L_S.text]
                score_doc.write(W_N.text + " " + W_S.text + " " + L_S.text + "\n")
    score_doc.close()
    return 0
    
    
@app.route('/')
def index():
    with open('total_season.txt', 'r') as f:
        content = f.read()
    return render_template('index.html', content=content)

@app.route('/run_predictions')
def run_predictions_route():
    run_predictions()
    return "Predictions calculated and total season scores updated."

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/show_results', methods=['POST'])
def show_results():
    # Capture the output of run_predictions in a string
    f = io.StringIO()
    with redirect_stdout(f):
        get_scores()
        Jay_Game_Scores = create_dict("Jay_Scores.txt")
        J_Game_Scores = create_dict("J_Scores.txt")
        B_Game_Scores = create_dict("Ben_Scores.txt")
        T_Game_Scores = create_dict("Tre_Scores.txt")
        calc(NFL_Game_Scores, Jay_Game_Scores, J_Game_Scores, B_Game_Scores, T_Game_Scores)
    
    results = f.getvalue()
    return render_template('results.html', results=results)

@app.route('/update_scores', methods=['POST'])
def update_scores():
    try:
        # Read current total season scores
        with open("total_season.txt", "r") as f:
            lines = f.readlines()
            print('step 1')
            if len(lines) >= 2:
                scores = lines[1].strip().split("-")
                current_scores = list(map(int, scores))
                
                # Get the latest game scores
                get_scores()
                Jay_Game_Scores = create_dict("Jay_Scores.txt")
                J_Game_Scores = create_dict("J_Scores.txt")
                B_Game_Scores = create_dict("Ben_Scores.txt")
                T_Game_Scores = create_dict("Tre_Scores.txt")
                
                # Calculate new scores
                f = io.StringIO()
                with redirect_stdout(f):
                    calc(NFL_Game_Scores, Jay_Game_Scores, J_Game_Scores, B_Game_Scores, T_Game_Scores)
                print('current_scores', current_scores)
                # Get the score values from the calculation
                calc_output = f.getvalue()
                print('calc_output', calc_output)
                scores_line = str(calc_output).split('\n')
                scores = []
                for line in scores_line:                    
                    if line.strip():  # Ensure the line is not empty
                        parts = line.split('[')[0].split(':')[1].strip().split()
                        scores.extend([int(s) for s in parts])
                print('scores_line', scores_line)
                print('scores', scores)
                # Update scores
                new_scores = [
                    current_scores[0] + scores[2],  # Ben
                    current_scores[1] + scores[1],  # J
                    current_scores[2] + scores[0],  # Jay
                    current_scores[3] + scores[3]   # Tre
                ]
                print('step 5')
                
                # Write updated scores back to file
                with open("total_season.txt", "w") as f:
                    f.write("B-J-Jay-T\n")
                    f.write(f"{new_scores[0]}-{new_scores[1]}-{new_scores[2]}-{new_scores[3]}")
                print('step 6')
                message = "Scores updated successfully!"
                
        return render_template('results.html', message=message)
    except Exception as e:
        return render_template('results.html', message=f"Error updating scores: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
    
def run_predictions():
    get_scores()
    Jay_Game_Scores = create_dict("Jay_Scores.txt")
    J_Game_Scores = create_dict("J_Scores.txt")
    B_Game_Scores = create_dict("Ben_Scores.txt")
    T_Game_Scores = create_dict("Tre_Scores.txt")
    calc(NFL_Game_Scores, Jay_Game_Scores, J_Game_Scores, B_Game_Scores, T_Game_Scores)

