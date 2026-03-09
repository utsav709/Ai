import streamlit as st
from groq import Groq
import json
from datetime import datetime

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Project Intelligence Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap');

  :root {
    --bg:       #0d0f14;
    --surface:  #141720;
    --border:   #252934;
    --accent:   #4fffb0;
    --red:      #ff4f6d;
    --yellow:   #ffd84f;
    --blue:     #4faaff;
    --purple:   #b04fff;
    --text:     #e8ecf4;
    --muted:    #6b7280;
  }

  html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    font-family: 'Syne', sans-serif;
    color: var(--text);
  }

  [data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
  }

  h1, h2, h3, h4 { font-family: 'Syne', sans-serif; font-weight: 800; }

  .hero-title {
    font-size: 2.4rem;
    font-weight: 800;
    letter-spacing: -1px;
    background: linear-gradient(135deg, var(--accent) 0%, var(--blue) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
  }

  .hero-sub {
    color: var(--muted);
    font-family: 'DM Mono', monospace;
    font-size: 0.82rem;
    margin-top: 4px;
    letter-spacing: 0.5px;
  }

  .card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 22px;
    margin-bottom: 14px;
    position: relative;
    overflow: hidden;
  }

  .card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    border-radius: 12px 0 0 12px;
  }

  .card-red::before   { background: var(--red); }
  .card-yellow::before{ background: var(--yellow); }
  .card-blue::before  { background: var(--blue); }
  .card-accent::before{ background: var(--accent); }
  .card-purple::before{ background: var(--purple); }

  .card-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 8px;
  }

  .label-red    { color: var(--red); }
  .label-yellow { color: var(--yellow); }
  .label-blue   { color: var(--blue); }
  .label-accent { color: var(--accent); }
  .label-purple { color: var(--purple); }

  .card-body { color: var(--text); font-size: 0.93rem; line-height: 1.6; }

  .badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 99px;
    font-size: 0.72rem;
    font-family: 'DM Mono', monospace;
    font-weight: 500;
    margin: 2px;
  }

  .badge-red    { background: rgba(255,79,109,.15); color: var(--red);    border: 1px solid rgba(255,79,109,.3); }
  .badge-yellow { background: rgba(255,216,79,.15); color: var(--yellow); border: 1px solid rgba(255,216,79,.3); }
  .badge-accent { background: rgba(79,255,176,.15); color: var(--accent); border: 1px solid rgba(79,255,176,.3); }
  .badge-blue   { background: rgba(79,170,255,.15); color: var(--blue);   border: 1px solid rgba(79,170,255,.3); }

  .metric-row { display: flex; gap: 14px; flex-wrap: wrap; margin-bottom: 16px; }

  .metric-box {
    flex: 1;
    min-width: 120px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px 18px;
    text-align: center;
  }

  .metric-val {
    font-size: 2rem;
    font-weight: 800;
    line-height: 1;
  }

  .metric-lbl {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: var(--muted);
    margin-top: 4px;
    letter-spacing: 0.8px;
    text-transform: uppercase;
  }

  .divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 20px 0;
  }

  .stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--blue)) !important;
    color: #0d0f14 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 24px !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.3px;
    width: 100%;
  }

  .stButton > button:hover { opacity: 0.88; }

  .stTextInput > div > div > input,
  .stTextArea > div > div > textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.9rem !important;
  }

  .stSelectbox > div > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
  }

  .stRadio > div { gap: 8px; }
  .stRadio label { color: var(--text) !important; font-size: 0.9rem; }

  [data-testid="stFileUploader"] {
    background: var(--surface);
    border: 1px dashed var(--border);
    border-radius: 12px;
    padding: 8px;
  }

  .section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text);
    margin: 20px 0 12px;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .tag-row { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; }

  ::-webkit-scrollbar { width: 6px; }
  ::-webkit-scrollbar-track { background: var(--bg); }
  ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def ask_claude(system_prompt: str, user_prompt: str) -> str:
    api_key = st.session_state.get("groq_api_key", "")
    if not api_key:
        st.error("⚠️  Please enter your Groq API key in the sidebar.")
        st.stop()
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
        max_tokens=4096,
    )
    return response.choices[0].message.content


def parse_json_safe(text: str) -> dict:
    try:
        start = text.find("{")
        end   = text.rfind("}") + 1
        return json.loads(text[start:end])
    except Exception:
        return {}


def render_metric(value, label, color):
    st.markdown(f"""
    <div class="metric-box">
      <div class="metric-val" style="color:{color};">{value}</div>
      <div class="metric-lbl">{label}</div>
    </div>""", unsafe_allow_html=True)


def render_card(label, label_cls, body, card_cls):
    st.markdown(f"""
    <div class="card {card_cls}">
      <div class="card-label {label_cls}">{label}</div>
      <div class="card-body">{body}</div>
    </div>""", unsafe_allow_html=True)


def render_badges(items: list, badge_cls: str):
    html = '<div class="tag-row">'
    for item in items:
        html += f'<span class="badge {badge_cls}">{item}</span>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="hero-title" style="font-size:1.5rem;">🧠 PulseAI</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-sub">Project Intelligence</p>', unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.markdown("**View Mode**")
    view_mode = st.radio(
        "", ["👨‍💼 Manager View", "👩‍💻 Developer View"],
        label_visibility="collapsed"
    )

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("**Source Types**")
    src_slack  = st.checkbox("💬 Slack Messages",  value=True)
    src_email  = st.checkbox("📧 Email Threads",   value=True)
    src_jira   = st.checkbox("🎯 Jira Updates",    value=True)
    src_meet   = st.checkbox("📝 Meeting Notes",   value=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("**🔑 Groq API Key**")
    groq_key_input = st.text_input(
        "", type="password", placeholder="gsk_...",
        label_visibility="collapsed",
        value=st.session_state.get("groq_api_key", "")
    )
    if groq_key_input:
        st.session_state["groq_api_key"] = groq_key_input
        st.markdown('<p style="color:#4fffb0;font-size:0.75rem;font-family:DM Mono,monospace;">✓ Key saved</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p style="color:#6b7280;font-size:0.75rem;font-family:DM Mono,monospace;">Get free key at console.groq.com</p>', unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<p style="color:#6b7280;font-size:0.75rem;font-family:DM Mono,monospace;">Powered by Groq · llama3-70b</p>', unsafe_allow_html=True)


# ── Main area ─────────────────────────────────────────────────────────────────
st.markdown('<p class="hero-title">Project Intelligence Dashboard</p>', unsafe_allow_html=True)
st.markdown(f'<p class="hero-sub">// {view_mode.upper()}</p>', unsafe_allow_html=True)

st.markdown("---")

# Upload zone
uploaded_files = st.file_uploader(
    "📂 Upload communication files (.txt, .md, .csv, .json)",
    accept_multiple_files=True,
    type=["txt", "md", "csv", "json"],
)

col_a, col_b = st.columns([3, 1])
with col_a:
    analyze_btn = st.button("⚡ Analyze Project Communications", use_container_width=True)
with col_b:
    clear_btn = st.button("🗑 Clear", use_container_width=True)

if clear_btn:
    for key in ["analysis", "all_text"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

# ── Analysis ──────────────────────────────────────────────────────────────────
if analyze_btn:
    if not uploaded_files:
        st.warning("⚠️  Please upload at least one file.")
    else:
        all_text = ""
        for f in uploaded_files:
            try:
                content = f.read().decode("utf-8")
                all_text += f"\n\n--- SOURCE: {f.name} ---\n{content}"
            except Exception:
                st.warning(f"Could not read {f.name}")

        st.session_state["all_text"] = all_text

        is_manager = "Manager" in view_mode

        system_prompt = """You are an elite AI project analyst embedded in an engineering team.
Return ONLY a valid JSON object — no markdown, no explanation, just the raw JSON.
"""

        if is_manager:
            user_prompt = f"""
Analyze these communications and return a JSON object with:
{{
  "executive_summary": "3-4 sentence overview of the project's current state",
  "health_score": <integer 0-100>,
  "health_label": "Healthy | At Risk | Critical",
  "kpis": {{
    "total_risks": <int>,
    "blocked_tasks": <int>,
    "unowned_items": <int>,
    "decision_delays": <int>
  }},
  "top_risks": [
    {{"title": "...", "severity": "High|Medium|Low", "detail": "...", "owner": "..."}}
  ],
  "key_decisions_pending": ["..."],
  "team_highlights": ["..."],
  "recommended_actions": [
    {{"action": "...", "priority": "Urgent|Normal", "owner": "..."}}
  ],
  "recurring_themes": ["..."],
  "timeline_concerns": "paragraph about schedule risks"
}}

Communications:
{all_text}
"""
        else:
            user_prompt = f"""
Analyze these communications for developers and return a JSON object with:
{{
  "dev_summary": "3-4 sentence technical overview",
  "health_score": <integer 0-100>,
  "health_label": "Healthy | At Risk | Critical",
  "kpis": {{
    "open_bugs": <int>,
    "blocked_tasks": <int>,
    "pr_issues": <int>,
    "tech_debt_mentions": <int>
  }},
  "blockers": [
    {{"title": "...", "severity": "High|Medium|Low", "detail": "...", "mentioned_by": "..."}}
  ],
  "tech_debt_items": ["..."],
  "missing_ownership": ["..."],
  "frequently_mentioned_issues": ["..."],
  "action_items": [
    {{"task": "...", "assignee": "...", "priority": "Urgent|Normal"}}
  ],
  "code_review_concerns": ["..."],
  "deployment_risks": "paragraph about deployment or release risks"
}}

Communications:
{all_text}
"""

        with st.spinner("🔍 Analyzing communications with Claude..."):
            raw = ask_claude(system_prompt, user_prompt)
            data = parse_json_safe(raw)
            st.session_state["analysis"] = data
            st.session_state["is_manager"] = is_manager


# ── Render results ────────────────────────────────────────────────────────────
if "analysis" in st.session_state:
    data       = st.session_state["analysis"]
    is_manager = st.session_state.get("is_manager", True)

    if not data:
        st.error("Could not parse the AI response. Please try again.")
    else:
        kpis = data.get("kpis", {})

        # ── Health score ──
        score = data.get("health_score", 0)
        label = data.get("health_label", "Unknown")
        score_color = "#4fffb0" if score >= 70 else "#ffd84f" if score >= 40 else "#ff4f6d"

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.markdown(f"""
            <div class="metric-box">
              <div class="metric-val" style="color:{score_color};">{score}</div>
              <div class="metric-lbl">Health Score</div>
            </div>""", unsafe_allow_html=True)

        kpi_items = list(kpis.items())[:4]
        kpi_colors = ["#ff4f6d", "#ffd84f", "#4faaff", "#b04fff"]
        kpi_cols   = [col2, col3, col4, col5]
        for i, (k, v) in enumerate(kpi_items):
            with kpi_cols[i]:
                st.markdown(f"""
                <div class="metric-box">
                  <div class="metric-val" style="color:{kpi_colors[i]};">{v}</div>
                  <div class="metric-lbl">{k.replace('_',' ')}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("---")

        # ── Two-column layout ──
        left, right = st.columns([3, 2])

        with left:
            # Summary
            summary_key = "executive_summary" if is_manager else "dev_summary"
            summary     = data.get(summary_key, "")
            if summary:
                render_card("📋 SUMMARY", "label-accent", summary, "card-accent")

            # Risks / Blockers
            risk_key = "top_risks" if is_manager else "blockers"
            risks    = data.get(risk_key, [])
            if risks:
                st.markdown('<div class="section-title">🚨 Risks & Blockers</div>', unsafe_allow_html=True)
                for r in risks:
                    sev   = r.get("severity", "Medium")
                    cls   = "red" if sev == "High" else "yellow" if sev == "Medium" else "blue"
                    title = r.get("title", "")
                    detail= r.get("detail", "")
                    owner = r.get("owner") or r.get("mentioned_by", "Unassigned")
                    render_card(
                        f"⚠ {sev.upper()} · {title}",
                        f"label-{cls}",
                        f"{detail}<br><span style='color:#6b7280;font-size:0.8rem;font-family:DM Mono,monospace;'>Owner: {owner}</span>",
                        f"card-{cls}",
                    )

            # Timeline / Deployment risks
            risk_para_key = "timeline_concerns" if is_manager else "deployment_risks"
            risk_para     = data.get(risk_para_key, "")
            if risk_para:
                render_card("🗓 TIMELINE / DEPLOYMENT RISKS", "label-purple", risk_para, "card-purple")

        with right:
            # Action items
            action_key = "recommended_actions" if is_manager else "action_items"
            actions    = data.get(action_key, [])
            if actions:
                st.markdown('<div class="section-title">✅ Action Items</div>', unsafe_allow_html=True)
                for a in actions:
                    task     = a.get("action") or a.get("task", "")
                    priority = a.get("priority", "Normal")
                    owner    = a.get("owner") or a.get("assignee", "Unassigned")
                    badge    = "badge-red" if priority == "Urgent" else "badge-blue"
                    st.markdown(f"""
                    <div class="card card-blue" style="padding:14px 16px;margin-bottom:8px;">
                      <span class="badge {badge}">{priority}</span>
                      <div class="card-body" style="margin-top:6px;">{task}</div>
                      <div style="color:#6b7280;font-size:0.78rem;font-family:DM Mono,monospace;margin-top:4px;">→ {owner}</div>
                    </div>""", unsafe_allow_html=True)

            # Pending decisions / Missing ownership
            if is_manager:
                decisions = data.get("key_decisions_pending", [])
                if decisions:
                    st.markdown('<div class="section-title">⏳ Pending Decisions</div>', unsafe_allow_html=True)
                    render_card("DECISIONS NEEDED", "label-yellow",
                                "<br>".join(f"• {d}" for d in decisions), "card-yellow")

                highlights = data.get("team_highlights", [])
                if highlights:
                    st.markdown('<div class="section-title">🌟 Team Highlights</div>', unsafe_allow_html=True)
                    render_card("WINS", "label-accent",
                                "<br>".join(f"• {h}" for h in highlights), "card-accent")
            else:
                missing = data.get("missing_ownership", [])
                if missing:
                    st.markdown('<div class="section-title">👤 Missing Ownership</div>', unsafe_allow_html=True)
                    render_card("UNOWNED ITEMS", "label-yellow",
                                "<br>".join(f"• {m}" for m in missing), "card-yellow")

                td = data.get("tech_debt_items", [])
                if td:
                    st.markdown('<div class="section-title">🔧 Tech Debt</div>', unsafe_allow_html=True)
                    render_card("TECH DEBT", "label-purple",
                                "<br>".join(f"• {t}" for t in td), "card-purple")

        # ── Recurring themes / Frequently mentioned ──
        themes_key = "recurring_themes" if is_manager else "frequently_mentioned_issues"
        themes     = data.get(themes_key, [])
        if themes:
            st.markdown('<div class="section-title">🔁 Recurring Themes</div>', unsafe_allow_html=True)
            render_badges(themes, "badge-accent")

        if not is_manager:
            cr = data.get("code_review_concerns", [])
            if cr:
                st.markdown('<div class="section-title">🔍 Code Review Concerns</div>', unsafe_allow_html=True)
                render_badges(cr, "badge-yellow")


# ── Q&A ───────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="section-title">💬 Ask About Your Communications</div>', unsafe_allow_html=True)

question = st.text_input(
    "",
    placeholder="e.g. Who owns the login bug? What decisions are delayed? What's blocking the release?",
    label_visibility="collapsed",
)

if question:
    all_text = st.session_state.get("all_text", "")
    if not all_text:
        st.warning("Upload and analyze files first before asking questions.")
    else:
        with st.spinner("Thinking..."):
            system = "You are a concise, direct project analyst. Answer in 2-4 sentences max unless a list is needed."
            answer = ask_claude(system, f"Communications:\n{all_text}\n\nQuestion: {question}")
        render_card("🤖 AI ANSWER", "label-accent", answer, "card-accent")
