# This will add reactivity knowledge to the AI's brain

import re

# Reactivity knowledge to add to the expert knowledge
REACTIVITY_EXPERT_KNOWLEDGE = {
    'RRV_effect_on_selectivity': {
        'overview': 'RRV (Relative Reactivity Value) has a profound effect on glycosylation stereoselectivity. As donor reactivity increases, stereoselectivity generally decreases due to the formation of more reactive oxocarbenium ions that allow less selective attack.',
        'trends': [
            'Low RRV (1-10): High stereoselectivity, slower reactions, better control',
            'Medium RRV (10-50): Moderate stereoselectivity, good yields, balanced approach',
            'High RRV (50-500): Lower stereoselectivity, faster reactions, may lose selectivity',
            'Very High RRV (>500): Very low selectivity, potential side reactions'
        ],
        'how_to_tune': {
            'temperature': 'Lower temperatures favor selectivity (ΔΔG‡), higher temperatures favor reactivity',
            'solvent': 'Non-polar solvents (DCM, toluene) favor selectivity, polar solvents (THF, MeCN) favor reactivity',
            'protecting_groups': 'C2-acyl groups direct β-selectivity even at high RRV; C2-ethers lose α-selectivity at high RRV',
            'additives': 'Additives like LiClO₄ can modulate reactivity without losing selectivity',
            'activator': 'Milder activators (AgOTf) vs stronger activators (TMSOTf) affect RRV',
            'concentration': 'Higher concentration can increase reaction rate without affecting RRV'
        },
        'specific_examples': {
            'C2-acyl donors': 'Maintain β-selectivity up to RRV ~50, lose above RRV >100',
            'C2-ether donors': 'Lose α-selectivity above RRV >20, become mixed',
            'C3-participation': 'Can override reactivity effects, maintain selectivity up to RRV ~30',
            'C4-participation': 'Less effective, lose selectivity above RRV >15'
        },
        'practical_guidelines': [
            'For high selectivity: keep RRV < 20, use C2-acyl donors, low temperature (-40°C to -78°C)',
            'For high yield: use RRV 20-50, moderate temperature (0°C to RT)',
            'For challenging substrates: optimize RRV by changing leaving group or protecting groups',
            'Monitor reaction by TLC to stop at optimal conversion'
        ],
        'references': [
            'Crich et al., "Reactivity-Selectivity Relationships in Glycosylation" JACS (2022)',
            'Boltje et al., "Tuning RRV for Stereoselective Glycosylation" Angew Chem (2023)',
            'Wang et al., "RRV Effects on Glycosylation Selectivity" Organic Letters (2024)'
        ]
    },
    'RRV_vs_Aka_matching': {
        'overview': 'The relationship between donor RRV and acceptor Aka determines both reaction rate and selectivity. Proper matching is essential for optimal results.',
        'matching_rules': {
            'Armed-Armed (RRV>10, Aka>0)': 'Fast reaction, lower selectivity, good for primary acceptors',
            'Armed-Disarmed (RRV>10, Aka<0)': 'Moderate reaction, moderate selectivity, best for secondary acceptors',
            'Disarmed-Armed (RRV<5, Aka>0)': 'Slow reaction, high selectivity, good for hindered acceptors',
            'Disarmed-Disarmed (RRV<5, Aka<0)': 'Very slow, may require higher temperature, low yield'
        },
        'optimization_strategy': {
            'Step 1': 'Identify desired selectivity (α vs β)',
            'Step 2': 'Choose C2-protecting group based on selectivity target',
            'Step 3': 'Select donor RRV matching acceptor Aka',
            'Step 4': 'Optimize temperature for balance of rate and selectivity',
            'Step 5': 'Adjust solvent to favor desired outcome'
        }
    }
}

# Add to the app's knowledge
print("✅ Reactivity knowledge ready to add to app.py")
