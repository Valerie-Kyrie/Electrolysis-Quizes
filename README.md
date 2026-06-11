# Electrolysis Quizes

A desktop quiz application for studying electrolysis concepts and chapter-based question sets.
Workbook: Milady: Elecytolysis and Hair Removal 1st Edition.

## Quick Start (Prebuilt Binaries)

Sorry, no Mac instructions, as I don't have a Mac available to test functionality on.

### Windows

1. Download the latest Windows ZIP release.
2. Create a new folder wherever you want to keep the program.
3. Copy the ZIP file into that folder.
4. Extract the ZIP file into the same folder.
5. Ensure the extracted files and folders remain together, including the `data` directory.
6. Run the executable.

### Linux

1. Download the latest Linux ZIP release.
2. Create a new folder wherever you want to keep the program.
3. Copy the ZIP file into that folder.
4. Extract the ZIP file into the same folder.
5. Ensure the extracted files and folders remain together, including the `data` directory.
6. Make the executable runnable if necessary:

```bash
chmod +x main
```

7. Run the program.

## Important

Do not move the executable away from the accompanying files and folders. The application requires the contents of the `data` directory, including the SQLite database.

---

## Manual Installation (Python)

### Requirements

* Python 3.11 or newer
* pip

### Clone the Repository

```bash
git clone https://github.com/Valerie-Kyrie/Electrolysis-Quizes.git
cd Electrolysis-Quizes
```

### Create a Virtual Environment

Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows:

```cmd
python -m venv .venv
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
python main.py
```

---

## Project Structure

```text
Electrolysis-Quizes/
├── data/
│   └── electrolysis.db
├── database/
├── gui/
├── main.py
└── requirements.txt
```

The `data/electrolysis.db` file contains the quiz database and must be present for the application to function correctly.
