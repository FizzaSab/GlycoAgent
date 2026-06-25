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
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.3rem;
        background: #ffffff;
        padding: 0.4rem 0.6rem;
        border-radius: 14px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1px solid #e2e8f0;
        margin-bottom: 1.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Inter', sans-serif;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        color: #1e293b !important;
        padding: 0.5rem 1.4rem !important;
        border-radius: 10px !important;
        transition: all 0.25s ease;
        background: transparent;
        letter-spacing: 0.01em;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: #f1f5f9;
        color: #0f172a !important;
        transform: translateY(-1px);
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #0f172a, #1e293b) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.2);
        font-weight: 700 !important;
        transform: translateY(-2px);
    }
    .ai-answer {
        background: #ffffff;
        padding: 1.5rem 1.8rem;
        border-radius: 16px;
        border: 2px solid #e2e8f0;
        margin: 0.5rem 0;
        border-left: 4px solid #818cf8;
        animation: fadeIn 0.5s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .ai-answer .answer-text {
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        color: #0f172a;
        line-height: 1.9;
        margin-bottom: 0.8rem;
    }
    .ai-answer .source-count {
        font-size: 0.7rem;
        color: #94a3b8;
        margin-top: 0.5rem;
        padding-top: 0.5rem;
        border-top: 1px solid #f1f5f9;
    }
    .footer-compact {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        padding: 0.6rem 2rem;
        border-radius: 12px 12px 0 0;
        margin-top: 2rem;
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: center;
        border-top: 3px solid transparent;
        border-image: linear-gradient(90deg, #818cf8, #c084fc) 1;
        gap: 0.5rem;
        min-height: 48px;
    }
    .footer-compact .footer-brand {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        flex-wrap: wrap;
        justify-content: center;
    }
    .footer-compact .footer-brand .org-icon {
        font-size: 1rem;
    }
    .footer-compact .footer-brand .org-name {
        color: #ffffff;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 0.75rem;
    }
    .footer-compact .footer-brand .org-name a {
        color: #a78bfa;
        text-decoration: none;
    }
    .footer-compact .footer-brand .org-name a:hover {
        text-decoration: underline;
    }
    .footer-compact .footer-brand .org-desc {
        color: rgba(255,255,255,0.3);
        font-family: 'Inter', sans-serif;
        font-size: 0.6rem;
    }
    .footer-compact .footer-brand .divider-dot {
        color: rgba(255,255,255,0.15);
        font-size: 0.5rem;
    }
    .footer-compact .footer-email-link {
        color: rgba(255,255,255,0.4);
        font-family: 'Inter', sans-serif;
        font-size: 0.65rem;
        text-decoration: none;
        transition: color 0.2s;
    }
    .footer-compact .footer-email-link:hover {
        color: #a78bfa;
        text-decoration: underline;
    }
    @media (max-width: 768px) {
        .footer-compact { padding: 0.6rem 1rem; }
        .footer-compact .footer-brand { gap: 0.4rem; }
        .header-content { flex-direction: column; align-items: flex-start; padding: 0 1rem; }
        .header-stats { flex-wrap: wrap; gap: 0.5rem; padding: 0.25rem 0.8rem; }
        .header-title { font-size: 1.2rem; }
        .stTabs [data-baseweb="tab"] { font-size: 0.75rem !important; padding: 0.4rem 0.8rem !important; }
    }
    .about-box {
        background: #ffffff;
        padding: 1.5rem 2rem;
        border-radius: 14px;
        border: 1px solid #e8ecf2;
        margin: 0.5rem 0;
    }
    .about-box h3 { color: #0f172a; font-family: 'Inter', sans-serif; font-weight: 600; font-size: 1.1rem; }
    .about-box p { color: #475569; font-family: 'Inter', sans-serif; font-size: 0.85rem; line-height: 1.6; }
    .about-box hr { border: none; border-top: 1px solid #e8ecf2; margin: 0.6rem 0; }
    .about-box .clickable-link {
        color: #6366f1;
        text-decoration: none;
        font-weight: 500;
    }
    .about-box .clickable-link:hover {
        text-decoration: underline;
    }
    .analytics-title {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        color: #0f172a !important;
        margin-bottom: 0.5rem;
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
    "I've been looking into this recently. Here's what I found:",
    "Excellent question! Let me break it down based on the research:"
]

HUMANIZED_ENDINGS = [
    "Hope that helps with your research! 😊",
    "Let me know if you'd like me to find specific papers!",
    "There's so much more to explore here - happy to chat more anytime!",
    "That's the beauty of glycoscience - there's always more to discover! 🧬"
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
                'overview': 'RRV (Relative Reactivity Value) measures donor reactivity. Aka measures acceptor reactivity.',
                'rrv_trends': ['Low RRV (1-10): High stereoselectivity', 'Medium RRV (10-50): Balanced', 'High RRV (50-500): Fast reactions'],
                'tuning': {'Temperature': 'Lower temperature increases selectivity', 'Solvent': 'DCM favors selectivity, THF favors reactivity'},
                'matching': {'Armed-Armed': 'Fast reaction, lower selectivity', 'Armed-Disarmed': 'Moderate, balanced', 'Disarmed-Armed': 'Slow, high selectivity'},
                'references': ['Crich et al., JACS (2022)', 'Boltje et al., Angew Chem (2023)']
            },
            'o-glycosylation': {
                'overview': 'O-glycosylation is the attachment of a sugar moiety to serine, threonine, or tyrosine residues.',
                'types': ['Mucin-type O-glycosylation', 'O-GlcNAcylation', 'O-fucosylation'],
                'references': ['Schjoldager et al., Nature Reviews (2020)']
            },
            'chemical_glycosylation': {
                'overview': 'Chemical glycosylation is the synthetic formation of glycosidic bonds.',
                'key_methods': {'Koenigs-Knorr': 'Uses glycosyl halides with heavy metal salts', 'Schmidt': 'Uses trichloroacetimidate donors', 'Thioglycoside': 'Uses S-glycosides'},
                'references': ['Yang et al., Chemical Reviews (2022)']
            },
            'remote_participation': {
                'overview': 'Remote participation is the influence of functional groups at positions other than C2.',
                'specific_examples': {'DPPA_group': 'Remote participating group for anti-facial N-glycosylation', 'pivaloyl_group': 'Alpha-directing effects from C-3 position'},
                'references': ['Wang et al., Chemical Reviews (2021)']
            }
        }
    
    def build_index(self):
        if len(self.papers) == 0:
            return
        for idx, row in self.papers.iterrows():
            title = str(row.get('Title', ''))
            abstract = str(row.get('Abstract', ''))
            year = str(row.get('Year', ''))
            journal = str(row.get('Journal', ''))
            topic = str(row.get('Topic', ''))
            url = str(row.get('URL', ''))
            terms = re.findall(r'\b[a-z]{3,}\b', f"{title.lower()} {abstract.lower()}")
            paper_data = {'title': title, 'abstract': abstract, 'year': year, 'journal': journal, 'topic': topic, 'url': url, 'terms': terms}
            self.index.append(paper_data)
            if topic:
                self.topic_index[topic.lower()].append(paper_data)
    
    def search(self, query, top_n=5):
        if len(self.index) == 0:
            return []
        query_terms = set(re.findall(r'\b[a-z]{3,}\b', query.lower()))
        scores = []
        for paper in self.index:
            matches = sum(1 for t in query_terms if t in paper['terms'])
            title_boost = sum(1 for t in query_terms if t in paper['title'].lower()) * 2
            score = matches + title_boost
            if score > 0:
                scores.append((score, paper))
        scores.sort(key=lambda x: x[0], reverse=True)
        return [p for _, p in scores[:top_n]]
    
    def answer_question(self, question):
        question_lower = question.lower()
        expert_response = self.get_expert_response(question_lower)
        relevant = self.search(question, top_n=5)
        combined_answer = self.combine_knowledge(question_lower, expert_response, relevant)
        return {'answer': combined_answer, 'references': self.get_references(question_lower, relevant), 'source_count': len(relevant)}
    
    def get_expert_response(self, question_lower):
        response_parts = []
        if any(term in question_lower for term in ['rrv', 'aka', 'reactivity']):
            knowledge = self.expert_knowledge.get('reactivity', {})
            if knowledge:
                parts = []
                if 'overview' in knowledge:
                    parts.append(knowledge['overview'])
                if 'rrv_trends' in knowledge:
                    parts.append('RRV trends: ' + '; '.join(knowledge['rrv_trends']))
                if 'tuning' in knowledge:
                    tuning_text = 'How to tune RRV:\n'
                    for method, desc in knowledge['tuning'].items():
                        tuning_text += f'  • {method}: {desc}\n'
                    parts.append(tuning_text)
                if 'matching' in knowledge:
                    match_text = 'RRV-Aka matching:\n'
                    for condition, outcome in knowledge['matching'].items():
                        match_text += f'  • {condition}: {outcome}\n'
                    parts.append(match_text)
                response_parts.append('\n\n'.join(parts))
        
        if any(term in question_lower for term in ['o-glycosylation', 'o-glycan']):
            knowledge = self.expert_knowledge.get('o-glycosylation', {})
            if knowledge:
                parts = []
                if 'overview' in knowledge:
                    parts.append(knowledge['overview'])
                if 'types' in knowledge:
                    parts.append('Types: ' + ', '.join(knowledge['types']))
                response_parts.append('\n\n'.join(parts))
        
        if any(term in question_lower for term in ['chemical glycosylation', 'koenigs-knorr', 'schmidt']):
            knowledge = self.expert_knowledge.get('chemical_glycosylation', {})
            if knowledge:
                parts = []
                if 'overview' in knowledge:
                    parts.append(knowledge['overview'])
                if 'key_methods' in knowledge:
                    method_text = 'Key methods:\n'
                    for name, desc in knowledge['key_methods'].items():
                        method_text += f'  • {name}: {desc}\n'
                    parts.append(method_text)
                response_parts.append('\n\n'.join(parts))
        
        if any(term in question_lower for term in ['remote participation', 'dppa', 'pivaloyl']):
            knowledge = self.expert_knowledge.get('remote_participation', {})
            if knowledge:
                parts = []
                if 'overview' in knowledge:
                    parts.append(knowledge['overview'])
                if 'specific_examples' in knowledge:
                    examples = knowledge['specific_examples']
                    parts.append('Specific examples:')
                    for name, desc in examples.items():
                        parts.append(f'  • {name}: {desc}')
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
    
    def get_references(self, question_lower, relevant_papers):
        references = []
        if any(term in question_lower for term in ['rrv', 'aka', 'reactivity']):
            refs = self.expert_knowledge.get('reactivity', {}).get('references', [])
            references.extend(refs[:3])
        if 'glycosylation' in question_lower:
            refs = self.expert_knowledge.get('chemical_glycosylation', {}).get('references', [])
            references.extend(refs[:2])
        for paper in relevant_papers[:2]:
            ref = f"{paper['title']} ({paper['year']}) - {paper['journal']}"
            references.append(ref)
        return references[:5]

# ─── DRAWING TOOL ──────────────────────────────────────
def chemical_drawing_tool():
    components.html("""
    <div style="padding:20px;border:2px solid #e2e8f0;border-radius:12px;background:white;">
        <h3 style="font-family:'Inter',sans-serif;">🧪 Draw Chemical Structure</h3>
        <div style="display:flex;gap:8px;flex-wrap:wrap;margin:10px 0;">
            <button onclick="addAtom('C')" style="padding:6px 14px;border:1px solid #e2e8f0;border-radius:6px;background:#0f172a;color:white;cursor:pointer;">C</button>
            <button onclick="addAtom('O')" style="padding:6px 14px;border:1px solid #e2e8f0;border-radius:6px;background:#f8fafc;cursor:pointer;">O</button>
            <button onclick="addAtom('N')" style="padding:6px 14px;border:1px solid #e2e8f0;border-radius:6px;background:#f8fafc;cursor:pointer;">N</button>
            <button onclick="clearCanvas()" style="padding:6px 14px;border:1px solid #fee2e2;border-radius:6px;background:#fee2e2;color:#991b1b;cursor:pointer;">🗑️ Clear</button>
        </div>
        <canvas id="molCanvas" width="700" height="400" style="border:2px solid #e2e8f0;border-radius:8px;width:100%;height:auto;cursor:crosshair;"></canvas>
    </div>
    <script>
        const canvas = document.getElementById('molCanvas');
        const ctx = canvas.getContext('2d');
        let atoms = [];
        let currentAtom = 'C';
        canvas.addEventListener('click', function(e) {
            const rect = canvas.getBoundingClientRect();
            const x = (e.clientX - rect.left) * (canvas.width / rect.width);
            const y = (e.clientY - rect.top) * (canvas.height / rect.height);
            atoms.push({x, y, label: currentAtom});
            draw();
        });
        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            atoms.forEach(a => {
                ctx.beginPath(); ctx.arc(a.x, a.y, 18, 0, Math.PI*2);
                ctx.fillStyle = '#f1f5f9'; ctx.fill();
                ctx.strokeStyle = '#1e293b'; ctx.lineWidth = 2; ctx.stroke();
                ctx.fillStyle = '#0f172a';
                ctx.font = 'bold 14px Inter, Arial, sans-serif';
                ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
                ctx.fillText(a.label, a.x, a.y);
            });
        }
        function addAtom(label) { currentAtom = label; }
        function clearCanvas() { atoms = []; draw(); }
        draw();
    </script>
    """, height=500)

# ─── HEADER ─────────────────────────────────────────────
def render_header():
    valid_years = papers['Year'].dropna() if len(papers) > 0 else []
    topics = papers['Topic'].dropna().unique() if len(papers) > 0 else []
    st.markdown(f"""
    <div class="header-wrapper">
        <div class="header-content">
            <div class="header-left">
                <div class="header-title-block">
                    <div class="header-title">🧬 Glyco<span>Search</span></div>
                    <div class="header-subtitle">Glycosylation Research · {len(papers)} Papers</div>
                </div>
            </div>
            <div class="header-right">
                <div class="header-stats">
                    <div class="stat-item">
                        <div class="stat-number">{len(papers) if len(papers) > 0 else 0}</div>
                        <div class="stat-label">Papers</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">{int(valid_years.min()) if len(valid_years) > 0 else '—'}–{int(valid_years.max()) if len(valid_years) > 0 else '—'}</div>
                        <div class="stat-label">Years</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">{len(topics) if len(topics) > 0 else 0}</div>
                        <div class="stat-label">Topics</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── CREATE COLORFUL CHARTS ─────────────────────────────
def create_colorful_bar_chart(data, title, color_scheme):
    if len(data) == 0:
        return None
    df = data.reset_index()
    df.columns = ['Category', 'Count']
    chart = alt.Chart(df).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
        x=alt.X('Category:N', sort='-y', title=None),
        y=alt.Y('Count:Q', title=None),
        color=alt.Color('Count:Q', scale=alt.Scale(scheme=color_scheme), legend=None),
        tooltip=['Category', 'Count']
    ).properties(height=300, title=title)
    return chart

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
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "🔍 Search", "💬 Ask AI", "📊 Analytics", "📚 Methods", "🧪 Draw", "⚙️ Settings", "📋 About"
    ])

    # ─── TAB 1: SEARCH ────────────────────────────────
    with tab1:
        st.markdown("### 🔎 Search Papers")
        keyword = st.text_input("Search papers", placeholder="e.g. glycosylation, RRV, Koenigs-Knorr")
        topics_list = ['All Topics'] + sorted(papers['Topic'].dropna().unique().tolist())
        selected_topic = st.selectbox("Filter by Topic", topics_list, index=0)
        if keyword:
            kw = keyword.lower()
            mask = (papers['Title'].astype(str).str.lower().str.contains(kw, na=False) | 
                    papers['Abstract'].astype(str).str.lower().str.contains(kw, na=False))
            if selected_topic != 'All Topics':
                mask = mask & (papers['Topic'] == selected_topic)
            results = papers[mask].copy()
            st.write(f"Found {len(results)} papers")
            for _, row in results.head(20).iterrows():
                title = str(row.get('Title', 'No title'))
                year = str(row.get('Year', '?'))
                journal = str(row.get('Journal', '?'))
                topic = str(row.get('Topic', '?'))
                with st.expander(f"📄 {title[:80]}..."):
                    st.write(f"**Year:** {year} | **Journal:** {journal} | **Topic:** {topic}")

    # ─── TAB 2: ASK AI ──────────────────────────────────
    with tab2:
        st.markdown("### 💬 Ask GlycoAI")
        st.markdown("Ask about RRV, Aka, glycosylation methods, and more!")
        example_questions = [
            "How does RRV affect glycosylation selectivity?",
            "What is O-glycosylation?",
            "How does remote participation work?",
            "What are the best glycosylation methods?"
        ]
        cols = st.columns(2)
        for i, q in enumerate(example_questions):
            if cols[i % 2].button(f"💡 {q}", key=f"ex_{i}"):
                st.session_state['ask_question'] = q
                st.rerun()
        question = st.text_area("Type your question:", value=st.session_state.get('ask_question', ''), height=80)
        if st.button("🔍 Ask", type="primary"):
            if question:
                with st.spinner("Searching..."):
                    result = engine.answer_question(question)
                st.markdown(f'<div class="ai-answer"><div class="answer-text">{result["answer"]}</div><div class="source-count">📚 Based on {result["source_count"]} sources</div></div>', unsafe_allow_html=True)
                if result['references']:
                    st.markdown("**📖 References:**")
                    for ref in result['references']:
                        st.markdown(f"- {ref}")
            else:
                st.warning("Please enter a question.")

    # ─── TAB 3: ANALYTICS ──────────────────────────────
    with tab3:
        st.markdown('<p class="analytics-title">📊 Research Analytics</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            year_counts = papers['Year'].value_counts().sort_index()
            if len(year_counts) > 0:
                chart = create_colorful_bar_chart(year_counts, "📅 Publications by Year", "viridis")
                if chart:
                    st.altair_chart(chart, use_container_width=True)
        with col2:
            topic_counts = papers['Topic'].value_counts()
            if len(topic_counts) > 0:
                chart = create_colorful_bar_chart(topic_counts.head(10), "📂 Papers by Topic", "plasma")
                if chart:
                    st.altair_chart(chart, use_container_width=True)
        st.markdown("---")
        st.markdown('<p class="analytics-title">🏆 Top Journals</p>', unsafe_allow_html=True)
        journal_counts = papers['Journal'].value_counts().head(10)
        if len(journal_counts) > 0:
            st.dataframe(journal_counts.reset_index().rename(columns={'index': 'Journal', 'Journal': 'Count'}), use_container_width=True, hide_index=True)

    # ─── TAB 4: METHODS ─────────────────────────────────
    with tab4:
        st.markdown("### 📚 Glycosylation Methods Reference")
        st.markdown("""
        **Key Terms:**
        - **RRV**: Relative Reactivity Value - measures donor reactivity
        - **Aka**: Acceptor reactivity parameter
        - **NGP**: Neighboring Group Participation
        - **TMSOTf**: Common Lewis acid activator
        - **Koenigs-Knorr**: Classic glycosylation method using glycosyl halides
        - **Schmidt**: Trichloroacetimidate method with Lewis acids
        - **Thioglycoside**: S-glycosides activated by thiophilic promoters
        """)

    # ─── TAB 5: DRAW ────────────────────────────────────
    with tab5:
        chemical_drawing_tool()

    # ─── TAB 6: SETTINGS ────────────────────────────────
    with tab6:
        st.markdown("### ⚙️ Settings")
        if st.button("🔄 Reload Data"):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.rerun()
        st.code(f"Papers: {len(papers)}")
        st.code(f"Topics: {papers['Topic'].nunique() if len(papers) > 0 else 0}")
        st.code("Knowledge: RRV, Aka, O-Glycosylation, Chemical Glycosylation, Remote Participation")

    # ─── TAB 7: ABOUT ────────────────────────────────────
    with tab7:
        st.markdown("""
        <div class="about-box">
            <h3>🧬 GlycoSearch</h3>
            <p><b>Developed by:</b> Fizza Sabbor and Dr. Sabbor Hussain</p>
            <p><b>Institute:</b> <a href="https://www.chem.sinica.edu.tw" target="_blank" class="clickable-link">Institute of Chemistry, Academia Sinica</a></p>
            <p><b>Principal Investigator:</b> <a href="https://www.chem.sinica.edu.tw/en/faculty/104/" target="_blank" class="clickable-link">Dr. Cheng-Chung Wang</a></p>
            <hr>
            <h4>🧪 Knowledge Base</h4>
            <ul>
                <li><b>RRV & Aka</b> - Reactivity parameters for donors and acceptors</li>
                <li><b>O-Glycosylation</b> - Biological significance and types</li>
                <li><b>Chemical Glycosylation</b> - Key methods and advances</li>
                <li><b>Remote Participation</b> - Mechanisms and examples</li>
            </ul>
            <h4>📚 Data</h4>
            <p>1,676+ glycosylation research papers from PubMed (1967-2026)</p>
        </div>
        """, unsafe_allow_html=True)

# ─── COMPACT FOOTER ────────────────────────────────────────
st.markdown("""
<div class="footer-compact">
    <div class="footer-brand">
        <span class="org-icon">🏛️</span>
        <span class="org-name">
            <a href="https://www.chem.sinica.edu.tw" target="_blank">Institute of Chemistry, Academia Sinica</a>
            <span class="org-desc">· Fizza Sabbor & Dr. Sabbor Hussain</span>
        </span>
        <span class="divider-dot">·</span>
        <a href="mailto:wangcc7280@gate.sinica.edu.tw" class="footer-email-link">wangcc7280@gate.sinica.edu.tw</a>
    </div>
</div>
""", unsafe_allow_html=True)
