import os
import rispy
import bibtexparser
from collections import defaultdict
import re
import csv

def collect_all_papers(database_dir):
    all_papers = []
    original_papers = set()
    duplicate_count = 0
    
    for filename in os.listdir(database_dir):
        file_path = os.path.join(database_dir, filename)
        database_name = filename[:-4]
        
        if filename.endswith('.ris'):
            with open(file_path, 'r', encoding='utf-8') as bibliography_file:
                entries = list(rispy.load(bibliography_file))
                for entry in entries:
                    title = entry.get('title', '').lower()
                    if not title:
                        continue
                    if title in original_papers:
                        duplicate_count += 1
                    else:
                        original_papers.add(title)
                        all_papers.append((entry, database_name))
                        
        elif filename.endswith('.bib'):
            with open(file_path, 'r', encoding='utf-8') as bibtex_file:
                bib_database = bibtexparser.load(bibtex_file)
                for entry in bib_database.entries:
                    title = entry.get('title', '').lower()
                    if not title:
                        continue
                    if title in original_papers:
                        duplicate_count += 1
                    else:
                        original_papers.add(title)
                        all_papers.append((entry, database_name))
    
    return all_papers, duplicate_count, len(all_papers) + duplicate_count

def extract_paper_info(entry, database_name, category_info):
    info = {
        'database': database_name,
        'title': entry.get('title', '').strip(),
        'authors': entry.get('authors', []),
        'year': entry.get('year', ''),
        'journal': entry.get('journal', ''),
        'volume': entry.get('volume', ''),
        'issue': entry.get('issue', ''),
        'doi': entry.get('doi', ''),
        'abstract': entry.get('abstract', ''),
        'keywords': entry.get('keywords', []),
        'url': entry.get('url', ''),
        'type': entry.get('type', ''),
        'category': category_info['main_category'],
        'is_dataset': category_info['is_dataset'],
        'is_ml': category_info['is_ml']
    }
    return info

def analyze_entry(entry, database_name, patterns):
    title = entry.get('title', '').lower()
    abstract = entry.get('abstract', '').lower()
    combined_text = f"{title} {abstract}"
    
    emotion_match_title = patterns['emotion'].search(title)
    empathy_match_title = patterns['empathy'].search(title)
    
    if emotion_match_title and empathy_match_title:
        main_category = 'emotion_and_empathy'
    elif empathy_match_title:
        main_category = 'empathy'
    elif emotion_match_title:
        main_category = 'emotion'
    else:
        return None

    is_ml = bool(patterns['task'].search(combined_text) and 
                patterns['result'].search(combined_text))
    
    is_dataset = bool(patterns['dataset'].search(combined_text) and
                     (patterns['annotation'].search(combined_text) or 
                      patterns['labeling'].search(combined_text)))

    category_info = {
        'main_category': main_category,
        'is_dataset': is_dataset,
        'is_ml': is_ml
    }
    
    return extract_paper_info(entry, database_name, category_info)

def analyze_databases(database_dir):
    patterns = {
        'emotion': re.compile(r'\bemotion(?:s|al)?\b', re.IGNORECASE),
        'empathy': re.compile(r'\bempath(?:y|ic|i[zs]e)\b', re.IGNORECASE),
        'task': re.compile(r'\b(?:classif(?:y|ication)|recogn(?:ize|ition)|predict(?:ion)?|regress(?:ion)?|generat(?:e|ion))\b', re.IGNORECASE),
        'result': re.compile(r'\b(?:result|perform(?:ance|ed|ing)|f1|accurac(?:y|ies)|pearson)\b', re.IGNORECASE),
        'dataset': re.compile(r'\bdata(?:set|base)?\b', re.IGNORECASE),
        'annotation': re.compile(r'\bannotat(?:ion|ed|ing)\b', re.IGNORECASE),
        'labeling': re.compile(r'\blabell?(?:ing|ed|s)?\b', re.IGNORECASE)
    }

    all_papers, total_duplicates, total_papers = collect_all_papers(database_dir)
    
    papers_info = []
    database_stats = defaultdict(lambda: {
        'emotion': {'papers': 0, 'machine_learning': 0, 'dataset': 0},
        'empathy': {'papers': 0, 'machine_learning': 0, 'dataset': 0},
        'emotion_and_empathy': {'papers': 0, 'machine_learning': 0, 'dataset': 0}
    })
    
    global_stats = {
        'emotion': {'papers': 0, 'machine_learning': 0, 'dataset': 0},
        'empathy': {'papers': 0, 'machine_learning': 0, 'dataset': 0},
        'emotion_and_empathy': {'papers': 0, 'machine_learning': 0, 'dataset': 0},
        'total_papers': total_papers,
        'original_papers': len(all_papers),
        'duplicates': total_duplicates
    }

    for entry, database_name in all_papers:
        paper_info = analyze_entry(entry, database_name, patterns)
        if paper_info:
            papers_info.append(paper_info)
            
            category = paper_info['category']
            database_stats[database_name][category]['papers'] += 1
            global_stats[category]['papers'] += 1
            
            if paper_info['is_ml']:
                database_stats[database_name][category]['machine_learning'] += 1
                global_stats[category]['machine_learning'] += 1
                
            if paper_info['is_dataset']:
                database_stats[database_name][category]['dataset'] += 1
                global_stats[category]['dataset'] += 1

    return dict(database_stats), global_stats, papers_info

def save_paper_info_to_csv(papers_info, output_file):
    """
    논문 정보를 CSV 파일로 저장
    """
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'database', 'title', 'authors', 'year', 'journal', 
            'volume', 'issue', 'doi', 'abstract', 'keywords', 'url', 'type',
            'category', 'is_dataset', 'is_ml'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for paper in papers_info:
            # authors와 keywords를 문자열로 변환
            paper['authors'] = '; '.join(paper['authors']) if isinstance(paper['authors'], list) else paper['authors']
            paper['keywords'] = '; '.join(paper['keywords']) if isinstance(paper['keywords'], list) else paper['keywords']
            # boolean 값을 'Yes'/'No'로 변환
            paper['is_dataset'] = 'Yes' if paper['is_dataset'] else 'No'
            paper['is_ml'] = 'Yes' if paper['is_ml'] else 'No'
            writer.writerow(paper)

def print_and_save_stats(database_stats, global_stats, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        def write_line(line):
            print(line)
            f.write(line + '\n')

        write_line("Overall Statistics:")
        write_line(f"Total papers across all databases: {global_stats['total_papers']}")
        write_line(f"Total unique papers: {global_stats['original_papers']}")
        write_line(f"Total duplicates removed: {global_stats['duplicates']}")
        
        for category in ['emotion', 'empathy', 'emotion_and_empathy']:
            write_line(f"\nTotal {category} related papers: {global_stats[category]['papers']}")
            write_line(f"  - Dataset related papers: {global_stats[category]['dataset']}")
            write_line(f"  - Machine Learning/Deep Learning papers: {global_stats[category]['machine_learning']}")

        write_line("\nStatistics by database:")
        for db, stats in database_stats.items():
            write_line(f"\nDatabase: {db}")
            for category in ['emotion', 'empathy', 'emotion_and_empathy']:
                write_line(f"{category.capitalize()} papers: {stats[category]['papers']}")
                write_line(f"  - Dataset papers: {stats[category]['dataset']}")
                write_line(f"  - Machine Learning papers: {stats[category]['machine_learning']}")

def main():
    database_dir = '/Volumes/ssd/01-ckj-postdoc/LLM-CCR/boolean-search/all-zot-items'
    
    database_stats, global_stats, papers_info = analyze_databases(database_dir)
    
    paper_info_file = 'final_automatically_screened_papers.csv'
    save_paper_info_to_csv(papers_info, paper_info_file)
    print(f"Detailed paper information saved to {paper_info_file}")
    
    stats_output_file = 'final_analysis_statistics.txt'
    print_and_save_stats(database_stats, global_stats, stats_output_file)
    print(f"Statistics saved to {stats_output_file}")

if __name__ == "__main__":
    main()