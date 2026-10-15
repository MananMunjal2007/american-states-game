
import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="American States Challenge",
    page_icon="🇺🇸",
    layout="wide"
)

states = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California",
    "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
    "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
    "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
    "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri",
    "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
    "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
    "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
    "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
    "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
]

codes = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "MA", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]

# Correct Maine's abbreviation and Massachusetts' abbreviation
codes[18] = "ME"
codes[20] = "MA"

# Initialize game data
if "guessed" not in st.session_state:
    st.session_state.guessed = set()

if "repetitions" not in st.session_state:
    st.session_state.repetitions = 0

if "message" not in st.session_state:
    st.session_state.message = "Start guessing!"

if "finished" not in st.session_state:
    st.session_state.finished = False

guessed = st.session_state.guessed

# American-themed styling
st.markdown("""
<style>
.stApp {
    background: linear-gradient(
        135deg, #071A38 0%, #123C69 55%, #7F1D2D 100%
    );
    color: white;
}

h1 {
    color: white !important;
    text-align: center;
    font-weight: 800 !important;
}

.stApp p, .stApp label, .stApp h2, .stApp h3 {
    color: white;
}

.flag-banner {
    background: white;
    color: #123C69;
    text-align: center;
    padding: 15px;
    border-radius: 16px;
    font-size: 22px;
    font-weight: bold;
    margin-bottom: 25px;
}

/* Scoreboard */
[data-testid="stMetric"] {
    background: #FFFFFF;
    padding: 18px;
    border-radius: 14px;
    border-top: 5px solid #C62828;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricValue"],
[data-testid="stMetricLabel"] *,
[data-testid="stMetricValue"] * {
    color: #123C69 !important;
}

/* Progress bar */
.stProgress > div {
    background-color: #F5EBD7;
    border-radius: 10px;
}

.stProgress > div > div > div {
    background-color: #C62828;
}

/* Input */
.stTextInput input {
    background-color: white;
    color: #123C69;
    border-radius: 8px;
}

/* Buttons */
.stButton > button,
.stFormSubmitButton > button {
    background-color: #C62828;
    color: white;
    border: 2px solid white;
    border-radius: 10px;
    font-weight: bold;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background-color: #123C69;
    color: white;
    border-color: white;
}
</style>

<div class="flag-banner">
    🇺🇸 ★ UNITED STATES OF AMERICA ★ 🇺🇸
</div>
""", unsafe_allow_html=True)

# Title
st.title("🇺🇸 American States Challenge 🇺🇸")
st.write("⭐ How many of the 50 states can you name?")
st.caption("RED • WHITE • BLUE • 50 STATES")

# Scoreboard
col1, col2, col3 = st.columns(3)

col1.metric("States Found", f"{len(guessed)}/50")
col2.metric("States Remaining", 50 - len(guessed))
col3.metric("Repeated Guesses", st.session_state.repetitions)

st.progress(len(guessed) / 50)

# Guess input
if not st.session_state.finished and len(guessed) < 50:
    with st.form("guess_form", clear_on_submit=True):
        answer = st.text_input(
            "Enter a state, or type 'hint' or 'quit'"
        )
        submitted = st.form_submit_button("Submit")

    if submitted:
        answer = answer.strip()

        if answer.lower() == "hint":
            remaining = [s for s in states if s not in guessed]
            st.session_state.message = (
                "States remaining: " + ", ".join(remaining)
            )

        elif answer.lower() == "quit":
            st.session_state.finished = True
            st.session_state.message = "You ended the game."

        elif answer.title() not in states:
            st.session_state.message = (
                "That is not a valid US state. Try again!"
            )

        elif answer.title() in guessed:
            st.session_state.repetitions += 1
            st.session_state.message = (
                f"You already guessed {answer.title()}!"
            )

        else:
            guessed.add(answer.title())
            st.session_state.message = (
                f"Correct! You found {answer.title()}!"
            )

        st.rerun()

st.info(st.session_state.message)

# Map colors: red, blue, and white for guessed states
# Cream for states not yet guessed
flag_colors = ["#C62828", "#2455A4", "#FFFFFF"]

map_data = pd.DataFrame({
    "State": states,
    "Code": codes,
    "Status": [
        (
            flag_colors[states.index(state) % 3]
            if state in guessed
            else "#F5EBD7"
        )
        for state in states
    ]
})

fig = px.choropleth(
    map_data,
    locations="Code",
    locationmode="USA-states",
    color="Status",
    hover_name="State",
    color_discrete_map={
        "#C62828": "#C62828",
        "#2455A4": "#2455A4",
        "#FFFFFF": "#FFFFFF",
        "#F5EBD7": "#F5EBD7"
    },
    scope="usa"
)

fig.update_traces(
    marker_line_color="#123C69",
    marker_line_width=1
)

fig.update_layout(
    geo=dict(
        showlakes=True,
        lakecolor="#D9E2F2",
        bgcolor="rgba(0,0,0,0)"
    ),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white"),
    margin=dict(l=0, r=0, t=10, b=0),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# Color legend
st.markdown("""
<div style="text-align:center; color:white; font-size:16px;">
    <span style="color:#FF7777;">■</span> Guessed — Red
    &nbsp;&nbsp;
    <span style="color:#79A9FF;">■</span> Guessed — Blue
    &nbsp;&nbsp;
    <span style="color:white;">■</span> Guessed — White
    &nbsp;&nbsp;
    <span style="color:#F5EBD7;">■</span> Not guessed — Cream
</div>
""", unsafe_allow_html=True)

# Reveal remaining states
if st.button("💡 Show all remaining states"):
    remaining = [s for s in states if s not in guessed]

    if remaining:
        st.write(", ".join(remaining))
    else:
        st.success("You found every state!")

# Game completion
if len(guessed) == 50:
    st.balloons()
    st.success("🎉 Incredible! You guessed all 50 states!")

if st.session_state.finished:
    st.subheader("Game Results")
    st.write(f"States found: {len(guessed)}/50")
    st.write(f"Repeated guesses: {st.session_state.repetitions}")

    remaining = [s for s in states if s not in guessed]
    if remaining:
        st.write("States missed:", ", ".join(remaining))

# Bottom banner
st.markdown("""
<div class="flag-banner">
    ⭐ LAND OF THE FREE • HOME OF THE BRAVE ⭐<br>
    🇺🇸 UNITED STATES OF AMERICA 🇺🇸
</div>
""", unsafe_allow_html=True)

# Restart
if st.button("🔄 Restart Game"):
    st.session_state.guessed = set()
    st.session_state.repetitions = 0
    st.session_state.message = "Start guessing!"
    st.session_state.finished = False
    st.rerun()
