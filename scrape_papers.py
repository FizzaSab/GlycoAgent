#!/usr/bin/env python3
"""
Enhanced paper scraper for glycosylation research
Collects papers from multiple sources
"""
import requests
import pandas as pd
import time
import re
from datetime import datetime
from tqdm import tqdm

def fetch_pubmed(query, max_results=500):
    """Fetch papers from PubMed API"""
    papers = []
    try:
        # PubMed E-utilities API
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        
        # Search for papers
        search_url = f"{base_url}esearch.fcgi?db=pubmed&term={query}&retmax={max_results}&retmode=json"
        response = requests.get(search_url)
        data = response.json()
        
        ids = data.get('esearchresult', {}).get('idlist', [])
        
        # Fetch details
        for pmid in ids:
            fetch_url = f"{base_url}efetch.fcgi?db=pubmed&id={pmid}&retmode=xml"
            # Would need XML parsing - simplified here
            papers.append({'pmid': pmid})
            time.sleep(0.3)
    except Exception as e:
        print(f"PubMed error: {e}")
    
    return papers

def search_sources():
    """Search multiple sources for glycosylation papers"""
    
    queries = [
        "glycosylation",
        "O-glycosylation",
        "chemical glycosylation",
        "glycosidic bond formation",
        "carbohydrate chemistry",
        "glycan synthesis",
        "remote participation glycosylation",
        "thioglycoside",
        "Koenigs-Knorr",
        "Schmidt glycosylation"
    ]
    
    all_papers = []
    
    for query in queries:
        print(f"Searching: {query}")
        papers = fetch_pubmed(query, max_results=200)
        all_papers.extend(papers)
        time.sleep(1)
    
    # Remove duplicates
    seen = set()
    unique_papers = []
    for p in all_papers:
        if p['pmid'] not in seen:
            seen.add(p['pmid'])
            unique_papers.append(p)
    
    print(f"Found {len(unique_papers)} unique papers")
    
    # Save to Excel
    df = pd.DataFrame(unique_papers)
    df.to_excel('glycosylation_papers_enhanced.xlsx', index=False)
    print("Saved to glycosylation_papers_enhanced.xlsx")

if __name__ == "__main__":
    search_sources()
