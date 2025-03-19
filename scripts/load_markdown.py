import os
import markdown_it

def load_markdown_files(directory="./documents"):
    """Load and extract text from all Markdown files in a directory."""
    md_parser = markdown_it.MarkdownIt()
    documents = []

    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                raw_text = file.read()
                parsed_text = md_parser.render(raw_text)  # Convert to plain text
                documents.append({"filename": filename, "text": parsed_text})

    return documents
