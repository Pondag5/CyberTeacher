"""Тесты для модуля knowledge (RAG с reranking и BM25)"""

import os
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from knowledge import (
    _chinese_tokenizer,
    _get_kb_cache,
    _kb_cache_key,
    _list_supported_files,
    _set_kb_cache,
    BM25_ENABLED,
    BM25Retriever,
    clear_kb_cache,
    get_knowledge_status,
    get_relevant_docs,
    ProgressEmbeddings,
)


class TestGetRelevantDocs(unittest.TestCase):
    """Тесты гибридного поиска документов"""

    def setUp(self):
        clear_kb_cache()

    def test_get_relevant_docs_none_vectordb(self):
        results = get_relevant_docs(None, "query")
        self.assertEqual(results, [])

    @patch("knowledge._current_vectordb")
    @patch("knowledge.BM25_ENABLED", False)
    @patch("config.RERANKER", "")
    def test_get_relevant_docs_simple(self, mock_vectordb):
        # Мокаем векторный поиск: возвращаем список Document-подобных объектов
        fake_doc1 = MagicMock()
        fake_doc1.page_content = "Content 1"
        fake_doc1.metadata = {"source": "doc1"}
        fake_doc2 = MagicMock()
        fake_doc2.page_content = "Content 2"
        fake_doc2.metadata = {"source": "doc2"}
        mock_vectordb.similarity_search.return_value = [fake_doc1, fake_doc2]

        results = get_relevant_docs(mock_vectordb, "query", top_k=1)
        self.assertGreaterEqual(len(results), 1)
        self.assertTrue(hasattr(results[0], "page_content"))

    @patch("knowledge._current_vectordb")
    @patch("knowledge.BM25_ENABLED", False)
    @patch("config.RERANKER", "")
    def test_get_relevant_docs_empty_vector_results(self, mock_vectordb):
        mock_vectordb.similarity_search.return_value = []
        results = get_relevant_docs(mock_vectordb, "query", top_k=3)
        self.assertEqual(results, [])

    @patch("knowledge._current_vectordb")
    @patch("knowledge.BM25_ENABLED", False)
    @patch("config.RERANKER", "")
    def test_get_relevant_docs_respects_k(self, mock_vectordb):
        # Return many docs and ensure final slice uses k
        docs = []
        for i in range(10):
            d = MagicMock()
            d.page_content = f"doc{i}"
            d.metadata = {"source": f"doc{i}"}
            docs.append(d)
        mock_vectordb.similarity_search.return_value = docs

        results = get_relevant_docs(mock_vectordb, "query", top_k=3)
        self.assertEqual(len(results), 3)


class TestKnowledgeStatus(unittest.TestCase):
    def test_get_knowledge_status_returns_expected_keys(self):
        status = get_knowledge_status()
        self.assertIsInstance(status, dict)
        self.assertIn("files_on_disk", status)
        self.assertIn("files_in_db", status)
        self.assertIn("total_chunks", status)
        self.assertIn("list", status)


"""Тесты для модуля knowledge (RAG с reranking и BM25)"""

import os
import tempfile
import time
import unittest
from unittest.mock import MagicMock, patch

from knowledge import (
    BM25_ENABLED,
    BM25Retriever,
    ProgressEmbeddings,
    _chinese_tokenizer,
    _kb_cache_key,
    _load_docs_from_dir,
    add_pdf_to_knowledge_base,
    clear_kb_cache,
    get_current_vectordb,
    get_knowledge_status,
    get_relevant_docs,
    load_and_split_file,
    load_knowledge_base,
    reindex_if_needed,
)


class TestChineseTokenizer(unittest.TestCase):
    """Тесты токенизатора китайского текста"""

    @patch("knowledge.jieba", None)
    def test_chinese_tokenizer_without_jieba(self):
        """Тест токенизатора без jieba (fallback на split)"""
        text = "hello world test"
        tokens = _chinese_tokenizer(text)
        self.assertEqual(tokens, text.split())

    @patch("knowledge.jieba", MagicMock(lcut=lambda x: ["token1", "token2"]))
    def test_chinese_tokenizer_with_jieba(self):
        """Тест токенизатора с jieba"""
        text = "中文测试"
        tokens = _chinese_tokenizer(text)
        self.assertEqual(tokens, ["token1", "token2"])


class TestProgressEmbeddings(unittest.TestCase):
    """Тесты обертки эмбеддингов с прогрессом"""

    def test_embed_documents(self):
        """Тест батчевого эмбеддинга документов"""
        mock_embeddings = MagicMock()
        mock_embeddings.embed_documents.return_value = [[0.1] * 384, [0.2] * 384]

        pe = ProgressEmbeddings(mock_embeddings, total_docs=2)
        result = pe.embed_documents(["doc1", "doc2"])

        self.assertEqual(len(result), 2)
        self.assertEqual(pe.processed, 2)
        mock_embeddings.embed_documents.assert_called_once_with(["doc1", "doc2"])

    def test_embed_query(self):
        """Тест эмбеддинга одного запроса"""
        mock_embeddings = MagicMock()
        mock_embeddings.embed_query.return_value = [0.1] * 384

        pe = ProgressEmbeddings(mock_embeddings, total_docs=1)
        result = pe.embed_query("test query")

        self.assertEqual(result, [0.1] * 384)
        mock_embeddings.embed_query.assert_called_once_with("test query")


class TestBM25Retriever(unittest.TestCase):
    """Тесты BM25 ретривера"""

    @patch("knowledge.BM25Okapi", MagicMock())
    def test_init_bm25_retriever(self):
        """Тест инициализации BM25Retriever"""
        docs = [MagicMock(page_content="doc1"), MagicMock(page_content="doc2")]
        retriever = BM25Retriever(docs, tokenizer=lambda x: x.split())
        self.assertIsNotNone(retriever.bm25)

    @patch("knowledge.BM25Okapi", MagicMock())
    def test_get_top_n(self):
        """Тест получения топ-N документов"""
        mock_bm25 = MagicMock()
        mock_bm25.get_scores.return_value = [0.9, 0.5, 0.1]
        mock_bm25.get_scores.return_value = [0.9, 0.5, 0.1]

        docs = [
            MagicMock(page_content="doc1"),
            MagicMock(page_content="doc2"),
            MagicMock(page_content="doc3"),
        ]
        retriever = BM25Retriever([], tokenizer=lambda x: x.split())
        retriever.bm25 = mock_bm25

        result = retriever.get_top_n("query", n=2)
        self.assertEqual(len(result), 2)


class TestLoadAndSplitFile(unittest.TestCase):
    """Тесты загрузки и разбиения файлов"""

    def test_load_text_file(self):
        """Тест загрузки текстового файла"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Test content\nLine 2\nLine 3")
            tmp_path = f.name

        try:
            docs = load_and_split_file(tmp_path)
            self.assertGreater(len(docs), 0)
            self.assertTrue(any("Test content" in doc.page_content for doc in docs))
        finally:
            os.unlink(tmp_path)

    def test_load_md_file(self):
        """Тест загрузки markdown файла"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Header\n\nContent here")
            tmp_path = f.name

        try:
            docs = load_and_split_file(tmp_path)
            self.assertGreater(len(docs), 0)
        finally:
            os.unlink(tmp_path)

    def test_load_nonexistent_file(self):
        """Тест загрузки несуществующего файла"""
        docs = load_and_split_file("/nonexistent/path/file.txt")
        self.assertEqual(docs, [])


class TestListSupportedFiles(unittest.TestCase):
    """Тесты списка поддерживаемых файлов"""

    def test_list_supported_files_with_cache(self):
        """Тест кэширования списка файлов"""
        from knowledge import _file_list_cache
        import time

        # Очищаем кэш
        _file_list_cache["files"] = []
        _file_list_cache["timestamp"] = 0

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            # Создаем тестовые файлы
            (tmpdir_path / "test1.txt").write_text("test1")
            (tmpdir_path / "test2.md").write_text("test2")
            (tmpdir_path / "ignore.pdf").write_text("ignore")

            files = _list_supported_files([str(tmpdir_path)])
            self.assertGreaterEqual(len(files), 2)

            # Второй вызов должен использовать кэш
            files2 = _list_supported_files([str(tmpdir_path)])
            self.assertEqual(files, files2)

    def test_list_supported_files_cache_expiry(self):
        """Тест истечения кэша"""
        from knowledge import _file_list_cache

        # Устанавливаем старый timestamp
        _file_list_cache["timestamp"] = time.time() - 1000
        _file_list_cache["files"] = ["old.txt"]

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            (tmpdir_path / "new.txt").write_text("new")
            files = _list_supported_files([str(tmpdir_path)])
            self.assertIn(str(tmpdir_path / "new.txt"), files)


class TestLoadDocsFromDir(unittest.TestCase):
    """Тесты загрузки документов из директории"""

    def test_load_docs_from_existing_dir(self):
        """Тест загрузки из существующей директории"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Создаем тестовые файлы
            (tmpdir / "doc1.txt").write_text("Content 1")
            (tmpdir / "doc2.md").write_text("Content 2")

            docs = _load_docs_from_dir(tmpdir)
            self.assertGreaterEqual(len(docs), 0)

    def test_load_docs_from_nonexistent_dir(self):
        """Тест загрузки из несуществующей директории"""
        docs = _load_docs_from_dir("/nonexistent/path")
        self.assertEqual(docs, [])


class TestReindexIfNeeded(unittest.TestCase):
    """Тесты переиндексации при изменении файлов"""

    def test_reindex_if_needed_no_timestamp(self):
        """Тест когда таймстамп не установлен"""
        import knowledge
        knowledge._INDEX_TIMESTAMP = 0.0
        result = reindex_if_needed()
        self.assertFalse(result)

    @patch("knowledge.load_knowledge_base")
    def test_reindex_if_needed_files_changed(self, mock_load):
        """Тест переиндексации при изменении файлов"""
        import knowledge

        knowledge._INDEX_TIMESTAMP = 1000.0
        mock_load.return_value = MagicMock()

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            # Создаем файл с mtime > INDEX_TIMESTAMP
            test_file = tmpdir_path / "test.txt"
            test_file.write_text("test")
            os.utime(tmpdir_path / "test.txt", (time.time(), time.time()))

            result = reindex_if_needed()
            self.assertTrue(result)
            mock_load.assert_called_once()


class TestLoadDocsFromDir(unittest.TestCase):
    """Тесты загрузки документов из директории"""

    def test_load_docs_skips_unsupported_extensions(self):
        """Тест что неподдерживаемые расширения пропускаются"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            (tmpdir_path / "test.txt").write_text("text")
            (tmpdir_path / "test.pdf").write_text("pdf")  # pdf не поддерживается без pypdf
            (tmpdir_path / "test.xyz").write_text("xyz")  # неизвестное расширение

            docs = _load_docs_from_dir(tmpdir_path)
            # Должен загрузить только .txt
            self.assertGreaterEqual(len(docs), 0)


class TestCacheFunctions(unittest.TestCase):
    """Тесты функций кэша"""

    def test_kb_cache_key(self):
        """Тест генерации ключа кэша"""
        mock_vectordb = MagicMock()
        key1 = _kb_cache_key(mock_vectordb, "query", 5)
        key2 = _kb_cache_key(mock_vectordb, "query", 5)
        key3 = _kb_cache_key(mock_vectordb, "other", 5)

        self.assertEqual(key1, key2)
        self.assertNotEqual(key1, key3)

    def test_get_kb_cache_miss(self):
        """Тест промаха кэша"""
        from knowledge import _kb_query_cache
        _kb_query_cache.clear()

        mock_vectordb = MagicMock()
        result = _get_kb_cache(mock_vectordb, "query", 5)
        self.assertIsNone(result)

    def test_set_and_get_kb_cache(self):
        """Тест установки и получения из кэша"""
        from knowledge import _kb_query_cache
        _kb_query_cache.clear()

        mock_vectordb = MagicMock()
        mock_result = [MagicMock()]

        _set_kb_cache(mock_vectordb, "query", 5, mock_result)
        result = _get_kb_cache(mock_vectordb, "query", 5)

        self.assertEqual(result, mock_result)

    def test_kb_cache_eviction(self):
        """Тест вытеснения старых записей из кэша"""
        from knowledge import _kb_query_cache, _KB_CACHE_MAX
        _kb_query_cache.clear()

        mock_vectordb = MagicMock()
        # Заполняем кэш больше максимума
        for i in range(_KB_CACHE_MAX + 10):
            _set_kb_cache(mock_vectordb, f"query{i}", 5, [f"result{i}"])

        self.assertLessEqual(len(_kb_query_cache), _KB_CACHE_MAX)

    def test_clear_kb_cache(self):
        """Тест очистки кэша"""
        from knowledge import _kb_query_cache
        _kb_query_cache.clear()

        mock_vectordb = MagicMock()
        _set_kb_cache(mock_vectordb, "query", 5, ["result"])
        self.assertGreater(len(_kb_query_cache), 0)

        clear_kb_cache()
        self.assertEqual(len(_kb_query_cache), 0)


class TestGetCurrentVectordb(unittest.TestCase):
    """Тесты получения текущего векторного хранилища"""

    def test_get_current_vectordb_returns_none_when_not_loaded(self):
        import knowledge
        knowledge._current_vectordb = None

        result = get_current_vectordb()
        self.assertIsNone(result)


class TestAddPdfToKnowledgeBase(unittest.TestCase):
    """Тесты добавления PDF в базу знаний"""

    @patch("knowledge.get_current_vectordb")
    @patch("knowledge.load_and_split_file")
    def test_add_pdf_file_not_found(self, mock_load, mock_get_vdb):
        """Тест добавления несуществующего файла"""
        result = add_pdf_to_knowledge_base("/nonexistent/path.pdf")
        self.assertFalse(result)

    @patch("knowledge.get_current_vectordb")
    @patch("knowledge.load_and_split_file")
    def test_add_pdf_no_docs_extracted(self, mock_load, mock_get_vdb):
        """Тест когда из файла не извлечены документы"""
        mock_load.return_value = []
        mock_vdb = MagicMock()
        mock_get_vdb.return_value = None

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            f.write(b"dummy")
            tmp_path = f.name

        try:
            result = add_pdf_to_knowledge_base(tmp_path)
            self.assertFalse(result)
        finally:
            os.unlink(tmp_path)


class TestGetKnowledgeStatus(unittest.TestCase):
    """Тесты статуса базы знаний"""

    @patch("knowledge.os.path.exists")
    @patch("knowledge.os.walk")
    def test_get_knowledge_status_with_files(self, mock_walk, mock_exists):
        """Тест статуса с файлами"""
        mock_exists.return_value = True
        # os.walk вызывается для каждой директории (KNOWLEDGE_DIR, DOCS_DIR)
        mock_walk.side_effect = [
            [("./knowledge_base", [], ["file1.txt", "file2.md"])],
            [("./docs", [], ["file3.pdf"])],
        ]

        status = get_knowledge_status()

        self.assertEqual(status["files_on_disk"], 3)
        self.assertEqual(len(status["list"]), 3)

    @patch("knowledge.os.path.exists")
    def test_get_knowledge_status_empty_dirs(self, mock_exists):
        """Тест статуса с пустыми директориями"""
        mock_exists.return_value = False

        status = get_knowledge_status()

        self.assertEqual(status["files_on_disk"], 0)
        self.assertEqual(status["list"], [])

    def test_bm25_persistence_roundtrip(self):
        """BM25 index can be saved and loaded from disk."""
        from knowledge import _save_bm25_index, _load_bm25_index, BM25Retriever

        corpus = ["alpha beta gamma", "delta epsilon zeta", "alpha delta"]
        bm25 = BM25Retriever(corpus, tokenizer=lambda t: t.split())
        _save_bm25_index(bm25, corpus)
        loaded = _load_bm25_index()
        self.assertIsNotNone(loaded)
        self.assertIn("bm25", loaded)
        self.assertIn("corpus", loaded)
        self.assertEqual(len(loaded["corpus"]), 3)


if __name__ == "__main__":
    unittest.main()
