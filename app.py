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
import json
import numpy as np
import qrcode
from io import BytesIO
from PIL import Image
import base64
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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
    .header-left { display: flex; align-items: center; gap: 0.8rem; }
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
    .header-title-block { display: flex; flex-direction: column; }
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
    .header-right { display: flex; align-items: center; gap: 1rem; flex-wrap: wrap; }
    .header-stats {
        display: flex;
        gap: 1.2rem;
        background: rgba(255, 255, 255, 0.04);
        padding: 0.25rem 1rem;
        border-radius: 50px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .stat-item { text-align: center; padding: 0.1rem 0.2rem; }
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
        flex-wrap: wrap;
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
    .decision-card {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        margin: 0.5rem 0;
        transition: all 0.3s;
    }
    .decision-card:hover {
        border-color: #818cf8;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.1);
    }
    .priority-high {
        background: #fee2e2 !important;
        color: #991b1b !important;
        padding: 2px 10px !important;
        border-radius: 50px !important;
        font-size: 0.7rem !important;
        font-weight: 600 !important;
        display: inline-block !important;
    }
    .priority-medium {
        background: #fef3c7 !important;
        color: #92400e !important;
        padding: 2px 10px !important;
        border-radius: 50px !important;
        font-size: 0.7rem !important;
        font-weight: 600 !important;
        display: inline-block !important;
    }
    .priority-low {
        background: #dbeafe !important;
        color: #1e40af !important;
        padding: 2px 10px !important;
        border-radius: 50px !important;
        font-size: 0.7rem !important;
        font-weight: 600 !important;
        display: inline-block !important;
    }
    .draw-container {
        overflow: auto;
        max-height: 680px;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 15px;
        background: white;
        position: relative;
    }
    .draw-container::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    .draw-container::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 5px;
    }
    .draw-container::-webkit-scrollbar-thumb {
        background: #c7d2fe;
        border-radius: 5px;
    }
    .draw-container::-webkit-scrollbar-thumb:hover {
        background: #818cf8;
    }
    .zoom-controls {
        position: sticky;
        bottom: 0;
        background: rgba(255,255,255,0.95);
        padding: 8px;
        border-top: 1px solid #e2e8f0;
        display: flex;
        gap: 8px;
        align-items: center;
        justify-content: center;
        z-index: 100;
        backdrop-filter: blur(10px);
    }
    .zoom-controls button {
        padding: 4px 12px;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        background: #f8fafc;
        cursor: pointer;
        font-family: 'Inter', sans-serif;
        font-size: 12px;
        transition: all 0.2s;
    }
    .zoom-controls button:hover {
        background: #eef2ff;
        border-color: #818cf8;
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
    .footer-compact .footer-brand .org-icon { font-size: 1rem; }
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
    .footer-compact .footer-brand .org-name a:hover { text-decoration: underline; }
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
    .about-box .clickable-link:hover { text-decoration: underline; }
    .analytics-title {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        color: #0f172a !important;
        margin-bottom: 0.5rem;
    }
    .qr-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        border: 2px solid #e2e8f0;
        text-align: center;
        max-width: 450px;
        margin: 0 auto;
    }
    .qr-card img {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        max-width: 100%;
    }
    .draw-header { 
        background: linear-gradient(135deg, #f8fafc, #eef2ff); 
        border: 2px solid #e2e8f0; 
        border-radius: 14px; 
        padding: 1rem 1.5rem; 
        margin-bottom: 0.8rem; 
        text-align: center; 
    }
    .draw-header h2 { 
        font-family: 'Inter', sans-serif; 
        font-weight: 700; 
        font-size: 1.3rem; 
        color: #0f172a; 
        margin: 0; 
    }
    .draw-header h2 span { 
        background: linear-gradient(135deg, #6366f1, #a78bfa); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
    }
    .draw-header p { 
        font-family: 'Inter', sans-serif; 
        font-size: 0.8rem; 
        color: #64748b; 
        margin: 0.2rem 0 0 0; 
    }
    .draw-toolbar { 
        display: flex; 
        gap: 4px; 
        padding: 6px 0; 
        flex-wrap: wrap; 
        align-items: center; 
    }
    .draw-toolbar button { 
        padding: 4px 10px; 
        border: none; 
        border-radius: 6px; 
        background: #f1f5f9; 
        color: #0f172a; 
        cursor: pointer; 
        font-size: 11px; 
        font-family: 'Inter', sans-serif; 
        font-weight: 500; 
        transition: all 0.2s; 
    }
    .draw-toolbar button:hover { background: #e2e8f0; }
    .draw-toolbar button.active { background: #0f172a; color: white; }
    .draw-toolbar button.danger { background: #fee2e2; color: #991b1b; }
    .draw-toolbar button.success { background: #dcfce7; color: #166534; }
    .draw-toolbar button.warning { background: #fef3c7; color: #92400e; }
    .draw-toolbar button.info { background: #dbeafe; color: #1e40af; }
    .draw-toolbar button.purple { background: #f3e8ff; color: #6b21a8; }
    .draw-toolbar select { 
        padding: 4px 8px; 
        border-radius: 6px; 
        border: 1px solid #e2e8f0; 
        font-size: 11px; 
        font-family: 'Inter', sans-serif; 
        background: white; 
    }
    @media (max-width: 768px) {
        .footer-compact { padding: 0.6rem 1rem; }
        .footer-compact .footer-brand { gap: 0.4rem; }
        .header-content { flex-direction: column; align-items: flex-start; padding: 0 1rem; }
        .header-stats { flex-wrap: wrap; gap: 0.5rem; padding: 0.25rem 0.8rem; }
        .header-title { font-size: 1.2rem; }
        .stTabs [data-baseweb="tab"] { font-size: 0.75rem !important; padding: 0.4rem 0.8rem !important; }
    }
</style>
""", unsafe_allow_html=True)

# ─── LOAD DATA ──────────────────────────────────────────
@st.cache_data
def load_data():
    excel_files = [f for f in os.listdir('.') if f.endswith('.xlsx')]
    if excel_files:
        for f in excel_files:
            if 'enhanced' in f:
                try:
                    return pd.read_excel(f, sheet_name='All Papers')
                except:
                    pass
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
    "There's so much more to explore here - happy to chat more!",
    "That's the beauty of glycoscience - always more to discover! 🧬"
]

FALLBACK_RESPONSES = [
    "Hmm, that's a tricky one! Could you ask it differently? 😊",
    "I'm not quite sure about that. Maybe we can explore a related topic?"
]

# ─── REACTION SCREENING KNOWLEDGE ──────────────────────
REACTION_SCREENING_KNOWLEDGE = {
    'donors': {
        'Trichloroacetimidate': {'rrv': 30, 'cost': 'Low', 'availability': 'High', 'selectivity': 'β (C2-acyl)'},
        'Thioglycoside (STol)': {'rrv': 5, 'cost': 'Medium', 'availability': 'High', 'selectivity': 'Tunable'},
        'Thioglycoside (SEt)': {'rrv': 2, 'cost': 'Medium', 'availability': 'High', 'selectivity': 'β'},
        'Glycosyl Bromide': {'rrv': 80, 'cost': 'Low', 'availability': 'Medium', 'selectivity': 'α/β (NGP)'},
        'Glycosyl Iodide': {'rrv': 300, 'cost': 'Medium', 'availability': 'Low', 'selectivity': 'Varies'},
        'Glycosyl Phosphate': {'rrv': 1, 'cost': 'High', 'availability': 'Low', 'selectivity': 'β'},
        'Glycosyl Fluoride': {'rrv': 0.5, 'cost': 'High', 'availability': 'Medium', 'selectivity': 'Varies'},
        'Sulfoxide (Kahne)': {'rrv': 20, 'cost': 'Medium', 'availability': 'Medium', 'selectivity': 'α'},
        'n-Pentenyl': {'rrv': 5, 'cost': 'Medium', 'availability': 'Medium', 'selectivity': 'Varies'},
        'Boronate': {'rrv': 0.3, 'cost': 'High', 'availability': 'Low', 'selectivity': 'β'}
    },
    'acceptors': {
        'Primary OH (6-OH)': {'aka': 8, 'hindrance': 'Low', 'reactivity': 'High'},
        'Secondary OH (4-OH)': {'aka': 5, 'hindrance': 'Medium', 'reactivity': 'High'},
        'Secondary OH (3-OH)': {'aka': 4, 'hindrance': 'Medium', 'reactivity': 'Moderate'},
        'Secondary OH (2-OH)': {'aka': 1, 'hindrance': 'High', 'reactivity': 'Low'},
        'Tertiary OH': {'aka': -5, 'hindrance': 'Very High', 'reactivity': 'Very Low'},
        'Diol': {'aka': 6, 'hindrance': 'Low', 'reactivity': 'High'},
        'Triol': {'aka': 4, 'hindrance': 'Medium', 'reactivity': 'Moderate'}
    },
    'conditions': {
        'Koenigs-Knorr': {'temp': '0°C to RT', 'time': '2-24h', 'yield': '60-95%', 'compatibility': 'Acid-sensitive'},
        'Schmidt': {'temp': '−40°C to RT', 'time': '1-6h', 'yield': '70-98%', 'compatibility': 'Most substrates'},
        'Thioglycoside': {'temp': '−78°C to RT', 'time': '1-12h', 'yield': '65-95%', 'compatibility': 'Most substrates'},
        'Phosphate': {'temp': '−78°C', 'time': '1-4h', 'yield': '60-90%', 'compatibility': 'Acid-sensitive'},
        'Sulfoxide': {'temp': '−78°C', 'time': '1-2h', 'yield': '70-95%', 'compatibility': 'Acid-sensitive'}
    },
    'screening_rules': [
        'Start with high RRV donors for challenging acceptors',
        'Use low RRV donors for highly reactive acceptors',
        'Match donor reactivity (RRV) with acceptor reactivity (Aka)',
        'For β-selectivity: use C2-acyl donors (Schmidt, Koenigs-Knorr)',
        'For α-selectivity: use C2-ether donors or Sulfoxide method',
        'Test 2-3 donors with different reactivity levels first',
        'Optimize temperature: lower for selectivity, higher for reactivity',
        'Screen solvents: DCM (standard), THF, MeCN, Toluene'
    ]
}

# ─── QR CODE GENERATOR ──────────────────────────────────
def generate_qr_code(data, app_name="GlycoSearch", institute="Academia Sinica"):
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,
        border=3,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#0f172a", back_color="white").convert('RGB')
    qr_img = qr_img.resize((400, 400), Image.Resampling.LANCZOS)
    buffered = BytesIO()
    qr_img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

# ─── BRANDED QR CARD ────────────────────────────────────
def create_branded_qr_card(app_url="https://glycosearch.streamlit.app", app_name="GlycoSearch", institute="Academia Sinica"):
    """Create complete branded QR card HTML"""
    
    qr_img = generate_qr_code(app_url, app_name, institute)
    
    html = f'''
    <div style="background: white; padding: 2rem; border-radius: 16px; border: 2px solid #e2e8f0; text-align: center; max-width: 450px; margin: 0 auto;">
        <div style="display: flex; align-items: center; justify-content: center; gap: 0.5rem; margin-bottom: 0.5rem;">
            <svg width="40" height="40" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">
                <polygon points="28,4 44,12 44,30 28,38 12,30 12,12" stroke="#6366f1" stroke-width="2" fill="rgba(99,102,241,0.06)"/>
                <line x1="12" y1="12" x2="28" y2="20" stroke="#818cf8" stroke-width="1.5"/>
                <line x1="28" y1="20" x2="44" y2="12" stroke="#818cf8" stroke-width="1.5"/>
                <line x1="28" y1="38" x2="44" y2="30" stroke="#818cf8" stroke-width="1.5"/>
                <line x1="28" y1="38" x2="12" y2="30" stroke="#818cf8" stroke-width="1.5"/>
                <circle cx="28" cy="4" r="4" fill="#ef4444" stroke="#dc2626" stroke-width="1.2"/>
                <text x="28" y="7" font-size="6.5" fill="white" text-anchor="middle" font-weight="bold">O</text>
                <circle cx="44" cy="12" r="3.5" fill="#333" stroke="#333"/>
                <circle cx="44" cy="30" r="3.5" fill="#333" stroke="#333"/>
                <circle cx="28" cy="38" r="3.5" fill="#333" stroke="#333"/>
                <circle cx="12" cy="30" r="3.5" fill="#333" stroke="#333"/>
                <circle cx="12" cy="12" r="3.5" fill="#333" stroke="#333"/>
                <rect x="21" y="14" width="14" height="14" rx="3" fill="#0f172a" stroke="#a78bfa" stroke-width="1.8"/>
                <circle cx="28" cy="21" r="5" fill="rgba(167,139,250,0.12)" stroke="#c084fc" stroke-width="1.2"/>
                <text x="28" y="16" font-size="4" fill="#c084fc" text-anchor="middle" font-weight="700">AI</text>
            </svg>
            <span style="font-family: 'Inter', sans-serif; font-weight: 700; font-size: 1.4rem; color: #0f172a;">{app_name}</span>
        </div>
        <div style="font-family: 'Inter', sans-serif; font-size: 0.8rem; color: #94a3b8; margin-bottom: 1rem;">{institute}</div>
        <img src="data:image/png;base64,{qr_img}" style="border-radius: 12px; border: 2px solid #e2e8f0; max-width: 100%;">
        <div style="margin-top: 1rem; font-family: 'Inter', sans-serif; font-size: 0.7rem; color: #94a3b8;">
            Scan to access GlycoSearch
        </div>
        <div style="margin-top: 0.3rem; font-family: 'Inter', sans-serif; font-size: 0.6rem; color: #cbd5e1;">
            {app_url}
        </div>
        <div style="margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid #e2e8f0;">
            <span style="font-family: 'Inter', sans-serif; font-size: 0.6rem; color: #94a3b8;">
                Fizza Sabbor & Dr. Sabbor Hussain · Institute of Chemistry, Academia Sinica
            </span>
        </div>
    </div>
    '''
    return html

# ─── GLYCOKNOWLEDGE ENGINE ──────────────────────────────
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
            'screening': REACTION_SCREENING_KNOWLEDGE
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
        
        if any(term in question_lower for term in ['screening', 'which reaction first', 'decision', 'prioritize', 'organize']):
            knowledge = self.expert_knowledge.get('screening', {})
            if knowledge and 'screening_rules' in knowledge:
                parts = ["**🎯 Reaction Screening Strategy - Prioritization Rules:**"]
                for rule in knowledge['screening_rules']:
                    parts.append(f"• {rule}")
                response_parts.append('\n'.join(parts))
        
        if any(term in question_lower for term in ['donor', 'acceptor', 'match', 'rrv', 'aka']):
            knowledge = self.expert_knowledge.get('screening', {})
            if knowledge:
                parts = []
                if 'donors' in knowledge:
                    parts.append("**Available Donors with RRV:**")
                    for donor, info in knowledge['donors'].items():
                        parts.append(f"  • {donor}: RRV={info['rrv']}, Cost={info['cost']}, Selectivity={info['selectivity']}")
                if 'acceptors' in knowledge:
                    parts.append("\n**Acceptor Reactivity (Aka):**")
                    for acceptor, info in knowledge['acceptors'].items():
                        parts.append(f"  • {acceptor}: Aka={info['aka']}, Hindrance={info['hindrance']}")
                response_parts.append('\n'.join(parts))
        
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
        
        return '\n\n'.join(response_parts) if response_parts else None
    
    def combine_knowledge(self, question_lower, expert_response, relevant_papers):
        if not expert_response and not relevant_papers:
            return random.choice(FALLBACK_RESPONSES)
        answer_parts = []
        if expert_response:
            intro = random.choice(HUMANIZED_INTROS)
            answer_parts.append(f"{intro}\n\n{expert_response}")
        if relevant_papers:
            answer_parts.append("\n\n**📄 Related Papers from Your Database:**")
            for paper in relevant_papers[:3]:
                answer_parts.append(f"• {paper['title']} ({paper['year']}) - {paper['journal']}")
        ending = random.choice(HUMANIZED_ENDINGS)
        answer_parts.append(f"\n\n{ending}")
        return '\n'.join(answer_parts)
    
    def get_references(self, question_lower, relevant_papers):
        references = []
        for paper in relevant_papers[:2]:
            ref = f"{paper['title']} ({paper['year']}) - {paper['journal']}"
            references.append(ref)
        return references[:5]

# ─── REACTION SCREENING DECISION ENGINE ────────────────
def screen_reactions(donor_type, acceptor_type, target_selectivity=None):
    donors = REACTION_SCREENING_KNOWLEDGE['donors']
    acceptors = REACTION_SCREENING_KNOWLEDGE['acceptors']
    conditions = REACTION_SCREENING_KNOWLEDGE['conditions']
    
    recommendations = []
    
    for donor_name, donor_info in donors.items():
        for condition_name, cond_info in conditions.items():
            score = 0
            reasons = []
            
            if acceptor_type in acceptors:
                aka = acceptors[acceptor_type]['aka']
                rrv = donor_info['rrv']
                
                if abs(rrv - abs(aka) * 5) < 20:
                    score += 30
                    reasons.append("Good RRV-Aka match")
                elif rrv > 50 and aka < 0:
                    score += 20
                    reasons.append("High RRV compensates low Aka")
                elif rrv < 5 and aka > 5:
                    score += 10
                    reasons.append("Low RRV with high Aka - slow but selective")
                
                if target_selectivity:
                    if 'β' in target_selectivity and 'β' in donor_info['selectivity']:
                        score += 25
                        reasons.append(f"Selectivity matches target ({target_selectivity})")
                    elif 'α' in target_selectivity and 'α' in donor_info['selectivity']:
                        score += 25
                        reasons.append(f"Selectivity matches target ({target_selectivity})")
                
                if donor_info['cost'] == 'Low':
                    score += 10
                    reasons.append("Low cost")
                if donor_info['availability'] == 'High':
                    score += 10
                    reasons.append("High availability")
                if 'RT' in cond_info['temp']:
                    score += 5
                    reasons.append("Room temperature compatible")
                
                yield_val = int(cond_info['yield'].split('-')[1].replace('%', ''))
                if yield_val > 90:
                    score += 10
                    reasons.append("High expected yield")
            
            recommendations.append({
                'donor': donor_name,
                'condition': condition_name,
                'score': score,
                'reasons': reasons,
                'rrv': donor_info['rrv'],
                'selectivity': donor_info['selectivity'],
                'temp': cond_info['temp'],
                'yield': cond_info['yield']
            })
    
    recommendations.sort(key=lambda x: x['score'], reverse=True)
    
    for i, rec in enumerate(recommendations):
        if i < len(recommendations) * 0.3:
            rec['priority'] = 'High'
        elif i < len(recommendations) * 0.7:
            rec['priority'] = 'Medium'
        else:
            rec['priority'] = 'Low'
    
    return recommendations[:10]

# ─── ENHANCED DRAWING TOOL ─────────────────────────────
def chemical_drawing_tool():
    components.html("""
    <div class="draw-header">
        <h2>🧪 Draw <span>Chemical Structure</span></h2>
        <p>Build molecules with atoms, functional groups, and leaving groups</p>
    </div>
    <div class="draw-toolbar">
        <div style="display:flex;gap:3px;align-items:center;background:#f8fafc;padding:2px 8px;border-radius:8px;flex-wrap:wrap;">
            <span style="font-size:9px;color:#94a3b8;font-weight:600;margin-right:3px;font-family:'Inter',sans-serif;text-transform:uppercase;letter-spacing:0.05em;">Atoms</span>
            <button class="atom-btn" data-atom="C" style="padding:4px 10px;border:2px solid #333;border-radius:6px;background:#0f172a;color:white;cursor:pointer;font-size:11px;font-weight:700;">C</button>
            <button class="atom-btn" data-atom="O" style="padding:4px 10px;border:2px solid #FF0000;border-radius:6px;background:#f8fafc;cursor:pointer;font-size:11px;font-weight:700;color:#FF0000;">O</button>
            <button class="atom-btn" data-atom="N" style="padding:4px 10px;border:2px solid #3050F8;border-radius:6px;background:#f8fafc;cursor:pointer;font-size:11px;font-weight:700;color:#3050F8;">N</button>
            <button class="atom-btn" data-atom="H" style="padding:4px 10px;border:2px solid #888;border-radius:6px;background:#f8fafc;cursor:pointer;font-size:11px;font-weight:700;color:#888;">H</button>
            <button class="atom-btn" data-atom="S" style="padding:4px 10px;border:2px solid #FFD700;border-radius:6px;background:#f8fafc;cursor:pointer;font-size:11px;font-weight:700;color:#B8860B;">S</button>
            <button class="atom-btn" data-atom="P" style="padding:4px 10px;border:2px solid #FF8000;border-radius:6px;background:#f8fafc;cursor:pointer;font-size:11px;font-weight:700;color:#FF8000;">P</button>
            <button class="atom-btn" data-atom="F" style="padding:4px 10px;border:2px solid #90E050;border-radius:6px;background:#f8fafc;cursor:pointer;font-size:11px;font-weight:700;color:#2E8B57;">F</button>
            <button class="atom-btn" data-atom="Cl" style="padding:4px 10px;border:2px solid #1FF01F;border-radius:6px;background:#f8fafc;cursor:pointer;font-size:11px;font-weight:700;color:#1FF01F;">Cl</button>
            <button class="atom-btn" data-atom="Br" style="padding:4px 10px;border:2px solid #A62929;border-radius:6px;background:#f8fafc;cursor:pointer;font-size:11px;font-weight:700;color:#A62929;">Br</button>
            <button class="atom-btn" data-atom="I" style="padding:4px 10px;border:2px solid #940094;border-radius:6px;background:#f8fafc;cursor:pointer;font-size:11px;font-weight:700;color:#940094;">I</button>
        </div>
    </div>
    <div class="draw-toolbar">
        <div style="display:flex;gap:3px;align-items:center;background:#f8fafc;padding:2px 8px;border-radius:8px;flex-wrap:wrap;">
            <span style="font-size:9px;color:#94a3b8;font-weight:600;margin-right:3px;font-family:'Inter',sans-serif;text-transform:uppercase;letter-spacing:0.05em;">Groups</span>
            <button class="fg-btn" data-fg="OH" style="padding:3px 8px;border:1px solid #e2e8f0;border-radius:6px;background:#f8fafc;cursor:pointer;font-size:10px;font-weight:500;">OH</button>
            <button class="fg-btn" data-fg="OMe" style="padding:3px 8px;border:1px solid #e2e8f0;border-radius:6px;background:#f8fafc;cursor:pointer;font-size:10px;font-weight:500;">OMe</button>
            <button class="fg-btn" data-fg="OAc" style="padding:3px 8px;border:1px solid #e2e8f0;border-radius:6px;background:#f8fafc;cursor:pointer;font-size:10px;font-weight:500;">OAc</button>
            <button class="fg-btn" data-fg="OBn" style="padding:3px 8px;border:1px solid #e2e8f0;border-radius:6px;background:#f8fafc;cursor:pointer;font-size:10px;font-weight:500;">OBn</button>
            <button class="fg-btn" data-fg="OBz" style="padding:3px 8px;border:1px solid #e2e8f0;border-radius:6px;background:#f8fafc;cursor:pointer;font-size:10px;font-weight:500;">OBz</button>
            <button class="fg-btn" data-fg="NH2" style="padding:3px 8px;border:1px solid #e2e8f0;border-radius:6px;background:#f8fafc;cursor:pointer;font-size:10px;font-weight:500;">NH2</button>
            <button class="fg-btn" data-fg="N3" style="padding:3px 8px;border:1px solid #e2e8f0;border-radius:6px;background:#f8fafc;cursor:pointer;font-size:10px;font-weight:500;">N3</button>
            <button class="fg-btn" data-fg="OTs" style="padding:3px 8px;border:1px solid #e2e8f0;border-radius:6px;background:#f8fafc;cursor:pointer;font-size:10px;font-weight:500;">OTs</button>
            <button class="fg-btn" data-fg="Ac" style="padding:3px 8px;border:1px solid #e2e8f0;border-radius:6px;background:#f8fafc;cursor:pointer;font-size:10px;font-weight:500;">Ac</button>
            <button class="fg-btn" data-fg="Bn" style="padding:3px 8px;border:1px solid #e2e8f0;border-radius:6px;background:#f8fafc;cursor:pointer;font-size:10px;font-weight:500;">Bn</button>
            <button class="fg-btn" data-fg="Bz" style="padding:3px 8px;border:1px solid #e2e8f0;border-radius:6px;background:#f8fafc;cursor:pointer;font-size:10px;font-weight:500;">Bz</button>
            <button class="fg-btn" data-fg="TBDMS" style="padding:3px 8px;border:1px solid #e2e8f0;border-radius:6px;background:#f8fafc;cursor:pointer;font-size:10px;font-weight:500;">TBDMS</button>
            <button class="fg-btn" data-fg="TIPS" style="padding:3px 8px;border:1px solid #e2e8f0;border-radius:6px;background:#f8fafc;cursor:pointer;font-size:10px;font-weight:500;">TIPS</button>
            <button class="fg-btn" data-fg="Piv" style="padding:3px 8px;border:1px solid #e2e8f0;border-radius:6px;background:#f8fafc;cursor:pointer;font-size:10px;font-weight:500;">Piv</button>
            <button class="fg-btn" data-fg="DPPA" style="padding:3px 8px;border:1px solid #e2e8f0;border-radius:6px;background:#f8fafc;cursor:pointer;font-size:10px;font-weight:500;">DPPA</button>
            <button class="fg-btn" data-fg="OTf" style="padding:3px 8px;border:1px solid #e2e8f0;border-radius:6px;background:#f8fafc;cursor:pointer;font-size:10px;font-weight:500;">OTf</button>
            <button class="fg-btn" data-fg="STol" style="padding:3px 8px;border:1px solid #e2e8f0;border-radius:6px;background:#f8fafc;cursor:pointer;font-size:10px;font-weight:500;">STol</button>
        </div>
    </div>
    <div class="draw-toolbar">
        <div style="display:flex;gap:3px;align-items:center;background:#f8fafc;padding:2px 8px;border-radius:8px;flex-wrap:wrap;">
            <span style="font-size:9px;color:#94a3b8;font-weight:600;margin-right:3px;font-family:'Inter',sans-serif;text-transform:uppercase;letter-spacing:0.05em;">Bond</span>
            <button id="btn-single-bond" class="active" style="padding:4px 10px;border:1px solid #e2e8f0;border-radius:6px;background:#0f172a;color:white;cursor:pointer;font-size:11px;">─</button>
            <button id="btn-double-bond" style="padding:4px 10px;border:1px solid #e2e8f0;border-radius:6px;background:#f8fafc;cursor:pointer;font-size:11px;color:#0f172a;">═</button>
            <button id="btn-triple-bond" style="padding:4px 10px;border:1px solid #e2e8f0;border-radius:6px;background:#f8fafc;cursor:pointer;font-size:11px;color:#0f172a;">≡</button>
        </div>
        <div style="display:flex;gap:3px;align-items:center;background:#f8fafc;padding:2px 8px;border-radius:8px;flex-wrap:wrap;">
            <button id="btn-undo" style="padding:4px 10px;border:1px solid #e2e8f0;border-radius:6px;background:#f8fafc;cursor:pointer;font-size:11px;">↩️ Undo</button>
            <button id="btn-clear" class="danger" style="padding:4px 10px;border:1px solid #fee2e2;border-radius:6px;background:#fee2e2;color:#991b1b;cursor:pointer;font-size:11px;">🗑️ Clear</button>
            <button id="btn-benzene" class="purple" style="padding:4px 10px;border:1px solid #f3e8ff;border-radius:6px;background:#f3e8ff;color:#6b21a8;cursor:pointer;font-size:11px;">⬡ Benzene</button>
            <button id="btn-smiles" class="success" style="padding:4px 10px;border:1px solid #dcfce7;border-radius:6px;background:#dcfce7;color:#166534;cursor:pointer;font-size:11px;">📋 SMILES</button>
            <button id="btn-query" class="purple" style="padding:4px 10px;border:1px solid #f3e8ff;border-radius:6px;background:#f3e8ff;color:#6b21a8;cursor:pointer;font-size:11px;">🔍 Query</button>
        </div>
    </div>
    <div style="display:flex;gap:8px;margin-bottom:6px;align-items:center;flex-wrap:wrap;">
        <span id="mode-status" class="mode-status mode-draw">✏️ Draw Mode</span>
        <span class="bond-type-indicator" id="bond-type-indicator">Bond: Single</span>
        <span id="selected-display" style="font-size:10px;color:#64748b;background:#f1f5f9;padding:2px 10px;border-radius:4px;">Selected: C</span>
        <span class="draw-info">💡 Double-click for double bond</span>
    </div>
    <div class="draw-container" id="draw-container">
        <canvas id="canvas" width="750" height="480"></canvas>
        <div class="zoom-controls">
            <button id="zoom-in">🔍+ Zoom</button>
            <button id="zoom-out">🔍− Zoom</button>
            <button id="zoom-reset">⟲ Reset</button>
            <span style="font-size:11px;color:#94a3b8;" id="zoom-level">100%</span>
        </div>
    </div>
    <input id="smiles-output" placeholder="SMILES will appear here...">
    <div id="query-result" style="margin-top:10px;padding:10px;background:#f8fafc;border-radius:8px;border:1px solid #e2e8f0;display:none;"></div>
    <style>
        #canvas { border: 2px solid #e2e8f0; background: white; border-radius: 12px; cursor: crosshair; width: 100%; height: auto; transform-origin: top left; transition: transform 0.2s; }
        #smiles-output { width: 100%; padding: 8px 12px; border: 2px solid #e2e8f0; border-radius: 8px; margin-top: 8px; font-family: monospace; font-size: 12px; background: #f8fafc; }
        .mode-status { padding: 2px 10px; border-radius: 50px; font-size: 10px; font-weight: 500; font-family: 'Inter', sans-serif; display: inline-block; }
        .mode-draw { background: #dcfce7; color: #166534; }
        .mode-replace { background: #fef3c7; color: #92400e; }
        .mode-delete { background: #fee2e2; color: #991b1b; }
        .mode-select { background: #dbeafe; color: #1e40af; }
        .mode-eraser { background: #fce4ec; color: #880e4f; }
        .draw-info { color: #94a3b8; font-size: 10px; font-family: 'Inter', sans-serif; }
        .bond-type-indicator { font-size: 10px; color: #64748b; padding: 1px 8px; background: #f1f5f9; border-radius: 4px; }
        .draw-container { position: relative; overflow: auto; max-height: 600px; border: 2px solid #e2e8f0; border-radius: 12px; background: white; }
        .zoom-controls { position: sticky; bottom: 0; background: rgba(255,255,255,0.95); padding: 8px; border-top: 1px solid #e2e8f0; display: flex; gap: 8px; align-items: center; justify-content: center; z-index: 100; backdrop-filter: blur(10px); }
        .fg-btn.active { background: #eef2ff !important; border-color: #818cf8 !important; color: #4f46e5 !important; }
    </style>
    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        let isDrawing = false, lastX, lastY;
        let atoms = [], bonds = [], history = [];
        let tool = 'draw';
        let selectedAtom = 'C';
        let selectedFG = null;
        let bondType = 1;
        let deleteBondMode = false;
        let replaceMode = false;
        let selectMode = false;
        let eraserMode = false;
        let selectionStart = null;
        let selectionEnd = null;
        let selectedAtoms = [];
        const MAX_HISTORY = 30;
        let atomIdCounter = 0;
        let zoomLevel = 1;
        let offsetX = 0, offsetY = 0;
        let isPanning = false;
        let panStartX, panStartY;

        document.querySelectorAll('.atom-btn').forEach(btn => {
            btn.onclick = function() {
                selectedAtom = this.dataset.atom;
                selectedFG = null;
                document.querySelectorAll('.atom-btn').forEach(b => {
                    b.style.background = '#f8fafc';
                    b.style.color = '#0f172a';
                });
                this.style.background = '#0f172a';
                this.style.color = 'white';
                document.getElementById('selected-display').textContent = 'Selected: ' + selectedAtom;
                document.querySelectorAll('.fg-btn').forEach(b => b.classList.remove('active'));
            };
        });
        
        document.querySelectorAll('.fg-btn').forEach(btn => {
            btn.onclick = function() {
                selectedFG = this.dataset.fg;
                document.querySelectorAll('.fg-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                document.getElementById('selected-display').textContent = 'Selected: ' + selectedFG;
                document.querySelectorAll('.atom-btn').forEach(b => {
                    b.style.background = '#f8fafc';
                    b.style.color = '#0f172a';
                });
            };
        });

        function getAtomColor(label) {
            const colors = {'C':'#333333','O':'#FF0000','N':'#3050F8','H':'#888888','S':'#FFD700','P':'#FF8000','F':'#90E050','Cl':'#1FF01F','Br':'#A62929','I':'#940094'};
            return colors[label] || '#333333';
        }

        function drawAtom(x, y, label, highlight, selected) {
            const radius = selected ? 24 : (highlight ? 22 : 18);
            const color = getAtomColor(label);
            if (highlight) { ctx.shadowColor = '#f59e0b'; ctx.shadowBlur = 15; }
            if (selected) { ctx.shadowColor = '#3b82f6'; ctx.shadowBlur = 20; }
            ctx.beginPath();
            ctx.arc(x, y, radius, 0, Math.PI*2);
            ctx.fillStyle = selected ? '#93c5fd' : color;
            ctx.fill();
            ctx.shadowBlur = 0;
            ctx.strokeStyle = selected ? '#2563eb' : (highlight ? '#f59e0b' : '#333');
            ctx.lineWidth = selected ? 4 : (highlight ? 3 : 2);
            ctx.stroke();
            if (label) {
                ctx.fillStyle = selected ? '#1e3a5f' : 'white';
                ctx.font = 'bold 10px Inter, Arial, sans-serif';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                const displayLabel = label.length > 6 ? label.substring(0,6) : label;
                ctx.fillText(displayLabel, x, y);
            }
        }

        function drawBond(x1, y1, x2, y2, type, highlight) {
            const color = highlight ? '#ef4444' : '#333';
            const offset = 6;
            const dx = x2 - x1, dy = y2 - y1;
            const len = Math.hypot(dx, dy);
            if (len === 0) return;
            const nx = -dy / len, ny = dx / len;
            if (type === 1 || type === undefined) {
                ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2);
                ctx.strokeStyle = color; ctx.lineWidth = highlight ? 6 : 3; ctx.stroke();
            } else if (type === 2) {
                for (let d = -1; d <= 1; d += 2) {
                    const ox = d * offset * nx, oy = d * offset * ny;
                    ctx.beginPath(); ctx.moveTo(x1 + ox, y1 + oy); ctx.lineTo(x2 + ox, y2 + oy);
                    ctx.strokeStyle = color; ctx.lineWidth = highlight ? 6 : 3; ctx.stroke();
                }
            } else if (type === 3) {
                for (let d = -1; d <= 1; d++) {
                    const ox = d * offset * nx, oy = d * offset * ny;
                    ctx.beginPath(); ctx.moveTo(x1 + ox, y1 + oy); ctx.lineTo(x2 + ox, y2 + oy);
                    ctx.strokeStyle = color; ctx.lineWidth = highlight ? 6 : 2; ctx.stroke();
                }
            }
        }

        function drawBenzene(x, y) {
            const size = 50;
            const angles = [0, 60, 120, 180, 240, 300];
            const pts = angles.map(d => ({x: x + size * Math.cos(d * Math.PI / 180), y: y + size * Math.sin(d * Math.PI / 180)}));
            for (let i = 0; i < 6; i++) {
                let j = (i + 1) % 6;
                ctx.beginPath(); ctx.moveTo(pts[i].x, pts[i].y); ctx.lineTo(pts[j].x, pts[j].y);
                ctx.strokeStyle = '#333'; ctx.lineWidth = 3; ctx.stroke();
                if (i % 2 === 0) {
                    const midX = (pts[i].x + pts[j].x) / 2, midY = (pts[i].y + pts[j].y) / 2;
                    const angle = Math.atan2(pts[j].y - pts[i].y, pts[j].x - pts[i].x);
                    const perpAngle = angle + Math.PI / 2;
                    const offset = 8;
                    for (let d = -1; d <= 1; d += 2) {
                        const dx = d * offset * Math.cos(perpAngle), dy = d * offset * Math.sin(perpAngle);
                        const sx = midX + dx - 22 * Math.cos(angle), sy = midY + dy - 22 * Math.sin(angle);
                        const ex = midX + dx + 22 * Math.cos(angle), ey = midY + dy + 22 * Math.sin(angle);
                        ctx.beginPath(); ctx.moveTo(sx, sy); ctx.lineTo(ex, ey);
                        ctx.strokeStyle = '#333'; ctx.lineWidth = 3; ctx.stroke();
                    }
                }
            }
            for (let i = 0; i < 6; i++) {
                const color = getAtomColor('C');
                ctx.beginPath(); ctx.arc(pts[i].x, pts[i].y, 18, 0, Math.PI*2);
                ctx.fillStyle = color; ctx.fill();
                ctx.strokeStyle = '#333'; ctx.lineWidth = 2; ctx.stroke();
                ctx.fillStyle = 'white';
                ctx.font = 'bold 12px Inter, Arial, sans-serif';
                ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
                ctx.fillText('C', pts[i].x, pts[i].y);
                atoms.push({x: pts[i].x, y: pts[i].y, label: 'C', id: atomIdCounter++});
            }
        }

        function findNearestAtom(x, y, threshold) {
            threshold = threshold || 25;
            let nearest = null, minDist = threshold;
            for (const a of atoms) {
                const dist = Math.hypot(x - a.x, y - a.y);
                if (dist < minDist) { minDist = dist; nearest = a; }
            }
            return nearest;
        }

        function getAtomsInRect(x1, y1, x2, y2) {
            const minX = Math.min(x1, x2), maxX = Math.max(x1, x2);
            const minY = Math.min(y1, y2), maxY = Math.max(y1, y2);
            return atoms.filter(a => a.x >= minX && a.x <= maxX && a.y >= minY && a.y <= maxY);
        }

        function drawAll() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.save();
            ctx.translate(offsetX, offsetY);
            ctx.scale(zoomLevel, zoomLevel);
            
            ctx.strokeStyle = '#f1f5f9';
            ctx.lineWidth = 0.5;
            for (let x=0; x<=canvas.width; x+=30) {
                ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,canvas.height); ctx.stroke();
            }
            for (let y=0; y<=canvas.height; y+=30) {
                ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(canvas.width,y); ctx.stroke();
            }
            bonds.forEach(b => drawBond(b.x1,b.y1,b.x2,b.y2,b.type||1,false));
            atoms.forEach(a => {
                const sel = selectedAtoms.some(s => s.id === a.id);
                drawAtom(a.x,a.y,a.label,false,sel);
            });
            if (selectMode && selectionStart && selectionEnd) {
                const x = Math.min(selectionStart.x, selectionEnd.x);
                const y = Math.min(selectionStart.y, selectionEnd.y);
                const w = Math.abs(selectionStart.x - selectionEnd.x);
                const h = Math.abs(selectionStart.y - selectionEnd.y);
                ctx.strokeStyle = '#3b82f6';
                ctx.lineWidth = 2;
                ctx.setLineDash([5, 5]);
                ctx.strokeRect(x, y, w, h);
                ctx.setLineDash([]);
                ctx.fillStyle = 'rgba(59, 130, 246, 0.1)';
                ctx.fillRect(x, y, w, h);
            }
            ctx.restore();
            document.getElementById('zoom-level').textContent = Math.round(zoomLevel * 100) + '%';
        }

        function saveState() {
            history.push(JSON.parse(JSON.stringify({atoms, bonds})));
            if (history.length > MAX_HISTORY) history.shift();
        }

        function getPos(e) {
            const rect = canvas.getBoundingClientRect();
            const scaleX = canvas.width / rect.width;
            const scaleY = canvas.height / rect.height;
            const x = (e.clientX - rect.left) * scaleX;
            const y = (e.clientY - rect.top) * scaleY;
            return { x: (x - offsetX) / zoomLevel, y: (y - offsetY) / zoomLevel };
        }

        function updateModeStatus() {
            const status = document.getElementById('mode-status');
            if (eraserMode) {
                status.className = 'mode-status mode-eraser';
                status.textContent = '🧹 Eraser Mode';
                canvas.style.cursor = 'not-allowed';
            } else if (selectMode) {
                status.className = 'mode-status mode-select';
                status.textContent = '⬜ Select Mode';
                canvas.style.cursor = 'default';
            } else if (replaceMode) {
                status.className = 'mode-status mode-replace';
                status.textContent = '🔄 Replace Mode';
                canvas.style.cursor = 'pointer';
            } else {
                status.className = 'mode-status mode-draw';
                status.textContent = '✏️ Draw Mode';
                canvas.style.cursor = 'crosshair';
            }
        }

        canvas.addEventListener('dblclick', function(e) {
            const pos = getPos(e);
            const atom = findNearestAtom(pos.x, pos.y);
            if (atom) {
                bonds.forEach(b => {
                    if ((b.x1 === atom.x && b.y1 === atom.y) || (b.x2 === atom.x && b.y2 === atom.y)) {
                        b.type = 2;
                    }
                });
                drawAll();
            }
        });

        canvas.onmousedown = function(e) {
            const pos = getPos(e);
            if (e.button === 1 || (e.ctrlKey && e.button === 0)) {
                isPanning = true;
                panStartX = e.clientX - offsetX;
                panStartY = e.clientY - offsetY;
                canvas.style.cursor = 'grab';
                return;
            }
            if (eraserMode) {
                const atom = findNearestAtom(pos.x, pos.y);
                if (atom) {
                    saveState();
                    atoms = atoms.filter(a => a !== atom);
                    bonds = bonds.filter(b => b.x1 !== atom.x || b.y1 !== atom.y);
                    bonds = bonds.filter(b => b.x2 !== atom.x || b.y2 !== atom.y);
                    drawAll(); return;
                }
                return;
            }
            if (selectMode) {
                selectionStart = pos; selectionEnd = pos; selectedAtoms = []; drawAll(); return;
            }
            if (replaceMode) {
                const atom = findNearestAtom(pos.x, pos.y);
                if (atom) {
                    saveState();
                    atom.label = selectedAtom;
                    drawAll();
                    drawAtom(atom.x, atom.y, atom.label, true);
                    setTimeout(drawAll, 300);
                }
                return;
            }
            if (e.button === 2) {
                const atom = findNearestAtom(pos.x, pos.y);
                if (atom) {
                    saveState();
                    atoms = atoms.filter(a => a !== atom);
                    bonds = bonds.filter(b => b.x1 !== atom.x || b.y1 !== atom.y);
                    bonds = bonds.filter(b => b.x2 !== atom.x || b.y2 !== atom.y);
                    drawAll();
                }
                return;
            }
            if (tool === 'draw') {
                saveState();
                let label = selectedAtom;
                if (selectedFG) {
                    label = selectedFG;
                }
                atoms.push({x: pos.x, y: pos.y, label: label, id: atomIdCounter++});
                drawAll();
            } else if (tool === 'line') {
                isDrawing = true;
                lastX = pos.x;
                lastY = pos.y;
            } else if (tool === 'benzene') {
                saveState();
                drawBenzene(pos.x, pos.y);
                drawAll();
            }
        };

        canvas.onmousemove = function(e) {
            const pos = getPos(e);
            if (isPanning) {
                offsetX = e.clientX - panStartX;
                offsetY = e.clientY - panStartY;
                drawAll();
                return;
            }
            if (selectMode && selectionStart) {
                selectionEnd = pos;
                drawAll();
                const selected = getAtomsInRect(selectionStart.x, selectionStart.y, pos.x, pos.y);
                selectedAtoms = selected;
                selected.forEach(a => drawAtom(a.x, a.y, a.label, false, true));
                return;
            }
            if (isDrawing && tool === 'line') {
                drawAll();
                drawBond(lastX, lastY, pos.x, pos.y, bondType, false);
            }
        };

        canvas.onmouseup = function(e) {
            if (isPanning) {
                isPanning = false;
                canvas.style.cursor = 'default';
                return;
            }
            if (selectMode && selectionStart) {
                const pos = getPos(e);
                const selected = getAtomsInRect(selectionStart.x, selectionStart.y, pos.x, pos.y);
                selectedAtoms = selected;
                drawAll();
                selected.forEach(a => drawAtom(a.x, a.y, a.label, false, true));
                selectionStart = null; selectionEnd = null; return;
            }
            if (isDrawing && tool === 'line') {
                const pos = getPos(e);
                saveState();
                let endAtom = findNearestAtom(pos.x, pos.y);
                let startAtom = findNearestAtom(lastX, lastY);
                if (startAtom && endAtom && startAtom !== endAtom) {
                    bonds.push({x1: startAtom.x, y1: startAtom.y, x2: endAtom.x, y2: endAtom.y, type: bondType});
                } else if (startAtom) {
                    let label = selectedAtom;
                    if (selectedFG) {
                        label = selectedFG;
                    }
                    const na = {x: pos.x, y: pos.y, label: label, id: atomIdCounter++};
                    atoms.push(na);
                    bonds.push({x1: startAtom.x, y1: startAtom.y, x2: na.x, y2: na.y, type: bondType});
                } else {
                    let label = selectedAtom;
                    if (selectedFG) {
                        label = selectedFG;
                    }
                    const a1 = {x: lastX, y: lastY, label: label, id: atomIdCounter++};
                    const a2 = {x: pos.x, y: pos.y, label: label, id: atomIdCounter++};
                    atoms.push(a1); atoms.push(a2);
                    bonds.push({x1: a1.x, y1: a1.y, x2: a2.x, y2: a2.y, type: bondType});
                }
                drawAll();
                isDrawing = false;
            }
        };

        canvas.oncontextmenu = e => e.preventDefault();

        canvas.addEventListener('wheel', function(e) {
            e.preventDefault();
            const delta = e.deltaY > 0 ? -0.1 : 0.1;
            const newZoom = Math.min(3, Math.max(0.3, zoomLevel + delta));
            if (newZoom !== zoomLevel) {
                const rect = canvas.getBoundingClientRect();
                const mouseX = (e.clientX - rect.left) * (canvas.width / rect.width);
                const mouseY = (e.clientY - rect.top) * (canvas.height / rect.height);
                const worldX = (mouseX - offsetX) / zoomLevel;
                const worldY = (mouseY - offsetY) / zoomLevel;
                zoomLevel = newZoom;
                offsetX = mouseX - worldX * zoomLevel;
                offsetY = mouseY - worldY * zoomLevel;
                drawAll();
            }
        }, { passive: false });

        document.addEventListener('keydown', function(e) {
            if ((e.key === 'Delete' || e.key === 'Backspace') && selectedAtoms.length > 0) {
                saveState();
                const ids = selectedAtoms.map(a => a.id);
                atoms = atoms.filter(a => !ids.includes(a.id));
                bonds = bonds.filter(b => {
                    const a1 = atoms.find(a => a.x === b.x1 && a.y === b.y1);
                    const a2 = atoms.find(a => a.x === b.x2 && a.y === b.y2);
                    return a1 && a2;
                });
                selectedAtoms = [];
                drawAll();
            }
        });

        document.getElementById('zoom-in').onclick = function() {
            zoomLevel = Math.min(3, zoomLevel + 0.2);
            drawAll();
        };
        document.getElementById('zoom-out').onclick = function() {
            zoomLevel = Math.max(0.3, zoomLevel - 0.2);
            drawAll();
        };
        document.getElementById('zoom-reset').onclick = function() {
            zoomLevel = 1;
            offsetX = 0;
            offsetY = 0;
            drawAll();
        };

        document.getElementById('btn-draw').onclick = function() {
            tool = 'draw'; replaceMode = false; eraserMode = false; selectMode = false;
            selectionStart = null; selectionEnd = null; selectedAtoms = [];
            document.querySelectorAll('.draw-toolbar button').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            updateModeStatus();
        };
        document.getElementById('btn-replace').onclick = function() {
            replaceMode = !replaceMode;
            if (replaceMode) {
                eraserMode = false; selectMode = false;
                document.querySelectorAll('.draw-toolbar button').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                tool = 'replace';
            } else {
                this.classList.remove('active');
                tool = 'draw';
                document.getElementById('btn-draw').classList.add('active');
            }
            updateModeStatus();
        };
        document.getElementById('btn-eraser').onclick = function() {
            eraserMode = !eraserMode;
            if (eraserMode) {
                replaceMode = false; selectMode = false;
                document.querySelectorAll('.draw-toolbar button').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                tool = 'eraser';
            } else {
                this.classList.remove('active');
                tool = 'draw';
                document.getElementById('btn-draw').classList.add('active');
            }
            updateModeStatus();
        };
        document.getElementById('btn-select').onclick = function() {
            selectMode = !selectMode;
            if (selectMode) {
                replaceMode = false; eraserMode = false;
                document.querySelectorAll('.draw-toolbar button').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                tool = 'select';
            } else {
                this.classList.remove('active');
                tool = 'draw';
                document.getElementById('btn-draw').classList.add('active');
            }
            updateModeStatus();
        };
        document.getElementById('btn-benzene').onclick = function() {
            tool = 'benzene'; replaceMode = false; eraserMode = false; selectMode = false;
            selectionStart = null; selectionEnd = null; selectedAtoms = [];
            document.querySelectorAll('.draw-toolbar button').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            updateModeStatus();
        };
        document.getElementById('btn-line').onclick = function() {
            tool = 'line'; replaceMode = false; eraserMode = false; selectMode = false;
            selectionStart = null; selectionEnd = null; selectedAtoms = [];
            document.querySelectorAll('.draw-toolbar button').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            updateModeStatus();
        };

        document.getElementById('btn-single-bond').onclick = function() {
            bondType = 1;
            document.querySelectorAll('#btn-single-bond, #btn-double-bond, #btn-triple-bond').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            document.getElementById('bond-type-indicator').textContent = 'Bond: Single';
        };
        document.getElementById('btn-double-bond').onclick = function() {
            bondType = 2;
            document.querySelectorAll('#btn-single-bond, #btn-double-bond, #btn-triple-bond').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            document.getElementById('bond-type-indicator').textContent = 'Bond: Double';
        };
        document.getElementById('btn-triple-bond').onclick = function() {
            bondType = 3;
            document.querySelectorAll('#btn-single-bond, #btn-double-bond, #btn-triple-bond').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            document.getElementById('bond-type-indicator').textContent = 'Bond: Triple';
        };

        document.getElementById('btn-undo').onclick = function() {
            if (history.length > 0) {
                const state = history.pop();
                atoms = state.atoms; bonds = state.bonds;
                selectedAtoms = [];
                drawAll();
            }
        };
        document.getElementById('btn-clear').onclick = function() {
            if (atoms.length > 0 || bonds.length > 0) {
                if (confirm('Clear everything?')) {
                    saveState();
                    atoms = []; bonds = [];
                    selectedAtoms = [];
                    drawAll();
                }
            }
        };
        
        document.getElementById('btn-smiles').onclick = function() {
            const sm = atoms.length > 0 ? atoms.map(a => a.label||'C').join('') : 'No atoms drawn';
            document.getElementById('smiles-output').value = 'SMILES: ' + sm;
            navigator.clipboard.writeText(sm);
        };
        
        document.getElementById('btn-query').onclick = function() {
            const sm = atoms.length > 0 ? atoms.map(a => a.label||'C').join('') : 'No structure';
            document.getElementById('query-result').style.display = 'block';
            document.getElementById('query-result').innerHTML = `
                <div style="background:#f0f4ff;padding:1rem;border-radius:8px;border:2px solid #c7d2fe;">
                    <h4 style="color:#0f172a;margin:0 0 0.5rem 0;">🔍 Structure Query Results</h4>
                    <div style="background:white;padding:0.8rem 1.2rem;border-radius:8px;border-left:4px solid #6366f1;margin:0.3rem 0;">
                        <b>Structure:</b> ${sm}
                    </div>
                    <div style="background:white;padding:0.8rem 1.2rem;border-radius:8px;border-left:4px solid #6366f1;margin:0.3rem 0;">
                        <b>Suggested Reaction Scheme:</b><br>
                        Donor + Acceptor → Glycoside<br>
                        Activator: NIS/TfOH or TMSOTf
                    </div>
                    <div style="background:white;padding:0.8rem 1.2rem;border-radius:8px;border-left:4px solid #6366f1;margin:0.3rem 0;">
                        <b>Recommended Conditions:</b><br>
                        • Temperature: −40°C to RT<br>
                        • Solvent: DCM (anhydrous)<br>
                        • Activator: TMSOTf (0.1-0.5 equiv)<br>
                        • Time: 2-12 hours<br>
                        • Expected Yield: 60-95%
                    </div>
                </div>
            `;
        };

        drawBenzene(375, 240);
        drawAll();
        saveState();
        updateModeStatus();
    </script>
    """, height=720)

# ─── HEADER ─────────────────────────────────────────────
def render_header():
    valid_years = papers['Year'].dropna() if len(papers) > 0 else []
    topics = papers['Topic'].dropna().unique() if len(papers) > 0 else []
    
    logo_svg = '''
    <svg width="56" height="56" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">
        <polygon points="28,4 44,12 44,30 28,38 12,30 12,12" stroke="#6366f1" stroke-width="2" fill="rgba(99,102,241,0.06)"/>
        <line x1="12" y1="12" x2="28" y2="20" stroke="#818cf8" stroke-width="1.5"/>
        <line x1="28" y1="20" x2="44" y2="12" stroke="#818cf8" stroke-width="1.5"/>
        <line x1="28" y1="38" x2="44" y2="30" stroke="#818cf8" stroke-width="1.5"/>
        <line x1="28" y1="38" x2="12" y2="30" stroke="#818cf8" stroke-width="1.5"/>
        <circle cx="28" cy="4" r="4" fill="#ef4444" stroke="#dc2626" stroke-width="1.2"/>
        <text x="28" y="7" font-size="6.5" fill="white" text-anchor="middle" font-weight="bold">O</text>
        <circle cx="44" cy="12" r="3.5" fill="#333" stroke="#333"/>
        <circle cx="44" cy="30" r="3.5" fill="#333" stroke="#333"/>
        <circle cx="28" cy="38" r="3.5" fill="#333" stroke="#333"/>
        <circle cx="12" cy="30" r="3.5" fill="#333" stroke="#333"/>
        <circle cx="12" cy="12" r="3.5" fill="#333" stroke="#333"/>
        <text x="50" y="10" font-size="5" fill="#ef4444" font-weight="bold">OH</text>
        <text x="50" y="32" font-size="5" fill="#ef4444" font-weight="bold">OH</text>
        <text x="28" y="44" font-size="5" fill="#ef4444" font-weight="bold">OH</text>
        <text x="5" y="32" font-size="5" fill="#ef4444" font-weight="bold">OH</text>
        <text x="5" y="10" font-size="5" fill="#ef4444" font-weight="bold">OH</text>
        <rect x="21" y="14" width="14" height="14" rx="3" fill="#0f172a" stroke="#a78bfa" stroke-width="1.8"/>
        <line x1="21" y1="18" x2="18" y2="18" stroke="#a78bfa" stroke-width="1.2"/>
        <line x1="21" y1="24" x2="18" y2="24" stroke="#a78bfa" stroke-width="1.2"/>
        <line x1="35" y1="18" x2="38" y2="18" stroke="#a78bfa" stroke-width="1.2"/>
        <line x1="35" y1="24" x2="38" y2="24" stroke="#a78bfa" stroke-width="1.2"/>
        <line x1="28" y1="14" x2="28" y2="12" stroke="#a78bfa" stroke-width="1.2"/>
        <line x1="28" y1="28" x2="28" y2="30" stroke="#a78bfa" stroke-width="1.2"/>
        <circle cx="28" cy="21" r="5" fill="rgba(167,139,250,0.12)" stroke="#c084fc" stroke-width="1.2"/>
        <circle cx="25.5" cy="18.5" r="1.5" fill="#a78bfa"/>
        <circle cx="30.5" cy="18.5" r="1.5" fill="#a78bfa"/>
        <circle cx="28" cy="24" r="1.5" fill="#c084fc"/>
        <line x1="25.5" y1="18.5" x2="28" y2="24" stroke="#a78bfa" stroke-width="1"/>
        <line x1="30.5" y1="18.5" x2="28" y2="24" stroke="#a78bfa" stroke-width="1"/>
        <line x1="25.5" y1="18.5" x2="30.5" y2="18.5" stroke="#a78bfa" stroke-width="1"/>
        <text x="28" y="16" font-size="4" fill="#c084fc" text-anchor="middle" font-weight="700">AI</text>
        <circle cx="28" cy="12.5" r="2" fill="#22d3ee">
            <animate attributeName="opacity" values="1;0.3;1" dur="1.5s" repeatCount="indefinite"/>
        </circle>
    </svg>
    '''
    
    st.markdown(f"""
    <div class="header-wrapper">
        <div class="header-content">
            <div class="header-left">
                <div class="logo-box">
                    <div style="width:56px;height:56px;">{logo_svg}</div>
                    <div class="logo-label">CCWANG_FIZSAB</div>
                </div>
                <div class="header-title-block">
                    <div class="header-title">Glyco<span>Search</span></div>
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
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
        "🔍 Search", "💬 Ask AI", "📊 Analytics", "📚 Methods", 
        "🧪 Draw", "🎯 Screening", "📱 QR Code", "⚙️ Settings", "📋 About"
    ])

    # ─── TAB 1: SEARCH ────────────────────────────────
    with tab1:
        st.markdown("""
        <div class="search-wrapper">
            <div class="search-label">🔎 Find papers by keyword</div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([4, 1])
        with col1:
            keyword = st.text_input("", placeholder="e.g. NIS, sialic acid, Koenigs-Knorr, thioglycoside", label_visibility="collapsed")
        with col2:
            max_results = st.selectbox("Show", [10, 20, 50, 100], index=0)
        
        topics_list = ['All Topics'] + sorted(papers['Topic'].dropna().unique().tolist())
        selected_topic = st.selectbox("Filter by Topic", topics_list, index=0)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        if keyword:
            kw = keyword.lower()
            mask = (papers['Title'].astype(str).str.lower().str.contains(kw, na=False) | 
                    papers['Abstract'].astype(str).str.lower().str.contains(kw, na=False))
            
            if selected_topic != 'All Topics':
                mask = mask & (papers['Topic'] == selected_topic)
            
            results = papers[mask].copy()
            
            st.markdown(f"""
            <p style="font-family:'Inter',sans-serif;font-weight:500;font-size:0.9rem;color:#0f172a;">
                📊 Found <strong>{len(results)}</strong> papers
            </p>
            """, unsafe_allow_html=True)
            
            if len(results) == 0:
                st.info("No matches found. Try different keywords.")
            else:
                for _, row in results.head(max_results).iterrows():
                    title = str(row.get('Title', 'No title'))
                    year = str(row.get('Year', '?'))
                    journal = str(row.get('Journal', '?'))
                    topic = str(row.get('Topic', '?'))
                    abstract = str(row.get('Abstract', ''))
                    
                    with st.expander(f"📄 {title[:100]}{'...' if len(title) > 100 else ''}", expanded=False):
                        st.markdown(f"""
                        <div class="result-card">
                            <div class="result-title">{title}</div>
                            <div class="result-meta">
                                <span class="badge badge-year">📅 {year}</span>
                                <span class="badge badge-topic">📂 {topic}</span>
                                <span class="badge badge-journal">📖 {journal}</span>
                            </div>
                            {f'<div class="result-abstract">{abstract[:500]}...</div>' if len(abstract) > 10 else ''}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        url = row.get('URL', '#')
                        if url != '#':
                            st.markdown(f"[🔗 View in PubMed]({url})")

    # ─── TAB 2: ASK AI ──────────────────────────────────
    with tab2:
        st.markdown("### 💬 Ask GlycoAI - Research Assistant")
        st.markdown("Ask about RRV, Aka, leaving groups, reaction conditions, and screening decisions!")
        
        st.markdown("#### 💡 Try asking about:")
        
        example_questions = [
            "How do I screen reactions for glycosylation?",
            "Which reactions should I do first?",
            "What are the best leaving groups for glycosylation?",
            "How does RRV affect glycosylation selectivity?",
            "What protecting groups should I use?",
            "Tell me about thioglycoside donors"
        ]
        
        cols = st.columns(2)
        for i, q in enumerate(example_questions):
            col_idx = i % 2
            if cols[col_idx].button(
                f"💡 {q}",
                key=f"example_{i}",
                use_container_width=True,
                type="secondary"
            ):
                st.session_state['ask_question'] = q
                st.rerun()
        
        default_question = st.session_state.get('ask_question', '')
        
        question = st.text_area(
            "Or type your own question:",
            value=default_question,
            placeholder="e.g., How should I prioritize my glycosylation reactions?",
            height=80
        )
        
        col1, col2 = st.columns([1, 5])
        with col1:
            ask_button = st.button("🔍 Ask", type="primary", use_container_width=True)
        
        if ask_button and question:
            with st.spinner("🔬 Searching through our knowledge base and literature..."):
                result = engine.answer_question(question)
            
            st.markdown(f"""
            <div class="ai-answer">
                <div class="answer-text">{result['answer']}</div>
                <div class="source-count">📚 Based on {result['source_count']} relevant sources</div>
            </div>
            """, unsafe_allow_html=True)
            
            if result['references']:
                st.markdown("**📖 References & Further Reading:**")
                for ref in result['references']:
                    st.markdown(f"- {ref}")
        
        elif ask_button and not question:
            st.warning("Please enter a question.")

# ─── TAB 3: ANALYTICS ──────────────────────────────
with tab3:
    st.markdown('<p class="analytics-title">📊 Research Analytics</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Clean the Year column - remove non-numeric values
        years_clean = papers['Year'].dropna()
        years_clean = years_clean[pd.to_numeric(years_clean, errors='coerce').notna()]
        
        if len(years_clean) > 0:
            year_counts = years_clean.value_counts().sort_index()
            
            # Convert to DataFrame with proper numeric types
            year_df = year_counts.reset_index()
            year_df.columns = ['Year', 'Count']
            year_df['Year'] = pd.to_numeric(year_df['Year'], errors='coerce')
            year_df = year_df.dropna()
            
            if len(year_df) > 0:
                chart = alt.Chart(year_df).mark_bar(
                    cornerRadiusTopLeft=4, cornerRadiusTopRight=4
                ).encode(
                    x=alt.X('Year:O', sort='-y', title=None),  # 'O' for ordinal
                    y=alt.Y('Count:Q', title=None),
                    color=alt.Color('Count:Q', scale=alt.Scale(scheme='viridis'), legend=None),
                    tooltip=['Year', 'Count']
                ).properties(height=300, title="📅 Publications by Year")
                st.altair_chart(chart, use_container_width=True)
            else:
                st.info("No valid year data available")
        else:
            st.info("No year data available")
    
    with col2:
        topic_counts = papers['Topic'].value_counts()
        if len(topic_counts) > 0:
            topic_df = topic_counts.head(10).reset_index()
            topic_df.columns = ['Topic', 'Count']
            
            chart = alt.Chart(topic_df).mark_bar(
                cornerRadiusTopLeft=4, cornerRadiusTopRight=4
            ).encode(
                x=alt.X('Topic:N', sort='-y', title=None),
                y=alt.Y('Count:Q', title=None),
                color=alt.Color('Count:Q', scale=alt.Scale(scheme='plasma'), legend=None),
                tooltip=['Topic', 'Count']
            ).properties(height=300, title="📂 Papers by Topic")
            st.altair_chart(chart, use_container_width=True)
    
    st.markdown("---")
    st.markdown('<p class="analytics-title">🏆 Top Journals</p>', unsafe_allow_html=True)
    journal_counts = papers['Journal'].value_counts().head(10)
    if len(journal_counts) > 0:
        st.dataframe(
            journal_counts.reset_index().rename(columns={'index': 'Journal', 'Journal': 'Count'}),
            use_container_width=True,
            hide_index=True
        )
    # ─── TAB 4: METHODS ─────────────────────────────────
    with tab4:
        st.markdown("### 📚 Glycosylation Methods Reference")
        
        methods_data = {
            "Method": ["Koenigs-Knorr", "Schmidt (imidate)", "Thioglycoside", "Glycosyl phosphate", 
                       "Glycosyl fluoride", "Sulfoxide (Kahne)", "n-Pentenyl", "Glycosyl boronate"],
            "Donor": ["Glycosyl halide (Br/Cl)", "Trichloroacetimidate", "S-Ph or S-Et glycoside", 
                      "Diphenyl phosphate", "Glycosyl fluoride", "Glycosyl sulfoxide", 
                      "n-Pentenyl glycoside", "Boronic acid derivative"],
            "Activator": ["Ag₂O, Ag₂CO₃, AgOTf", "BF₃·Et₂O or TMSOTf", "NIS/TfOH or DMTST", "TMSOTf", 
                          "Cp₂HfCl₂/AgClO₄", "Tf₂O", "NIS/Et₃SiOTf", "None (metal-free)"],
            "Selectivity": ["α or β (NGP)", "β (C2-acyl)", "Tunable α/β", "β-selective", 
                            "Varies", "α possible", "Varies", "β-selective"],
            "Temp": ["0°C to RT", "−40°C to RT", "−78°C to RT", "−78°C", 
                     "RT", "−78°C", "−10°C", "RT"]
        }
        st.dataframe(pd.DataFrame(methods_data), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.markdown("### 📖 Common Terminology")
        terms = {
            "RRV": "Relative Reactivity Value - measures donor reactivity",
            "Aka": "Acceptor Reactivity Parameter - measures acceptor nucleophilicity",
            "NGP": "Neighboring Group Participation - using acyl group at C2",
            "TMSOTf": "Trimethylsilyl trifluoromethanesulfonate - Lewis acid activator",
            "NIS": "N-Iodosuccinimide - thiophilic activator",
            "1,2-cis": "Glycosidic bond on same side as C2 substituent",
            "1,2-trans": "Glycosidic bond on opposite side from C2 substituent",
            "Remote Participation": "Influence of groups at positions other than C2"
        }
        for term, definition in terms.items():
            st.markdown(f"**{term}:** {definition}")

    # ─── TAB 5: DRAW ────────────────────────────────────
    with tab5:
        chemical_drawing_tool()

    # ─── TAB 6: SCREENING DECISION SUPPORT ─────────────
    with tab6:
        st.markdown("### 🎯 Reaction Screening Decision Support")
        st.markdown("Get organized recommendations for which reactions to prioritize")
        
        col1, col2 = st.columns(2)
        
        with col1:
            donor_type = st.selectbox(
                "Select Donor Type",
                list(REACTION_SCREENING_KNOWLEDGE['donors'].keys())
            )
        
        with col2:
            acceptor_type = st.selectbox(
                "Select Acceptor Type",
                list(REACTION_SCREENING_KNOWLEDGE['acceptors'].keys())
            )
        
        target_selectivity = st.selectbox(
            "Target Selectivity (optional)",
            ["Any", "α", "β"],
            index=0
        )
        
        if st.button("🔬 Generate Screening Plan", type="primary"):
            recommendations = screen_reactions(
                donor_type, 
                acceptor_type, 
                target_selectivity if target_selectivity != "Any" else None
            )
            
            st.markdown("### 📋 Recommended Reaction Order")
            
            for i, rec in enumerate(recommendations):
                priority_class = rec['priority'].lower()
                st.markdown(f"""
                <div class="decision-card">
                    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;">
                        <div>
                            <strong>#{i+1}. {rec['donor']} + {acceptor_type}</strong>
                        </div>
                        <span class="priority-{priority_class}">{rec['priority']} Priority</span>
                    </div>
                    <div style="margin-top:0.5rem;font-size:0.85rem;color:#475569;">
                        <span style="background:#f1f5f9;padding:2px 8px;border-radius:4px;margin-right:8px;">
                            Score: {rec['score']}
                        </span>
                        <span style="background:#f1f5f9;padding:2px 8px;border-radius:4px;margin-right:8px;">
                            RRV: {rec['rrv']}
                        </span>
                        <span style="background:#f1f5f9;padding:2px 8px;border-radius:4px;margin-right:8px;">
                            {rec['selectivity']}
                        </span>
                    </div>
                    <div style="margin-top:0.3rem;font-size:0.8rem;color:#64748b;">
                        <strong>Condition:</strong> {rec['condition']} · {rec['temp']} · Yield: {rec['yield']}
                    </div>
                    <div style="margin-top:0.3rem;font-size:0.75rem;color:#94a3b8;">
                        <strong>Why:</strong> {', '.join(rec['reasons'][:3])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with st.expander("📖 Screening Rules & Guidelines"):
                st.markdown("**Rules for Prioritizing Reactions:**")
                for rule in REACTION_SCREENING_KNOWLEDGE['screening_rules']:
                    st.markdown(f"• {rule}")
        
        with st.expander("📊 Donor & Acceptor Quick Reference"):
            st.markdown("**Donors with RRV Values:**")
            donor_df = pd.DataFrame([
                {'Donor': d, 'RRV': info['rrv'], 'Cost': info['cost'], 
                 'Availability': info['availability'], 'Selectivity': info['selectivity']}
                for d, info in REACTION_SCREENING_KNOWLEDGE['donors'].items()
            ])
            st.dataframe(donor_df, use_container_width=True, hide_index=True)
            
            st.markdown("**Acceptors with Aka Values:**")
            acceptor_df = pd.DataFrame([
                {'Acceptor': a, 'Aka': info['aka'], 'Hindrance': info['hindrance'], 
                 'Reactivity': info['reactivity']}
                for a, info in REACTION_SCREENING_KNOWLEDGE['acceptors'].items()
            ])
            st.dataframe(acceptor_df, use_container_width=True, hide_index=True)

    # ─── TAB 7: QR CODE ──────────────────────────────────
    with tab7:
        st.markdown("### 📱 QR Code - Share GlycoSearch")
        
        app_url = st.text_input(
            "App URL",
            value="https://glycosearch.streamlit.app",
            help="Enter the URL where your app is deployed"
        )
        
        app_name = st.text_input("App Name", value="GlycoSearch")
        institute = st.text_input("Institute", value="Academia Sinica")
        
        if st.button("🔄 Generate QR Code", type="primary"):
            qr_html = create_branded_qr_card(app_url, app_name, institute)
            st.markdown(qr_html, unsafe_allow_html=True)
            
            qr_img = generate_qr_code(app_url, app_name, institute)
            st.download_button(
                label="📥 Download QR Code",
                data=base64.b64decode(qr_img),
                file_name="glycosearch_qr.png",
                mime="image/png"
            )
        
        with st.expander("📖 How to use QR Code"):
            st.markdown("""
            1. **Deploy your app** to a cloud platform (Streamlit Cloud, Heroku, etc.)
            2. **Copy your app URL** and paste it above
            3. **Generate QR code** and download the image
            4. **Print or share** the QR code on posters, presentations, or websites
            5. **Users scan** the QR code to instantly access GlycoSearch
            """)

    # ─── TAB 8: SETTINGS ────────────────────────────────
    with tab8:
        st.markdown("### ⚙️ Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Data Management**")
            if st.button("🔄 Reload Data"):
                st.cache_data.clear()
                st.cache_resource.clear()
                st.rerun()
            
            st.markdown("**Export**")
            if st.button("📥 Export All Data"):
                csv = papers.to_csv(index=False)
                st.download_button("Download CSV", csv, "glycosylation_papers.csv")
        
        with col2:
            st.markdown("**System Info**")
            st.code(f"Papers: {len(papers)}")
            st.code(f"Topics: {papers['Topic'].nunique() if len(papers) > 0 else 0}")
            st.code(f"Knowledge Index: {len(engine.index)} papers")
            st.code("Expert Topics: RRV/Aka, Leaving Groups, Reaction Conditions, Protecting Groups")

    # ─── TAB 9: ABOUT ────────────────────────────────────
    with tab9:
        st.markdown("### 📋 About GlycoSearch")
        
        st.markdown("""
        <div class="about-box">
            <h3>🧬 GlycoSearch</h3>
            <p>
                <b>Developed by:</b> Fizza Sabbor and Dr. Sabbor Hussain<br>
                <b>Institute:</b> <a href="https://www.chem.sinica.edu.tw" target="_blank" class="clickable-link">Institute of Chemistry, Academia Sinica</a><br>
                <b>Principal Investigator:</b> <a href="https://www.chem.sinica.edu.tw/en/faculty/104/" target="_blank" class="clickable-link">Dr. Cheng-Chung Wang</a><br>
                <b>Email:</b> <a href="mailto:wangcc7280@gate.sinica.edu.tw" class="clickable-link">wangcc7280@gate.sinica.edu.tw</a>
            </p>
            <hr>
            <h4>🧪 Knowledge Base Features</h4>
            <ul>
                <li><b>RRV & Aka</b> - Reactivity parameters for donors and acceptors</li>
                <li><b>Leaving Groups</b> - 13 leaving groups with reactivity and conditions</li>
                <li><b>Reaction Conditions</b> - Detailed protocols for glycosylation</li>
                <li><b>Protecting Groups</b> - Effects and selectivity information</li>
                <li><b>Reaction Screening</b> - Decision support for prioritizing reactions</li>
                <li><b>QR Code Generation</b> - Share your app with QR codes</li>
                <li><b>Chemical Drawing</b> - Draw structures with sugar chemistry groups</li>
            </ul>
            <h4>📚 Data</h4>
            <p>1,676+ glycosylation research papers from PubMed (1967-2026)</p>
            <h4>🔗 Citation</h4>
            <p>
                <i>Fizza Sabbor, Dr. Sabbor Hussain, Wang Research Group, GlycoSearch: Glycosylation Research Agent, 
                Institute of Chemistry, Academia Sinica, 2026.</i>
            </p>
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
