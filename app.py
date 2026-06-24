import streamlit as st
import pandas as pd
import os
import streamlit.components.v1 as components
from datetime import datetime
import csv

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
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.2rem;
        background: #ffffff;
        padding: 0.3rem 0.5rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        border: 1px solid #e8ecf2;
        margin-bottom: 1.2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 0.85rem !important;
        color: #64748b;
        padding: 0.4rem 1.2rem !important;
        border-radius: 8px;
        transition: all 0.2s ease;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #f1f5f9;
        color: #0f172a;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: #0f172a;
        color: #ffffff;
        box-shadow: 0 2px 10px rgba(15, 23, 42, 0.12);
        font-weight: 600;
    }
    
    .search-wrapper {
        background: #ffffff;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        border: 1px solid #e8ecf2;
        margin-bottom: 1rem;
    }
    
    .search-label {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 0.8rem;
        color: #0f172a;
        margin-bottom: 0.2rem;
    }
    
    .result-card {
        background: #ffffff;
        padding: 0.7rem 1.2rem;
        border-radius: 10px;
        border: 1px solid #e8ecf2;
        margin-bottom: 0.5rem;
        transition: all 0.2s ease;
    }
    
    .result-card:hover {
        border-color: #c7d2fe;
        box-shadow: 0 2px 12px rgba(99, 102, 241, 0.05);
    }
    
    .result-title {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.9rem;
        color: #0f172a;
        line-height: 1.4;
    }
    
    .result-meta {
        font-family: 'Inter', sans-serif;
        font-size: 0.65rem;
        color: #94a3b8;
        margin-top: 0.2rem;
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem;
        align-items: center;
    }
    
    .badge {
        display: inline-block;
        padding: 0.08rem 0.6rem;
        border-radius: 50px;
        font-size: 0.55rem;
        font-weight: 500;
    }
    .badge-year { background: #f1f5f9; color: #475569; }
    .badge-topic { background: #eef2ff; color: #4f46e5; }
    .badge-journal { background: #fce7f3; color: #be185d; }
    
    .result-abstract {
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        font-size: 0.78rem;
        color: #475569;
        line-height: 1.5;
        margin-top: 0.3rem;
        padding-top: 0.3rem;
        border-top: 1px solid #f1f5f9;
    }
    
    .footer-container {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        padding: 1.2rem 0;
        border-radius: 16px 16px 0 0;
        margin-top: 2rem;
        text-align: center;
        border-top: 3px solid transparent;
        border-image: linear-gradient(90deg, #818cf8, #c084fc) 1;
    }
    
    .footer-container .org-name {
        color: #ffffff;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 0.9rem;
        margin-bottom: 0.1rem;
    }
    
    .footer-container .org-desc {
        color: rgba(255,255,255,0.4);
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
    }
    
    .footer-container .divider {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.06);
        margin: 0.5rem auto;
        width: 25%;
    }
    
    .footer-container .footer-links {
        display: flex;
        justify-content: center;
        gap: 1.2rem;
        flex-wrap: wrap;
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem;
        color: rgba(255,255,255,0.3);
    }
    
    .footer-container .footer-links a {
        color: #a78bfa;
        text-decoration: none;
    }
    
    .footer-container .footer-links a:hover {
        text-decoration: underline;
    }
    
    .footer-container .footer-address {
        font-family: 'Inter', sans-serif;
        font-size: 0.6rem;
        color: rgba(255,255,255,0.12);
        margin-top: 0.3rem;
    }
    
    .footer-container .footer-email {
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem;
        color: rgba(255,255,255,0.25);
        margin-top: 0.1rem;
    }
    
    @media (max-width: 768px) {
        .header-content { flex-direction: column; align-items: flex-start; padding: 0 1rem; }
        .header-stats { flex-wrap: wrap; gap: 0.5rem; padding: 0.25rem 0.8rem; }
        .header-title { font-size: 1.2rem; }
        .stTabs [data-baseweb="tab"] { font-size: 0.7rem !important; padding: 0.3rem 0.8rem !important; }
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
    .about-box .highlight { color: #6366f1; font-weight: 500; }
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

# ─── DRAWING TOOL ──────────────────────────────────────
def chemical_drawing_tool():
    components.html("""
    <style>
        .draw-header { background: linear-gradient(135deg, #f8fafc, #eef2ff); border: 2px solid #e2e8f0; border-radius: 14px; padding: 1rem 1.5rem; margin-bottom: 0.8rem; text-align: center; }
        .draw-header h2 { font-family: 'Inter', sans-serif; font-weight: 700; font-size: 1.3rem; color: #0f172a; margin: 0; }
        .draw-header h2 span { background: linear-gradient(135deg, #6366f1, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .draw-header p { font-family: 'Inter', sans-serif; font-size: 0.8rem; color: #64748b; margin: 0.2rem 0 0 0; }
        .draw-toolbar { display: flex; gap: 4px; padding: 6px 0; flex-wrap: wrap; align-items: center; }
        .draw-toolbar button { padding: 4px 10px; border: none; border-radius: 6px; background: #f1f5f9; color: #0f172a; cursor: pointer; font-size: 11px; font-family: 'Inter', sans-serif; font-weight: 500; transition: all 0.2s; }
        .draw-toolbar button:hover { background: #e2e8f0; }
        .draw-toolbar button.active { background: #0f172a; color: white; }
        .draw-toolbar button.danger { background: #fee2e2; color: #991b1b; }
        .draw-toolbar button.success { background: #dcfce7; color: #166534; }
        .draw-toolbar button.warning { background: #fef3c7; color: #92400e; }
        .draw-toolbar button.info { background: #dbeafe; color: #1e40af; }
        .draw-toolbar button.purple { background: #f3e8ff; color: #6b21a8; }
        .draw-toolbar select { padding: 4px 8px; border-radius: 6px; border: 1px solid #e2e8f0; font-size: 11px; font-family: 'Inter', sans-serif; background: white; }
        #canvas { border: 2px solid #e2e8f0; background: white; border-radius: 12px; cursor: crosshair; width: 100%; height: auto; }
        #smiles-output { width: 100%; padding: 8px 12px; border: 2px solid #e2e8f0; border-radius: 8px; margin-top: 8px; font-family: monospace; font-size: 12px; background: #f8fafc; }
        .mode-status { padding: 2px 10px; border-radius: 50px; font-size: 10px; font-weight: 500; font-family: 'Inter', sans-serif; display: inline-block; }
        .mode-draw { background: #dcfce7; color: #166534; }
        .mode-replace { background: #fef3c7; color: #92400e; }
        .mode-delete { background: #fee2e2; color: #991b1b; }
        .mode-select { background: #dbeafe; color: #1e40af; }
        .mode-eraser { background: #fce4ec; color: #880e4f; }
        .draw-info { color: #94a3b8; font-size: 10px; font-family: 'Inter', sans-serif; }
        .toolbar-group { display: flex; gap: 3px; align-items: center; background: #f8fafc; padding: 2px 8px; border-radius: 8px; }
        .toolbar-label { font-size: 9px; color: #94a3b8; font-weight: 600; margin-right: 3px; font-family: 'Inter', sans-serif; text-transform: uppercase; letter-spacing: 0.05em; }
        .bond-type-indicator { font-size: 10px; color: #64748b; padding: 1px 8px; background: #f1f5f9; border-radius: 4px; }
    </style>
    <div class="draw-header">
        <h2>🧪 Draw <span>Chemical Structure</span></h2>
        <p>Build molecules by adding atoms and bonds • Select from tool palette below</p>
    </div>
    <div class="draw-toolbar">
        <div class="toolbar-group">
            <span class="toolbar-label">Mode</span>
            <button id="btn-draw" class="active">✏️ Atom</button>
            <button id="btn-replace" class="warning">🔄 Replace</button>
            <button id="btn-line">🔗 Bond</button>
            <button id="btn-eraser" class="danger">🧹 Eraser</button>
            <button id="btn-select" class="info">⬜ Select</button>
            <button id="btn-benzene" class="purple">⬡ Benzene</button>
        </div>
        <div class="toolbar-group">
            <span class="toolbar-label">Atom</span>
            <select id="atom-select">
                <option value="C">C</option><option value="O">O</option><option value="N">N</option><option value="H">H</option>
                <option value="S">S</option><option value="P">P</option><option value="F">F</option><option value="Cl">Cl</option>
                <option value="Br">Br</option><option value="I">I</option>
                <option value="OH">OH</option><option value="OMe">OMe</option><option value="OBn">OBn</option><option value="OBz">OBz</option>
                <option value="OAc">OAc</option><option value="N3">N3</option><option value="NH2">NH2</option><option value="OTs">OTs</option>
                <option value="STol">STol</option>
                <option value="TBDMS">TBDMS</option><option value="TIPS">TIPS</option>
                <option value="Bz">Bz</option><option value="Bn">Bn</option><option value="Ac">Ac</option>
            </select>
        </div>
        <div class="toolbar-group">
            <span class="toolbar-label">Bond</span>
            <button id="btn-single-bond" class="active">─</button>
            <button id="btn-double-bond">═</button>
            <button id="btn-triple-bond">≡</button>
        </div>
        <div class="toolbar-group">
            <button id="btn-undo">↩️ Undo</button>
            <button id="btn-clear" class="danger">🗑️ Clear</button>
            <button id="btn-smiles" class="success">📋 SMILES</button>
        </div>
    </div>
    <div style="display:flex; gap:8px; margin-bottom:6px; align-items:center; flex-wrap:wrap;">
        <span id="mode-status" class="mode-status mode-draw">✏️ Draw Mode</span>
        <span class="bond-type-indicator" id="bond-type-indicator">Bond: Single</span>
        <span class="draw-info">💡 Click to add • Eraser: click to remove • Select: drag + Delete</span>
    </div>
    <canvas id="canvas" width="750" height="480"></canvas>
    <input id="smiles-output" placeholder="SMILES will appear here...">
    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        let isDrawing = false, lastX, lastY;
        let atoms = [], bonds = [], history = [];
        let tool = 'draw';
        let selectedAtom = 'C';
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

        document.getElementById('atom-select').onchange = function() { selectedAtom = this.value; };

        function getAtomColor(label) {
            const colors = {'C':'#333333','O':'#FF0000','N':'#3050F8','H':'#FFFFFF','S':'#FFFF30','P':'#FF8000','F':'#90E050','Cl':'#1FF01F','Br':'#A62929','I':'#940094','OH':'#FF0000','OMe':'#CD5C5C','OBn':'#8B4513','OBz':'#8B6914','OAc':'#CD853F','N3':'#4169E1','NH2':'#4169E1','OTs':'#DAA520','STol':'#8B008B','TBDMS':'#2E8B57','TIPS':'#2E8B57','Bz':'#8B6914','Bn':'#8B4513','Ac':'#CD853F'};
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
                ctx.font = 'bold 11px Inter, Arial, sans-serif';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(label.length > 4 ? label.substring(0,4) : label, x, y);
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
            if (highlight) {
                const mx = (x1+x2)/2, my = (y1+y2)/2;
                ctx.strokeStyle = '#ef4444'; ctx.lineWidth = 2;
                const s = 8;
                ctx.beginPath(); ctx.moveTo(mx-s, my-s); ctx.lineTo(mx+s, my+s);
                ctx.moveTo(mx+s, my-s); ctx.lineTo(mx-s, my+s); ctx.stroke();
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

        function findNearestBond(x, y, threshold) {
            threshold = threshold || 15;
            let nearest = null, minDist = threshold;
            for (const b of bonds) {
                const dx = b.x2 - b.x1, dy = b.y2 - b.y1;
                const len = Math.hypot(dx, dy);
                if (len === 0) continue;
                const t = Math.max(0, Math.min(1, ((x - b.x1)*dx + (y - b.y1)*dy) / (len*len)));
                const px = b.x1 + t*dx, py = b.y1 + t*dy;
                const dist = Math.hypot(x - px, y - py);
                if (dist < minDist) { minDist = dist; nearest = b; }
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
        }

        function saveState() {
            history.push(JSON.parse(JSON.stringify({atoms, bonds})));
            if (history.length > MAX_HISTORY) history.shift();
        }

        function getPos(e) {
            const r = canvas.getBoundingClientRect();
            return { x: (e.clientX - r.x) * (canvas.width / r.width), y: (e.clientY - r.y) * (canvas.height / r.height) };
        }

        function updateModeStatus() {
            const status = document.getElementById('mode-status');
            if (eraserMode) {
                status.className = 'mode-status mode-eraser';
                status.textContent = '🧹 Eraser Mode (click to remove)';
                canvas.style.cursor = 'not-allowed';
            } else if (selectMode) {
                status.className = 'mode-status mode-select';
                status.textContent = '⬜ Select Mode (drag to select, Delete to remove)';
                canvas.style.cursor = 'default';
            } else if (replaceMode) {
                status.className = 'mode-status mode-replace';
                status.textContent = '🔄 Replace Mode (click atom)';
                canvas.style.cursor = 'pointer';
            } else if (deleteBondMode) {
                status.className = 'mode-status mode-delete';
                status.textContent = '✖️ Delete Bond Mode (click bond)';
                canvas.style.cursor = 'crosshair';
            } else {
                status.className = 'mode-status mode-draw';
                status.textContent = '✏️ Draw Mode (click canvas)';
                canvas.style.cursor = 'crosshair';
            }
        }

        canvas.onmousedown = function(e) {
            const pos = getPos(e);
            if (eraserMode) {
                const atom = findNearestAtom(pos.x, pos.y);
                if (atom) {
                    saveState();
                    atoms = atoms.filter(a => a !== atom);
                    bonds = bonds.filter(b => b.x1 !== atom.x || b.y1 !== atom.y);
                    bonds = bonds.filter(b => b.x2 !== atom.x || b.y2 !== atom.y);
                    drawAll(); return;
                }
                const bond = findNearestBond(pos.x, pos.y);
                if (bond) { saveState(); bonds = bonds.filter(b => b !== bond); drawAll(); }
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
            if (deleteBondMode) {
                const bond = findNearestBond(pos.x, pos.y);
                if (bond) { saveState(); bonds = bonds.filter(b => b !== bond); drawAll(); }
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
                atoms.push({x: pos.x, y: pos.y, label: selectedAtom, id: atomIdCounter++});
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
            if (replaceMode) {
                canvas.style.cursor = findNearestAtom(pos.x, pos.y) ? 'pointer' : 'default';
            }
            if (eraserMode) {
                const atom = findNearestAtom(pos.x, pos.y);
                const bond = findNearestBond(pos.x, pos.y);
                canvas.style.cursor = (atom || bond) ? 'pointer' : 'not-allowed';
            }
        };

        canvas.onmouseup = function(e) {
            if (selectMode && selectionStart) {
                const pos = getPos(e);
                const selected = getAtomsInRect(selectionStart.x, selectionStart.y, pos.x, pos.y);
                selectedAtoms = selected;
                drawAll();
                selected.forEach(a => drawAtom(a.x, a.y, a.label, false, true));
                if (selected.length > 0) {
                    document.getElementById('mode-status').textContent = `✅ ${selected.length} atoms selected. Press Delete to remove.`;
                }
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
                    const na = {x: pos.x, y: pos.y, label: selectedAtom, id: atomIdCounter++};
                    atoms.push(na);
                    bonds.push({x1: startAtom.x, y1: startAtom.y, x2: na.x, y2: na.y, type: bondType});
                } else {
                    const a1 = {x: lastX, y: lastY, label: selectedAtom, id: atomIdCounter++};
                    const a2 = {x: pos.x, y: pos.y, label: selectedAtom, id: atomIdCounter++};
                    atoms.push(a1); atoms.push(a2);
                    bonds.push({x1: a1.x, y1: a1.y, x2: a2.x, y2: a2.y, type: bondType});
                }
                drawAll();
                isDrawing = false;
            }
        };

        canvas.oncontextmenu = e => e.preventDefault();

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
                document.getElementById('mode-status').textContent = '🗑️ Deleted selected atoms';
            }
        });

        document.getElementById('btn-draw').onclick = function() {
            tool = 'draw'; replaceMode = false; deleteBondMode = false; selectMode = false; eraserMode = false;
            selectionStart = null; selectionEnd = null; selectedAtoms = [];
            document.querySelectorAll('.draw-toolbar button').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            updateModeStatus();
        };
        document.getElementById('btn-replace').onclick = function() {
            replaceMode = !replaceMode;
            if (replaceMode) {
                deleteBondMode = false; selectMode = false; eraserMode = false;
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
        document.getElementById('btn-line').onclick = function() {
            tool = 'line'; replaceMode = false; deleteBondMode = false; selectMode = false; eraserMode = false;
            selectionStart = null; selectionEnd = null; selectedAtoms = [];
            document.querySelectorAll('.draw-toolbar button').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            updateModeStatus();
        };
        document.getElementById('btn-eraser').onclick = function() {
            eraserMode = !eraserMode;
            if (eraserMode) {
                replaceMode = false; deleteBondMode = false; selectMode = false;
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
                replaceMode = false; deleteBondMode = false; eraserMode = false;
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
            tool = 'benzene'; replaceMode = false; deleteBondMode = false; selectMode = false; eraserMode = false;
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

        drawBenzene(375, 240);
        drawAll();
        saveState();
        updateModeStatus();
    </script>
    """, height=560)

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
                    <div class="logo-label">CCWang_FizSab</div>
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
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🔍 Search",
        "📊 Analytics", 
        "📚 Methods",
        "🧪 Draw",
        "⚙️ Settings",
        "📋 About"
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
            max_results = st.selectbox("Show", [10, 20, 50, 100], index=0, label_visibility="collapsed")
        
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

    # ─── TAB 2: ANALYTICS ──────────────────────────────
    with tab2:
        st.markdown("### 📊 Research Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📅 Publications by Year**")
            year_counts = papers['Year'].value_counts().sort_index()
            if len(year_counts) > 0:
                st.bar_chart(year_counts)
        
        with col2:
            st.markdown("**📂 Papers by Topic**")
            topic_counts = papers['Topic'].value_counts()
            if len(topic_counts) > 0:
                st.bar_chart(topic_counts.head(10))
        
        st.markdown("---")
        st.markdown("**🏆 Top Journals**")
        journal_counts = papers['Journal'].value_counts().head(10)
        if len(journal_counts) > 0:
            st.dataframe(
                journal_counts.reset_index().rename(columns={'index': 'Journal', 'Journal': 'Count'}),
                use_container_width=True,
                hide_index=True
            )

    # ─── TAB 3: METHODS ─────────────────────────────────
    with tab3:
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
            "NGP": "Neighboring Group Participation - using an acyl group at C2 to direct β-selectivity",
            "TMSOTf": "Trimethylsilyl trifluoromethanesulfonate - common Lewis acid activator",
            "NIS": "N-Iodosuccinimide - thiophilic activator for thioglycosides",
            "DMTST": "Dimethyl(methylthio)sulfonium triflate - thiophilic activator",
            "1,2-cis": "The newly formed glycosidic bond is on the same side as the C2 substituent",
            "1,2-trans": "The newly formed glycosidic bond is on the opposite side from the C2 substituent"
        }
        for term, definition in terms.items():
            st.markdown(f"**{term}:** {definition}")

    # ─── TAB 4: DRAW ────────────────────────────────────
    with tab4:
        chemical_drawing_tool()

    # ─── TAB 5: SETTINGS ────────────────────────────────
    with tab5:
        st.markdown("### ⚙️ Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Data Management**")
            if st.button("🔄 Reload Data"):
                st.cache_data.clear()
                st.rerun()
            
            st.markdown("**Export**")
            if st.button("📥 Export All Data"):
                csv = papers.to_csv(index=False)
                st.download_button("Download CSV", csv, "glycosylation_papers.csv")
        
        with col2:
            st.markdown("**System Info**")
            st.code(f"Papers: {len(papers)}")
            st.code(f"Topics: {papers['Topic'].nunique() if len(papers) > 0 else 0}")
            
            if os.path.exists("feedback.csv"):
                fb_df = pd.read_csv("feedback.csv")
                st.metric("📊 Feedback Entries", len(fb_df))

    # ─── TAB 6: ABOUT ────────────────────────────────────
    with tab6:
        st.markdown("### 📋 About GlycoSearch")
        
        st.markdown("""
        <div class="about-box">
            <h3>🧬 GlycoSearch</h3>
            <p>
                <b>Developer:</b> Wang Research Group<br>
                <b>Institute:</b> Institute of Chemistry, Academia Sinica<br>
                <b>Principal Investigator:</b> Dr. Cheng-Chung Wang<br>
                <b>Email:</b> <span class="highlight">wangcc7280@gate.sinica.edu.tw</span>
            </p>
            <hr>
            <h4>📄 License</h4>
            <p>MIT License — Free for academic and research use.</p>
            <h4>© Copyright</h4>
            <p>© 2026 Wang Research Group, Institute of Chemistry, Academia Sinica</p>
            <h4>📚 Data Sources</h4>
            <p>PubMed publications extracted with AI (2026).<br>Contains 1,040+ glycosylation research papers.</p>
            <h4>🔗 Citation</h4>
            <p>
                If you use this tool, please cite:<br>
                <i>Wang Research Group, GlycoSearch: Glycosylation Research Agent, 
                Institute of Chemistry, Academia Sinica, 2026.</i>
            </p>
        </div>
        """, unsafe_allow_html=True)

# ─── FOOTER ─────────────────────────────────────────────
st.markdown("""
<div class="footer-container">
    <div class="org-name">🏛️ Institute of Chemistry, Academia Sinica</div>
    <div class="org-desc">Wang Research Group · Dr. Cheng-Chung Wang</div>
    <div class="footer-email">wangcc7280@gate.sinica.edu.tw</div>
    
    <hr class="divider">
    
    <div class="footer-links">
        <span>📄 MIT License</span>
        <span>© 2026 Academia Sinica</span>
        <span><a href="https://github.com/FizzaSab/GlycoAgent" target="_blank">GitHub</a></span>
        <span><a href="https://www.chem.sinica.edu.tw" target="_blank">Institute Website</a></span>
    </div>
    
    <div class="footer-address">
        128 Academia Road, Section 2, Nankang, Taipei 115201, Taiwan
    </div>
</div>
""", unsafe_allow_html=True)
