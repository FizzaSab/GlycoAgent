import streamlit as st
import pandas as pd
import os
import streamlit.components.v1 as components

st.set_page_config(page_title="Glycosylation Research Agent", page_icon="🧪", layout="wide")
st.title("🧪 Glycosylation Research Agent")

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

def chemical_drawing_tool():
    """Embed a chemical structure drawing tool"""
    components.html("""
    <style>
        #canvas { border: 1px solid #667eea; background: white; cursor: crosshair; border-radius: 8px; }
        .toolbar { display: flex; gap: 8px; padding: 10px 0; flex-wrap: wrap; }
        .toolbar button { padding: 8px 16px; border: none; border-radius: 6px; background: #667eea; color: white; cursor: pointer; font-size: 14px; }
        .toolbar button:hover { background: #5a67d8; }
        .toolbar button.danger { background: #e74c3c; }
        .toolbar button.danger:hover { background: #c0392b; }
        .toolbar button.success { background: #27ae60; }
        .toolbar button.success:hover { background: #219a52; }
        .toolbar button.active { background: #764ba2; }
        #smiles-output { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 6px; margin-top: 10px; font-family: monospace; }
        .info-text { color: #666; font-size: 12px; text-align: center; }
    </style>
    <div>
        <div class="toolbar">
            <button id="btn-draw" class="active">✏️ Draw</button>
            <button id="btn-line">📏 Bond</button>
            <button id="btn-benzene">⬡ Benzene</button>
            <button id="btn-undo">↩️ Undo</button>
            <button id="btn-clear" class="danger">🗑️ Clear</button>
            <button id="btn-smiles" class="success">📋 Get SMILES</button>
        </div>
        <canvas id="canvas" width="600" height="400"></canvas>
        <input id="smiles-output" placeholder="SMILES will appear here...">
        <p class="info-text">💡 Click to draw atoms • Drag to make bonds • Right-click to delete</p>
    </div>
    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        let isDrawing = false, lastX, lastY;
        let atoms = [], bonds = [], history = [];
        let tool = 'draw';
        const MAX_HISTORY = 20;

        function drawAtom(x, y, color, label) {
            const radius = 15;
            ctx.beginPath();
            ctx.arc(x, y, radius, 0, Math.PI*2);
            ctx.fillStyle = color || '#000000';
            ctx.fill();
            ctx.strokeStyle = '#333';
            ctx.lineWidth = 2;
            ctx.stroke();
            if (label) {
                ctx.fillStyle = 'white';
                ctx.font = 'bold 12px Arial';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(label, x, y);
            }
        }

        function drawBond(x1, y1, x2, y2) {
            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.strokeStyle = '#333';
            ctx.lineWidth = 4;
            ctx.stroke();
        }

        function drawBenzene(x, y) {
            const size = 40;
            const pts = [0,60,120,180,240,300].map(d => ({
                x: x + size * Math.cos(d * Math.PI / 180),
                y: y + size * Math.sin(d * Math.PI / 180)
            }));
            for (let i = 0; i < 6; i++) {
                let j = (i + 1) % 6;
                drawBond(pts[i].x, pts[i].y, pts[j].x, pts[j].y);
            }
            for (let i = 0; i < 6; i++) {
                ctx.fillStyle = '#333';
                ctx.font = '12px Arial';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(i % 2 === 0 ? 'CH₂' : 'CH', pts[i].x, pts[i].y);
            }
        }

        function drawAll() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            // Grid
            ctx.strokeStyle = '#f0f0f0';
            ctx.lineWidth = 1;
            for (let x = 0; x <= canvas.width; x += 30) {
                ctx.beginPath();
                ctx.moveTo(x, 0);
                ctx.lineTo(x, canvas.height);
                ctx.stroke();
            }
            for (let y = 0; y <= canvas.height; y += 30) {
                ctx.beginPath();
                ctx.moveTo(0, y);
                ctx.lineTo(canvas.width, y);
                ctx.stroke();
            }
            bonds.forEach(b => drawBond(b.x1, b.y1, b.x2, b.y2));
            atoms.forEach(a => drawAtom(a.x, a.y, a.color, a.label));
        }

        function saveState() {
            history.push(JSON.parse(JSON.stringify({atoms, bonds})));
            if (history.length > MAX_HISTORY) history.shift();
        }

        function getPos(e) {
            const r = canvas.getBoundingClientRect();
            return {
                x: (e.clientX - r.x) * (canvas.width / r.width),
                y: (e.clientY - r.y) * (canvas.height / r.height)
            };
        }

        canvas.onmousedown = function(e) {
            const pos = getPos(e);
            // Right click = delete
            if (e.button === 2) {
                for (let i = atoms.length - 1; i >= 0; i--) {
                    if (Math.hypot(pos.x - atoms[i].x, pos.y - atoms[i].y) < 20) {
                        saveState();
                        atoms.splice(i, 1);
                        bonds = bonds.filter(b => {
                            const a = atoms[i];
                            return !(b.x1 === a?.x && b.y1 === a?.y || b.x2 === a?.x && b.y2 === a?.y);
                        });
                        drawAll();
                        return;
                    }
                }
                return;
            }
            if (tool === 'draw') {
                const label = prompt('Atom label (C, O, N, H):', 'C');
                if (label) {
                    saveState();
                    atoms.push({x: pos.x, y: pos.y, color: '#000000', label: label});
                    drawAll();
                }
            } else if (tool === 'line') {
                isDrawing = true;
                lastX = pos.x;
                lastY = pos.y;
            } else if (tool === 'benzene') {
                saveState();
                drawBenzene(pos.x, pos.y);
            }
        };

        canvas.onmousemove = function(e) {
            if (isDrawing && tool === 'line') {
                const pos = getPos(e);
                drawAll();
                drawBond(lastX, lastY, pos.x, pos.y);
            }
        };

        canvas.onmouseup = function(e) {
            if (isDrawing && tool === 'line') {
                const pos = getPos(e);
                saveState();
                let endAtom = null;
                for (const a of atoms) {
                    if (Math.hypot(pos.x - a.x, pos.y - a.y) < 20) {
                        endAtom = a;
                        break;
                    }
                }
                if (endAtom) {
                    bonds.push({x1: lastX, y1: lastY, x2: endAtom.x, y2: endAtom.y});
                } else {
                    const label = prompt('Atom label (C, O, N, H):', 'C');
                    if (label) {
                        const na = {x: pos.x, y: pos.y, color: '#000000', label: label};
                        atoms.push(na);
                        bonds.push({x1: lastX, y1: lastY, x2: na.x, y2: na.y});
                    }
                }
                drawAll();
                isDrawing = false;
            }
        };

        canvas.oncontextmenu = e => e.preventDefault();

        // Toolbar buttons
        document.getElementById('btn-draw').onclick = function() {
            tool = 'draw';
            document.querySelectorAll('.toolbar button').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
        };
        document.getElementById('btn-line').onclick = function() {
            tool = 'line';
            document.querySelectorAll('.toolbar button').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
        };
        document.getElementById('btn-benzene').onclick = function() {
            tool = 'benzene';
            document.querySelectorAll('.toolbar button').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
        };

        document.getElementById('btn-undo').onclick = function() {
            if (history.length > 0) {
                const state = history.pop();
                atoms = state.atoms;
                bonds = state.bonds;
                drawAll();
            }
        };

        document.getElementById('btn-clear').onclick = function() {
            saveState();
            atoms = [];
            bonds = [];
            drawAll();
        };

        document.getElementById('btn-smiles').onclick = function() {
            const sm = atoms.map(a => a.label || 'C').join('');
            document.getElementById('smiles-output').value = sm || 'C1=CC=CC=C1';
            navigator.clipboard.writeText(sm || 'C1=CC=CC=C1').then(() => {
                const el = document.getElementById('smiles-output');
                el.style.borderColor = '#27ae60';
                setTimeout(() => el.style.borderColor = '#ddd', 2000);
            });
        };

        // Start with a benzene ring
        drawBenzene(300, 200);
    </script>
    """, height=520)

if len(papers) == 0:
    st.warning("Upload your Excel file")
    uploaded = st.file_uploader("Choose Excel file", type=['xlsx'])
    if uploaded:
        papers = pd.read_excel(uploaded, sheet_name='All Papers')
        st.rerun()
else:
    st.success(f"Loaded {len(papers)} papers")
    
    tab1, tab2, tab3 = st.tabs(["🔍 Search", "📊 Stats", "🧪 Draw"])
    
    with tab1:
        keyword = st.text_input("Search papers", placeholder="e.g. NIS, sialic acid")
        if keyword:
            mask = papers['Title'].str.contains(keyword, case=False, na=False)
            results = papers[mask]
            st.write(f"Found {len(results)} papers")
            for _, row in results.head(20).iterrows():
                with st.expander(f"[{row.get('Year', '?')}] {row.get('Title', '')[:80]}..."):
                    st.write(f"**Journal:** {row.get('Journal', '?')}")
                    st.write(f"**Topic:** {row.get('Topic', '?')}")
                    st.write(f"**Abstract:** {str(row.get('Abstract', ''))[:500]}...")
    
    with tab2:
        st.write("**📊 Papers per Year**")
        year_counts = papers['Year'].value_counts().sort_index()
        if len(year_counts) > 0:
            st.bar_chart(year_counts)
        st.write("**📚 Papers by Topic**")
        st.bar_chart(papers['Topic'].value_counts().head(10))
    
    with tab3:
        st.markdown("### 🧪 Draw Chemical Structure")
        st.markdown("Click to add atoms, drag to make bonds, right-click to delete")
        chemical_drawing_tool()
