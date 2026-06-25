import re

# Read app.py
with open('app.py', 'r') as f:
    lines = f.readlines()

# Find the reactivity section and fix it
new_lines = []
skip_until = -1
in_reactivity = False
reactivity_fixed = False

for i, line in enumerate(lines):
    if "'reactivity_parameters':" in line and not reactivity_fixed:
        # Skip the old reactivity section
        in_reactivity = True
        brace_count = 0
        continue
    
    if in_reactivity:
        if '{' in line:
            brace_count += line.count('{')
        if '}' in line:
            brace_count -= line.count('}')
        
        if brace_count <= 0:
            # End of reactivity section
            in_reactivity = False
            reactivity_fixed = True
            # Add the new reactivity section
            new_lines.append("            'reactivity_parameters': {\n")
            new_lines.append("                'overview': 'RRV (Relative Reactivity Value) measures donor reactivity, while Aka measures acceptor nucleophilicity. Both parameters are essential for predicting glycosylation outcomes.',\n")
            new_lines.append("                'RRV_trends': [\n")
            new_lines.append("                    'Low RRV (1-10): High stereoselectivity, slower reactions',\n")
            new_lines.append("                    'Medium RRV (10-50): Balanced reactivity and selectivity',\n")
            new_lines.append("                    'High RRV (50-500): Fast reactions, lower stereoselectivity',\n")
            new_lines.append("                    'Very High RRV (>500): Very fast, poor selectivity'\n")
            new_lines.append("                ],\n")
            new_lines.append("                'tuning_RRV': {\n")
            new_lines.append("                    'Temperature': 'Lower temperature (-78°C) increases selectivity',\n")
            new_lines.append("                    'Solvent': 'DCM favors selectivity, THF favors reactivity',\n")
            new_lines.append("                    'C2-protecting groups': 'Acyl groups maintain β-selectivity'\n")
            new_lines.append("                },\n")
            new_lines.append("                'references': [\n")
            new_lines.append("                    'Crich et al., JACS (2022)',\n")
            new_lines.append("                    'Boltje et al., Angew Chem (2023)'\n")
            new_lines.append("                ]\n")
            new_lines.append("            },\n")
            continue
    
    if not in_reactivity:
        new_lines.append(line)

# Write back
with open('app.py', 'w') as f:
    f.writelines(new_lines)

print("✅ Reactivity section completely rewritten and fixed")
