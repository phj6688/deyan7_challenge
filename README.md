# Product Documentation Assistant

This project implements a Product Documentation Assistant using OpenAI's API and vector search capabilities. It allows users to query product information from a collection of PDF documents.

## Solution Overview

The solution consists of three main components:

1. `create_pickle.py`: Uploads PDF files to OpenAI's vector store and saves the vector store ID.
2. `main.py`: Implements the question-answering system using the OpenAI Assistant API.
3. `eval.ipynb`: Evaluates the system's performance using predefined questions.

### How it works

1. PDF documents are uploaded and indexed in OpenAI's vector store.
2. User queries are processed by an AI assistant that searches the vector store for relevant information.
3. The assistant provides answers based on the retrieved information, with citations to source documents.

## Evaluation and Scaling

### Evaluation

The current evaluation uses cosine similarity between question and answer embeddings. To improve evaluation:

1. Implement hybrid search: Combine semantic search with keyword-based search for better accuracy.
2. Rerank top-k results: Use another model to rerank the top-k results based on keyword matching or other criteria.
3. Set a similarity threshold: Filter out low-confidence answers based on a predefined threshold.
4. Fact-checking: Compare the answer against the source document and the original query to ensure accuracy.
5. Question-answering validation: Generate follow-up questions based on the original query and answer to validate consistency.

### Scaling

The current approach using OpenAI's vector store can handle up to 5,000,000 tokens per file. For larger scale or more advanced features:

- Pgvector for PostgreSQL-based vector search.
- Elasticsearch for robust full-text search capabilities combined with vector search.
- Zilliz (built on Milvus) for high-performance vector search at scale.

ref: https://superlinked.com/vector-db-comparison


These solutions offer more flexibility and advanced features like hybrid search, which can be crucial for large-scale deployments.

## Setup and Usage

### Environment Setup

1. Create a virtual environment:
2. Install the required packages using the provided `requirements.txt` file.
3. Set up OpenAI API credentials and store them in a `.env` file.

### Running the Project

1. Prepare your PDF documents:
- Place your PDF files in the `data/knowledge_base` directory.
- Alternatively, update the `pdf_dir` path in `create_pickle.py` if your files are located elsewhere.

2. Create the vector store:
```bash
python create_pickle.py
```
It should take about a minute for the 21 PDFs in the `data/knowledge_base` directory.

3. Run the main script:
```bash
python main.py
```
The script will prompt you to enter a **question**. Type your question and press Enter to get the answer. (English or Deutsch)

4. (Optional) Run the evaluation notebook:
- Open `eval.ipynb` in Jupyter Notebook or JupyterLab.
- No need to run the cells, as the results are already included. You can run them to see the evaluation process.