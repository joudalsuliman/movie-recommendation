import streamlit as st
from tmdb_helper import search_movie, get_recommendations, get_poster_url, get_movie_details
import hashlib
import re

def is_valid_password(password):
    # At least 6 characters, at least one capital letter, no special characters
    if len(password) < 6:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if re.search(r'[^a-zA-Z0-9]', password):  # checks for special characters
        return False
    return True

# ---------- Custom Styling ----------
st.markdown(
    """
    <style>
    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {
        border: 2px solid #AF8260 !important;
        border-radius: 6px !important;
        box-shadow: none !important;
    }
    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="select"] > div:focus-within {
        border: 2px solid #AF8260 !important;
    }
    .stApp {
        background-color: #322C2B;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    input[type="text"], input[type="password"] {
        width: 100% !important;
        box-sizing: border-box;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Auth Setup ----------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

if "users" not in st.session_state:
    st.session_state.users = {
        "admin": hash_password("admin123")
    }

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "show_signup" not in st.session_state:
    st.session_state.show_signup = False
if "watchlist" not in st.session_state:
    st.session_state.watchlist = {}

# ---------- Auth Screens ----------
def login_screen():
    st.markdown("<h2 style='font-size:2.60rem;'>˚｡☆˚｡ Your Golden Watchlist ˚｡☆˚｡</h2>", unsafe_allow_html=True)
    st.markdown("""
    <p style='
        color:#E4C59E;
        font-size:20px;
        font-family:"Libertinus Math", serif;
        text-align:center;
    '>
        If you already have an account, please log in or sign up to create an account.
    </p>
""", unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username] == hash_password(password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Incorrect username or password")

    if st.button("Sign Up Instead"):
        st.session_state.show_signup = True
        st.rerun()

def signup_screen():
    st.markdown(
        """
        <style>
        .signup-wrapper {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding-top: 5vh;
        }
        .signup-box {
            background-color: #3D3634;
            padding: 2rem;
            border-radius: 12px;
            width: 100%;
            max-width: 420px;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }
        .signup-title {
            margin-bottom: 0.5rem;
            text-align: center;
            color: #FFEAC5;
            font-size: 2rem;
            font-weight: bold;
        }
        .signup-note-title {
            color: #FFEAC5;
            font-size: 14px;
            margin-top: 1rem;
            text-align: left;
            font-weight: bold;
        }
        .signup-note {
            margin: 0;
            color: #FFEAC5;
            font-size: 14px;
            text-align: left;
        }
        </style>
        """, unsafe_allow_html=True
    )

    st.markdown("""
        <div class="signup-wrapper">
            <div class="signup-box">
                <div class="signup-title">Create a New Account</div>
                <p class="signup-note-title">Please Note, Password must be:</p>
                <p class="signup-note">● at least 6 characters, include one capital letter, and no special characters.</p>
                <p class="signup-note">● include one capital letter, and no special characters.</p>
                <p class="signup-note">● no special characters.</p>
    """, unsafe_allow_html=True)

    new_user = st.text_input("New Username", key="signup_user")
    new_pass = st.text_input("New Password", type="password", key="signup_pass")

    if st.button("Sign Up"):
        if new_user in st.session_state.users:
            st.warning("Username already exists.")
        elif not is_valid_password(new_pass):
            st.error("Password must be at least 6 characters, include one capital letter, and contain no special characters.")
        else:
            st.session_state.users[new_user] = hash_password(new_pass)
            st.success("Account created! You can log in now.")
            st.session_state.show_signup = False
            st.rerun()

    if st.button("Back to Login"):
        st.session_state.show_signup = False
        st.rerun()

    st.markdown('</div></div>', unsafe_allow_html=True)

# ---------- Auth Check ----------
if not st.session_state.logged_in:
    if st.session_state.show_signup:
        signup_screen()
    else:
        login_screen()
    st.stop()

# ---------- Initialize watchlist per user ----------
if "watchlist" not in st.session_state:
    st.session_state.watchlist = {}

if st.session_state.username not in st.session_state.watchlist:
    st.session_state.watchlist[st.session_state.username] = []

watchlist = st.session_state.watchlist[st.session_state.username]

# ---------- UI Setup ----------
if "recent" not in st.session_state:
    st.session_state.recent = []

st.set_page_config(
    page_title="Golden watchlist",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Sidebar Watchlist ----------
with st.sidebar:
    st.header("Your Watchlist:")
    current_watchlist = st.session_state.watchlist[st.session_state.username]

    if current_watchlist:
        for title in current_watchlist:
            col1, col2 = st.columns([6,1])
            col1.write(f"✧˖° {title}")
            if col2.button("☒", key=f"del_{title}"):
                current_watchlist.remove(title)
                st.session_state.watchlist[st.session_state.username] = current_watchlist
                st.rerun()
    else:
        st.caption("Your list is still glowing with possibility ✦")

    st.markdown("---")
    if st.button("Sign Out"):
        st.session_state.logged_in = False
        st.rerun()

# ---------- App UI ----------
st.markdown('<h1 style="color:#FFEAC5;">🎞️ Golden Watchlist </h1>', unsafe_allow_html=True)
st.markdown("Because your next favorite film deserves to feel right 𓂃𓊝")

typed_query = st.text_input("Type in your golden pick:")

if typed_query:
    search_results = search_movie(typed_query)
    suggestions = [movie["title"] for movie in search_results]
else:
    suggestions = list(reversed(st.session_state.recent[-5:]))

selected_movie = st.selectbox("Picks from search result:", options=suggestions)

# Always run search again to get correct matched_result
all_results = search_movie(selected_movie) if selected_movie else []
matched_result = next((m for m in all_results if m['title'].lower() == selected_movie.lower()), None)
if not matched_result and all_results:
    matched_result = all_results[0]

st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #803D3B;
    }
    </style>
""", unsafe_allow_html=True)

if matched_result:
    if selected_movie not in st.session_state.recent:
        st.session_state.recent.append(selected_movie)

    details = get_movie_details(matched_result['id'])

    st.markdown("<h3 style='color:#E4C59E;'>Your Featured Pick</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(get_poster_url(details.get("poster_path")), width=400)
    with col2:
        st.markdown(f"""
            <div style="color:#E4C59E;">
                <h3 style="color:#803D3B;">{details.get('title', 'Unknown Title')}</h3>
                <p><strong>Release Date:</strong> {details.get('release_date', 'N/A')}</p>
                <p><strong>Rating:</strong> {details.get('vote_average', 'N/A')} ⭐</p>
                {f"<p><strong>Tagline:</strong> <em>{details['tagline']}</em></p>" if details.get("tagline") else ""}
                {f"<p><strong>Runtime:</strong> {details['runtime']} minutes</p>" if details.get("runtime") else ""}
                <p><strong>Genres:</strong> {', '.join([g['name'] for g in details.get('genres', [])]) or 'N/A'}</p>
                <p><strong>Overview:</strong></p>
                <p>{details.get("overview", "No overview available.")}</p>
            </div>
        """, unsafe_allow_html=True)
        if selected_movie not in watchlist:
            if st.button("➕ Add to Watchlist"):
                watchlist.append(selected_movie)
                st.session_state.watchlist[st.session_state.username] = watchlist
                st.success(f"✦ Added ✦")
                st.rerun()

    # Recommendations
    st.markdown("<h3 style='color:#E4C59E;'>Lights, Camera, More Picks!</h3>", unsafe_allow_html=True)
    recommendations = get_recommendations(matched_result['id'])

    num_cols = 4
    for i in range(0, len(recommendations), num_cols):
        row = recommendations[i:i + num_cols]
        cols = st.columns(num_cols)
        for col, movie in zip(cols, row):
            with col:
                st.image(get_poster_url(movie['poster_path']), width=200)
                st.caption(movie['title'])
                if movie["title"] not in watchlist:
                    if st.button(f"Save: {movie['title']}", key=f"save_{movie['id']}"):
                        watchlist.append(movie["title"])
                        st.session_state.watchlist[st.session_state.username] = watchlist
                        st.success(f"Saved {movie['title']}!")
                        st.rerun()
elif selected_movie:
    st.warning("Our scrolls don’t hold any info on this one")
