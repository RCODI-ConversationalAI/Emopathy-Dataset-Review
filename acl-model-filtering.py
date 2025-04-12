import os
import io
import pandas as pd
import fitz  # PyMuPDF
import spacy
from urllib.parse import urlparse
import requests
from collections import defaultdict

# Load SpaCy model for NLP processing
nlp = spacy.load("en_core_web_sm")

# --- 1. Scrape and process PDFs ---
def process_papers(spreadsheet_path, output_csv, sort_by="f1_score"):
    df = pd.read_csv(spreadsheet_path)
    data = []
    
    for index, row in df[:5].iterrows():  # TODO: Remove after testing
        url = row['url']
        print(f"Accessing {url}...")
        pdf_name = urlparse(url).path.split("/")[-1] + ".pdf"

        pdf_url = f"{url}.pdf"
        pdf_response = requests.get(pdf_url)
        if pdf_response.status_code != 200:
            print(f"Failed to download PDF from {pdf_url}")
            continue
        
        print(f"Processing {pdf_name}...")
        
        # Process the PDF content directly from the response
        try:
            pdf_stream = io.BytesIO(pdf_response.content)  # Create an in-memory byte stream
            text = extract_text_from_pdf(pdf_stream)  # Pass the stream to the text extraction function
            
            # Extract models and performance metrics
            results = extract_performance_and_models(text)
            
            data.append({
                "file": pdf_name,
                "models": ", ".join(results["models"]),
                "metrics": results["metrics"],
                **results["metrics"]  # Add metrics as individual columns
            })
        except Exception as e:
            print(f"Failed to process {pdf_name}: {e}")
            continue
    
    # Create a DataFrame and save results
    result_df = pd.DataFrame(data)
    if sort_by in result_df.columns:
        result_df = result_df.sort_values(by=sort_by, ascending=False)  # Sort by the chosen metric
    result_df.to_csv(output_csv, index=False)
    print(f"Results saved to {output_csv}")


# --- 2. Extract text from PDF ---
def extract_text_from_pdf(pdf_stream):
    try:
        doc = fitz.open(stream=pdf_stream, filetype="pdf")  # Open the PDF from the byte stream
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print(f"Failed to extract text from PDF: {e}")
        return ""


# --- 3. Extract models and performance metrics from sections ---
def extract_performance_and_models(text):
    # Tokenize the text using SpaCy
    doc = nlp(text)
    
    # Define model and metric keywords
    model_keywords = {
        "lstm", "cnn", "transformer", "bert", "gru", "rnn", "xlnet", "roberta",
        "gpt", "svm", "random forest", "xgboost", "lightgbm", "catboost", "knn",
        "naive bayes", "decision tree", "linear regression", "logistic regression", "ensemble"
    }
    metric_keywords = {
        "accuracy", "f1 score", "precision", "recall", "auc", "bleu", "rouge", "mse", "rmse"
    }
    
    # Extract models and metrics
    models = set()
    metrics = defaultdict(float)
    
    for token in doc:
        # Check for model keywords
        if token.text.lower() in model_keywords:
            models.add(token.text.lower())
        
        # Check for metric keywords and their values
        if token.text.lower() in metric_keywords:
            next_token = token.nbor(1) if token.i + 1 < len(doc) else None
            if next_token and next_token.like_num:
                metrics[token.text.lower()] = float(next_token.text)
    
    return {
        "models": list(models),
        "metrics": dict(metrics)
    }


# --- 4. Main Workflow ---
if __name__ == "__main__":
    SPREADSHEET_PATH = "statistics/final_automatically_screened_acl_papers.csv"
    OUTPUT_CSV = "statistics/model_performance.csv"
    SORT_BY = "f1_score"  # Metric to sort by

    process_papers(SPREADSHEET_PATH, OUTPUT_CSV, sort_by=SORT_BY)