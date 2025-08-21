import re
import pandas as pd
from PyPDF2 import PdfReader

def classify_risk(text):
    lower = text.lower()
    if any(x in lower for x in ["myocarditis", "anaphylaxis", "shortly after", "autopsy confirmed", "sudden death", "stroke after vaccine", "within 24 hours"]):
        return "75-100% (Very Likely)"
    elif any(x in lower for x in ["cardiac arrest", "arrhythmia", "collapse", "blood clot", "MI", "pulmonary embolism", "died within a week"]):
        return "50-75% (Likely)"
    elif any(x in lower for x in ["preexisting", "advanced cancer", "hospice", "severe comorbidity", "dementia", "parkinson", "alzheimer", "CHF"]):
        return "0-25% (Very Unlikely)"
    else:
        return "25-50% (Unclear/Unlikely)"

def process_vaers_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    all_text = ""
    for page in reader.pages:
        all_text += page.extract_text() + "\n"

    # Split into cases using "VAERS ID:"
    raw_blocks = re.split(r"(VAERS ID:\s*\d+)", all_text)
    entries = [raw_blocks[i] + raw_blocks[i+1] for i in range(1, len(raw_blocks)-1, 2)]

    data = []
    for block in entries:
        match = re.search(r"VAERS ID:\s*(\d+)", block)
        if not match:
            continue
        vaers_id = match.group(1)
        short_summary = block[:600].replace("\n", " ").strip()
        probability = classify_risk(block)
        data.append((vaers_id, short_summary, probability))

    df = pd.DataFrame(data, columns=["VAERS ID", "Summary", "Estimated Probability"])
    return df

# Example usage
import os
os.chdir("C:\\Users\\stk\\Documents\\GitHub\\covid\\VAERS")
df_result = process_vaers_pdf("500_vaers_death_reports.pdf")
df_result.to_csv("vaers_risk_estimates.csv", index=False)
print(df_result.head())
