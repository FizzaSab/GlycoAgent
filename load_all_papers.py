import pandas as pd
import os

# Find all Excel files
excel_files = [f for f in os.listdir('.') if f.endswith('.xlsx')]
print("Available Excel files:")
for f in excel_files:
    try:
        df = pd.read_excel(f, sheet_name='All Papers')
        print(f"  {f}: {len(df)} papers")
    except:
        print(f"  {f}: Error reading")

# If glycosylation_papers_enhanced.xlsx exists, use it
if 'glycosylation_papers_enhanced.xlsx' in excel_files:
    df = pd.read_excel('glycosylation_papers_enhanced.xlsx', sheet_name='All Papers')
    df.to_excel('glycosylation_papers.xlsx', sheet_name='All Papers', index=False)
    print(f"\n✅ Copied {len(df)} papers to glycosylation_papers.xlsx")
    print(f"   Now restart the app to see all {len(df)} papers!")
else:
    print("\n⚠️ glycosylation_papers_enhanced.xlsx not found")
    print("   Current file has:", len(pd.read_excel('glycosylation_papers.xlsx', sheet_name='All Papers')), "papers")
