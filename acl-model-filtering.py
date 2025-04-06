import os
import time
import pandas as pd
import fitz  # PyMuPDF
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import re

# --- 1. Download PDFs ---
def download_pdfs(spreadsheet_path, download_dir):
    df = pd.read_csv(spreadsheet_path)
    options = Options()
    options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "plugins.always_open_pdf_externally": True
    })
    driver = webdriver.Chrome(options=options, service=Service("chromedriver"))  # Replace with your chromedriver path
    
    for index, row in df.iterrows():
        url = row['url']
        driver.get(url)
        try:
            pdf_button = driver.find_element(By.LINK_TEXT, "PDF")
            pdf_button.click()
            time.sleep(3)
        except Exception as e:
            print(f"Failed to download PDF for {url}: {e}")
    
    driver.quit()

# --- 2. Extract text from PDF ---
def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print(f"Failed to extract text from {pdf_path}: {e}")
        return ""

# --- 3. Extract models and performance metrics from sections ---
def extract_performance_and_models(text):
    # Split text into sections based on headings (e.g., "1. Methods", "2. Results")
    section_pattern = r"(?i)(?:(?:^|\n)([0-9]+\.\s+[A-Za-z]+.*))"  # Matches headings like "1. Methods"
    sections = re.split(section_pattern, text)
    
    # If no sections found, consider the entire text as one "default" section
    if len(sections) <= 1:
        sections = ["Entire Text", text]

    # Define regex patterns
    model_patterns = [
        r"\bLSTM(s?)\b", r"\bCNN(s?)\b", r"\bTransformer(s?)\b", r"\bBERT(s?)\b",
        r"\bGRU(s?)\b", r"\bRNN(s?)\b", r"\bXLNet(s?)\b", r"\bRoBERTa(s?)\b",
        r"\bGPT(-\d?)?\b", r"\bSVM(s?)\b", r"\bRandom Forest(s?)\b", r"\bXGBoost\b",
        r"\bLightGBM\b", r"\bCatBoost\b", r"\bKNN\b", r"\bNaive Bayes\b",
        r"\bDecision Tree(s?)\b", r"\bLinear Regression\b", r"\bLogistic Regression\b",
        r"\bEnsemble(s?)\b"
    ]
    combined_model_pattern = r"(?:" + "|".join(model_patterns) + r")"
    
    performance_patterns = [
        r"(accuracy|f1 score|precision|recall|auc|bleu|rouge|mse|rmse)\s*[:=]?\s*(\d+\.?\d*)"
    ]
    combined_performance_pattern = r"(?:" + "|".join(performance_patterns) + r")"

    # Results
    section_results = {}
    
    for i in range(0, len(sections), 2):  # Process pairs of [heading, content]
        if i + 1 >= len(sections):
            break
        section_heading = sections[i].strip() if sections[i].strip() else "No Heading"
        section_content = sections[i + 1].strip()
        
        # Find models in the section
        found_models = re.findall(combined_model_pattern, section_content, re.IGNORECASE)
        unique_models = list(set(model.split("s", 1)[0] for model in found_models))  # Normalize
        
        # Find performance metrics in the section
        found_metrics = re.findall(combined_performance_pattern, section_content, re.IGNORECASE)
        metrics_dict = {metric.lower().replace(" ", "_"): float(value) for metric, value in found_metrics}
        
        section_results[section_heading] = {
            "models": unique_models,
            "metrics": metrics_dict
        }
    
    return section_results

# --- 4. Main Workflow ---
def main(spreadsheet_path, download_dir, output_csv, sort_by="f1_score"):
    print("Starting PDF download...")
    download_pdfs(spreadsheet_path, download_dir)
    print("PDF download completed.")
    
    data = []
    for pdf_file in os.listdir(download_dir):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(download_dir, pdf_file)
            print(f"Processing {pdf_file}...")
            
            text = extract_text_from_pdf(pdf_path)
            
            results = extract_performance_and_models(text)
            
            # Flatten the results for the entire document
            all_models = []
            all_metrics = {}
            for section, content in results.items():
                all_models.extend(content["models"])
                all_metrics.update(content["metrics"])
            
            # Remove duplicate models
            all_models = list(set(all_models))
            
            data.append({
                "file": pdf_file,
                "models": ", ".join(all_models),
                "metrics": all_metrics,
                **all_metrics  # Add metrics as individual columns
            })
    
    result_df = pd.DataFrame(data)
    if sort_by in result_df.columns:
        result_df = result_df.sort_values(by=sort_by, ascending=False)  # Sort by the chosen metric
    result_df.to_csv(output_csv, index=False)
    print(f"Results saved to {output_csv}")

if __name__ == "__main__":
    SPREADSHEET_PATH = "statistics/final_automatically_screened_acl_papers.csv"
    DOWNLOAD_DIR = "emopathy-acl-model-papers" # Your dir for pdf download
    OUTPUT_CSV = "statistics/model_performance.csv"
    SORT_BY = "f1_score"                 # Metric to sort by

    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    main(SPREADSHEET_PATH, DOWNLOAD_DIR, OUTPUT_CSV, sort_by=SORT_BY)
