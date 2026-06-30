"""
ShopMind AI - AI Powered Shopping Assistant
Frontend-only Streamlit application that consumes a FastAPI + RAG backend.

This file is intentionally self-contained (single file) per project spec.
It does NOT implement any backend logic - it only calls the existing
FastAPI endpoints via the `requests` library.
"""

import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# ============================================================
# CONFIG
# ============================================================

API_BASE_URL = "http://localhost:8000"  # Change to your deployed backend URL

st.set_page_config(
    page_title="ShopMind AI",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# DESIGN TOKENS (single source of truth for the custom CSS)
# ============================================================
# Palette: near-black charcoal surface, violet -> cyan gradient accent,
# warm gold for ratings, green for savings/discounts.
COLORS = {
    "bg": "#0A0D14",
    "bg_alt": "#0F1320",
    "surface": "#141925",
    "surface_2": "#1A2030",
    "border": "#262C3D",
    "text": "#EAECF3",
    "text_muted": "#8B92A8",
    "accent_a": "#7C5CFF",
    "accent_b": "#22D3EE",
    "gold": "#FBBF24",
    "green": "#34D399",
    "red": "#F87171",
}

# ============================================================
# CUSTOM CSS
# ============================================================

def inject_custom_css():
    """Injects the full design system as custom CSS into the app."""
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, sans-serif;
        color: {COLORS['text']};
    }}

    .stApp {{
        background:
            radial-gradient(circle at 15% 0%, rgba(124,92,255,0.10) 0%, transparent 45%),
            radial-gradient(circle at 85% 10%, rgba(34,211,238,0.08) 0%, transparent 40%),
            {COLORS['bg']};
    }}

    h1, h2, h3, h4, h5 {{
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        letter-spacing: -0.02em;
    }}

    #MainMenu, footer {{visibility: hidden;}}

    /* ---------- HERO HEADER ---------- */
    .hero-header {{
        background: linear-gradient(120deg, #1A1030 0%, #14182B 45%, #0E1F2C 100%);
        border: 1px solid {COLORS['border']};
        border-radius: 22px;
        padding: 2.4rem 2.6rem;
        margin-bottom: 1.6rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 60px -20px rgba(124,92,255,0.25);
    }}
    .hero-header::before {{
        content: "";
        position: absolute;
        top: -60%; right: -10%;
        width: 420px; height: 420px;
        background: radial-gradient(circle, rgba(124,92,255,0.35) 0%, transparent 70%);
        pointer-events: none;
    }}
    .hero-eyebrow {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: {COLORS['accent_b']};
        background: rgba(34,211,238,0.08);
        border: 1px solid rgba(34,211,238,0.25);
        padding: 5px 12px;
        border-radius: 999px;
        margin-bottom: 14px;
    }}
    .hero-title {{
        font-size: 2.6rem;
        font-weight: 800;
        line-height: 1.05;
        margin: 0;
        background: linear-gradient(90deg, #FFFFFF 0%, #C9C3FF 55%, {COLORS['accent_b']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .hero-subtitle {{
        font-size: 1.02rem;
        color: {COLORS['text_muted']};
        margin-top: 10px;
        max-width: 560px;
    }}

    /* ---------- SEARCH BAR ---------- */
    div[data-testid="stTextInput"] input {{
        background: {COLORS['surface']} !important;
        border: 1.5px solid {COLORS['border']} !important;
        border-radius: 16px !important;
        color: {COLORS['text']} !important;
        padding: 0.9rem 1.2rem !important;
        font-size: 1rem !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }}
    div[data-testid="stTextInput"] input:focus {{
        border-color: {COLORS['accent_a']} !important;
        box-shadow: 0 0 0 4px rgba(124,92,255,0.15) !important;
    }}

    .stButton > button {{
        border-radius: 14px !important;
        font-weight: 600 !important;
        border: 1px solid {COLORS['border']} !important;
        padding: 0.65rem 1.3rem !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
    }}
    .stButton > button:hover {{
        transform: translateY(-1px);
        border-color: {COLORS['accent_a']} !important;
        box-shadow: 0 8px 24px -8px rgba(124,92,255,0.5);
    }}
    button[kind="primary"] {{
        background: linear-gradient(90deg, {COLORS['accent_a']}, {COLORS['accent_b']}) !important;
        color: #0A0D14 !important;
        border: none !important;
    }}

    /* ---------- METRIC CARDS ---------- */
    div[data-testid="stMetric"] {{
        background: {COLORS['surface']};
        border: 1px solid {COLORS['border']};
        border-radius: 16px;
        padding: 1rem 1.2rem 0.8rem 1.2rem;
        transition: border-color 0.2s ease, transform 0.2s ease;
    }}
    div[data-testid="stMetric"]:hover {{
        border-color: {COLORS['accent_a']};
        transform: translateY(-2px);
    }}
    div[data-testid="stMetricLabel"] {{
        color: {COLORS['text_muted']} !important;
        font-size: 0.78rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}

    /* ---------- PRODUCT CARD ---------- */
    .product-card {{
        background: linear-gradient(180deg, {COLORS['surface']} 0%, {COLORS['surface_2']} 100%);
        border: 1px solid {COLORS['border']};
        border-radius: 18px;
        padding: 1.3rem 1.4rem;
        margin-bottom: 1rem;
        transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
        height: 100%;
    }}
    .product-card:hover {{
        transform: translateY(-4px);
        border-color: rgba(124,92,255,0.45);
        box-shadow: 0 16px 40px -12px rgba(124,92,255,0.30);
    }}
    .product-name {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 700;
        font-size: 1.05rem;
        margin-bottom: 0.5rem;
        color: {COLORS['text']};
    }}
    .price-row {{
        display: flex;
        align-items: baseline;
        gap: 10px;
        margin: 0.4rem 0 0.2rem 0;
    }}
    .price-current {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.35rem;
        font-weight: 700;
        color: {COLORS['green']};
    }}
    .price-original {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.92rem;
        color: {COLORS['text_muted']};
        text-decoration: line-through;
    }}
    .discount-badge {{
        display: inline-block;
        background: rgba(52,211,153,0.12);
        color: {COLORS['green']};
        border: 1px solid rgba(52,211,153,0.3);
        font-size: 0.74rem;
        font-weight: 600;
        padding: 2px 9px;
        border-radius: 999px;
        margin-left: 4px;
    }}
    .rating-row {{
        margin-top: 0.6rem;
        font-size: 0.9rem;
        color: {COLORS['gold']};
    }}
    .rating-count {{
        color: {COLORS['text_muted']};
        font-size: 0.8rem;
        margin-left: 4px;
    }}
    .sim-label {{
        font-size: 0.74rem;
        color: {COLORS['text_muted']};
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-top: 0.8rem;
        margin-bottom: 2px;
    }}

    /* progress bar restyle */
    div[data-testid="stProgress"] > div > div {{
        background: linear-gradient(90deg, {COLORS['accent_a']}, {COLORS['accent_b']}) !important;
    }}

    /* ---------- SIDEBAR ---------- */
    section[data-testid="stSidebar"] {{
        background: {COLORS['bg_alt']};
        border-right: 1px solid {COLORS['border']};
    }}
    .sidebar-brand {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 800;
        font-size: 1.3rem;
        background: linear-gradient(90deg, #FFFFFF, {COLORS['accent_b']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2px;
    }}
    .status-pill {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: {COLORS['surface']};
        border: 1px solid {COLORS['border']};
        border-radius: 10px;
        padding: 7px 12px;
        margin-bottom: 6px;
        font-size: 0.84rem;
    }}
    .dot {{
        width: 8px; height: 8px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 6px;
    }}
    .dot-green {{ background: {COLORS['green']}; box-shadow: 0 0 8px {COLORS['green']}; }}
    .dot-red {{ background: {COLORS['red']}; box-shadow: 0 0 8px {COLORS['red']}; }}
    .dot-gray {{ background: #4B5263; }}

    .history-chip {{
        background: {COLORS['surface']};
        border: 1px solid {COLORS['border']};
        border-radius: 10px;
        padding: 6px 10px;
        font-size: 0.82rem;
        margin-bottom: 5px;
        color: {COLORS['text_muted']};
    }}

    /* ---------- SECTION HEADERS ---------- */
    .section-title {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 700;
        font-size: 1.15rem;
        margin: 1.6rem 0 0.8rem 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    /* ---------- FOOTER ---------- */
    .app-footer {{
        margin-top: 3rem;
        padding: 1.4rem 0 0.6rem 0;
        border-top: 1px solid {COLORS['border']};
        text-align: center;
        color: {COLORS['text_muted']};
        font-size: 0.85rem;
    }}
    .stack-pill {{
        display: inline-block;
        background: {COLORS['surface']};
        border: 1px solid {COLORS['border']};
        border-radius: 999px;
        padding: 4px 12px;
        margin: 0 4px;
        font-size: 0.78rem;
        color: {COLORS['text_muted']};
    }}

    /* chat bubble tweak */
    div[data-testid="stChatMessage"] {{
        background: {COLORS['surface']} !important;
        border: 1px solid {COLORS['border']} !important;
        border-radius: 16px !important;
    }}

    @media (max-width: 768px) {{
        .hero-title {{ font-size: 1.8rem; }}
        .hero-header {{ padding: 1.6rem 1.4rem; }}
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# ============================================================
# SESSION STATE INIT
# ============================================================

def init_session_state():
    defaults = {
        "search_history": [],
        "chat_history": [],
        "current_results": None,
        "search_query": "",
        "is_searching": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ============================================================
# BACKEND HELPERS
# ============================================================

def check_backend_health():
    """Pings /health to determine if the backend is reachable."""
    try:
        resp = requests.get(f"{API_BASE_URL}/health", timeout=3)
        if resp.status_code == 200:
            return True, resp.json()
        return False, None
    except requests.exceptions.RequestException:
        return False, None


def get_backend_info():
    """Calls /info for service metadata (used for sidebar status)."""
    try:
        resp = requests.get(f"{API_BASE_URL}/info", timeout=3)
        if resp.status_code == 200:
            return resp.json()
        return None
    except requests.exceptions.RequestException:
        return None


def call_search_api(query, top_k=5):
    """Calls POST /search with the user's query. Returns (success, data/error)."""
    try:
        resp = requests.post(
            f"{API_BASE_URL}/search",
            json={"query": query, "top_k": top_k},
            timeout=30,
        )
        if resp.status_code == 200:
            return True, resp.json()
        return False, f"Backend returned status {resp.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Could not connect to the backend. Is FastAPI running?"
    except requests.exceptions.Timeout:
        return False, "The request timed out. Please try again."
    except requests.exceptions.RequestException as exc:
        return False, str(exc)


# ============================================================
# UI HELPER FUNCTIONS
# ============================================================

def render_hero():
    st.markdown(
        f"""
        <div class="hero-header">
            <span class="hero-eyebrow">🛒 RAG-Powered Retail Intelligence</span>
            <h1 class="hero-title">ShopMind AI</h1>
            <p class="hero-subtitle">
                Your AI shopping assistant — ask in plain language, get semantically
                ranked products and a natural-language recommendation, instantly.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stars(rating):
    """Returns a star-rating string for a given numeric rating."""
    try:
        rating = float(rating)
    except (TypeError, ValueError):
        return "—"
    full_stars = int(rating)
    half_star = (rating - full_stars) >= 0.5
    stars = "★" * full_stars
    if half_star:
        stars += "✬"
    stars += "☆" * (5 - full_stars - (1 if half_star else 0))
    return stars


def render_metrics(products):
    """Displays the top-of-page summary metrics."""
    col1, col2, col3, col4 = st.columns(4)

    total = len(products)
    avg_rating = sum(float(p.get("rating", 0) or 0) for p in products) / total if total else 0
    max_similarity = max((float(p.get("similarity_score", 0) or 0) for p in products), default=0)
    avg_discount = sum(float(p.get("discount_percentage", 0) or 0) for p in products) / total if total else 0

    with col1:
        st.metric("Products Retrieved", total)
    with col2:
        st.metric("Average Rating", f"{avg_rating:.1f} ★")
    with col3:
        st.metric("Highest Similarity", f"{max_similarity * 100:.0f}%")
    with col4:
        st.metric("Average Discount", f"{avg_discount:.0f}%")


def render_product_card(product):
    """Renders a single product inside a styled card."""
    name = product.get("product_name", "Unnamed product")
    current_price = product.get("discounted_price", 0)
    original_price = product.get("actual_price", 0)
    discount = product.get("discount_percentage", 0)
    rating = product.get("rating", 0)
    rating_count = product.get("rating_count", 0)
    similarity = float(product.get("similarity_score", 0) or 0)

    st.markdown(
        f"""
        <div class="product-card">
            <div class="product-name">{name}</div>
            <div class="price-row">
                <span class="price-current">₹{current_price:,.0f}</span>
                <span class="price-original">₹{original_price:,.0f}</span>
                <span class="discount-badge">-{discount:.0f}%</span>
            </div>
            <div class="rating-row">
                {render_stars(rating)} {rating}
                <span class="rating-count">({rating_count:,} ratings)</span>
            </div>
            <div class="sim-label">Semantic match</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.progress(min(max(similarity, 0.0), 1.0), text=f"{similarity * 100:.1f}% match")


def render_product_grid(products):
    """Lays products out in a responsive 3-column grid of cards."""
    cols_per_row = 3
    for i in range(0, len(products), cols_per_row):
        row_products = products[i: i + cols_per_row]
        cols = st.columns(cols_per_row)
        for col, product in zip(cols, row_products):
            with col:
                render_product_card(product)


def render_comparison_table(products):
    """Builds and displays a comparison dataframe when 2+ products exist."""
    if len(products) < 2:
        return

    st.markdown('<div class="section-title">📊 Compare products</div>', unsafe_allow_html=True)

    df = pd.DataFrame([
        {
            "Product": p.get("product_name", "—"),
            "Price": f"₹{p.get('discounted_price', 0):,.0f}",
            "Discount": f"{p.get('discount_percentage', 0):.0f}%",
            "Rating": f"{p.get('rating', 0)} ★",
            "Similarity": f"{float(p.get('similarity_score', 0) or 0) * 100:.1f}%",
        }
        for p in products
    ])
    st.dataframe(df, use_container_width=True, hide_index=True)


def render_ai_response(query, response_text):
    """Displays the AI's natural-language answer in a chat bubble."""
    st.markdown('<div class="section-title">🤖 AI recommendation</div>', unsafe_allow_html=True)
    try:
        with st.chat_message("assistant"):
            st.write(response_text)
    except Exception:
        st.info(response_text)


def render_sidebar():
    """Renders the full sidebar: brand, nav, status, history, about."""
    with st.sidebar:
        st.markdown('<div class="sidebar-brand">🛒 ShopMind AI</div>', unsafe_allow_html=True)
        st.caption("AI Shopping Assistant Dashboard")
        st.divider()

        # ---- API STATUS ----
        st.markdown("**System status**")
        is_healthy, _ = check_backend_health()

        backend_dot = "dot-green" if is_healthy else "dot-red"
        backend_label = "Online" if is_healthy else "Offline"
        st.markdown(
            f"""<div class="status-pill"><span><span class="dot {backend_dot}"></span>FastAPI backend</span><span>{backend_label}</span></div>""",
            unsafe_allow_html=True,
        )

        # These three depend on backend internals we can't query directly;
        # show as "linked" (gray/green based on overall backend reachability)
        sub_dot = "dot-green" if is_healthy else "dot-gray"
        sub_label = "Connected" if is_healthy else "Unknown"
        for service in ["Pinecone vector DB", "OpenRouter LLM", "Embedding model"]:
            st.markdown(
                f"""<div class="status-pill"><span><span class="dot {sub_dot}"></span>{service}</span><span>{sub_label}</span></div>""",
                unsafe_allow_html=True,
            )

        st.divider()

        # ---- SEARCH HISTORY ----
        st.markdown("**Search history**")
        if st.session_state.search_history:
            for past_query in reversed(st.session_state.search_history[-8:]):
                if st.button(f"🔎 {past_query}", key=f"hist_{past_query}_{len(st.session_state.search_history)}", use_container_width=True):
                    st.session_state.search_query = past_query
                    st.session_state.rerun_search = True
                    st.rerun()
        else:
            st.caption("No searches yet")

        st.divider()

        # ---- CHAT / CLEAR ----
        if st.button("🗑️ Clear chat & history", use_container_width=True):
            st.session_state.search_history = []
            st.session_state.chat_history = []
            st.session_state.current_results = None
            st.rerun()

        st.divider()

        # ---- ABOUT ----
        with st.expander("ℹ️ About this project"):
            st.write(
                "ShopMind AI is a RAG-powered shopping assistant. "
                "It retrieves semantically relevant products from a vector "
                "database and uses an LLM to generate a natural-language "
                "recommendation."
            )
        with st.expander("🧰 Technology stack"):
            st.write("- FastAPI\n- Pinecone\n- Sentence Transformers (MiniLM-L6-v2)\n- OpenRouter LLM\n- Streamlit")


def render_footer():
    st.markdown(
        f"""
        <div class="app-footer">
            Built with
            <span class="stack-pill">FastAPI</span>
            <span class="stack-pill">Pinecone</span>
            <span class="stack-pill">OpenRouter</span>
            <span class="stack-pill">Sentence Transformers</span>
            <span class="stack-pill">Streamlit</span>
            <br><br>
            © {datetime.now().year} ShopMind AI — AI Powered Shopping Assistant
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# MAIN APP
# ============================================================

def main():
    inject_custom_css()
    init_session_state()
    render_sidebar()
    render_hero()

    # ---- SEARCH BAR ----
    search_col, btn_col, clear_col = st.columns([5, 1, 1])
    with search_col:
        query = st.text_input(
            "Search",
            value=st.session_state.search_query,
            placeholder="Search for Gaming Laptop under ₹70000",
            label_visibility="collapsed",
        )
    with btn_col:
        search_clicked = st.button("Search", type="primary", use_container_width=True)
    with clear_col:
        clear_clicked = st.button("Clear", use_container_width=True)

    if clear_clicked:
        st.session_state.current_results = None
        st.session_state.search_query = ""
        st.rerun()

    should_search = search_clicked or st.session_state.pop("rerun_search", False)

    if should_search and query.strip():
        st.session_state.search_query = query.strip()
        with st.spinner("🔍 Searching products..."):
            success, data = call_search_api(query.strip())

        if not success:
            st.error(f"⚠️ {data}")
            st.session_state.current_results = None
        else:
            st.session_state.current_results = data
            if query.strip() not in st.session_state.search_history:
                st.session_state.search_history.append(query.strip())
            st.session_state.chat_history.append(
                {"query": query.strip(), "response": data.get("response", "")}
            )
    elif should_search:
        st.warning("Please enter a search query.")

    # ---- RESULTS ----
    results = st.session_state.current_results
    if results:
        products = results.get("products", [])

        if not products:
            st.info("No matching products found. Try a different search.")
        else:
            render_metrics(products)
            st.markdown('<div class="section-title">🛍️ Matching products</div>', unsafe_allow_html=True)
            render_product_grid(products)
            render_comparison_table(products)

            ai_text = results.get("response", "")
            if ai_text:
                render_ai_response(results.get("query", ""), ai_text)

                dl_col1, dl_col2 = st.columns(2)
                with dl_col1:
                    st.download_button(
                        "⬇️ Download AI response (TXT)",
                        data=ai_text,
                        file_name="shopmind_ai_response.txt",
                        mime="text/plain",
                        use_container_width=True,
                    )
                with dl_col2:
                    df_export = pd.DataFrame(products)
                    st.download_button(
                        "⬇️ Export products (CSV)",
                        data=df_export.to_csv(index=False),
                        file_name="shopmind_products.csv",
                        mime="text/csv",
                        use_container_width=True,
                    )
    else:
        st.info("👋 Start by searching for a product above — e.g. *\"Gaming Laptop under ₹70000\"*.")

    # ---- CHAT HISTORY ----
    if len(st.session_state.chat_history) > 1:
        with st.expander("💬 Previous AI conversations"):
            for turn in reversed(st.session_state.chat_history[:-1]):
                st.markdown(f"**You:** {turn['query']}")
                st.markdown(f"**ShopMind AI:** {turn['response']}")
                st.divider()

    render_footer()


if __name__ == "__main__":
    main()