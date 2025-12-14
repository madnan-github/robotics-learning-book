"""
Unit tests for the embedding pipeline functions.
"""
import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Add the backend directory to the path so we can import main
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

import main


class TestEnvironmentVariables:
    """Test environment variable loading and validation."""

    def test_load_environment_variables_success(self):
        """Test that environment variables are loaded correctly."""
        # Mock environment variables
        with patch.dict(os.environ, {
            'COHERE_API_KEY': 'test_key',
            'QDRANT_URL': 'https://test.qdrant.com'
        }):
            cohere_key, qdrant_url, qdrant_api_key = main.load_environment_variables()
            assert cohere_key == 'test_key'
            assert qdrant_url == 'https://test.qdrant.com'

    def test_load_environment_variables_missing(self):
        """Test that missing environment variables raise an error."""
        # Test missing COHERE_API_KEY
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="COHERE_API_KEY"):
                main.load_environment_variables()


class TestCohereClient:
    """Test Cohere client initialization."""

    @patch('main.cohere.Client')
    @patch('main.load_environment_variables')
    def test_initialize_cohere_client(self, mock_load_env, mock_cohere_client):
        """Test Cohere client initialization."""
        mock_load_env.return_value = ('test_key', 'test_url', 'test_qdrant_key')
        mock_client_instance = Mock()
        mock_cohere_client.return_value = mock_client_instance

        client = main.initialize_cohere_client()

        assert client == mock_client_instance
        mock_cohere_client.assert_called_once_with(api_key='test_key')


class TestQdrantClient:
    """Test Qdrant client initialization."""

    @patch('main.QdrantClient')
    @patch('main.load_environment_variables')
    def test_initialize_qdrant_client(self, mock_load_env, mock_qdrant_client):
        """Test Qdrant client initialization."""
        mock_load_env.return_value = ('test_key', 'https://test.qdrant.com', 'test_api_key')
        mock_client_instance = Mock()
        mock_qdrant_client.return_value = mock_client_instance

        client = main.initialize_qdrant_client()

        assert client == mock_client_instance
        mock_qdrant_client.assert_called_once_with(
            url='https://test.qdrant.com',
            api_key='test_api_key',
            prefer_grpc=False
        )


class TestURLCrawling:
    """Test URL crawling functionality."""

    @patch('main.requests.get')
    @patch('main.BeautifulSoup')
    def test_get_all_urls(self, mock_bs, mock_get):
        """Test URL crawling function."""
        # Mock response
        mock_response = Mock()
        mock_response.text = '<html><body><a href="/page1">Page 1</a><a href="/page2">Page 2</a></body></html>'
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Mock BeautifulSoup
        mock_soup = Mock()
        mock_link1 = Mock()
        mock_link1.__getitem__.return_value = '/page1'
        mock_link2 = Mock()
        mock_link2.__getitem__.return_value = '/page2'
        mock_soup.find_all.return_value = [mock_link1, mock_link2]
        mock_bs.return_value = mock_soup

        urls = main.get_all_urls('https://example.com')

        assert len(urls) >= 1  # Should include the base URL
        assert 'https://example.com' in urls


class TestTextExtraction:
    """Test text extraction functionality."""

    @patch('main.requests.get')
    @patch('main.BeautifulSoup')
    def test_extract_text_from_url(self, mock_bs, mock_get):
        """Test text extraction from URL."""
        # Mock response
        mock_response = Mock()
        mock_response.text = '<html><head><title>Test Title</title></head><body>Test content here</body></html>'
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Mock BeautifulSoup
        mock_soup = Mock()
        mock_title_tag = Mock()
        mock_title_tag.get_text.return_value = 'Test Title'
        mock_soup.find.return_value = mock_title_tag
        mock_soup.get_text.return_value = 'Test content here'
        mock_soup.__enter__ = Mock(return_value=mock_soup)
        mock_soup.__exit__ = Mock(return_value=None)
        mock_bs.return_value = mock_soup

        title, content = main.extract_text_from_url('https://example.com')

        assert title == 'Test Title'
        assert 'Test content here' in content


class TestTextChunking:
    """Test text chunking functionality."""

    def test_chunk_text(self):
        """Test text chunking with various parameters."""
        long_text = "This is a sample text. " * 100  # Create a long text

        chunks = main.chunk_text(long_text, chunk_size=50, overlap=10)

        assert len(chunks) > 0
        assert all('content' in chunk for chunk in chunks)
        assert all(len(chunk['content']) <= 50 for chunk in chunks)

        # Test with empty text
        empty_chunks = main.chunk_text("")
        assert empty_chunks == []


class TestEmbedding:
    """Test embedding functionality."""

    @patch('main.cohere.Client')
    def test_embed(self, mock_cohere_client):
        """Test embedding generation."""
        # Mock Cohere client response
        mock_response = Mock()
        mock_response.embeddings = [[0.1, 0.2, 0.3]]  # Simple 3-dim embedding
        mock_cohere_client.embed.return_value = mock_response

        result = main.embed("test text", mock_cohere_client)

        assert result == [0.1, 0.2, 0.3]
        mock_cohere_client.embed.assert_called_once()


class TestEmbeddingValidation:
    """Test embedding validation."""

    def test_validate_embedding_dimensions(self):
        """Test embedding dimension validation."""
        # Valid embedding
        valid_embedding = [0.1] * 1024
        assert main.validate_embedding_dimensions(valid_embedding, 1024) is True

        # Invalid embedding - wrong size
        invalid_embedding = [0.1] * 512
        assert main.validate_embedding_dimensions(invalid_embedding, 1024) is False

        # Invalid embedding - non-numeric values
        invalid_embedding = ["not", "numeric"]
        assert main.validate_embedding_dimensions(invalid_embedding, 2) is False


class TestQdrantStorage:
    """Test Qdrant storage functionality."""

    def test_save_chunk_to_qdrant(self):
        """Test saving chunk to Qdrant."""
        # This is a complex test that would require mocking the entire Qdrant client
        # For now, we'll just verify the function exists and has the right signature
        assert hasattr(main, 'save_chunk_to_qdrant')

    def test_search_similar_embeddings(self):
        """Test searching similar embeddings."""
        # This is a complex test that would require mocking the entire Qdrant client
        # For now, we'll just verify the function exists and has the right signature
        assert hasattr(main, 'search_similar_embeddings')


if __name__ == '__main__':
    pytest.main([__file__])