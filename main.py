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

# Initialize session state with query params for persistence
def init_session_state():
    # Try to load from query params first (for page refresh persistence)
    query_params = st.query_params
    
    if 'tournament_data' in query_params:
        try:
            data = json.loads(query_params['tournament_data'])
            st.session_state.players = data.get('players', [])
            st.session_state.matches = data.get('matches', [])
            st.session_state.tournament_generated = data.get('tournament_generated', False)
            st.session_state.num_players = data.get('num_players', 4)
            st.session_state.rounds = data.get('rounds', 1)
        except:
            pass
    
    # Initialize defaults if not already set
    if 'players' not in st.session_state:
        st.session_state.players = []
    if 'matches' not in st.session_state:
        st.session_state.matches = []
    if 'tournament_generated' not in st.session_state:
        st.session_state.tournament_generated = False
    if 'num_players' not in st.session_state:
        st.session_state.num_players = 4
    if 'rounds' not in st.session_state:
        st.session_state.rounds = 1

def save_to_query_params():
    """Save tournament state to query params for persistence across refreshes"""
    data = {
        'players': st.session_state.players,
        'matches': st.session_state.matches,
        'tournament_generated': st.session_state.tournament_generated,
        'num_players': st.session_state.num_players,
        'rounds': st.session_state.rounds
    }
    st.query_params['tournament_data'] = json.dumps(data)

# MongoDB connection
@st.cache_resource
def init_connection():
    try:
        client = pymongo.MongoClient(st.secrets["mongo"]["connection_string"])
        return client[st.secrets["mongo"]["database"]]
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

def get_elo_rankings():
    """Fetch ELO rankings from MongoDB"""
    db = init_connection()
    st.write(db.tournamentDB)
    if db is None:
        return None
    
    try:
        # Assuming your collection name is 'players' or similar
        # Adjust the collection name as needed
        collection = db['players']
        players_data = list(collection.find({}, {'player': 1, 'ELO': 1, '_id': 0}))
        
        # Convert to DataFrame and sort by ELO (descending)
        if players_data:
            df = pd.DataFrame(players_data)
            df = df.sort_values('ELO', ascending=False)
            df = df.reset_index(drop=True)
            df.index = df.index + 1  # Start positions from 1
            return df
        else:
            return None
    except Exception as e:
        st.error(f"Error fetching ELO rankings: {e}")
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
                        'completed': False
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

# Number of players - using text input as workaround for visibility
num_players_str = st.sidebar.text_input(
    "Number of Players",
    value=str(st.session_state.num_players),
    key="num_players_input"
)

# Convert to integer and validate
try:
    num_players = int(num_players_str)
    if num_players < 2:
        num_players = 2
        st.sidebar.warning("Minimum 2 players required")
    elif num_players > 20:
        num_players = 20
        st.sidebar.warning("Maximum 20 players allowed")
except ValueError:
    num_players = st.session_state.num_players
    st.sidebar.error("Please enter a valid number")

# Update session state if number changes
if num_players != st.session_state.num_players:
    st.session_state.num_players = num_players
    st.session_state.tournament_generated = False

# Rounds (how many times each player plays each other) - using text input
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
st.sidebar.markdown('<h3 style="text-align: center;">👥 Player Names</h3>', unsafe_allow_html=True)

# Dynamic player name inputs
player_names = []
for i in range(num_players):
    default_name = st.session_state.players[i] if i < len(st.session_state.players) else f"Player {i+1}"
    name = st.sidebar.text_input(
        f"Player {i+1}",
        value=default_name,
        key=f"player_{i}"
    )
    player_names.append(name)

st.sidebar.markdown("---")

# Generate tournament button
if st.sidebar.button("🏆 Generate Tournament", type="primary", use_container_width=True):
    # Validate unique names
    if len(set(player_names)) != len(player_names):
        st.sidebar.error("⚠️ All player names must be unique!")
    elif any(name.strip() == "" for name in player_names):
        st.sidebar.error("⚠️ All player names must be filled!")
    else:
        st.session_state.players = player_names
        
        # Generate matches using round-robin scheduling
        st.session_state.matches = round_robin_schedule(player_names, rounds)
        st.session_state.tournament_generated = True
        
        # Save to query params for persistence
        save_to_query_params()
        st.rerun()

# Reset button
if st.sidebar.button("🔄 Reset Tournament", use_container_width=True):
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
        'num_players': st.session_state.num_players
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
            st.session_state.num_players = import_data['num_players']
            st.session_state.tournament_generated = True
            save_to_query_params()
            st.sidebar.success("✅ Tournament loaded!")
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"❌ Error loading file: {str(e)}")

# Main content with tabs
tab1, tab2 = st.tabs(["🏆 Tournament", "📈 ELO Rankings"])

with tab1:
    if not st.session_state.tournament_generated:
        st.info("👈 Configure your tournament in the sidebar and click 'Generate Tournament' to start!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🎯 How to use:
            1. **Set the number of players** - Choose 2-20 participants
            2. **Enter player names** - Customize each player's name
            3. **Choose rounds** - Decide how many times each pair plays
            4. **Generate!** - Click the button to create your tournament
            5. **Enter scores** - Update results as matches are played
            6. **Track standings** - Watch the leaderboard update in real-time
            """)
        
        with col2:
            st.markdown("""
            ### 💡 Features:
            - **Smart Scheduling** - Uses official round-robin algorithm
            - **Auto-Save** - Your data is saved in the URL
            - **No Data Loss** - Refresh the page safely
            - **Export/Import** - Download and restore tournaments
            - **Real-time Updates** - Instant standings calculation
            - **Fair Distribution** - Balanced match scheduling
            """)
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
                        if st.button(
                            "✅ Update" if not match['completed'] else "✓ Updated",
                            key=f"update_{match['match_id']}",
                            type="secondary" if match['completed'] else "primary",
                            use_container_width=True
                        ):
                            # Update match
                            for m in st.session_state.matches:
                                if m['match_id'] == match['match_id']:
                                    m['score1'] = score1
                                    m['score2'] = score2
                                    m['completed'] = True
                                    break
                            
                            # Save to query params
                            save_to_query_params()
                            st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    if idx < len(round_matches) - 1:
                        st.markdown("<br>", unsafe_allow_html=True)

with tab2:
    st.markdown('<h2 style="text-align: center;">📈 ELO Rankings</h2>', unsafe_allow_html=True)
    
    # Fetch ELO rankings from database
    elo_df = get_elo_rankings()
    
    if elo_df is not None and not elo_df.empty:
        # Create custom HTML table for ELO rankings
        elo_html = '<div class="standings-table">'
        
        # Header for ELO rankings
        elo_html += '''
        <div class="standings-header">
            <div class="standings-cell">Rank</div>
            <div class="standings-cell">Player</div>
            <div class="standings-cell">ELO</div>
        </div>
        '''
        
        # Rows for ELO rankings
        for idx, row in elo_df.iterrows():
            elo_html += '<div class="standings-row">'
            elo_html += f'<div class="standings-cell position">{idx}</div>'
            elo_html += f'<div class="standings-cell player-name">{row["player"]}</div>'
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
        st.info("""
        **Expected database structure:**
        - Collection: 'players' (or adjust in code)
        - Fields: 'player' (string), 'ELO' (number)
        
        **To test the connection:**
        1. Make sure your MongoDB connection string is correct
        2. Ensure the database has a collection with player ELO data
        3. Verify the collection has documents with 'player' and 'ELO' fields
        """)

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: rgba(255, 255, 255, 0.7); font-family: Inter, sans-serif;">'
    'Made with ❤️ | Tournament Generator v2.0 | Now with ELO Rankings!'
    '</div>',
    unsafe_allow_html=True
)
