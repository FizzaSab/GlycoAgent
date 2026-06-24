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
    components.html("""
    <style>
        #canvas { border: 1px solid #667eea; background: white; cursor: crosshair; border-radius: 8px; }
        .toolbar { display: flex; gap: 6px; padding: 10px 0; flex-wrap: wrap; align-items: center; }
        .toolbar button { padding: 6px 14px; border: none; border-radius: 6px; background: #667eea; color: white; cursor: pointer; font-size: 13px; }
        .toolbar button:hover { background: #5a67d8; }
        .toolbar button.danger { background: #e74c3c; }
        .toolbar button.danger:hover { background: #c0392b; }
        .toolbar button.success { background: #27ae60; }
        .toolbar button.success:hover { background: #219a52; }
        .toolbar button.active { background: #764ba2; }
        .toolbar button.warning { background: #f39c12; }
        .toolbar button.warning:hover { background: #e67e22; }
        .toolbar select { padding: 6px 12px; border-radius: 6px; border: 1px solid #ddd; font-size: 13px; }
        #smiles-output { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 6px; margin-top: 10px; font-family: monospace; }
        .info-text { color: #666; font-size: 12px; text-align: center; }
        .toolbar-group { display: flex; gap: 4px; align-items: center; background: #f8f9fa; padding: 4px 8px; border-radius: 6px; }
        .toolbar-label { font-size: 11px; color: #888; font-weight: bold; margin-right: 4px; }
    </style>
    <div>
        <div class="toolbar">
            <div class="toolbar-group">
                <span class="toolbar-label">✏️ Draw:</span>
                <button id="btn-draw" class="active">Atom</button>
                <button id="btn-line">Bond</button>
                <button id="btn-benzene">Benzene</button>
                <button id="btn-delete-bond" class="warning">🗑️ Delete Bond</button>
            </div>
            <div class="toolbar-group">
                <span class="toolbar-label">🔬 Atom:</span>
                <select id="atom-select">
                    <option value="C">C</option>
                    <option value="O">O</option>
                    <option value="N">N</option>
                    <option value="H">H</option>
                    <option value="S">S</option>
                    <option value="P">P</option>
                    <option value="F">F</option>
                    <option value="Cl">Cl</option>
                    <option value="Br">Br</option>
                    <option value="I">I</option>
                    <option value="OBn">OBn</option>
                    <option value="OBz">OBz</option>
                    <option value="OAc">OAc</option>
                    <option value="N3">N3</option>
                    <option value="NH2">NH2</option>
                    <option value="OH">OH</option>
                    <option value="OMe">OMe</option>
                    <option value="OTs">OTs</option>
                    <option value="TBDMS">TBDMS</option>
                    <option value="TIPS">TIPS</option>
                    <option value="Bz">Bz</option>
                    <option value="Bn">Bn</option>
                    <option value="Ac">Ac</option>
                </select>
            </div>
            <div class="toolbar-group">
                <button id="btn-undo">↩️ Undo</button>
                <button id="btn-clear" class="danger">🗑️ Clear</button>
                <button id="btn-smiles" class="success">📋 Get SMILES</button>
            </div>
        </div>
        <canvas id="canvas" width="700" height="450"></canvas>
        <input id="smiles-output" placeholder="SMILES will appear here...">
        <p class="info-text">💡 Click to add selected atom • Drag to make bonds • Click "Delete Bond" then click a bond to remove it</p>
    </div>
    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        let isDrawing = false, lastX, lastY;
        let atoms = [], bonds = [], history = [];
        let tool = 'draw';
        let selectedAtom = 'C';
        let deleteBondMode = false;
        const MAX_HISTORY = 30;

        // Get atom label from dropdown
        document.getElementById('atom-select').onchange = function() {
            selectedAtom = this.value;
        };

        function drawAtom(x, y, color, label) {
            const radius = 18;
            ctx.beginPath();
            ctx.arc(x, y, radius, 0, Math.PI*2);
            ctx.fillStyle = color || '#000000';
            ctx.fill();
            ctx.strokeStyle = '#333';
            ctx.lineWidth = 2;
            ctx.stroke();
            if (label) {
                ctx.fillStyle = 'white';
                ctx.font = 'bold 11px Arial';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                // Handle longer labels
                const displayLabel = label.length > 3 ? label.substring(0,3) : label;
                ctx.fillText(displayLabel, x, y);
                // Show full label on hover via title
                ctx.canvas.title = label;
            }
        }

        function drawBond(x1, y1, x2, y2, highlight) {
            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.strokeStyle = highlight ? '#e74c3c' : '#333';
            ctx.lineWidth = highlight ? 6 : 4;
            ctx.stroke();
            if (highlight) {
                // Draw X on bond to indicate delete
                const mx = (x1 + x2) / 2;
                const my = (y1 + y2) / 2;
                ctx.strokeStyle = '#e74c3c';
                ctx.lineWidth = 2;
                const s = 8;
                ctx.beginPath();
                ctx.moveTo(mx - s, my - s);
                ctx.lineTo(mx + s, my + s);
                ctx.moveTo(mx + s, my - s);
                ctx.lineTo(mx - s, my + s);
                ctx.stroke();
            }
        }

        function drawBenzene(x, y) {
            const size = 45;
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

        function findNearestAtom(x, y, threshold) {
            threshold = threshold || 25;
            let nearest = null;
            let minDist = threshold;
            for (const a of atoms) {
                const dist = Math.hypot(x - a.x, y - a.y);
                if (dist < minDist) {
                    minDist = dist;
                    nearest = a;
                }
            }
            return nearest;
        }

        function findNearestBond(x, y, threshold) {
            threshold = threshold || 15;
            let nearest = null;
            let minDist = threshold;
            for (const b of bonds) {
                // Check distance from point to line segment
                const dx = b.x2 - b.x1;
                const dy = b.y2 - b.y1;
                const len = Math.hypot(dx, dy);
                if (len === 0) continue;
                const t = Math.max(0, Math.min(1, ((x - b.x1) * dx + (y - b.y1) * dy) / (len * len)));
                const px = b.x1 + t * dx;
                const py = b.y1 + t * dy;
                const dist = Math.hypot(x - px, y - py);
                if (dist < minDist) {
                    minDist = dist;
                    nearest = b;
                }
            }
            return nearest;
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
            bonds.forEach(b => drawBond(b.x1, b.y1, b.x2, b.y2, false));
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

        // Mouse events
        canvas.onmousedown = function(e) {
            const pos = getPos(e);
            
            // Delete bond mode
            if (deleteBondMode) {
                const bond = findNearestBond(pos.x, pos.y);
                if (bond) {
                    saveState();
                    bonds = bonds.filter(b => b !== bond);
                    drawAll();
                    deleteBondMode = false;
                    document.getElementById('btn-delete-bond').style.background = '#f39c12';
                }
                return;
            }

            // Right click = delete atom
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
                const label = selectedAtom;
                saveState();
                atoms.push({x: pos.x, y: pos.y, color: '#000000', label: label});
                drawAll();
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
            const pos = getPos(e);
            if (isDrawing && tool === 'line') {
                drawAll();
                drawBond(lastX, lastY, pos.x, pos.y, false);
            }
            // Update cursor for delete bond mode
            if (deleteBondMode) {
                const bond = findNearestBond(pos.x, pos.y);
                canvas.style.cursor = bond ? 'pointer' : 'crosshair';
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
                    const label = selectedAtom;
                    const na = {x: pos.x, y: pos.y, color: '#000000', label: label};
                    atoms.push(na);
                    bonds.push({x1: startAtom.x, y1: startAtom.y, x2: na.x, y2: na.y});
                } else {
                    // Just draw a line with atoms at both ends
                    const label1 = selectedAtom;
                    const label2 = selectedAtom;
                    const a1 = {x: lastX, y: lastY, color: '#000000', label: label1};
                    const a2 = {x: pos.x, y: pos.y, color: '#000000', label: label2};
                    atoms.push(a1);
                    atoms.push(a2);
                    bonds.push({x1: a1.x, y1: a1.y, x2: a2.x, y2: a2.y});
                }
                drawAll();
                isDrawing = false;
            }
        };

        canvas.oncontextmenu = e => e.preventDefault();

        // Toolbar buttons
        document.getElementById('btn-draw').onclick = function() {
            tool = 'draw';
            deleteBondMode = false;
            document.getElementById('btn-delete-bond').style.background = '#f39c12';
            document.querySelectorAll('.toolbar button').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
        };
        document.getElementById('btn-line').onclick = function() {
            tool = 'line';
            deleteBondMode = false;
            document.getElementById('btn-delete-bond').style.background = '#f39c12';
            document.querySelectorAll('.toolbar button').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
        };
        document.getElementById('btn-benzene').onclick = function() {
            tool = 'benzene';
            deleteBondMode = false;
            document.getElementById('btn-delete-bond').style.background = '#f39c12';
            document.querySelectorAll('.toolbar button').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
        };
        document.getElementById('btn-delete-bond').onclick = function() {
            deleteBondMode = !deleteBondMode;
            this.style.background = deleteBondMode ? '#e74c3c' : '#f39c12';
            this.textContent = deleteBondMode ? '🔴 Click Bond to Delete' : '🗑️ Delete Bond';
            canvas.style.cursor = deleteBondMode ? 'crosshair' : 'default';
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
            if (atoms.length > 0 || bonds.length > 0) {
                saveState();
                atoms = [];
                bonds = [];
                drawAll();
            }
        };

        document.getElementById('btn-smiles').onclick = function() {
            // Generate a simple SMILES-like string
            let sm = '';
            if (atoms.length === 0) {
                sm = 'No atoms drawn';
            } else {
                // Create a connected graph representation
                const labels = atoms.map(a => a.label || 'C');
                // Simple: just list atoms and bonds
                sm = labels.join('') + ' ';
                if (bonds.length > 0) {
                    sm += 'bonds:' + bonds.length;
                }
            }
            document.getElementById('smiles-output').value = sm;
            navigator.clipboard.writeText(sm).then(() => {
                const el = document.getElementById('smiles-output');
                el.style.borderColor = '#27ae60';
                setTimeout(() => el.style.borderColor = '#ddd', 2000);
            });
        };

        // Start with a benzene ring
        drawBenzene(350, 225);
        // Add some atoms as example
        saveState();
    </script>
    """, height=580)

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
        st.markdown("Select atom from dropdown, click to add, drag to bond, click 'Delete Bond' then click a bond")
        chemical_drawing_tool()
