import streamlit as st
import pandas as pd
from itertools import combinations
import random
import json
import pymongo

# Page configuration
st.set_page_config(
    page_title="Group Stage Generator",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🏆"
)

# Custom CSS for modern, vibrant styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&family=Inter:wght@300;400;500;600&display=swap');
    
    /* Main background with gradient */
    .stApp {
        background: linear-gradient(180deg, #2c3e7a 0%, #1a2456 50%, #0f1736 100%);
    }
    
    /* Glassmorphism container */
    .main .block-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2c4080 0%, #1e2d5f 100%);
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stSidebar"] label {
        color: white !important;
    }
    
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: white !important;
    }
    
    /* Sidebar input - nuclear option with specific Streamlit classes */
    [data-testid="stSidebar"] input {
        color: white !important;
        -webkit-text-fill-color: white !important;
    }
    
    /* Override Streamlit's default input styling */
    [data-testid="stSidebar"] .stTextInput input,
    [data-testid="stSidebar"] .stNumberInput input {
        color: white !important;
        -webkit-text-fill-color: white !important;
        filter: brightness(1) !important;
    }
    
    /* Add text shadow for extra visibility */
    [data-testid="stSidebar"] input {
        text-shadow: 0 0 1px rgba(255, 255, 255, 0.5) !important;
    }
    
    /* Title styling */
    h1 {
        font-family: 'Montserrat', sans-serif;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem !important;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        letter-spacing: -1px;
    }
    
    /* Headers */
    h2, h3 {
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Info box styling */
    .stAlert {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 15px;
        color: white;
        font-family: 'Inter', sans-serif;
    }
    
    /* Custom standings table */
    .standings-table {
        width: 100%;
        background: linear-gradient(135deg, rgba(45, 70, 130, 0.6) 0%, rgba(30, 50, 100, 0.6) 100%);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.15);
        overflow: hidden;
    }
    
    .standings-row {
        display: grid;
        grid-template-columns: 60px 2fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr;
        gap: 10px;
        padding: 12px 20px;
        align-items: center;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .standings-row:hover {
        background: rgba(61, 90, 254, 0.2);
        transform: translateX(5px);
    }
    
    .standings-header {
        display: grid;
        grid-template-columns: 60px 2fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr;
        gap: 10px;
        padding: 15px 20px;
        background: rgba(61, 90, 254, 0.4);
        border-radius: 10px;
        margin-bottom: 10px;
        font-weight: 700;
        font-family: 'Montserrat', sans-serif;
        font-size: 0.9rem;
        color: white;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .standings-cell {
        color: white;
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        text-align: center;
    }
    
    .standings-cell.player-name {
        text-align: left;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    .standings-cell.position {
        font-weight: 700;
        font-size: 1.2rem;
        font-family: 'Montserrat', sans-serif;
    }
    
    .standings-cell.points {
        font-weight: 700;
        color: #5a7dff;
        font-size: 1.1rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #3d5afe 0%, #2948c6 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        font-family: 'Montserrat', sans-serif;
        box-shadow: 0 4px 15px rgba(61, 90, 254, 0.4);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(61, 90, 254, 0.6);
    }
    
    .stButton > button:active {
        transform: translateY(0px);
    }
    
    /* Primary button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #5a7dff 0%, #3d5afe 100%);
        box-shadow: 0 4px 15px rgba(90, 125, 255, 0.4);
    }
    
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 20px rgba(90, 125, 255, 0.6);
    }
    
    /* Secondary button */
    .stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, #4a6fa5 0%, #2c4a7c 100%);
        box-shadow: 0 4px 15px rgba(74, 111, 165, 0.4);
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 10px;
        color: white !important;
        font-family: 'Inter', sans-serif;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.6);
    }
    
    /* Sidebar text inputs */
    [data-testid="stSidebar"] .stTextInput > div > div > input,
    [data-testid="stSidebar"] .stNumberInput > div > div > input {
        background: rgba(255, 255, 255, 0.2);
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stTextInput input {
        color: white !important;
        -webkit-text-fill-color: white !important;
    }
    
    [data-testid="stSidebar"] .stNumberInput input {
        color: white !important;
        -webkit-text-fill-color: white !important;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        color: white;
        font-weight: 600;
        font-family: 'Montserrat', sans-serif;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        font-family: 'Montserrat', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: white;
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.9);
    }
    
    /* Match card styling */
    .match-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Team name styling */
    .team-name {
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
        font-size: 1.1rem;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Separator styling */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        margin: 2rem 0;
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        border: none;
        border-radius: 25px;
        font-weight: 600;
        font-family: 'Montserrat', sans-serif;
        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.4);
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 15px;
        padding: 1rem;
        border: 2px dashed rgba(255, 255, 255, 0.3);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Trophy icon animation */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .trophy-icon {
        animation: float 3s ease-in-out infinite;
        display: inline-block;
    }
    
    /* Pulse animation for metrics */
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    [data-testid="stMetricValue"] {
        animation: pulse 2s ease-in-out infinite;
    }
    
    /* Card hover effect */
    .stDataFrame:hover {
        transform: translateY(-5px);
        transition: transform 0.3s ease;
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.5);
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    # Try to load from query params first (for page refresh persistence)
    query_params = st.query_params
    
    if 'tournament_data' in query_params:
        try:
            data = json.loads(query_params['tournament_data'])
            st.session_state.players = data.get('players', [])
            st.session_state.matches = data.get('matches', [])
            st.session_state.tournament_generated = data.get('tournament_generated', False)
            st.session_state.rounds = data.get('rounds', 1)
            st.session_state.selected_players = data.get('selected_players', [])
        except:
            pass
    
    # Initialize defaults if not already set
    if 'players' not in st.session_state:
        st.session_state.players = []
    if 'matches' not in st.session_state:
        st.session_state.matches = []
    if 'tournament_generated' not in st.session_state:
        st.session_state.tournament_generated = False
    if 'rounds' not in st.session_state:
        st.session_state.rounds = 1
    if 'selected_players' not in st.session_state:
        st.session_state.selected_players = []

def save_to_query_params():
    """Save tournament state to query params for persistence across refreshes"""
    data = {
        'players': st.session_state.players,
        'matches': st.session_state.matches,
        'tournament_generated': st.session_state.tournament_generated,
        'rounds': st.session_state.rounds,
        'selected_players': st.session_state.selected_players
    }
    st.query_params['tournament_data'] = json.dumps(data)

# MongoDB connection
@st.cache_resource
def init_connection():
    try:
        client = pymongo.MongoClient(st.secrets["mongo"]["connection_string"])
        # Access the tournamentDB database
        return client["tournamentDB"]
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

def get_player_elo(player_name):
    """Get current ELO of a player from database"""
    db = init_connection()
    if db is None:
        return 500  # Default ELO if no connection
    
    try:
        collection_names = ['players', 'player', 'elos', 'elo_rankings']
        
        for collection_name in collection_names:
            try:
                collection = db[collection_name]
                player_data = collection.find_one({'player': player_name})
                if player_data and 'ELO' in player_data:
                    return player_data['ELO']
            except:
                continue
        return 500  # Default ELO if player not found
    except:
        return 500

def update_player_elo(player_name, new_elo):
    """Update player's ELO in database"""
    db = init_connection()
    if db is None:
        return False
    
    try:
        collection_names = ['players', 'player', 'elos', 'elo_rankings']
        
        for collection_name in collection_names:
            try:
                collection = db[collection_name]
                result = collection.update_one(
                    {'player': player_name},
                    {'$set': {'ELO': new_elo}},
                    upsert=True  # Create if doesn't exist
                )
                return result.modified_count > 0 or result.upserted_id is not None
            except:
                continue
        return False
    except:
        return False

def calculate_elo_change(player1_elo, player2_elo, score1, score2, k_factor=32):
    """
    Calculate ELO changes after a match
    score1 and score2 are the actual scores
    Returns: (new_elo1, new_elo2, change1, change2)
    """
    # Calculate expected scores
    expected1 = 1 / (1 + 10 ** ((player2_elo - player1_elo) / 400))
    expected2 = 1 / (1 + 10 ** ((player1_elo - player2_elo) / 400))
    
    # Determine actual scores based on match result
    if score1 > score2:
        actual1, actual2 = 1, 0  # Player 1 wins
    elif score2 > score1:
        actual1, actual2 = 0, 1  # Player 2 wins
    else:
        actual1, actual2 = 0.5, 0.5  # Draw
    
    # Calculate ELO changes
    change1 = k_factor * (actual1 - expected1)
    change2 = k_factor * (actual2 - expected2)
    
    # Calculate new ELOs
    new_elo1 = player1_elo + change1
    new_elo2 = player2_elo + change2
    
    return round(new_elo1), round(new_elo2), round(change1), round(change2)

def update_match_with_elo(match, score1, score2):
    """Update match and calculate ELO changes"""
    # Get current ELOs
    player1_elo = get_player_elo(match['player1'])
    player2_elo = get_player_elo(match['player2'])
    
    # Calculate new ELOs
    new_elo1, new_elo2, change1, change2 = calculate_elo_change(
        player1_elo, player2_elo, score1, score2
    )
    
    # Update database
    update_player_elo(match['player1'], new_elo1)
    update_player_elo(match['player2'], new_elo2)
    
    # Return ELO change information
    return {
        'player1_elo_change': change1,
        'player2_elo_change': change2,
        'player1_new_elo': new_elo1,
        'player2_new_elo': new_elo2
    }

def get_elo_rankings():
    """Fetch ELO rankings from MongoDB"""
    db = init_connection()
    if db is None:
        return None
    
    try:
        # Try different possible collection names within tournamentDB
        collection_names = ['players', 'player', 'elos', 'elo_rankings', 'rankings', 'tournamentDB']
        
        for collection_name in collection_names:
            try:
                collection = db[collection_name]
                # Get all documents
                players_data = list(collection.find({}, {'_id': 0}))
                
                if players_data:
                    # Normalize field names - try common variations
                    normalized_data = []
                    for doc in players_data:
                        normalized_doc = {}
                        
                        # Handle player name field - check all possible field names
                        player_name = None
                        for field in ['player', 'name', 'username', 'Player', 'Name']:
                            if field in doc and doc[field]:
                                player_name = doc[field]
                                break
                        
                        if not player_name:
                            continue  # Skip if no player name found
                        
                        # Handle ELO field - check all possible field names
                        elo_value = None
                        for field in ['ELO', 'elo', 'rating', 'Rating', 'score', 'points']:
                            if field in doc and doc[field] is not None:
                                try:
                                    elo_value = int(doc[field])
                                    break
                                except (ValueError, TypeError):
                                    continue
                        
                        if elo_value is None:
                            continue  # Skip if no ELO field found or can't convert to int
                        
                        normalized_doc['player'] = player_name
                        normalized_doc['ELO'] = elo_value
                        normalized_data.append(normalized_doc)
                    
                    if normalized_data:
                        # Convert to DataFrame and sort by ELO (descending)
                        df = pd.DataFrame(normalized_data)
                        df = df.sort_values('ELO', ascending=False)
                        df = df.reset_index(drop=True)
                        df.index = df.index + 1  # Start positions from 1
                        return df
                        
            except Exception as e:
                continue
        
        return None
        
    except Exception as e:
        return None

def round_robin_schedule(players, rounds):
    """
    Generate a balanced round-robin schedule using the circle method.
    This ensures fair distribution of matches across all rounds.
    """
    n = len(players)
    matches = []
    match_id = 1
    
    # If odd number of players, add a "bye"
    if n % 2 == 1:
        players_with_bye = players + ["BYE"]
        n = len(players_with_bye)
    else:
        players_with_bye = players.copy()
    
    # Circle method for round-robin
    for round_num in range(rounds):
        # Create a list for rotation (keep first player fixed)
        rotation_list = players_with_bye.copy()
        
        # For each matchday in a complete round-robin
        for matchday in range(n - 1):
            round_matches = []
            
            # Generate matches for this matchday
            for i in range(n // 2):
                player1 = rotation_list[i]
                player2 = rotation_list[n - 1 - i]
                
                # Skip if either player is BYE
                if player1 != "BYE" and player2 != "BYE":
                    # Alternate home/away for different rounds
                    if round_num % 2 == 1 and matchday % 2 == 0:
                        player1, player2 = player2, player1
                    
                    round_matches.append({
                        'match_id': match_id,
                        'round': round_num + 1,
                        'matchday': matchday + 1,
                        'player1': player1,
                        'player2': player2,
                        'score1': None,
                        'score2': None,
                        'completed': False,
                        'elo_updated': False  # Track if ELO has been updated for this match
                    })
                    match_id += 1
            
            # Shuffle matches within matchday to distribute evenly
            random.shuffle(round_matches)
            matches.extend(round_matches)
            
            # Rotate players (keep first fixed, rotate others)
            rotation_list = [rotation_list[0]] + [rotation_list[-1]] + rotation_list[1:-1]
    
    return matches

# Initialize session state
init_session_state()

# Force sidebar input visibility - copy from working match inputs
st.sidebar.markdown("""
<style>
    /* Apply same styling as match score inputs which DO work */
    [data-testid="stSidebar"] .stTextInput > div > div > input,
    [data-testid="stSidebar"] .stNumberInput > div > div > input {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Also target the increment/decrement buttons container */
    [data-testid="stSidebar"] .stNumberInput > div > div {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 10px !important;
    }
    
    /* Style the +/- buttons */
    [data-testid="stSidebar"] .stNumberInput button {
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown('<h2 style="text-align: center;">Tournament Setup</h2>', unsafe_allow_html=True)
st.sidebar.markdown("---")

# Initialize session state for selected players
if 'selected_players' not in st.session_state:
    st.session_state.selected_players = []

def get_all_players_from_db():
    """Get all players from database for dropdown"""
    db = init_connection()
    if db is None:
        return []
    
    try:
        # Try different collection names
        collection_names = ['players', 'player', 'elos', 'elo_rankings', 'rankings', 'tournamentDB']
        
        for collection_name in collection_names:
            try:
                collection = db[collection_name]
                players_data = list(collection.find({}, {'_id': 0}))
                
                if players_data:
                    players = []
                    for doc in players_data:
                        # Extract player name
                        player_name = None
                        for field in ['player', 'name', 'username', 'Player', 'Name']:
                            if field in doc and doc[field]:
                                player_name = doc[field]
                                break
                        
                        # Extract ELO
                        elo_value = 500  # default
                        for field in ['ELO', 'elo', 'rating', 'Rating', 'score', 'points']:
                            if field in doc and doc[field] is not None:
                                try:
                                    elo_value = int(doc[field])
                                    break
                                except (ValueError, TypeError):
                                    continue
                        
                        if player_name:
                            players.append({
                                'name': player_name,
                                'elo': elo_value
                            })
                    
                    return players
            except:
                continue
        return []
    except:
        return []

def add_player_to_db(player_name, elo=500):
    """Add a new player to the database"""
    db = init_connection()
    if db is None:
        return False
    
    try:
        # Try different collection names
        collection_names = ['players', 'player', 'elos', 'elo_rankings']
        
        for collection_name in collection_names:
            try:
                collection = db[collection_name]
                # Check if player already exists
                existing = collection.find_one({'player': player_name})
                if not existing:
                    collection.insert_one({
                        'player': player_name,
                        'ELO': elo
                    })
                    return True
                else:
                    return False  # Player already exists
            except:
                continue
        return False
    except:
        return False

st.sidebar.markdown('<h3 style="text-align: center;">👥 Select Players</h3>', unsafe_allow_html=True)

# Get all available players from database
all_players = get_all_players_from_db()
available_players = [p for p in all_players if p['name'] not in [sp['name'] for sp in st.session_state.selected_players]]

# Player selection dropdown
if available_players:
    # Create formatted options for dropdown
    dropdown_options = [f"{p['name']} ({p['elo']})" for p in available_players]
    dropdown_options.insert(0, "Select a player...")
    
    selected_option = st.sidebar.selectbox(
        "Choose from database",
        options=dropdown_options,
        key="player_dropdown"
    )
    
    # Add selected player to tournament
    if selected_option and selected_option != "Select a player...":
        selected_index = dropdown_options.index(selected_option) - 1  # -1 because of the placeholder
        if selected_index >= 0 and selected_index < len(available_players):
            selected_player = available_players[selected_index]
            if selected_player not in st.session_state.selected_players:
                st.session_state.selected_players.append(selected_player)
                st.session_state.tournament_generated = False
                st.rerun()

# Display selected players with remove buttons
st.sidebar.markdown("### Selected Players")
if st.session_state.selected_players:
    for i, player in enumerate(st.session_state.selected_players):
        col1, col2 = st.sidebar.columns([3, 1])
        with col1:
            st.sidebar.markdown(
                f'<div style="background: rgba(255,255,255,0.1); padding: 8px 12px; border-radius: 8px; margin: 5px 0; border: 1px solid rgba(255,255,255,0.2);">'
                f'<span style="font-weight: 600; color: white;">{player["name"]}</span> '
                f'<span style="color: #5a7dff; font-size: 0.9em;">({player["elo"]})</span>'
                f'</div>',
                unsafe_allow_html=True
            )
        with col2:
            if st.sidebar.button("🗑️", key=f"remove_{i}", help="Remove player"):
                st.session_state.selected_players.pop(i)
                st.session_state.tournament_generated = False
                st.rerun()

# Add new player section
st.sidebar.markdown("---")
st.sidebar.markdown('<h3 style="text-align: center;">➕ Add New Player</h3>', unsafe_allow_html=True)

new_player_name = st.sidebar.text_input(
    "Player Name",
    placeholder="Enter new player name...",
    key="new_player_input"
)

new_player_elo = 500
st.sidebar.markdown("<br>", unsafe_allow_html=True)
add_button = st.sidebar.button("Add Player", type="secondary", use_container_width=True)

if add_button and new_player_name.strip():
    # Check if player already exists in database
    existing_names = [p['name'] for p in all_players]
    if new_player_name.strip() in existing_names:
        st.sidebar.error("Player already exists in database!")
    else:
        # Add to database
        if add_player_to_db(new_player_name.strip(), new_player_elo):
            # Also add to selected players
            new_player = {'name': new_player_name.strip(), 'elo': new_player_elo}
            if new_player not in st.session_state.selected_players:
                st.session_state.selected_players.append(new_player)
                st.session_state.tournament_generated = False
                st.sidebar.success(f"Added {new_player_name.strip()}!")
                st.rerun()
        else:
            st.sidebar.error("Failed to add player to database")

st.sidebar.markdown("---")

# Rounds selection
st.sidebar.markdown('<h3 style="text-align: center;">🔄 Tournament Rounds</h3>', unsafe_allow_html=True)
rounds_str = st.sidebar.text_input(
    "Rounds (matches per pair)",
    value=str(st.session_state.rounds),
    key="rounds_input",
    help="Number of times each player plays against each other player"
)

# Convert to integer and validate
try:
    rounds = int(rounds_str)
    if rounds < 1:
        rounds = 1
        st.sidebar.warning("Minimum 1 round required")
    elif rounds > 5:
        rounds = 5
        st.sidebar.warning("Maximum 5 rounds allowed")
except ValueError:
    rounds = st.session_state.rounds
    st.sidebar.error("Please enter a valid number")

if rounds != st.session_state.rounds:
    st.session_state.rounds = rounds
    st.session_state.tournament_generated = False

st.sidebar.markdown("---")

# Generate tournament button
if st.sidebar.button("🏆 Generate Tournament", type="primary", use_container_width=True):
    if len(st.session_state.selected_players) < 2:
        st.sidebar.error("⚠️ At least 2 players required!")
    else:
        # Extract just the player names for tournament generation
        player_names = [player['name'] for player in st.session_state.selected_players]
        st.session_state.players = player_names
        
        # Generate matches using round-robin scheduling
        st.session_state.matches = round_robin_schedule(player_names, rounds)
        st.session_state.tournament_generated = True
        
        # Save to query params for persistence
        save_to_query_params()
        st.rerun()

# Reset button
if st.sidebar.button("🔄 Reset Tournament", use_container_width=True):
    st.session_state.selected_players = []
    st.session_state.matches = []
    st.session_state.tournament_generated = False
    st.query_params.clear()
    st.rerun()

# Export/Import functionality
if st.session_state.tournament_generated:
    st.sidebar.markdown("---")
    st.sidebar.markdown('<h3 style="text-align: center;">💾 Save/Load</h3>', unsafe_allow_html=True)
    
    # Export tournament data
    export_data = {
        'players': st.session_state.players,
        'matches': st.session_state.matches,
        'rounds': st.session_state.rounds,
        'selected_players': st.session_state.selected_players
    }
    
    st.sidebar.download_button(
        label="📥 Download Tournament",
        data=json.dumps(export_data, indent=2),
        file_name="tournament_data.json",
        mime="application/json",
        help="Download tournament data to restore later",
        use_container_width=True
    )
    
    # Import tournament data
    uploaded_file = st.sidebar.file_uploader("📤 Upload Tournament", type=['json'])
    if uploaded_file is not None:
        try:
            import_data = json.load(uploaded_file)
            st.session_state.players = import_data['players']
            st.session_state.matches = import_data['matches']
            st.session_state.rounds = import_data['rounds']
            st.session_state.selected_players = import_data.get('selected_players', [])
            st.session_state.tournament_generated = True
            save_to_query_params()
            st.sidebar.success("✅ Tournament loaded!")
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"❌ Error loading file: {str(e)}")

# Main content with tabs
tab1, tab2 = st.tabs(["🏆 Tournament", "📈 ELO Rankings"])

with tab1:
    with tab1:
    if not st.session_state.tournament_generated:
        st.info("👈 Configure your tournament in the sidebar and click 'Generate Tournament' to start!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="how-to-use-section">
            <h3>🎯 How to use:</h3>
            <ol>
            <li><strong>Select players</strong> - Choose from database or add new ones</li>
            <li><strong>Set rounds</strong> - Decide how many times each pair plays</li>
            <li><strong>Generate!</strong> - Click the button to create your tournament</li>
            <li><strong>Enter scores</strong> - Update results as matches are played</li>
            <li><strong>Track standings</strong> - Watch the leaderboard update in real-time</li>
            <li><strong>ELO updates</strong> - Player ratings automatically adjust after matches</li>
            </ol>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="how-to-use-section">
            <h3>💡 Features:</h3>
            <ul>
            <li><strong>Smart Scheduling</strong> - Uses official round-robin algorithm</li>
            <li><strong>Auto ELO Updates</strong> - Ratings adjust automatically after matches</li>
            <li><strong>Real-time Rankings</strong> - ELO rankings update instantly</li>
            <li><strong>Database Integration</strong> - All data stored in MongoDB</li>
            <li><strong>Export/Import</strong> - Download and restore tournaments</li>
            <li><strong>Fair Distribution</strong> - Balanced match scheduling</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
    else:
        # Calculate standings
        def calculate_standings():
            standings = {player: {
                'played': 0,
                'won': 0,
                'drawn': 0,
                'lost': 0,
                'gf': 0,  # goals for
                'ga': 0,  # goals against
                'gd': 0,  # goal difference
                'points': 0
            } for player in st.session_state.players}
            
            for match in st.session_state.matches:
                if match['completed']:
                    p1, p2 = match['player1'], match['player2']
                    s1, s2 = match['score1'], match['score2']
                    
                    standings[p1]['played'] += 1
                    standings[p2]['played'] += 1
                    standings[p1]['gf'] += s1
                    standings[p2]['gf'] += s2
                    standings[p1]['ga'] += s2
                    standings[p2]['ga'] += s1
                    
                    if s1 > s2:
                        standings[p1]['won'] += 1
                        standings[p1]['points'] += 3
                        standings[p2]['lost'] += 1
                    elif s2 > s1:
                        standings[p2]['won'] += 1
                        standings[p2]['points'] += 3
                        standings[p1]['lost'] += 1
                    else:
                        standings[p1]['drawn'] += 1
                        standings[p2]['drawn'] += 1
                        standings[p1]['points'] += 1
                        standings[p2]['points'] += 1
            
            # Calculate goal difference
            for player in standings:
                standings[player]['gd'] = standings[player]['gf'] - standings[player]['ga']
            
            return standings
        
        standings = calculate_standings()
        
        # Convert to DataFrame and sort
        standings_df = pd.DataFrame(standings).T
        standings_df = standings_df.sort_values(
            by=['points', 'gd', 'gf'],
            ascending=[False, False, False]
        )
        standings_df.index.name = 'Player'
        standings_df = standings_df.reset_index()
        standings_df.insert(0, 'Pos', range(1, len(standings_df) + 1))
        
        # Rename columns for display
        standings_df.columns = ['Pos', 'Player', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']
        
        # Display standings
        st.markdown('<h2 style="text-align: center;">📊 Live Standings</h2>', unsafe_allow_html=True)
        
        # Create custom HTML table
        standings_html = '<div class="standings-table">'
        
        # Header
        standings_html += '''
        <div class="standings-header">
            <div class="standings-cell">Pos</div>
            <div class="standings-cell">Player</div>
            <div class="standings-cell">P</div>
            <div class="standings-cell">W</div>
            <div class="standings-cell">D</div>
            <div class="standings-cell">L</div>
            <div class="standings-cell">GF</div>
            <div class="standings-cell">GA</div>
            <div class="standings-cell">GD</div>
            <div class="standings-cell">Pts</div>
        </div>
        '''
        
        # Rows
        for idx, row in standings_df.iterrows():
            standings_html += '<div class="standings-row">'
            standings_html += f'<div class="standings-cell position">{row["Pos"]}</div>'
            standings_html += f'<div class="standings-cell player-name">{row["Player"]}</div>'
            standings_html += f'<div class="standings-cell">{row["P"]}</div>'
            standings_html += f'<div class="standings-cell">{row["W"]}</div>'
            standings_html += f'<div class="standings-cell">{row["D"]}</div>'
            standings_html += f'<div class="standings-cell">{row["L"]}</div>'
            standings_html += f'<div class="standings-cell">{row["GF"]}</div>'
            standings_html += f'<div class="standings-cell">{row["GA"]}</div>'
            standings_html += f'<div class="standings-cell">{row["GD"]}</div>'
            standings_html += f'<div class="standings-cell points">{row["Pts"]}</div>'
            standings_html += '</div>'
        
        standings_html += '</div>'
        
        st.markdown(standings_html, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Match schedule
        st.markdown('<h2 style="text-align: center;">📅 Match Schedule</h2>', unsafe_allow_html=True)
        
        # Group matches by round
        if st.session_state.rounds > 1:
            round_tabs = st.tabs([f"🔵 Round {i+1}" for i in range(st.session_state.rounds)])
        else:
            round_tabs = [st.container()]
        
        for round_num in range(st.session_state.rounds):
            with round_tabs[round_num]:
                round_matches = [m for m in st.session_state.matches if m['round'] == round_num + 1]
                
                for idx, match in enumerate(round_matches):
                    st.markdown('<div class="match-card">', unsafe_allow_html=True)
                    
                    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 2])
                    
                    with col1:
                        st.markdown(f'<p class="team-name" style="text-align: center;">{match["player1"]}</p>', unsafe_allow_html=True)
                    
                    with col2:
                        score1 = st.number_input(
                            "Score",
                            min_value=0,
                            max_value=99,
                            value=int(match['score1']) if match['score1'] is not None else 0,
                            key=f"score1_{match['match_id']}",
                            label_visibility="collapsed"
                        )
                    
                    with col3:
                        st.markdown("<div style='text-align: center; padding-top: 8px; color: white; font-weight: bold; font-size: 1.2rem;'>VS</div>", unsafe_allow_html=True)
                    
                    with col4:
                        score2 = st.number_input(
                            "Score",
                            min_value=0,
                            max_value=99,
                            value=int(match['score2']) if match['score2'] is not None else 0,
                            key=f"score2_{match['match_id']}",
                            label_visibility="collapsed"
                        )
                    
                    with col5:
                        st.markdown(f'<p class="team-name" style="text-align: center;">{match["player2"]}</p>', unsafe_allow_html=True)
                    
                    # Update button centered
                    col_empty1, col_button, col_empty2 = st.columns([2, 1, 2])
                    with col_button:
                        update_button = st.button(
                            "✅ Update" if not match['completed'] else "✓ Updated",
                            key=f"update_{match['match_id']}",
                            type="secondary" if match['completed'] else "primary",
                            use_container_width=True
                        )
                    
                    # Show ELO change info if match was completed and ELO was updated
                    if match['completed'] and match.get('elo_updated'):
                        st.info(f"""
                        **ELO Changes:**
                        - **{match['player1']}**: {match.get('player1_elo_change', 0):+d} (New ELO: {match.get('player1_new_elo', 0)})
                        - **{match['player2']}**: {match.get('player2_elo_change', 0):+d} (New ELO: {match.get('player2_new_elo', 0)})
                        """)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Handle match update
                    if update_button:
                        # Update match scores
                        for m in st.session_state.matches:
                            if m['match_id'] == match['match_id']:
                                m['score1'] = score1
                                m['score2'] = score2
                                
                                # Only update ELO if the match wasn't already completed
                                if not m['completed']:
                                    m['completed'] = True
                                    # Calculate and update ELO
                                    elo_info = update_match_with_elo(m, score1, score2)
                                    # Store ELO change information
                                    m.update(elo_info)
                                    m['elo_updated'] = True
                                    
                                    st.success("Match updated and ELO ratings adjusted!")
                                else:
                                    m['completed'] = True
                                    st.success("Match scores updated!")
                                break
                        
                        # Save to query params
                        save_to_query_params()
                        st.rerun()
                    
                    if idx < len(round_matches) - 1:
                        st.markdown("<br>", unsafe_allow_html=True)

with tab2:
    st.markdown('<h2 style="text-align: center;">📈 ELO Rankings</h2>', unsafe_allow_html=True)
    
    # Fetch ELO rankings from database
    elo_df = get_elo_rankings()
    
    if elo_df is not None and not elo_df.empty:
        # Create compact HTML table for ELO rankings
        elo_html = '''
        <div class="standings-table" style="max-width: 600px; margin: 0 auto;">
        '''
        
        # Header for ELO rankings - compact version
        elo_html += '''
        <div class="standings-header" style="grid-template-columns: 80px 1fr 100px;">
            <div class="standings-cell">Rank</div>
            <div class="standings-cell" style="text-align: center;">Player</div>
            <div class="standings-cell">ELO</div>
        </div>
        '''
        
        # Rows for ELO rankings - compact version
        for idx, row in elo_df.iterrows():
            elo_html += '<div class="standings-row" style="grid-template-columns: 80px 1fr 100px;">'
            elo_html += f'<div class="standings-cell position">{idx}</div>'
            elo_html += f'<div class="standings-cell player-name" style="text-align: center;">{row["player"]}</div>'
            elo_html += f'<div class="standings-cell points">{int(row["ELO"])}</div>'
            elo_html += '</div>'
        
        elo_html += '</div>'
        
        st.markdown(elo_html, unsafe_allow_html=True)
        
        # Add some statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Players", len(elo_df))
        
        with col2:
            highest_elo = int(elo_df['ELO'].max())
            st.metric("Highest ELO", highest_elo)
        
        with col3:
            avg_elo = int(elo_df['ELO'].mean())
            st.metric("Average ELO", avg_elo)
        
    else:
        st.warning("No ELO data found in the database. Please check your database connection and data.")
