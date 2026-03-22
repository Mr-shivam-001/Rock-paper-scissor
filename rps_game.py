import random
import streamlit as st

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Rock Paper Scissors", page_icon="✊", layout="centered")

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@400;500;600&display=swap');

:root {
    --bg:        #0d0d0f;
    --surface:   #18181c;
    --border:    #2a2a32;
    --accent:    #f0e040;
    --accent2:   #ff4f58;
    --accent3:   #40c4f0;
    --text:      #e8e8ec;
    --muted:     #6b6b7a;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 60% 40% at 20% 10%, rgba(240,224,64,.07) 0%, transparent 60%),
        radial-gradient(ellipse 50% 35% at 80% 90%, rgba(64,196,240,.06) 0%, transparent 60%),
        var(--bg) !important;
}

/* hide default header */
[data-testid="stHeader"] { display: none; }

/* ── Title ── */
.game-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(3rem, 8vw, 5.5rem);
    letter-spacing: .08em;
    line-height: 1;
    text-align: center;
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 55%, var(--accent3) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: .15em;
}
.game-sub {
    text-align: center;
    color: var(--muted);
    font-size: .85rem;
    letter-spacing: .25em;
    text-transform: uppercase;
    margin-bottom: 2.5rem;
}

/* ── Score Board ── */
.score-board {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1.5rem;
    margin-bottom: 2.5rem;
}
.score-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.1rem 2rem;
    text-align: center;
    min-width: 120px;
    position: relative;
    overflow: hidden;
}
.score-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}
.score-card.human::before  { background: var(--accent); }
.score-card.cpu::before    { background: var(--accent2); }
.score-card.vs             { background: transparent; border-color: transparent; }

.score-label {
    font-size: .7rem;
    letter-spacing: .2em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: .3rem;
}
.score-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3rem;
    line-height: 1;
    color: var(--text);
}
.score-card.human .score-num { color: var(--accent); }
.score-card.cpu   .score-num { color: var(--accent2); }
.vs-text {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.4rem;
    color: var(--muted);
    letter-spacing: .1em;
}

/* ── Choice buttons ── */
.choice-row {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 2rem;
    flex-wrap: wrap;
}
.choice-btn {
    background: var(--surface);
    border: 2px solid var(--border);
    border-radius: 20px;
    padding: 1.2rem 1.6rem;
    cursor: pointer;
    transition: all .18s ease;
    text-align: center;
    min-width: 110px;
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
    font-size: .8rem;
    font-weight: 600;
    letter-spacing: .1em;
    text-transform: uppercase;
}
.choice-btn:hover {
    transform: translateY(-4px);
    border-color: var(--accent);
    box-shadow: 0 8px 30px rgba(240,224,64,.18);
}
.choice-btn .emoji { font-size: 2.6rem; display: block; margin-bottom: .4rem; }

/* ── Result card ── */
.result-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 1.8rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
}
.result-picks {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1.5rem;
    margin-bottom: 1.2rem;
}
.pick-box {
    text-align: center;
}
.pick-emoji { font-size: 3rem; display: block; }
.pick-label {
    font-size: .7rem;
    text-transform: uppercase;
    letter-spacing: .15em;
    color: var(--muted);
    margin-top: .3rem;
}
.result-sep {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8rem;
    color: var(--muted);
}
.result-badge {
    display: inline-block;
    padding: .5rem 1.6rem;
    border-radius: 999px;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.3rem;
    letter-spacing: .1em;
    margin-top: .2rem;
}
.result-badge.win  { background: rgba(240,224,64,.15); color: var(--accent);  border: 1px solid rgba(240,224,64,.3); }
.result-badge.lose { background: rgba(255,79,88,.15);  color: var(--accent2); border: 1px solid rgba(255,79,88,.3); }
.result-badge.draw { background: rgba(107,107,122,.15); color: var(--muted);  border: 1px solid var(--border); }

/* ── Winner banner ── */
.winner-banner {
    text-align: center;
    padding: 2rem;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 24px;
    margin-bottom: 2rem;
}
.winner-emoji { font-size: 4rem; }
.winner-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.8rem;
    margin: .4rem 0;
    background: linear-gradient(90deg, var(--accent), var(--accent3));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.winner-title.lose {
    background: linear-gradient(90deg, var(--accent2), #ff9060);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ── Footer hint ── */
.hint {
    text-align: center;
    color: var(--muted);
    font-size: .78rem;
    margin-top: .5rem;
}

/* override streamlit button to blend in */
.stButton > button {
    background: var(--surface) !important;
    border: 2px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 14px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: .05em !important;
    padding: .7rem 2rem !important;
    transition: all .18s ease !important;
}
.stButton > button:hover {
    border-color: var(--accent) !important;
    box-shadow: 0 6px 24px rgba(240,224,64,.15) !important;
    transform: translateY(-2px) !important;
}
</style>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
def init_state():
    defaults = dict(hs=0, cs=0, last_user=None, last_com=None, last_result=None, game_over=False, winner=None)
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

CHOICES = {1: ("✊", "Rock"), 2: ("🖐️", "Paper"), 3: ("✌️", "Scissors")}
WINS_AGAINST = {1: 3, 2: 1, 3: 2}   # key beats value


def play(user_choice: int):
    if st.session_state.game_over:
        return
    com = random.randint(1, 3)
    st.session_state.last_user = user_choice
    st.session_state.last_com  = com

    if user_choice == com:
        result = "draw"
    elif WINS_AGAINST[user_choice] == com:
        result = "win"
        st.session_state.hs += 1
    else:
        result = "lose"
        st.session_state.cs += 1

    st.session_state.last_result = result

    if st.session_state.hs == 5:
        st.session_state.game_over = True
        st.session_state.winner = "human"
    elif st.session_state.cs == 5:
        st.session_state.game_over = True
        st.session_state.winner = "cpu"


def reset():
    for k in ["hs","cs","last_user","last_com","last_result","game_over","winner"]:
        del st.session_state[k]
    init_state()


# ── Render ────────────────────────────────────────────────────────────────────
st.markdown('<h1 class="game-title">Rock Paper Scissors</h1>', unsafe_allow_html=True)
st.markdown('<p class="game-sub">First to 5 wins the match</p>', unsafe_allow_html=True)

# Score board
st.markdown(f"""
<div class="score-board">
  <div class="score-card human">
    <div class="score-label">You</div>
    <div class="score-num">{st.session_state.hs}</div>
  </div>
  <div class="score-card vs">
    <div class="vs-text">VS</div>
  </div>
  <div class="score-card cpu">
    <div class="score-label">CPU</div>
    <div class="score-num">{st.session_state.cs}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Game over screen ──────────────────────────────────────────────────────────
if st.session_state.game_over:
    if st.session_state.winner == "human":
        st.markdown("""
        <div class="winner-banner">
          <div class="winner-emoji">🥳</div>
          <div class="winner-title">You Won the Match!</div>
          <p style="color:var(--muted);margin:0">Flawless victory against the machine.</p>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="winner-banner">
          <div class="winner-emoji">🤖</div>
          <div class="winner-title lose">CPU Won the Match!</div>
          <p style="color:var(--muted);margin:0">The machine prevails… this time.</p>
        </div>""", unsafe_allow_html=True)

    if st.button("🔄  Play Again", use_container_width=True):
        reset()
        st.rerun()

# ── Active game ───────────────────────────────────────────────────────────────
else:
    # Last round result
    if st.session_state.last_result is not None:
        u_emoji, u_name = CHOICES[st.session_state.last_user]
        c_emoji, c_name = CHOICES[st.session_state.last_com]
        badge_class = st.session_state.last_result
        badge_text  = {"win": "You Won! 👍", "lose": "CPU Wins 🤖", "draw": "Draw 😮‍💨"}[badge_class]

        st.markdown(f"""
        <div class="result-card">
          <div class="result-picks">
            <div class="pick-box">
              <span class="pick-emoji">{u_emoji}</span>
              <span class="pick-label">You — {u_name}</span>
            </div>
            <span class="result-sep">vs</span>
            <div class="pick-box">
              <span class="pick-emoji">{c_emoji}</span>
              <span class="pick-label">CPU — {c_name}</span>
            </div>
          </div>
          <span class="result-badge {badge_class}">{badge_text}</span>
        </div>
        """, unsafe_allow_html=True)

    # Choice buttons
    st.markdown('<div class="choice-row">', unsafe_allow_html=True)
    cols = st.columns(3)
    labels = [(1,"✊","Rock"), (2,"🖐️","Paper"), (3,"✌️","Scissors")]
    for col, (val, emoji, name) in zip(cols, labels):
        with col:
            if st.button(f"{emoji}\n{name}", key=f"btn_{val}", use_container_width=True):
                play(val)
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<p class="hint">Pick a move above — first to 5 rounds wins the match.</p>', unsafe_allow_html=True)
