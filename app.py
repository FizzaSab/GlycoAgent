import streamlit as st
import pandas as pd
import os
import streamlit.components.v1 as components

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
    
    .stApp {
        background: #f8fafc;
    }
    
    .header-wrapper {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        padding: 1.8rem 0 1.5rem 0;
        border-radius: 0 0 40px 40px;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(15, 23, 42, 0.15);
        position: relative;
        overflow: hidden;
    }
    
    .header-wrapper::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 500px;
        height: 500px;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.08) 0%, transparent 70%);
        border-radius: 50%;
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
        gap: 1rem;
    }
    
    .header-left {
        display: flex;
        align-items: center;
        gap: 1.2rem;
    }
    
    .logo-box {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        background: rgba(255, 255, 255, 0.04);
        padding: 0.4rem 1.2rem 0.4rem 0.8rem;
        border-radius: 100px;
        border: 1px solid rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(10px);
    }
    
    .logo-icon {
        font-size: 2.2rem;
        line-height: 1;
        background: linear-gradient(135deg, #818cf8, #c084fc);
        padding: 0.4rem 0.6rem;
        border-radius: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .logo-text {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 0.95rem;
        color: #ffffff;
        letter-spacing: 0.02em;
    }
    
    .logo-text span {
        color: #a78bfa;
    }
    
    .header-title {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 2rem;
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
        font-size: 0.85rem;
        color: rgba(255, 255, 255, 0.5);
        margin-top: 0.05rem;
        letter-spacing: 0.02em;
    }
    
    .header-right {
        display: flex;
        align-items: center;
        gap: 1.5rem;
        flex-wrap: wrap;
    }
    
    .header-stats {
        display: flex;
        gap: 1.8rem;
        background: rgba(255, 255, 255, 0.04);
        padding: 0.4rem 1.5rem;
        border-radius: 100px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.06);
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-number {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 1.1rem;
        color: #ffffff;
        letter-spacing: -0.01em;
    }
    
    .stat-label {
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        font-size: 0.65rem;
        color: rgba(255, 255, 255, 0.35);
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.3rem;
        background: #ffffff;
        padding: 0.5rem 0.6rem;
        border-radius: 18px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        border: 1px solid #eef2f6;
        margin-bottom: 1.8rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1.1rem !important;
        color: #64748b;
        padding: 0.8rem 2rem !important;
        border-radius: 14px;
        transition: all 0.25s ease;
        background: transparent;
        letter-spacing: 0.01em;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #f1f5f9;
        color: #0f172a;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: #0f172a;
        color: #ffffff;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.18);
        font-weight: 700;
    }
    
    .search-wrapper {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        border: 1px solid #eef2f6;
        margin-bottom: 1.5rem;
    }
    
    .result-card {
        background: #ffffff;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        border: 1px solid #eef2f6;
        margin-bottom: 0.75rem;
        transition: all 0.25s ease;
    }
    
    .result-card:hover {
        border-color: #c7d2fe;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.06);
        transform: translateY(-1px);
    }
    
    .result-title {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1.05rem;
        color: #0f172a;
    }
    
    .result-meta {
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        color: #94a3b8;
        margin-top: 0.3rem;
        display: flex;
        flex-wrap: wrap;
        gap: 0.75rem;
        align-items: center;
    }
    
    .badge {
        display: inline-block;
        padding: 0.15rem 0.7rem;
        border-radius: 100px;
        font-size: 0.7rem;
        font-weight: 500;
    }
    .badge-year { background: #f1f5f9; color: #475569; }
    .badge-topic { background: #eef2ff; color: #4f46e5; }
    .badge-journal { background: #fce7f3; color: #be185d; }
    
    .result-abstract {
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        font-size: 0.9rem;
        color: #475569;
        line-height: 1.6;
        margin-top: 0.5rem;
        padding-top: 0.5rem;
        border-top: 1px solid #f1f5f9;
    }
    
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #94a3b8;
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        border-top: 1px solid #eef2f6;
        margin-top: 3rem;
    }
    
    .footer a { color: #6366f1; text-decoration: none; }
    .footer a:hover { text-decoration: underline; }
    
    @media (max-width: 768px) {
        .header-content { flex-direction: column; align-items: flex-start; padding: 0 1rem; }
        .header-stats { flex-wrap: wrap; gap: 1rem; padding: 0.5rem 1rem; border-radius: 16px; }
        .header-title { font-size: 1.5rem; }
        .logo-box { padding: 0.3rem 0.8rem; }
        .logo-text { font-size: 0.75rem; }
        .stTabs [data-baseweb="tab"] { font-size: 0.85rem !important; padding: 0.5rem 1rem !important; }
        .stTabs [data-baseweb="tab-list"] { padding: 0.3rem; }
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

# ─── DRAWING TOOL ──────────────────────────────────────
def chemical_drawing_tool():
    components.html("""
    <style>
        .draw-toolbar { display: flex; gap: 6px; padding: 10px 0; flex-wrap: wrap; align-items: center; }
        .draw-toolbar button { padding: 6px 14px; border: none; border-radius: 6px; background: #eef2f6; color: #0f172a; cursor: pointer; font-size: 13px; font-family: 'Inter', sans-serif; font-weight: 500; transition: all 0.2s; }
        .draw-toolbar button:hover { background: #e2e8f0; }
        .draw-toolbar button.active { background: #0f172a; color: white; }
        .draw-toolbar button.danger { background: #fee2e2; color: #991b1b; }
        .draw-toolbar button.danger:hover { background: #fecaca; }
        .draw-toolbar button.success { background: #dcfce7; color: #166534; }
        .draw-toolbar button.success:hover { background: #bbf7d0; }
        .draw-toolbar button.warning { background: #fef3c7; color: #92400e; }
        .draw-toolbar button.warning:hover { background: #fde68a; }
        .draw-toolbar select { padding: 6px 12px; border-radius: 6px; border: 1px solid #e2e8f0; font-size: 13px; font-family: 'Inter', sans-serif; background: white; }
        #canvas { border: 2px solid #e2e8f0; background: white; border-radius: 12px; cursor: crosshair; width: 100%; height: auto; }
        #smiles-output { width: 100%; padding: 10px; border: 2px solid #e2e8f0; border-radius: 8px; margin-top: 10px; font-family: monospace; font-size: 13px; }
        .mode-status { padding: 4px 14px; border-radius: 100px; font-size: 12px; font-weight: 500; font-family: 'Inter', sans-serif; display: inline-block; }
        .mode-draw { background: #dcfce7; color: #166534; }
        .mode-replace { background: #fef3c7; color: #92400e; }
        .mode-delete { background: #fee2e2; color: #991b1b; }
        .draw-info { color: #94a3b8; font-size: 12px; font-family: 'Inter', sans-serif; margin-top: 6px; }
        .toolbar-group { display: flex; gap: 4px; align-items: center; background: #f8fafc; padding: 4px 10px; border-radius: 8px; }
        .toolbar-label { font-size: 11px; color: #94a3b8; font-weight: 600; margin-right: 4px; font-family: 'Inter', sans-serif; text-transform: uppercase; letter-spacing: 0.05em; }
    </style>
    <div>
        <div class="draw-toolbar">
            <div class="toolbar-group">
                <span class="toolbar-label">Mode</span>
                <button id="btn-draw" class="active">✏️ Atom</button>
                <button id="btn-replace" class="warning">🔄 Replace</button>
                <button id="btn-line">🔗 Bond</button>
                <button id="btn-benzene">⬡ Benzene</button>
                <button id="btn-delete-bond" class="danger">✖️ Delete</button>
            </div>
            <div class="toolbar-group">
                <span class="toolbar-label">Atom</span>
                <select id="atom-select">
                    <option value="C">C</option><option value="O">O</option><option value="N">N</option><option value="H">H</option>
                    <option value="S">S</option><option value="P">P</option><option value="F">F</option><option value="Cl">Cl</option>
                    <option value="Br">Br</option><option value="I">I</option>
                    <option value="OH">OH</option><option value="OMe">OMe</option><option value="OBn">OBn</option><option value="OBz">OBz</option>
                    <option value="OAc">OAc</option><option value="N3">N3</option><option value="NH2">NH2</option><option value="OTs">OTs</option>
                    <option value="TBDMS">TBDMS</option><option value="TIPS">TIPS</option><option value="Bz">Bz</option><option value="Bn">Bn</option><option value="Ac">Ac</option>
                </select>
            </div>
            <div class="toolbar-group">
                <button id="btn-undo">↩️ Undo</button>
                <button id="btn-clear" class="danger">🗑️ Clear</button>
                <button id="btn-smiles" class="success">📋 Get SMILES</button>
            </div>
        </div>
        <div style="display:flex; gap:12px; margin-bottom:8px; align-items:center; flex-wrap:wrap;">
            <span id="mode-status" class="mode-status mode-draw">✏️ Draw Mode</span>
            <span class="draw-info">💡 Click to add atom • Replace mode: click atom to change • Right-click to delete</span>
        </div>
        <canvas id="canvas" width="700" height="450"></canvas>
        <input id="smiles-output" placeholder="SMILES will appear here...">
    </div>
    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        let isDrawing = false, lastX, lastY;
        let atoms = [], bonds = [], history = [];
        let tool = 'draw';
        let selectedAtom = 'C';
        let deleteBondMode = false;
        let replaceMode = false;
        const MAX_HISTORY = 30;
        let atomIdCounter = 0;

        document.getElementById('atom-select').onchange = function() {
            selectedAtom = this.value;
        };

        function getAtomColor(label) {
            const colors = {
                'C': '#333333', 'O': '#FF0000', 'N': '#3050F8', 'H': '#FFFFFF',
                'S': '#FFFF30', 'P': '#FF8000', 'F': '#90E050', 'Cl': '#1FF01F',
                'Br': '#A62929', 'I': '#940094', 'OH': '#FF0000', 'OMe': '#CD5C5C',
                'OBn': '#8B4513', 'OBz': '#8B6914', 'OAc': '#CD853F', 'N3': '#4169E1',
                'NH2': '#4169E1', 'OTs': '#DAA520', 'TBDMS': '#2E8B57', 'TIPS': '#2E8B57',
                'Bz': '#8B6914', 'Bn': '#8B4513', 'Ac': '#CD853F'
            };
            return colors[label] || '#333333';
        }

        function drawAtom(x, y, label, highlight) {
            const radius = highlight ? 22 : 18;
            const color = getAtomColor(label);
            if (highlight) { ctx.shadowColor = '#f59e0b'; ctx.shadowBlur = 15; }
            ctx.beginPath();
            ctx.arc(x, y, radius, 0, Math.PI*2);
            ctx.fillStyle = color;
            ctx.fill();
            ctx.shadowBlur = 0;
            ctx.strokeStyle = highlight ? '#f59e0b' : '#333';
            ctx.lineWidth = highlight ? 3 : 2;
            ctx.stroke();
            if (label) {
                ctx.fillStyle = 'white';
                ctx.font = 'bold 11px Inter, Arial, sans-serif';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(label.length > 4 ? label.substring(0,4) : label, x, y);
            }
        }

        function drawBond(x1, y1, x2, y2, highlight) {
            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.strokeStyle = highlight ? '#ef4444' : '#333';
            ctx.lineWidth = highlight ? 6 : 3;
            ctx.stroke();
            if (highlight) {
                const mx = (x1+x2)/2, my = (y1+y2)/2;
                ctx.strokeStyle = '#ef4444';
                ctx.lineWidth = 2;
                const s = 8;
                ctx.beginPath();
                ctx.moveTo(mx-s, my-s); ctx.lineTo(mx+s, my+s);
                ctx.moveTo(mx+s, my-s); ctx.lineTo(mx-s, my+s);
                ctx.stroke();
            }
        }

        function drawBenzene(x, y) {
            const size = 45;
            const pts = [0,60,120,180,240,300].map(d => ({
                x: x + size * Math.cos(d * Math.PI / 180),
                y: y + size * Math.sin(d * Math.PI / 180)
            }));
            for (let i=0; i<6; i++) {
                let j=(i+1)%6;
                drawBond(pts[i].x, pts[i].y, pts[j].x, pts[j].y);
            }
            for (let i=0; i<6; i++) {
                const label = i%2===0 ? 'CH₂' : 'CH';
                const color = getAtomColor('C');
                ctx.beginPath();
                ctx.arc(pts[i].x, pts[i].y, 18, 0, Math.PI*2);
                ctx.fillStyle = color;
                ctx.fill();
                ctx.strokeStyle = '#333';
                ctx.lineWidth = 2;
                ctx.stroke();
                ctx.fillStyle = 'white';
                ctx.font = 'bold 11px Inter, Arial, sans-serif';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(label, pts[i].x, pts[i].y);
                atoms.push({x: pts[i].x, y: pts[i].y, label: label, id: atomIdCounter++});
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
            bonds.forEach(b => drawBond(b.x1,b.y1,b.x2,b.y2,false));
            atoms.forEach(a => drawAtom(a.x,a.y,a.label,false));
        }

        function saveState() {
            history.push(JSON.parse(JSON.stringify({atoms,bonds})));
            if (history.length > MAX_HISTORY) history.shift();
        }

        function getPos(e) {
            const r = canvas.getBoundingClientRect();
            return {
                x: (e.clientX - r.x) * (canvas.width / r.width),
                y: (e.clientY - r.y) * (canvas.height / r.height)
            };
        }

        function updateModeStatus() {
            const status = document.getElementById('mode-status');
            if (replaceMode) {
                status.className = 'mode-status mode-replace';
                status.textContent = '🔄 Replace Mode (click atom)';
                canvas.style.cursor = 'pointer';
            } else if (deleteBondMode) {
                status.className = 'mode-status mode-delete';
                status.textContent = '✖️ Delete Mode (click bond)';
                canvas.style.cursor = 'crosshair';
            } else {
                status.className = 'mode-status mode-draw';
                status.textContent = '✏️ Draw Mode (click canvas)';
                canvas.style.cursor = 'crosshair';
            }
        }

        canvas.onmousedown = function(e) {
            const pos = getPos(e);
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
                if (bond) {
                    saveState();
                    bonds = bonds.filter(b => b !== bond);
                    drawAll();
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
            if (isDrawing && tool === 'line') {
                drawAll();
                drawBond(lastX, lastY, pos.x, pos.y, false);
            }
            if (replaceMode) {
                canvas.style.cursor = findNearestAtom(pos.x, pos.y) ? 'pointer' : 'default';
            }
        };

        canvas.onmouseup = function(e) {
            if (isDrawing && tool === 'line') {
                const pos = getPos(e);
                saveState();
                let endAtom = findNearestAtom(pos.x, pos.y);
                let startAtom = findNearestAtom(lastX, lastY);
                if (startAtom && endAtom && startAtom !== endAtom) {
                    bonds.push({x1: startAtom.x, y1: startAtom.y, x2: endAtom.x, y2: endAtom.y});
                } else if (startAtom) {
                    const na = {x: pos.x, y: pos.y, label: selectedAtom, id: atomIdCounter++};
                    atoms.push(na);
                    bonds.push({x1: startAtom.x, y1: startAtom.y, x2: na.x, y2: na.y});
                } else {
                    const a1 = {x: lastX, y: lastY, label: selectedAtom, id: atomIdCounter++};
                    const a2 = {x: pos.x, y: pos.y, label: selectedAtom, id: atomIdCounter++};
                    atoms.push(a1); atoms.push(a2);
                    bonds.push({x1: a1.x, y1: a1.y, x2: a2.x, y2: a2.y});
                }
                drawAll();
                isDrawing = false;
            }
        };

        canvas.oncontextmenu = e => e.preventDefault();

        document.getElementById('btn-draw').onclick = function() {
            tool = 'draw'; replaceMode = false; deleteBondMode = false;
            document.querySelectorAll('.draw-toolbar button').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            updateModeStatus();
        };
        document.getElementById('btn-replace').onclick = function() {
            replaceMode = !replaceMode;
            if (replaceMode) {
                deleteBondMode = false;
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
            tool = 'line'; replaceMode = false; deleteBondMode = false;
            document.querySelectorAll('.draw-toolbar button').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            updateModeStatus();
        };
        document.getElementById('btn-benzene').onclick = function() {
            tool = 'benzene'; replaceMode = false; deleteBondMode = false;
            document.querySelectorAll('.draw-toolbar button').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            updateModeStatus();
        };
        document.getElementById('btn-delete-bond').onclick = function() {
            deleteBondMode = !deleteBondMode;
            if (deleteBondMode) {
                replaceMode = false;
                document.querySelectorAll('.draw-toolbar button').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
            } else {
                this.classList.remove('active');
                tool = 'draw';
                document.getElementById('btn-draw').classList.add('active');
            }
            updateModeStatus();
        };
        document.getElementById('btn-undo').onclick = function() {
            if (history.length > 0) {
                const state = history.pop();
                atoms = state.atoms; bonds = state.bonds;
                drawAll();
            }
        };
        document.getElementById('btn-clear').onclick = function() {
            if (atoms.length > 0 || bonds.length > 0) {
                saveState();
                atoms = []; bonds = [];
                drawAll();
            }
        };
        document.getElementById('btn-smiles').onclick = function() {
            const sm = atoms.length > 0 ? atoms.map(a => a.label||'C').join('-') : 'No atoms drawn';
            document.getElementById('smiles-output').value = sm;
            navigator.clipboard.writeText(sm);
        };

        drawBenzene(350, 225);
        drawAll();
        saveState();
        updateModeStatus();
    </script>
    """, height=580)

# ─── HEADER ─────────────────────────────────────────────
def render_header():
    valid_years = papers['Year'].dropna() if len(papers) > 0 else []
    topics = papers['Topic'].dropna().unique() if len(papers) > 0 else []
    
    st.markdown(f"""
    <div class="header-wrapper">
        <div class="header-content">
            <div class="header-left">
                <div class="logo-box">
                    <div class="logo-icon">🧬</div>
                    <div class="logo-text">CCWang-<span>FizSab</span></div>
                </div>
                <div>
                    <div class="header-title">Glyco<span>Search</span></div>
                    <div class="header-subtitle">Glycosylation Research · 1,000+ Papers</div>
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
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Search",
        "📊 Analytics",
        "📚 Methods", 
        "🧪 Draw"
    ])

    # ─── TAB 1: SEARCH ────────────────────────────────
    with tab1:
        st.markdown("""
        <div class="search-wrapper">
            <p style="font-family:'Inter',sans-serif;font-weight:500;font-size:0.95rem;color:#0f172a;margin-bottom:0.5rem;">
                🔎 Find papers by keyword
            </p>
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
            <p style="font-family:'Inter',sans-serif;font-weight:500;font-size:1rem;color:#0f172a;">
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
        st.markdown("### 🧪 Chemical Structure Editor")
        st.markdown("""
        <p style="font-family:'Inter',sans-serif;font-size:0.9rem;color:#64748b;margin-bottom:1rem;">
            Select an atom type, then click to add or replace atoms. Click "Replace Atom" to change existing atoms.
        </p>
        """, unsafe_allow_html=True)
        
        chemical_drawing_tool()

# ─── FOOTER ─────────────────────────────────────────────
st.markdown("""
<div class="footer">
    🧬 GlycoSearch · Built with Streamlit · 
    <a href="https://github.com/FizzaSab/GlycoAgent" target="_blank">GitHub</a> · 
    CCWang-FizSab · 2026
</div>
""", unsafe_allow_html=True)
