import streamlit as st
import pandas as pd
from pycaret.regression import load_model

# Load trained model
model = load_model("fpl_points_predictor3")

# Load dataset
df = pd.read_csv("final_fpl_data.csv")

# Initialize session state for selected players
if "selected_players" not in st.session_state:
    st.session_state.selected_players = []

if "team_count" not in st.session_state:
    st.session_state.team_count = {}

if "position_count" not in st.session_state:
    st.session_state.position_count = {"Goalkeeper": 2, "Defender": 5, "Midfielder": 5, "Forward": 3}

# Define position limits globally
position_limits = {"Goalkeeper": 2, "Defender": 5, "Midfielder": 5, "Forward": 3}

# Background Image Function
def add_bg_image(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRbnp591URYNq3268wZ5LtNeX7Xr_uxs8EEZ53NlGs3nlzNFRr6JBvpjKc4Zcj3oOq5Wxg&usqp=CAU")

# Function to remove a player
def remove_player(player_name):
    # Find the player in selected_players
    for i, player in enumerate(st.session_state.selected_players):
        if player["Name"] == player_name:
            # Update team count
            team = player["Team"]
            st.session_state.team_count[team] -= 1
            if st.session_state.team_count[team] == 0:
                del st.session_state.team_count[team]
            
            # Update position count
            position = player["Position"]
            st.session_state.position_count[position] += 1
            
            # Remove the player
            del st.session_state.selected_players[i]
            st.success(f"Removed {player_name} from your squad!")
            return True
    return False

# UI Layout
st.title("Fantasy Premier League - Best Player Predictor")

# Use Tabs for better organization
tab1, tab2 = st.tabs(["Player Selection", "Selected Squad"])

with tab1:
    st.header("Player Selection")
    position = st.selectbox("Select Position", df["Position"].unique())
    teams = st.multiselect("Select Team(s)", df["Team"].unique())
    
    # Price Range with Slider and Input Boxes
    min_price, max_price = st.slider("Select Price Range", float(df["Current Price"].min()), float(df["Current Price"].max()), (float(df["Current Price"].min()), float(df["Current Price"].max())))
    col1, col2 = st.columns(2)
    min_price = col1.number_input("Min Price", min_value=float(df["Current Price"].min()), value=min_price)
    max_price = col2.number_input("Max Price", max_value=float(df["Current Price"].max()), value=max_price)
    
    price_range = (min_price, max_price)
    
    # Filter dataset
    filtered_df = df[(df["Position"] == position) & (df["Team"].isin(teams)) & (df["Current Price"].between(price_range[0], price_range[1]))]
    
    if not filtered_df.empty:
        feature_columns = ["Event Points", "Points Per Game", "Total Points", "BPS", "Bonus", "Team", "Minutes", "Selected By Percent", "Influence", "Goals per 90", "Goals Conceded per 90", "Current Price", "Chance Of Playing"]
        X = filtered_df[feature_columns]
        filtered_df["EP Next"] = model.predict(X)
        
        # Display table of filtered players
        st.dataframe(
            filtered_df[["Name", "Team", "Position", "Current Price", "EP Next"]].sort_values(by="EP Next", ascending=False),
            use_container_width=True,
            height=400
        )
        
        # Create a selectbox for player selection
        selected_player_name = st.selectbox(
            "Select a player to add to your squad",
            filtered_df["Name"].sort_values(),
            index=None,
            placeholder="Choose a player..."
        )
        
        if selected_player_name and st.button(f"Add {selected_player_name}"):
            player_info = df[df["Name"] == selected_player_name].iloc[0]
            player_team = player_info["Team"]
            player_position = player_info["Position"]
            
            if player_team not in st.session_state.team_count:
                st.session_state.team_count[player_team] = 0
            
            if st.session_state.team_count[player_team] < 3:
                if len(st.session_state.selected_players) < 15:
                    if st.session_state.position_count[player_position] > 0:
                        st.session_state.selected_players.append({
                            "Name": player_info["Name"],
                            "Position": player_info["Position"],
                            "Team": player_info["Team"],
                            "Price": player_info["Current Price"],
                            "EP Next": model.predict(pd.DataFrame([player_info[feature_columns]]))[0]
                        })
                        st.session_state.team_count[player_team] += 1
                        st.session_state.position_count[player_position] -= 1
                        st.success(f"{selected_player_name} added successfully!")
                    else:
                        st.warning(f"No more slots available for {player_position}.")
                else:
                    st.warning("You can only select up to 15 players.")
            else:
                st.warning(f"You can only select up to 3 players from {player_team}.")

with tab2:
    st.header("Selected Squad")
    if st.session_state.selected_players:
        selected_df = pd.DataFrame(st.session_state.selected_players)
        
        # Display the squad with remove buttons
        for i, player in enumerate(st.session_state.selected_players):
            col1, col2, col3, col4, col5 = st.columns([4, 2, 2, 2, 2])
            col1.write(f"**{player['Name']}**")
            col2.write(player['Position'])
            col3.write(player['Team'])
            col4.write(f"£{player['Price']}")
            col5.write(f"{player['EP Next']:.1f}")
            
            # Add remove button for each player
            if col5.button("Remove", key=f"remove_{i}"):
                remove_player(player['Name'])
                st.rerun()  # Changed from st.experimental_rerun() to st.rerun()
        
        st.markdown("---")
        
        # Display summary information
        st.subheader("Team Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Players", len(st.session_state.selected_players))
        col2.metric("Total Cost", f"£{selected_df['Price'].sum():.1f}")
        col3.metric("Expected Points", f"{selected_df['EP Next'].sum():.1f}")
        
        # Display position counts
        st.subheader("Position Counts")
        pos_counts = selected_df['Position'].value_counts().to_dict()
        for position, count in pos_counts.items():
            st.write(f"{position}: {count}/{position_limits.get(position, 0)}")
            
        # Display team counts
        st.subheader("Team Counts")
        team_counts = selected_df['Team'].value_counts().to_dict()
        for team, count in team_counts.items():
            st.write(f"{team}: {count}/3")
    else:
        st.write("No players selected yet.")
    
    if st.button("Reset Selection"):
        st.session_state.selected_players = []
        st.session_state.team_count = {}
        st.session_state.position_count = {"Goalkeeper": 2, "Defender": 5, "Midfielder": 5, "Forward": 3}
        st.success("Selection reset!")
