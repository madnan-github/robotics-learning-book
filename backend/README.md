# Embedding Pipeline for Docusaurus Content

This project implements a pipeline that extracts text from Docusaurus URLs, generates embeddings using Cohere, and stores them in Qdrant for RAG-based retrieval.

## Overview

The embedding pipeline performs the following steps:
1. Crawls Docusaurus URLs to extract all accessible pages
2. Extracts clean text content from each page
3. Chunks the text appropriately for embedding generation
4. Generates embeddings using Cohere
5. Stores embeddings with metadata in Qdrant

## Setup

### Prerequisites

- Python 3.12+
- uv package manager

### Installation

1. Clone the repository
2. Navigate to the backend directory: `cd backend`
3. Install dependencies: `uv sync` (or `pip install -r requirements.txt`)

### Environment Variables

Create a `.env` file in the backend directory with the following variables:

```bash
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here  # if using Qdrant Cloud
```

You can use the `.env.example` file as a template.

## Usage

### Command Line Interface

The pipeline can be run directly from the command line:

```bash
python main.py --url "https://your-docusaurus-site.com" --chunk-size 1000 --overlap 100
```

#### Command Line Options

- `--url`: Target Docusaurus URL to process (default: https://robotics-learning-book79.vercel.app/)
- `--chunk-size`: Size of text chunks for embedding (default: 1000)
- `--overlap`: Overlap between chunks (default: 100)

### As a Module

You can also import and use the pipeline functions directly:

```python
from main import rag_embedding

# Process a specific URL with custom parameters
rag_embedding(
    target_url="https://your-docusaurus-site.com",
    chunk_size=1000,
    overlap=100
)
```

## Architecture

### Core Components

- `get_all_urls()`: Crawls Docusaurus site and extracts all accessible URLs
- `extract_text_from_url()`: Extracts clean text content from a single page
- `chunk_text()`: Splits text into appropriate sizes for embedding generation
- `embed()`: Generates embeddings using Cohere API
- `save_chunk_to_qdrant()`: Stores embeddings in Qdrant with metadata
- `rag_embedding()`: Orchestrates the complete pipeline flow

### Data Models

- `Document`: Represents extracted text content from a single URL
- `Chunk`: Represents a segment of text content for embedding
- `Embedding`: Vector representation of text content with metadata

## Configuration

The pipeline can be configured through command-line arguments or by modifying the default values in the `rag_embedding()` function.

## Testing

Run the unit tests using pytest:

```bash
cd backend
python -m pytest tests/test_pipeline.py -v
```

## Performance

The pipeline is designed to process at least 100 documents per hour with successful embedding generation and storage.

## Error Handling

The pipeline includes comprehensive error handling for:
- Network issues during URL crawling
- API rate limits from Cohere
- Qdrant storage operations
- Invalid or inaccessible URLs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

[Specify your license here]