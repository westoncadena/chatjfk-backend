from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import os
import torch  # For GPU checking

# Load Markdown files
from load_markdown import load_markdown_files
from chunk_text import chunk_text

# Configurable batch size to reduce RAM usage
BATCH_SIZE = 16  

# Ensure 'embeddings/' directory exists
EMBEDDINGS_DIR = os.path.join(os.path.dirname(__file__), "../embeddings")
os.makedirs(EMBEDDINGS_DIR, exist_ok=True)

# Paths for storing embeddings
FAISS_INDEX_PATH = os.path.join(EMBEDDINGS_DIR, "jfk_index.faiss")
METADATA_PATH = os.path.join(EMBEDDINGS_DIR, "metadata.json")

# Check if CUDA (GPU) is available
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🔍 Using device: {device}")

# Load BGE-M3 model on GPU if available
model = SentenceTransformer("BAAI/bge-m3", device=device)

# Load documents
documents = load_markdown_files()
chunks = []
metadata = []

for doc in documents:
    text_chunks = chunk_text(doc["text"])
    for chunk in text_chunks:
        chunks.append(chunk)
        metadata.append({"filename": doc["filename"]})

print(f"📄 Loaded {len(chunks)} text chunks for embedding.")

# Initialize FAISS
dimension = model.get_sentence_embedding_dimension()
index = faiss.IndexFlatL2(dimension)

# Process embeddings in batches
for i in range(0, len(chunks), BATCH_SIZE):
    batch = chunks[i : i + BATCH_SIZE]
    
    print(f"🔄 Processing batch {i // BATCH_SIZE + 1} / {len(chunks) // BATCH_SIZE + 1} on {device}")

    # Encode batch to embeddings on the selected device
    batch_embeddings = model.encode(batch, convert_to_numpy=True)

    # Add batch to FAISS
    index.add(batch_embeddings)

# Save FAISS index to embeddings directory
faiss.write_index(index, FAISS_INDEX_PATH)

# Save metadata to embeddings directory
with open(METADATA_PATH, "w") as f:
    json.dump(metadata, f)

print(f"✅ Successfully indexed {len(chunks)} text chunks!")
print(f"📁 Embeddings saved in: {EMBEDDINGS_DIR}")
