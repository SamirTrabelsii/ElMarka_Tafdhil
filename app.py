import streamlit as st
import pandas as pd

# Sidebar for player names
st.sidebar.title("Player Setup")
player_names = [
    st.sidebar.text_input("Enter Player 1 Name", value="Player 1"),
    st.sidebar.text_input("Enter Player 2 Name", value="Player 2"),
    st.sidebar.text_input("Enter Player 3 Name", value="Player 3"),
    st.sidebar.text_input("Enter Player 4 Name", value="Player 4"),
]

# Start Game Button
if st.sidebar.button("Start Game"):
    # Initialize session state for total scores
    st.session_state.total_scores = {name: 0 for name in player_names}

    # Initialize session state for scores table
    jokers_given_cols = [f"Jokers Given ({name})" for name in player_names]
    jokers_received_cols = [f"Jokers Received ({name})" for name in player_names]
    jokers_gained_cols = [f"Jokers Gained ({name})" for name in player_names]


    st.session_state.scores = pd.DataFrame(columns=[
        "Round", *player_names
        #, *jokers_given_cols, *jokers_received_cols, *jokers_gained_cols
    ])

    # Initialize round number
    st.session_state.round_number = 1

    # Display a message to indicate the game has started
    st.sidebar.success("Game has started! You can now begin adding rounds.")

# Function to reset inputs
def reset_inputs():
    st.session_state.winner = None
    st.session_state.hand_points = [0, 0, 0, 0]
    st.session_state.jokers_received = [0, 0, 0, 0]
    st.session_state.jokers_won = [0, 0, 0, 0]
    st.session_state.jokers_gained = [0, 0, 0, 0]

# Initialize input fields
reset_inputs()

# Select the winner of the round
st.subheader("Select Round Winner")
winner = st.selectbox("Select the winner of this round", options=player_names)
winner_index = player_names.index(winner)
st.session_state.winner = winner

# Enter points and jokers for each player
st.subheader("Enter Points and Jokers")
hand_points = []
jokers_received = []
jokers_gained = []
jokers_given = [0, 0, 0, 0]

columns = st.columns(4)

# Input fields per player in a single row
for i, player in enumerate(player_names):
    with columns[i]:
        st.markdown(f"### {player}")
        if i == winner_index:
            jokers_won = st.number_input(f"قداه فضلت", min_value=0, value=0, step=1, key=f"jokers_won_{i}")
            jokers_given[i] = jokers_won
            jokers_start = st.number_input(f"قداه نكت من جوك",min_value=0, value=0, step=1, key=f"jokers_gained_{i}")
            jokers_gained.append(jokers_start)
            st.session_state.jokers_won[i] = jokers_won
            hand_points.append(0)  # No hand points for the winner
            jokers_received.append(0)  # No jokers received for the winner
        else:
            points = st.number_input("قداه في كفك", min_value=0, value=0, step=100, key=f"hand_points_{i}")
            jokers = st.number_input("قداه كليت على راسك", min_value=0, value=0, step=1, key=f"jokers_received_{i}")
            jokers_start = st.number_input(f"قداه نكت من جوك",min_value=0, value=0, step=1, key=f"jokers_gained_{i}")
            jokers_gained.append(jokers_start)
            hand_points.append(points)
            jokers_received.append(jokers)

# Button to submit the round
if st.button("Submit Round"):
    # Calculate points for each player and update the total scores
    round_scores = []
    jokers_data_gained = []
    jokers_data_given = []
    jokers_data_received = []

    for i, player in enumerate(player_names):
        if i == winner_index:
            round_scores.append(st.session_state.total_scores[player])  # Winner's score remains the same
            jokers_data_given.append(jokers_given[i])
            jokers_data_received.append(0)
            jokers_data_gained.append(jokers_gained[i])
        else:
            score = hand_points[i] + jokers_received[i] * 50
            st.session_state.total_scores[player] += score
            round_scores.append(st.session_state.total_scores[player])
            jokers_data_given.append(0)
            jokers_data_gained.append(jokers_gained[i])
            jokers_data_received.append(jokers_received[i])

    # Add round score to dataframe with jokers tracking
    new_round_data = {
        "Round": st.session_state.round_number,
        player_names[0]: round_scores[0],
        player_names[1]: round_scores[1],
        player_names[2]: round_scores[2],
        player_names[3]: round_scores[3],
    }
    tafdhil_round_data = {
        f"Jokers Given ({player_names[0]})": jokers_data_given[0],
        f"Jokers Given ({player_names[1]})": jokers_data_given[1],
        f"Jokers Given ({player_names[2]})": jokers_data_given[2],
        f"Jokers Given ({player_names[3]})": jokers_data_given[3],
    }
    sheet_round_data = {
        "Round": st.session_state.round_number,
        player_names[0]: round_scores[0],
        player_names[1]: round_scores[1],
        player_names[2]: round_scores[2],
        player_names[3]: round_scores[3],
        f"Jokers Gained ({player_names[0]})": jokers_data_gained[0],
        f"Jokers Gained ({player_names[1]})": jokers_data_gained[1],
        f"Jokers Gained ({player_names[2]})": jokers_data_gained[2],
        f"Jokers Gained ({player_names[3]})": jokers_data_gained[3],
        f"Jokers Given ({player_names[0]})": jokers_data_given[0],
        f"Jokers Given ({player_names[1]})": jokers_data_given[1],
        f"Jokers Given ({player_names[2]})": jokers_data_given[2],
        f"Jokers Given ({player_names[3]})": jokers_data_given[3],
        f"Jokers Received ({player_names[0]})": jokers_data_received[0],
        f"Jokers Received ({player_names[1]})": jokers_data_received[1],
        f"Jokers Received ({player_names[2]})": jokers_data_received[2],
        f"Jokers Received ({player_names[3]})": jokers_data_received[3],
    }

    st.session_state.scores = pd.concat(
        [st.session_state.scores, pd.DataFrame([new_round_data])]
    ).reset_index(drop=True)

    st.success(f"Round {st.session_state.round_number} submitted successfully!")
    st.session_state.round_number += 1  # Increment round number

    # Reset input fields for the next round
    reset_inputs()

# Display score table
st.subheader("Score Tracker")
styled_df = st.session_state.scores.style.set_properties(**{
    'background-color': 'lightgray',
    'border': '1px solid black',
    'color': 'black',
    'text-align': 'center',
})
st.table(styled_df)

# Display final scores
st.subheader("Total Scores")
st.write(st.session_state.total_scores)
