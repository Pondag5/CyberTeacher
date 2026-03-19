"""Тесты для модуля knowledge (RAG с reranking и BM25)"""

import unittest
from unittest.mock import patch, MagicMock

from knowledge import get_relevant_docs, get_knowledge_status


class TestGetRelevantDocs(unittest.TestCase):
    """Тесты гибридного поиска документов"""

    def test_get_relevant_docs_none_vectordb(self):
        results = get_relevant_docs(None, "query")
        self.assertEqual(results, [])

    @patch("knowledge._current_vectordb")
    @patch("knowledge.BM25_ENABLED", False)
    @patch("knowledge.RERANKER", False)
    def test_get_relevant_docs_simple(self, mock_vectordb):
        # Мокаем векторный поиск: возвращаем список Document-подобных объектов
        fake_doc1 = MagicMock()
        fake_doc1.page_content = "Content 1"
        fake_doc1.metadata = {"source": "doc1"}
        fake_doc2 = MagicMock()
        fake_doc2.page_content = "Content 2"
        fake_doc2.metadata = {"source": "doc2"}
        mock_vectordb.similarity_search.return_value = [fake_doc1, fake_doc2]

        results = get_relevant_docs(mock_vectordb, "query", k=1)
        self.assertGreaterEqual(len(results), 1)
        self.assertTrue(hasattr(results[0], "page_content"))

    @patch("knowledge._current_vectordb")
    def test_get_relevant_docs_empty_vector_results(self, mock_vectordb):
        mock_vectordb.similarity_search.return_value = []
        results = get_relevant_docs(mock_vectordb, "query", k=3)
        self.assertEqual(results, [])

    @patch("knowledge._current_vectordb")
    @patch("knowledge.RERANKER", False)
    def test_get_relevant_docs_respects_k(self, mock_vectordb):
        # Return many docs and ensure final slice uses k
        docs = []
        for i in range(10):
            d = MagicMock()
            d.page_content = f"doc{i}"
            d.metadata = {"source": f"doc{i}"}
            docs.append(d)
        mock_vectordb.similarity_search.return_value = docs

        results = get_relevant_docs(mock_vectordb, "query", k=3)
        self.assertEqual(len(results), 3)


class TestKnowledgeStatus(unittest.TestCase):
    def test_get_knowledge_status_returns_expected_keys(self):
        status = get_knowledge_status()
        self.assertIsInstance(status, dict)
        self.assertIn("files_on_disk", status)
        self.assertIn("files_in_db", status)
        self.assertIn("total_chunks", status)
        self.assertIn("list", status)


if __name__ == "__main__":
    unittest.main()
