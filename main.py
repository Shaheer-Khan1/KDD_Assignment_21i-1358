from flask import Flask, render_template, request, redirect, url_for
import csv
from datasets import load_dataset

app = Flask(__name__)

# Load the dataset initially (placeholder for now)
ds = load_dataset("ccdv/pubmed-summarization", "document")  # or "section"

# Path to the CSV file for storing user entries
CSV_FILE = 'user_entries.csv'

# Initialize an empty list to hold user-added entries
user_entries = []

# Function to load existing user entries from CSV into a list
def load_user_entries():
    entries = []
    try:
        with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) >= 3:
                    entry = {
                        'article': row[0].strip() if row[0].strip() else "",
                        'abstract': row[1].strip() if row[1].strip() else "",
                        'section_names': row[2].strip() if row[2].strip() else ""
                    }
                    entries.append(entry)
                else:
                    print(f"Skipping incomplete row: {row}")
    except FileNotFoundError:
        print(f"CSV file '{CSV_FILE}' not found.")
    except Exception as e:
        print(f"Error reading CSV file '{CSV_FILE}': {str(e)}")
    
    print(f"Loaded entries: {entries}")  # Debug print
    
    return entries

# Function to save new user entry to the CSV file
def save_user_entry(entry):
    fieldnames = ['article', 'abstract', 'section_names']
    try:
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(entry)
    except FileNotFoundError:
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(entry)

# Load existing user entries from CSV into user_entries list
user_entries = load_user_entries()

# Route for rendering the homepage with just a greeting
@app.route('/')
def index():
    return render_template('index.html')

# Route for rendering add_entry.html and handling form submission
@app.route('/add_entry', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        article = request.form['article'].strip()
        abstract = request.form['abstract'].strip()
        section_names = request.form['section_names'].strip()
        
        new_entry = {
            'article': article,
            'abstract': abstract,
            'section_names': section_names
        }
        
        user_entries.append(new_entry)
        save_user_entry(new_entry)
        
        return redirect(url_for('index'))
    
    return render_template('add_entry.html', user_entries=user_entries)

# Route for rendering pubmed_articles.html
@app.route('/pubmed_articles')
def pubmed_articles():
    if 'train' in ds:
        first_entry = ds['train'][0]
    else:
        first_entry = {'article': '', 'abstract': '', 'section_names': ''}
    
    return render_template('pubmed_articles.html', data=first_entry)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
