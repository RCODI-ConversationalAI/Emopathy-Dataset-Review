import re
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
    
    for index, row in df.iterrows():
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
                "Title": row['title'],
                "Authors": row['authors'],
                "URL": row['url'],
                "Models": ", ".join(results["models"]),
                "Metrics": results["metrics"],
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

    # Define regex patterns for models and metrics
    model_patterns = [
        r"\bLSTM(s?)\b", r"\bCNN(s?)\b", r"\bTransformer(s?)\b", r"\bBERT(s?)\b",
        r"\bGRU(s?)\b", r"\bRNN(s?)\b", r"\bXLNet(s?)\b", r"\bRoBERTa(s?)\b",
        r"\bGPT(-\d+)?\b", r"\bSVM(s?)\b", r"\bRandom Forest(s?)\b", r"\bXGBoost\b",
        r"\bLightGBM\b", r"\bCatBoost\b", r"\bKNN\b", r"\bNaive Bayes\b",
        r"\bDecision Tree(s?)\b", r"\bLinear Regression\b", r"\bLogistic Regression\b",
        r"\bEnsemble(s?)\b"
    ]
    combined_model_pattern = r"(?:" + "|".join(model_patterns) + r")"

    metric_patterns = [
        r"(accuracy|f1|f1 score|f1-score|precision|recall|auc|bleu|rouge|mse|rmse)"
    ]
    combined_metric_pattern = r"(?:" + "|".join(metric_patterns) + r")"

    # Extract models
    models = set()
    seen_models = set()  # lowercased models to avoid duplicates
    for token in doc:
        if re.match(combined_model_pattern, token.text, re.IGNORECASE):
            model = token.text
            model_lower = model.lower()
            if model_lower not in seen_models:
                seen_models.add(model_lower)  # Add the lowercase version to the helper set
                models.add(model)  # Add the original case version to the models set

    # Extract metrics
    metrics = defaultdict(float)
    for i, token in enumerate(doc):
        cleaned_token = token.text.strip(".,:;!?()[]{}").lower()  # Clean and normalize the token
        if re.match(combined_metric_pattern, cleaned_token, re.IGNORECASE):  # Match only the metric name
            metric_name = cleaned_token.replace(" ", "_")  # Normalize the metric name
            # Check the next token for a numeric value
            if i + 1 < len(doc) and doc[i + 1].like_num:
                metrics[metric_name] = float(doc[i + 1].text)
            else:
                metrics[metric_name] = None

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