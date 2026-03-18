import unittest
from unittest.mock import MagicMock, patch

from handlers.summary import handle_summary


class TestSummary(unittest.TestCase):
    @patch("handlers.summary.input", create=True)
    @patch("config.LazyLoader")
    @patch("knowledge.get_relevant_docs")
    @patch("knowledge.get_current_vectordb")
    def test_handle_summary_success(
        self, mock_get_db, mock_get_docs, mock_lazy_loader, mock_input
    ):
        # Mock database and docs
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db

        mock_doc = MagicMock()
        mock_doc.page_content = "SQL injection is a web security vulnerability..."
        mock_get_docs.return_value = [mock_doc]

        # Mock LLM
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "## Summary of SQLi\nDefinition: ..."
        mock_llm.invoke.return_value = mock_response
        mock_lazy_loader.get_llm.return_value = mock_llm

        # Mock input (choose 'n')
        mock_input.return_value = "n"

        result = handle_summary("summary SQL injection")

        self.assertEqual(result, (True, None, None, True))
        mock_get_docs.assert_called()
        mock_llm.invoke.assert_called()

    @patch("knowledge.get_current_vectordb")
    def test_handle_summary_no_db(self, mock_get_db):
        mock_get_db.return_value = None
        result = handle_summary("summary Test")
        self.assertEqual(result, (True, None, None, True))

    @patch("knowledge.get_relevant_docs")
    @patch("knowledge.get_current_vectordb")
    def test_handle_summary_no_docs(self, mock_get_db, mock_get_docs):
        mock_get_db.return_value = MagicMock()
        mock_get_docs.return_value = []
        result = handle_summary("summary NonExistentTopic")
        self.assertEqual(result, (True, None, None, True))


if __name__ == "__main__":
    unittest.main()
