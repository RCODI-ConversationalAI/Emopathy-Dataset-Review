import bibtexparser
import re
from collections import defaultdict
import csv
import os

def load_bibtex_file(file_path):
    """Load and parse a BibTeX file."""
    with open(file_path, 'r', encoding='utf-8') as bibtex_file:
        parser = bibtexparser.bparser.BibTexParser(common_strings=True)
        return bibtexparser.load(bibtex_file, parser)

def compile_patterns():
    """Compile regex patterns for paper categorization."""
    return {
        'emotion': re.compile(r'\bemotion(?:s|al)?\b', re.IGNORECASE),
        'empathy': re.compile(r'\bempath(?:y|ic|i[zs]e)\b', re.IGNORECASE),
        'dataset': re.compile(
            r'\b(?:dataset|corpus|collection|benchmark|annotated?|labeled)\b',
            re.IGNORECASE
        ),
        'machine_learning': re.compile(
            r'\b(?:machine\s+learning|deep\s+learning|neural|classifier|classification|'
            r'supervised|unsupervised|transformer|bert|gpt|llm|embedding|fine-tun|'
            r'train(?:ing|ed)|model(?:s|ing|ed)?)\b',
            re.IGNORECASE
        ),
        'ai': re.compile(
            r'\b(?:artificial\s+intelligence|natural\s+language\s+processing|nlp|'
            r'computational\s+linguistics|language\s+model(?:s|ing)?)\b',
            re.IGNORECASE
        )
    }

def categorize_paper(entry, patterns):
    """
    Categorize a paper based on its abstract and title.
    Returns a dictionary with classification results and main category.
    """
    title = entry.get('title', '').lower()
    abstract = entry.get('abstract', '').lower()
    combined_text = f"{title} {abstract}"
    
    # Check for emotion and empathy in title
    emotion_match_title = patterns['emotion'].search(title)
    empathy_match_title = patterns['empathy'].search(title)
    
    # Determine main category based on title matches
    if emotion_match_title and empathy_match_title:
        main_category = 'emotion_and_empathy'
    elif empathy_match_title:
        main_category = 'empathy'
    elif emotion_match_title:
        main_category = 'emotion'
    else:
        return None  # Skip papers not related to emotion or empathy
    
    # Check for other categories in combined text
    categories = {
        'main_category': main_category,
        'is_dataset': bool(patterns['dataset'].search(combined_text)),
        'is_ml': bool(patterns['machine_learning'].search(combined_text)),
        'is_ai': bool(patterns['ai'].search(combined_text))
    }
    
    return categories

def extract_paper_info(entry, categories):
    """Extract relevant information from a paper entry."""
    # Clean up author string if it exists
    authors = entry.get('author', '')
    if authors:
        # Remove extra whitespace and newlines
        authors = ' and '.join(author.strip() for author in authors.split(' and '))
    
    return {
        'title': entry.get('title', '').strip(),
        'authors': authors,
        'year': entry.get('year', ''),
        'booktitle': entry.get('booktitle', ''),
        'doi': entry.get('doi', ''),
        'abstract': entry.get('abstract', ''),
        'url': entry.get('url', ''),
        'category': categories['main_category'],
        'is_dataset': categories['is_dataset'],
        'is_ml': categories['is_ml'],
        'is_ai': categories['is_ai']
    }

def analyze_papers(bib_database, patterns):
    """Analyze all papers in the database."""
    papers_info = []
    stats = defaultdict(lambda: {
        'papers': 0,
        'dataset': 0,
        'machine_learning': 0,
        'ai': 0
    })
    
    for entry in bib_database.entries:
        if 'abstract' not in entry:  # Skip entries without abstracts
            continue
            
        categories = categorize_paper(entry, patterns)
        if categories:  # Only process papers related to emotion/empathy
            paper_info = extract_paper_info(entry, categories)
            papers_info.append(paper_info)
            
            # Update statistics
            category = categories['main_category']
            stats[category]['papers'] += 1
            if categories['is_dataset']:
                stats[category]['dataset'] += 1
            if categories['is_ml']:
                stats[category]['machine_learning'] += 1
            if categories['is_ai']:
                stats[category]['ai'] += 1
    
    return papers_info, dict(stats)

def save_results_to_csv(papers_info, output_file):
    """Save paper information to a CSV file."""
    fieldnames = [
        'title', 'authors', 'year', 'booktitle', 'doi', 'abstract', 
        'url', 'category', 'is_dataset', 'is_ml', 'is_ai'
    ]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for paper in papers_info:
            # Convert boolean values to Yes/No
            paper_copy = paper.copy()
            for key in ['is_dataset', 'is_ml', 'is_ai']:
                paper_copy[key] = 'Yes' if paper_copy[key] else 'No'
            writer.writerow(paper_copy)

def print_statistics(stats, output_file):
    """Print and save analysis statistics."""
    with open(output_file, 'w', encoding='utf-8') as f:
        def write_line(line):
            print(line)
            f.write(line + '\n')
            
        write_line("Analysis Statistics:")
        for category in ['emotion', 'empathy', 'emotion_and_empathy']:
            if category in stats:
                write_line(f"\n{category.upper()} Papers:")
                write_line(f"Total papers: {stats[category]['papers']}")
                write_line(f"Dataset papers: {stats[category]['dataset']}")
                write_line(f"Machine Learning papers: {stats[category]['machine_learning']}")
                write_line(f"AI/NLP papers: {stats[category]['ai']}")

def main():
    # File paths
    input_file = '/Volumes/ssd/01-ckj-postdoc/emopathy-dataset-review/boolean-search/all-zot-items/anthology+abstracts.bib'  # Your input BibTeX file
    output_csv = 'final_automatically_screened_acl_papers.csv'
    stats_file = 'final_analysis_statistics_acl.txt'
    
    # Load and analyze papers
    bib_database = load_bibtex_file(input_file)
    patterns = compile_patterns()
    papers_info, stats = analyze_papers(bib_database, patterns)
    
    # Save results
    save_results_to_csv(papers_info, output_csv)
    print_statistics(stats, stats_file)
    
    print(f"\nResults saved to {output_csv}")
    print(f"Statistics saved to {stats_file}")

if __name__ == "__main__":
    main()