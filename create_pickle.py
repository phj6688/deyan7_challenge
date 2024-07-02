import os
import pickle
from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

client = OpenAI()
# Define the directory containing the PDF files
pdf_dir = 'data/knowledge_base'
file_paths = [os.path.join(pdf_dir, file) for file in os.listdir(pdf_dir) if file.endswith('.pdf')]

# Create a new vector store
vector_store = client.beta.vector_stores.create(name="Products Documentation")

# Read files from disk
file_streams = [open(path, "rb") for path in file_paths]

# Upload files to the vector store (openai server)
try:
    for file in tqdm(file_streams,desc='Uploading files'):
        file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id, files=[file]
    )
finally:
    # Ensure all files are closed after upload
    for file in file_streams:
        file.close()

# Save the vector store ID and paths to a pickle file
with open('vector_store.pkl', 'wb') as f:
    pickle.dump({'vector_store_id': vector_store.id, 'file_paths': file_paths}, f)
