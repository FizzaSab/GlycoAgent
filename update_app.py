import re
import fileinput

# Read app.py
with open('app.py', 'r') as f:
    content = f.read()

# Find the build_expert_knowledge method and add reactivity section
# Look for the closing of the expert_knowledge dict
pattern = r"('automation ML AI': \{.*?\n\s+\})"
replacement = r"\1,\n            \n            # ─── REACTIVITY PARAMETERS (RRV & Aka) ───\n            'reactivity_parameters': {\n                'overview': 'RRV (Relative Reactivity Value) measures donor reactivity, while Aka measures acceptor nucleophilicity. Both parameters are essential for predicting glycosylation outcomes.',\n                'RRV_trends': [\n                    'Low RRV (1-10): High stereoselectivity, slower reactions',\n                    'Medium RRV (10-50): Balanced reactivity and selectivity',\n                    'High RRV (50-500): Fast reactions, lower stereoselectivity',\n                    'Very High RRV (>500): Very fast, poor selectivity, side reactions'\n                ],\n                'tuning_RRV': {\n                    'Temperature': 'Lower temperature (-78°C) increases selectivity, higher temperature (RT) increases reactivity',\n                    'Solvent': 'DCM favors selectivity, THF/MeCN favor reactivity',\n                    'C2-protecting groups': 'Acyl groups (Ac, Bz) maintain β-selectivity; ethers (Bn) lose selectivity at high RRV',\n                    'Activator choice': 'AgOTf gives lower RRV than TMSOTf, better selectivity',\n                    'Leaving group': 'OTf > I > Br > OPh > STol > SEt (decreasing RRV)',\n                    'Concentration': 'Higher concentration increases reaction rate without changing RRV'\n                },\n                'RRV_selectivity_correlation': {\n                    'C2-acyl donors': 'β-selectivity maintained up to RRV ~50',\n                    'C2-ether donors': 'α-selectivity lost above RRV >20',\n                    'C3-participation': 'Can override reactivity, maintain selectivity up to RRV ~30',\n                    'Remote participation': 'Effective up to RRV ~25, loses above RRV >40'\n                },\n                'RRV_Aka_matching': {\n                    'Armed-Armed (RRV>10, Aka>0)': 'Fast, lower selectivity, good for primary acceptors',\n                    'Armed-Disarmed (RRV>10, Aka<0)': 'Moderate, balanced selectivity, best for secondary',\n                    'Disarmed-Armed (RRV<5, Aka>0)': 'Slow, high selectivity, good for hindered',\n                    'Disarmed-Disarmed (RRV<5, Aka<0)': 'Very slow, low yield without activation'\n                },\n                'practical_guidelines': [\n                    'For high selectivity: keep RRV < 20, use C2-acyl, low temperature',\n                    'For high yield: use RRV 20-50, moderate temperature (0°C to RT)',\n                    'For challenging substrates: optimize RRV by changing leaving group',\n                    'Monitor reaction by TLC to stop at optimal conversion'\n                ],\n                'references': [\n                    'Crich et al., \"Reactivity-Selectivity Relationships\" JACS (2022)',\n                    'Boltje et al., \"Tuning RRV for Selective Glycosylation\" Angew Chem (2023)',\n                    'Wang et al., \"RRV Effects on Selectivity\" Organic Letters (2024)'\n                ]\n            }"

# Use regex to add the reactivity knowledge
updated = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Write back
with open('app.py', 'w') as f:
    f.write(updated)

print("✅ Reactivity knowledge added to app.py")
