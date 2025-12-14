# Research: Embedding Pipeline Implementation

## Overview
Research findings for implementing the embedding pipeline that extracts text from Docusaurus URLs, generates embeddings using Cohere, and stores them in Qdrant.

## Decision: Use backend folder with uv package management
**Rationale**: The constitution specifies using uv as the package manager for Python projects. Creating a backend folder follows the architectural pattern specified in the constitution with FastAPI and proper project structure.
**Alternatives considered**:
- Single script without package management (simpler but not maintainable)
- Poetry instead of uv (uv is specifically required by constitution)

## Decision: Cohere and Qdrant client setup
**Rationale**: Cohere provides high-quality text embeddings and has good Python SDK support. Qdrant is a modern vector database with excellent Python client support and performance characteristics suitable for RAG applications.
**Alternatives considered**:
- OpenAI embeddings instead of Cohere (Cohere was specifically requested)
- Pinecone instead of Qdrant (Qdrant was specifically requested and is open source)
- FAISS for local storage (Qdrant provides better scalability and API features)

## Decision: Single main.py file with specified functions
**Rationale**: User specifically requested implementation in a single file named main.py with the functions: get_all_urls, extract_text_from_url, chunk_text, embed, rag_embedding, save_chunk_to_qdrant, and main execution function.
**Alternatives considered**:
- Multi-module structure (more maintainable but against user requirements)

## Decision: Target URL https://robotics-learning-book79.vercel.app/
**Rationale**: User provided this specific URL as the deployment target for the text extraction.
**Alternatives considered**: N/A - this was explicitly provided by the user.

## Research: Docusaurus site crawling
**Findings**: Docusaurus sites typically have a predictable structure with navigation elements that need to be excluded from text extraction. The site structure can be crawled using requests and BeautifulSoup, with special attention to excluding headers, footers, and navigation elements.

## Research: Text cleaning for Docusaurus
**Findings**: Docusaurus sites use standard HTML structures with content in specific classes. Text extraction should focus on main content areas and exclude navigation, headers, and other non-content elements. Common selectors include elements with classes like "main-content", "doc-content", or "markdown".

## Research: Content chunking strategies
**Findings**: For embedding generation, content should be chunked to fit within Cohere's token limits (typically 512-1024 tokens). Overlapping chunks with some context retention often work better for RAG systems. Common approaches include semantic chunking or fixed-length chunking with overlap.

## Research: Qdrant vector storage
**Findings**: Qdrant supports metadata storage alongside vectors, which is essential for RAG systems. Collections can be created with specific vector dimensions matching Cohere's embedding size (typically 1024 dimensions for most Cohere models). Payloads can store document metadata like URL, title, and chunk index.

## Research: Error handling and rate limits
**Findings**: Both Cohere and Qdrant APIs have rate limits that need to be handled gracefully. Exponential backoff strategies work well. Connection pooling and batch operations can improve performance.

## Implementation approach
The pipeline will follow these steps:
1. Crawl the specified Docusaurus URL to extract all page URLs
2. Extract clean text content from each page
3. Chunk the text appropriately for embedding generation
4. Generate embeddings using Cohere
5. Store embeddings with metadata in Qdrant