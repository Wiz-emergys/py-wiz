import os

results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results')
os.makedirs(results_dir, exist_ok=True)

def write_results_to_file(pdf_path, results):
    """
    Writes extracted data to a formatted text file.

    Args:
        pdf_path (str): The path of the processed PDF file.
        results (dict): A dictionary containing extracted CINs, emails, phone numbers, PANs, dates, and websites.
    """    
    filename = os.path.basename(pdf_path).replace('.pdf', '_results.txt')
    result_file_path = os.path.join(results_dir, filename)

    with open(result_file_path, 'w', encoding='utf-8') as f:
        f.write(f"\n{'='*50}\n")
        f.write(f"🗄  Processed File: {os.path.basename(pdf_path)}\n")
        f.write(f"{'='*50}\n\n")

        for key, values in results.items():
            formatted_key = key.replace("_", " ").title()
            f.write(f"{formatted_key} ({len(values)} found):\n")
            if values:
                for value in values:
                    f.write(f"➜ {value}\n")
            else:
                f.write("❌ No data found\n")
            f.write("\n")
        
        f.write(f"{'='*50}\n")
        f.write(f"✅ Extraction Completed Successfully\n")
        f.write(f"{'='*50}\n")

    print(f"📂 Results saved to: {result_file_path}\n")
