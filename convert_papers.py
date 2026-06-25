import pandas as pd
import requests
import time
import xml.etree.ElementTree as ET
from tqdm import tqdm

PUBMED_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def fetch_paper_details(pmid):
    """Fetch full paper details from PubMed"""
    try:
        url = f"{PUBMED_BASE}efetch.fcgi?db=pubmed&id={pmid}&retmode=xml"
        response = requests.get(url, timeout=30)
        
        if response.status_code != 200:
            return None
            
        root = ET.fromstring(response.content)
        article = root.find('.//Article')
        if article is None:
            return None
            
        # Title
        title_elem = article.find('.//ArticleTitle')
        title = title_elem.text if title_elem is not None else ""
        
        # Abstract
        abstract_elem = article.find('.//Abstract/AbstractText')
        abstract = abstract_elem.text if abstract_elem is not None else ""
        
        # Journal
        journal_elem = article.find('.//Journal/Title')
        journal = journal_elem.text if journal_elem is not None else ""
        
        # Year
        year_elem = article.find('.//PubDate/Year')
        year = year_elem.text if year_elem is not None else ""
        
        # Authors
        authors = []
        for author in article.findall('.//Author'):
            last = author.find('LastName')
            fore = author.find('ForeName')
            if last is not None and fore is not None:
                authors.append(f"{fore.text} {last.text}")
        
        # DOI
        doi_elem = root.find(".//ArticleId[@IdType='doi']")
        doi = doi_elem.text if doi_elem is not None else ""
        
        # Classify topic
        topic = classify_topic(title, abstract)
        
        return {
            'Title': title,
            'Authors': '; '.join(authors[:5]),
            'Year': year,
            'Journal': journal,
            'Abstract': abstract[:2000] if abstract else "",
            'DOI': doi,
            'URL': f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            'Topic': topic
        }
    except Exception as e:
        return None

def classify_topic(title, abstract):
    """Classify paper topic based on keywords"""
    text = f"{title} {abstract}".lower()
    
    topics = {
        'Chemical Glycosylation': ['glycosylation', 'glycosidic', 'synthesis', 'chemical', 'donor', 'acceptor', 'koenigs-knorr', 'schmidt', 'thioglycoside'],
        'O-Glycosylation': ['o-glycosylation', 'o-glycan', 'o-linked', 'mucin', 'galnac', 'o-glcnac'],
        'N-Glycosylation': ['n-glycosylation', 'n-glycan', 'n-linked', 'asparagine'],
        'Remote Participation': ['remote participation', 'remote group', 'c3', 'c4', 'c6', 'dppa', 'pivaloyl'],
        'Environmental Effects': ['temperature', 'solvent', 'water', 'pressure', 'additive', 'reaction conditions'],
        'L vs D Sugar Selectivity': ['l-sugar', 'd-sugar', 'enantiomer', 'l-ribose'],
        'Automation ML AI': ['machine learning', 'ai', 'automated', 'prediction', 'neural network'],
        'Glycoproteins': ['glycoprotein', 'glycopeptide', 'protein glycosylation'],
        'Glycan Synthesis': ['glycan', 'oligosaccharide', 'polysaccharide'],
        'Stereoselectivity': ['stereoselective', 'stereoselectivity', 'α', 'β']
    }
    
    for topic, keywords in topics.items():
        if any(kw in text for kw in keywords):
            return topic
    
    return 'General Glycosylation'

# Load the enhanced papers
print("📚 Loading papers...")
df = pd.read_excel('glycosylation_papers_enhanced.xlsx')

print(f"📊 Found {len(df)} papers to process")

# Convert to full paper details
papers = []
for pmid in tqdm(df['pmid'], desc="Fetching paper details"):
    paper = fetch_paper_details(pmid)
    if paper:
        papers.append(paper)
    time.sleep(0.2)  # Rate limit

# Create DataFrame with full details
result_df = pd.DataFrame(papers)

# Remove duplicates
result_df = result_df.drop_duplicates(subset=['Title'])

# Save to Excel
result_df.to_excel('glycosylation_papers.xlsx', sheet_name='All Papers', index=False)

print(f"\n✅ Saved {len(result_df)} papers to glycosylation_papers.xlsx")

# Show statistics
print("\n📊 Topic Distribution:")
print(result_df['Topic'].value_counts())

print("\n📊 Year Distribution:")
print(result_df['Year'].value_counts().sort_index().head(10))
