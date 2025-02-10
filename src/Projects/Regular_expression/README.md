# Regular Expression Project
 
This project is designed to extract specific information from PDF files using regular expressions. The extracted information includes Corporate Identification Numbers (CIN), email addresses, phone numbers, Permanent Account Numbers (PAN), dates, and website URLs. The project is implemented in Python and uses asynchronous programming to handle PDF downloads and processing efficiently.
 
## Directory Structure
 
```
Regular_expression/
├── README.md
├── Docs/
│   └── Psedocode.txt
└── src/
    ├── main.py
    ├── download/
    ├── results/
    │   ├── airtel_data_results.txt
    │   └── tata_moters_results.txt
    └── utils/
        ├── download.py
        ├── extract.py
        ├── file_operations.py
        ├── __pycache__/
        └── early_refrences/
            ├── Optimized_regular_experssion.py
            └── main.py
```
 
## Files Description
 
### `README.md`
This file provides an overview of the project, its structure, and instructions on how to use it.
 
### `Docs/Psedocode.txt`
This file contains the pseudocode for the project, outlining the steps and logic used in the implementation.
 
### `src/main.py`
The main script that orchestrates the downloading and processing of PDF files. It uses asynchronous programming to handle multiple PDFs concurrently.
 
### `src/results/`
This directory contains the results of the extraction process. Each processed PDF file has a corresponding results file.
 
### `src/utils/`
This directory contains utility scripts that handle various tasks such as downloading PDFs, extracting text, and writing results to files.
 
#### `download.py`
Handles the asynchronous downloading of PDF files from specified URLs.
 
#### `extract.py`
Contains functions to extract text from PDFs and use regular expressions to find specific patterns (CIN, emails, phone numbers, PAN, dates, and websites).
 
#### `file_operations.py`
Manages the writing of extracted data to result files.
 
#### `early_refrences/`
Contains earlier versions and references of the main scripts, including an optimized version of the regular expression extraction logic.
 
## How to Use
 
1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd Regular_expression
   ```
 
2. **Install Dependencies:**
   Ensure you have Python installed, then install the required packages:
   ```bash
   pip install aiohttp aiofiles pypdf selenium webdriver-manager
   ```
 
3. **Run the Script:**
   Execute the main script to start the PDF processing:
   ```bash
   python src/main.py
   ```
 
4. **Provide PDF URLs:**
   The script will prompt you to enter PDF URLs one by one. After entering each URL, specify the desired filename for the downloaded PDF.
 
5. **View Results:**
   Once the processing is complete, the extracted data will be saved in the `results/` directory with filenames corresponding to the processed PDFs.
 
## Example Output
 
### `airtel_data_results.txt`
```
==================================================
📄 Processed File: airtel_data.pdf
==================================================
 
🔹 Cin (13 found):
   ➜ L74899HR1995PLC095967
   ➜ U72400TG2017PLC117649
   ➜ U32039HR1985PLC032091
   ➜ U64201DL1997PLC091001
   ➜ U74899DL1995PLC067527
   ➜ U32204DL2008PLC183976
   ➜ U92200DL2006PLC156075
   ➜ U65100DL2010PLC201058
   ➜ U64200HR2009PLC096372
   ➜ U72200DL2013PLC254747
   ➜ U74140HR2015PLC096027
   ➜ U64200HR2021PLC093754
   ➜ U93000HR2010PLC094599
 
🔹 Emails (1 found):
   ➜ compliance.officer@bharti.in
 
🔹 Phone Numbers (1 found):
   ➜ ('0', '', '1146666100')
 
🔹 Pan (1 found):
   ➜ AAACB2894G
 
🔹 Dates (4 found):
   ➜ 07/07/1995
   ➜ 01/04/2021
   ➜ 31/03/2022
   ➜ 31/08/2022
 
🔹 Websites (1 found):
   ➜ www.airtel.com
 
==================================================
✅ Extraction Completed Successfully
==================================================
```
 
### `tata_moters_results.txt`
```
==================================================
📄 Processed File: tata_moters.pdf
==================================================
 
🔹 Cin (23 found):
   ➜ L28920MH1945PLC004520
   ➜ U74999MH2018PTC307859
   ➜ U72100MH1972PLC015561
   ➜ U50300MH1997PLC149349
   ➜ U65923MH2006PLC162503
   ➜ U72200PN1994PLC013313
   ➜ U34101MH2006PLC164771
   ➜ U29309MH2019PLC328152
   ➜ U72900MH2020PLC339230
   ➜ U45200MH1989PLC050444
   ➜ U34200MH2012FLC237194
   ➜ U34102TZ2016PTC027770
   ➜ U50500MH2021PLC361754
   ➜ U34100MH2021PLC373648
   ➜ U65910MH1992PLC187184
   ➜ L35911GA1980PLC000400
   ➜ U85110KA1998PTC024588
   ➜ U29120MP1995PLC009773
   ➜ U34100PN1995PLC158999
   ➜ U34101PN1993PTC190262
   ➜ U28900PN1997PTC130940
   ➜ U93000KA2008PLC046588
   ➜ U74900KA2015PTC080558
 
🔹 Emails (1 found):
   ➜ inv_rel@tatamotors.com
 
🔹 Phone Numbers (1 found):
   ➜ ('0', '', '2266658282')
 
🔹 Pan (1 found):
   ➜ AAACT2727Q
 
🔹 Dates (4 found):
   ➜ 01/09/1945
   ➜ 01/04/2021
   ➜ 31/03/2022
   ➜ 31/08/2022
 
🔹 Websites (1 found):
   ➜ www.tatamotors.com
 
==================================================
✅ Extraction Completed Successfully
==================================================
```
 
## Dependencies
 
- Python 3.x
- `aiohttp`
- `aiofiles`
- `pypdf`
- `selenium`
- `webdriver-manager`
 

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the developers of `aiohttp`, `beautifulsoup4`, and other libraries used in this project.
- Inspired by the need for efficient web scraping tools for news aggregation.

## Contact

For any questions or suggestions, please contact me at  [https://github.com/jain-nikhilkumar].

