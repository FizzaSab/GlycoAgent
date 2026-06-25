import re
import fileinput

# Read app.py
with open('app.py', 'r') as f:
    content = f.read()

# Find the get_expert_response method and add reactivity detection
# Add reactivity terms to the detection

# Find the section that checks for topics
pattern = r"(if any\(term in question_lower for term in \['automation', 'machine learning', 'ml', 'ai'\]\):.*?response_parts\.append\(\"\\n\\n\"\.join\(parts\)\))"

# Add reactivity detection after it
replacement = r"""\1
        
        # Check for reactivity parameters questions
        if any(term in question_lower for term in ['rrv', 'aka', 'relative reactivity', 'acceptor reactivity', 'reactivity value', 'reactivity parameter', 'donor reactivity', 'selectivity trend', 'tune reactivity']):
            knowledge = self.expert_knowledge.get('reactivity_parameters', {})
            if knowledge:
                parts = []
                if 'overview' in knowledge:
                    parts.append(knowledge['overview'])
                if 'RRV_trends' in knowledge:
                    parts.append("**RRV trends:** " + "; ".join(knowledge['RRV_trends']))
                if 'tuning_RRV' in knowledge:
                    tuning = knowledge['tuning_RRV']
                    tuning_text = "**How to tune RRV and selectivity:**\n"
                    for method, desc in tuning.items():
                        tuning_text += f"• **{method}:** {desc}\n"
                    parts.append(tuning_text)
                if 'RRV_selectivity_correlation' in knowledge:
                    corr = knowledge['RRV_selectivity_correlation']
                    corr_text = "**RRV-Selectivity correlation:**\n"
                    for donor, effect in corr.items():
                        corr_text += f"• **{donor}:** {effect}\n"
                    parts.append(corr_text)
                if 'RRV_Aka_matching' in knowledge:
                    match = knowledge['RRV_Aka_matching']
                    match_text = "**RRV-Aka matching rules:**\n"
                    for condition, outcome in match.items():
                        match_text += f"• **{condition}:** {outcome}\n"
                    parts.append(match_text)
                if 'practical_guidelines' in knowledge:
                    parts.append("**Practical guidelines:** " + "; ".join(knowledge['practical_guidelines']))
                response_parts.append("\n\n".join(parts))"""

# Apply the update
updated = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Write back
with open('app.py', 'w') as f:
    f.write(updated)

print("✅ Question detection updated for reactivity terms")
