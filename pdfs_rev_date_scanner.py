import fitz  # PyMuPDF 
import os 
from glob import glob 
from dateutil.parser import parse
import re
import pandas as pd

def replace_from_change(string):
    pattern = r'^.*\bchange\b.*$'
    
    # Check if the line contains "change" and not "supersede"
    if "change" in string and "supersede" not in string and "bars" not in string:
        # Use re.findall() to find all lines matching the pattern
        change_lines = re.findall(pattern, string, flags=re.MULTILINE | re.IGNORECASE)
        if change_lines:
            # If there are matching lines, replace all lines from the first matching line onwards with "change"
            start_index = string.find(change_lines[-1])
            string = string[start_index:]
            return str(change_lines)
    return string

def get_text_first_page(pdf_path): 
    doc = fitz.open(pdf_path) 
    page = doc.load_page(0) 
    page_text = [x for x in page.get_textpage().extractTEXT().lower().strip().splitlines()]
    return page_text

def is_date_or_revision(string, fuzzy=False):
    string = replace_from_change(string)
    try: 
        date_to = parse(string, fuzzy=fuzzy)
        return date_to
    except ValueError:
        return None
    except OverflowError:
        return None

def get_last_date(input_text):
    is_date_analyze = [x for x in input_text if is_date_or_revision(x)]
    if is_date_analyze:
        return is_date_analyze[-1]
    else:
        return None 

def process_pdf_files_in_folder(folder_path):
    print("STARTING PDF SCANNING PROCESS")
    results = {}
    pdf_files = glob(os.path.join(folder_path, '**/*.pdf'), recursive=True) 
    for pdf_file in pdf_files: 
        pdf_text = get_text_first_page(pdf_file) 
        usable_date = get_last_date(pdf_text)
        #print(f"FILE: {pdf_file[len(folder_path)+1:-4]} || DATE: {usable_date}")
        results[pdf_file[len(folder_path)+1:-4]] = {'date': usable_date, 'change_lines': replace_from_change('\n'.join(pdf_text))}
    return results

if __name__ == "__main__":
    print("INICIANDO PROGRAMA")

    result = process_pdf_files_in_folder(".\\")
    print("FINISHED !!")

    df = pd.DataFrame(result).T.reset_index().rename(columns={'index':'to'})
    df = df[['to', 'date', 'change_lines']]  # Reorder the columns if necessary

    # Filter for rows containing "change" in the "change_lines" column
    df["change_lines"] = df["change_lines"][df["change_lines"].str.contains("change")]

    # Filter out strings with length greater than 15 characters
    df["change_lines"] = df["change_lines"][df["change_lines"].str.len() <= 40]

    # remove folder path 
    df["to"] = df["to"].str.rsplit("\\", n=1).str[-1]

    #Change number and date columns
    df["change_number"] = df["change_lines"].str.extract(r'change (\d+)', expand=False)
    df["change_number"].fillna(0,inplace=True)
    df["change_date"] = df["change_lines"].str.rsplit("-", n=2).str[1]
    df["change_date"].fillna("",inplace=True)
    df["change_date"] = df["change_date"].str.replace("']", "")
    df["change_date"] = pd.to_datetime(df["change_date"], errors="ignore")
    df['change_date'] = df['change_date'].dt.date


    df["change_date"].fillna("-", inplace=True)
    df["date"] = pd.to_datetime(df["date"], format="%d %B %Y", errors="coerce")
    df['date'] = df['date'].dt.date

    df.drop("change_lines", axis=1, inplace=True)
    df.to_excel("export_usaf_extraction.xlsx")

    print(df)

    print(f"\n ----------------------------------------------------------\n \
        PROCESS ENDED. {len(df)} FILES HAVE BEEN PROCESSED\n ----------------------------------------------------------")
