# Quickstart: Embedding Pipeline

## Overview
Quick setup guide to run the embedding pipeline that extracts text from Docusaurus URLs, generates embeddings using Cohere, and stores them in Qdrant.

## Prerequisites
- Python 3.12+
- uv package manager
- Cohere API key
- Qdrant instance (local or cloud)

## Setup

1. **Create the backend directory and initialize uv project:**
   ```bash
   mkdir backend
   cd backend
   uv init
   ```

2. **Install required dependencies:**
   ```bash
   uv add requests beautifulsoup4 cohere qdrant-client python-dotenv
   ```

3. **Set up environment variables:**
   Create a `.env` file with:
   ```
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_URL=your_qdrant_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here  # if using cloud
   ```

4. **Create the main.py file:**
   The pipeline implementation will be in a single file with these functions:
   - `get_all_urls(base_url)` - Crawl and extract all URLs from the Docusaurus site
   - `extract_text_from_url(url)` - Extract clean text content from a single URL
   - `chunk_text(text, chunk_size=1000, overlap=100)` - Split text into processable chunks
   - `embed(text)` - Generate embedding vector using Cohere
   - `rag_embedding()` - Main orchestration function
   - `save_chunk_to_qdrant(chunk_data, vector, metadata)` - Store in Qdrant
   - `main()` - Entry point function

## Running the Pipeline

1. **Execute the pipeline:**
   ```bash
   cd backend
   python main.py
   ```

2. **Monitor the process:**
   - The pipeline will crawl https://robotics-learning-book79.vercel.app/
   - Extract text from all pages
   - Generate embeddings using Cohere
   - Store vectors in Qdrant with metadata

## Configuration

The pipeline can be configured via environment variables:
- `COHERE_MODEL`: Cohere model to use (default: embed-multilingual-v2.0)
- `CHUNK_SIZE`: Size of text chunks (default: 1000 characters)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 100 characters)
- `QDRANT_COLLECTION`: Name of Qdrant collection (default: embeddings)

## Expected Output

After running, you should see:
- All URLs from the target site crawled and processed
- Embeddings stored in Qdrant collection
- Console output showing progress and statistics