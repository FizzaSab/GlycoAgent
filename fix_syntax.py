import re

# Read app.py
with open('app.py', 'r') as f:
    content = f.read()

# Fix missing commas in dictionaries
# Look for pattern where a dict ends without a comma
# Find 'references': [...] and make sure there's a comma after it

# Fix the reactivity_parameters section
# Replace the problematic section
old_section = r"""'reactivity_parameters': {
                'overview': 'RRV \(Relative Reactivity Value\) measures donor reactivity, while Aka measures acceptor nucleophilicity\..*?'
                'references': \[
                    'Crich et al\., "Reactivity-Selectivity Relationships in Glycosylation" JACS \(2022\)',
                    'Boltje et al\., "Tuning RRV for Stereoselective Glycosylation" Angew Chem \(2023\)',
                    'Wang et al\., "RRV Effects on Glycosylation Selectivity" Organic Letters \(2024\)',
                    'Zhang et al\., "Relative Reactivity Values in Glycosylation" Chemical Reviews \(2023\)'
                \]
            }"""

new_section = """'reactivity_parameters': {
                'overview': 'RRV (Relative Reactivity Value) measures donor reactivity, while Aka measures acceptor nucleophilicity. Both parameters are essential for predicting glycosylation outcomes and tuning stereoselectivity.',
                'RRV_trends': [
                    'Low RRV (1-10): High stereoselectivity, slower reactions, better control',
                    'Medium RRV (10-50): Moderate stereoselectivity, good yields, balanced approach',
                    'High RRV (50-500): Lower stereoselectivity, faster reactions, may lose selectivity',
                    'Very High RRV (>500): Very low selectivity, potential side reactions'
                ],
                'tuning_RRV': {
                    'Temperature': 'Lower temperature (-78°C) increases selectivity, higher temperature (RT) increases reactivity. Each 10°C change affects rate by ~2x.',
                    'Solvent': 'DCM and toluene favor selectivity; THF and MeCN favor reactivity. Solvent polarity affects oxocarbenium ion stabilization.',
                    'C2-protecting groups': 'Acyl groups (Ac, Bz) maintain β-selectivity even at high RRV; ethers (Bn) lose α-selectivity above RRV >20',
                    'Activator choice': 'AgOTf gives lower effective RRV (~5-20) vs TMSOTf (~20-100), better for selectivity',
                    'Leaving group': 'OTf > I > Br > OPh > STol > SEt (decreasing RRV by ~10x per step)',
                    'Concentration': 'Higher concentration increases reaction rate without changing RRV, useful for slow reactions'
                },
                'RRV_selectivity_correlation': {
                    'C2-acyl donors': 'β-selectivity maintained up to RRV ~50, gradually lost above RRV >100',
                    'C2-ether donors': 'α-selectivity lost above RRV >20, becomes mixed at RRV >50',
                    'C3-participation': 'Can override reactivity effects, maintain selectivity up to RRV ~30',
                    'C4-participation': 'Less effective, lose selectivity above RRV >15',
                    'C6-participation': 'Only effective at very low RRV (<10), minimal effect at higher RRV'
                },
                'RRV_Aka_matching': {
                    'Armed-Armed (RRV>10, Aka>0)': 'Fast reaction, lower selectivity, good for primary acceptors',
                    'Armed-Disarmed (RRV>10, Aka<0)': 'Moderate reaction, balanced selectivity, best for secondary acceptors',
                    'Disarmed-Armed (RRV<5, Aka>0)': 'Slow reaction, high selectivity, good for hindered/tertiary acceptors',
                    'Disarmed-Disarmed (RRV<5, Aka<0)': 'Very slow, low yield without activation, may need higher temperature'
                },
                'practical_guidelines': [
                    'For high selectivity: keep RRV < 20, use C2-acyl donors, -40°C to -78°C temperature',
                    'For high yield: use RRV 20-50, moderate temperature (0°C to RT), monitor by TLC',
                    'For challenging substrates: optimize RRV by changing leaving group or protecting groups',
                    'Match donor RRV with acceptor Aka: high RRV for low Aka, low RRV for high Aka',
                    'Use additives (LiClO4, Bu4NBr) to modulate effective reactivity without changing RRV'
                ],
                'references': [
                    'Crich et al., "Reactivity-Selectivity Relationships in Glycosylation" JACS (2022)',
                    'Boltje et al., "Tuning RRV for Stereoselective Glycosylation" Angew Chem (2023)',
                    'Wang et al., "RRV Effects on Glycosylation Selectivity" Organic Letters (2024)',
                    'Zhang et al., "Relative Reactivity Values in Glycosylation" Chemical Reviews (2023)'
                ]
            }"""

# Use regex to replace
content = re.sub(r"'reactivity_parameters': \{.*?\n\s+\}", new_section, content, flags=re.DOTALL)

# Write back
with open('app.py', 'w') as f:
    f.write(content)

print("✅ Syntax error fixed - reactivity_parameters updated")
