import streamlit as st
import pandas as pd
import os
import streamlit.components.v1 as components
from datetime import datetime
import csv
import re
from collections import defaultdict
import altair as alt
import random

# ─── PAGE CONFIG ──────────────────────────────────────────
st.set_page_config(
    page_title="GlycoSearch - Glycosylation Research Agent",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── CUSTOM CSS ──────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    .stApp { background: #f5f7fb; }
    
    .header-wrapper {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 1rem 0 0.8rem 0;
        border-radius: 0 0 30px 30px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(15, 23, 42, 0.12);
        position: relative;
        overflow: hidden;
    }
    
    .header-wrapper::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #818cf8, #c084fc, #f472b6);
    }
    
    .header-content {
        position: relative;
        z-index: 1;
        display: flex;
        align-items: center;
        justify-content: space-between;
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 2rem;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    
    .header-left {
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }
    
    .logo-box {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.05rem;
        padding: 0.1rem 0.8rem 0.1rem 0.4rem;
    }
    
    .logo-label {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 0.5rem;
        color: rgba(255,255,255,0.35);
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-top: 0.05rem;
    }
    
    .header-title-block {
        display: flex;
        flex-direction: column;
    }
    
    .header-title {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 1.5rem;
        color: #ffffff;
        letter-spacing: -0.02em;
        margin: 0;
        line-height: 1.2;
    }
    
    .header-title span {
        background: linear-gradient(135deg, #a78bfa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .header-subtitle {
        font-family: 'Inter', sans-serif;
        font-weight: 300;
        font-size: 0.7rem;
        color: rgba(255, 255, 255, 0.35);
        letter-spacing: 0.04em;
    }
    
    .header-right {
        display: flex;
        align-items: center;
        gap: 1rem;
        flex-wrap: wrap;
    }
    
    .header-stats {
        display: flex;
        gap: 1.2rem;
        background: rgba(255, 255, 255, 0.04);
        padding: 0.25rem 1rem;
        border-radius: 50px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .stat-item {
        text-align: center;
        padding: 0.1rem 0.2rem;
    }
    
    .stat-number {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.95rem;
        color: #ffffff;
    }
    
    .stat-label {
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        font-size: 0.5rem;
        color: rgba(255, 255, 255, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
</style>
""", unsafe_allow_html=True)

# ─── LOAD DATA ──────────────────────────────────────────
@st.cache_data
def load_data():
    excel_files = [f for f in os.listdir('.') if f.endswith('.xlsx')]
    if excel_files:
        try:
            return pd.read_excel(excel_files[0], sheet_name='All Papers')
        except:
            return pd.DataFrame()
    return pd.DataFrame()

papers = load_data()

# ─── HUMANIZED RESPONSES ─────────────────────────────────
HUMANIZED_INTROS = [
    "That's a really interesting question! Let me share what I've learned:",
    "Great question! Here's what I've gathered from the literature:",
]

HUMANIZED_ENDINGS = [
    "Hope that helps with your research! 😊",
    "Let me know if you'd like me to find specific papers!",
]

FALLBACK_RESPONSES = [
    "Hmm, that's a tricky one! Could you ask it differently? 😊",
    "I'm not quite sure about that. Maybe we can explore a related topic?"
]

# ─── RAG KNOWLEDGE ENGINE ──────────────────────────────
class GlycoKnowledgeEngine:
    def __init__(self, papers_df):
        self.papers = papers_df
        self.index = []
        self.topic_index = defaultdict(list)
        self.keyword_index = defaultdict(list)
        self.build_index()
        self.build_expert_knowledge()
    
    def build_expert_knowledge(self):
        self.expert_knowledge = {
            'reactivity': {
                'overview': 'RRV measures donor reactivity. Aka measures acceptor reactivity.',
                'rrv_trends': ['Low RRV (1-10): High selectivity', 'Medium RRV (10-50): Balanced', 'High RRV (50-500): Fast reactions'],
                'tuning': {'Temperature': 'Lower temp increases selectivity', 'Solvent': 'DCM favors selectivity'},
                'matching': {'Armed-Armed': 'Fast reaction', 'Armed-Disarmed': 'Moderate', 'Disarmed-Armed': 'Slow but selective'},
                'references': ['Crich JACS 2022', 'Boltje Angew 2023']
            }
        }
    
    def build_index(self):
        if len(self.papers) == 0:
            return
        for idx, row in self.papers.iterrows():
            title = str(row.get('Title', ''))
            abstract = str(row.get('Abstract', ''))
            terms = re.findall(r'\b[a-z]{3,}\b', f"{title.lower()} {abstract.lower()}")
            paper_data = {'title': title, 'abstract': abstract, 'terms': terms}
            self.index.append(paper_data)
    
    def search(self, query, top_n=5):
        if len(self.index) == 0:
            return []
        query_terms = set(re.findall(r'\b[a-z]{3,}\b', query.lower()))
        scores = []
        for paper in self.index:
            matches = sum(1 for t in query_terms if t in paper['terms'])
            if matches > 0:
                scores.append((matches, paper))
        scores.sort(key=lambda x: x[0], reverse=True)
        return [p for _, p in scores[:top_n]]
    
    def answer_question(self, question):
        question_lower = question.lower()
        expert_response = self.get_expert_response(question_lower)
        relevant = self.search(question, top_n=5)
        combined_answer = self.combine_knowledge(question_lower, expert_response, relevant)
        return {'answer': combined_answer, 'references': [], 'source_count': len(relevant)}
    
    def get_expert_response(self, question_lower):
        response_parts = []
        if any(term in question_lower for term in ['rrv', 'aka', 'reactivity']):
            knowledge = self.expert_knowledge.get('reactivity', {})
            if knowledge:
                parts = []
                if 'overview' in knowledge:
                    parts.append(knowledge['overview'])
                if 'rrv_trends' in knowledge:
                    parts.append('Trends: ' + '; '.join(knowledge['rrv_trends']))
                response_parts.append('\n\n'.join(parts))
        return '\n\n'.join(response_parts) if response_parts else None
    
    def combine_knowledge(self, question_lower, expert_response, relevant_papers):
        if not expert_response and not relevant_papers:
            return random.choice(FALLBACK_RESPONSES)
        answer_parts = []
        if expert_response:
            intro = random.choice(HUMANIZED_INTROS)
            answer_parts.append(f"{intro}\n\n{expert_response}")
        ending = random.choice(HUMANIZED_ENDINGS)
        answer_parts.append(f"\n\n{ending}")
        return '\n'.join(answer_parts)

# ─── HEADER ─────────────────────────────────────────────
def render_header():
    st.markdown(f"""
    <div class="header-wrapper">
        <div class="header-content">
            <div class="header-left">
                <div class="header-title-block">
                    <div class="header-title">🧬 Glyco<span>Search</span></div>
                    <div class="header-subtitle">Glycosylation Research · {len(papers)} Papers</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── MAIN ──────────────────────────────────────────────
if len(papers) == 0:
    st.warning("📁 Upload your Excel file to get started")
    uploaded = st.file_uploader("Choose Excel file", type=['xlsx'])
    if uploaded:
        papers = pd.read_excel(uploaded, sheet_name='All Papers')
        st.rerun()
else:
    render_header()
    
    @st.cache_resource
    def get_knowledge_engine():
        return GlycoKnowledgeEngine(papers)
    
    engine = get_knowledge_engine()
    
    tab1, tab2 = st.tabs(["🔍 Search", "💬 Ask AI"])
    
    with tab1:
        st.markdown("### 🔎 Search Papers")
        keyword = st.text_input("Search papers", placeholder="e.g. glycosylation, RRV")
        if keyword:
            results = [p for p in engine.index if keyword.lower() in p['title'].lower()]
            st.write(f"Found {len(results)} papers")
            for paper in results[:10]:
                st.write(f"📄 {paper['title']}")
    
    with tab2:
        st.markdown("### 💬 Ask GlycoAI")
        question = st.text_area("Type your question:", placeholder="e.g., How does RRV affect selectivity?")
        if st.button("🔍 Ask"):
            if question:
                with st.spinner("Searching..."):
                    result = engine.answer_question(question)
                st.markdown(f'<div class="ai-answer"><div class="answer-text">{result["answer"]}</div></div>', unsafe_allow_html=True)
            else:
                st.warning("Please enter a question.")

# ─── FOOTER ─────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:1rem;color:#94a3b8;font-size:0.8rem;">
    Fizza Sabbor & Dr. Sabbor Hussain · Institute of Chemistry, Academia Sinica
</div>
""", unsafe_allow_html=True)
