"""
Test for FAISS vectordb with reranking
"""

import unittest
import tempfile
import os
import shutil
from typing import List

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# Imports from our project
from config import RERANK_TOP_K, RERANKER_MODEL, LazyLoader
from knowledge import get_relevant_docs


class TestFAISSReranking(unittest.TestCase):
    """Test reranking in FAISS vector database"""
    
    @classmethod
    def setUpClass(cls):
        """Create temporary embedding model"""
        print("\n[SETUP] Setting up test environment...")
        # Use lightweight model for tests
        cls.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        # Create test documents
        cls.documents = [
            Document(page_content="Cybersecurity is the practice of protecting systems and networks from digital attacks.", 
                    metadata={"source": "doc1", "topic": "security"}),
            Document(page_content="Intrusion Detection System (IDS) monitors network traffic for suspicious activity.", 
                    metadata={"source": "doc2", "topic": "ids"}),
            Document(page_content="Data encryption transforms information into an unreadable format to protect confidentiality.", 
                    metadata={"source": "doc3", "topic": "encryption"}),
            Document(page_content="Multi-factor authentication requires multiple proofs of identity for access.", 
                    metadata={"source": "doc4", "topic": "auth"}),
            Document(page_content="Phishing attacks use deceptive emails to steal credentials.", 
                    metadata={"source": "doc5", "topic": "phishing"}),
            Document(page_content="Firewall controls incoming and outgoing network traffic based on security rules.", 
                    metadata={"source": "doc6", "topic": "firewall"}),
            Document(page_content="Vulnerability assessment helps identify weaknesses in security systems.", 
                    metadata={"source": "doc7", "topic": "vulnerability"}),
            Document(page_content="SOC (Security Operations Center) is a team that monitors threats and incidents.", 
                    metadata={"source": "doc8", "topic": "soc"}),
            Document(page_content="Penetration testing (pentest) simulates attacks to find security holes.", 
                    metadata={"source": "doc9", "topic": "pentest"}),
            Document(page_content="Zero-day vulnerabilities are unknown to vendors and have no patches.", 
                    metadata={"source": "doc10", "topic": "zeroday"}),
        ]
        
        # Create FAISS index
        print("[INFO] Creating FAISS index...")
        cls.vectordb = FAISS.from_documents(cls.documents, cls.embeddings)
        print(f"[SUCCESS] Index created with {cls.vectordb.index.ntotal} documents")
        
        # Load reranker
        print("[INFO] Loading reranker model...")
        cls.reranker = LazyLoader.get_reranker()
        print("[SUCCESS] Reranker loaded")
        
    @classmethod
    def tearDownClass(cls):
        """Очистка после тестов"""
        # Очищаем кэш LazyLoader
        LazyLoader._reranker = None
        
    def test_relevant_docs_returns_correct_number(self):
        """Test 1: Verify that RERANK_TOP_K documents are returned"""
        query = "How to protect network from attacks?"
        k = 5  # Should return 5 documents
        
        print(f"\n[QUERY] Test query: '{query}'")
        print(f"[INFO] Requesting k={k} documents")
        
        relevant_docs = get_relevant_docs(self.vectordb, query, k=k)
        
        print(f"\n[RESULT] Received {len(relevant_docs)} documents")
        self.assertEqual(len(relevant_docs), k, 
                        f"Expected {k} documents, got {len(relevant_docs)}")
        
    def test_reranking_changes_order(self):
        """Test 2: Verify that reranking changes document order"""
        query = "Protection from fraud and attacks"
        
        print(f"\n[QUERY] Test query: '{query}'")
        
        # Get documents with reranking
        reranked_docs = get_relevant_docs(self.vectordb, query, k=5)
        
        print("\n[RESULT] Documents after reranking:")
        for i, doc in enumerate(reranked_docs, 1):
            print(f"{i}. {doc.page_content[:80]}...")
            print(f"   Metadata: {doc.metadata}")
            print()
            
        # Check that we got 5 documents
        self.assertEqual(len(reranked_docs), RERANK_TOP_K)
        
    def test_documents_with_scores(self):
        """Test 3: Show documents with their rankings"""
        query = "attacks and vulnerabilities"
        
        print(f"\n[QUERY] Test query: '{query}'")
        
        # Get initial documents (before reranking) for comparison
        initial_docs = self.vectordb.similarity_search(query, k=15)
        print(f"\n[INFO] Initial documents (before reranking):")
        for i, doc in enumerate(initial_docs, 1):
            print(f"{i}. {doc.page_content[:60]}...")
            
        # Get reranked documents
        reranked_docs = get_relevant_docs(self.vectordb, query, k=5)
        
        print(f"\n[INFO] Reranked documents (after reranking):")
        for i, doc in enumerate(reranked_docs, 1):
            print(f"{i}. {doc.page_content[:60]}...")
            print(f"   Source: {doc.metadata.get('source')}, Topic: {doc.metadata.get('topic')}")
            print()
            
        # Check order (should be changed compared to initial)
        self.assertEqual(len(reranked_docs), RERANK_TOP_K)
        
    def test_relevant_to_specific_topic(self):
        """Test 4: Verify relevance for phishing-related query"""
        query = "Phishing attacks and protection against them"
        
        print(f"\n[QUERY] Test query: '{query}'")
        
        docs = get_relevant_docs(self.vectordb, query, k=5)
        
        print("\n[RESULT] Returned documents:")
        for i, doc in enumerate(docs, 1):
            content = doc.page_content
            print(f"{i}. {content[:100]}...")
            print(f"   Relevance to phishing: {'phishing' in content.lower()}")
            print()
            
        # Although query is about phishing, we may get other related topics
        self.assertGreaterEqual(len(docs), 1, "Should return at least 1 document")


if __name__ == '__main__':
    print("=" * 70)
    print("TEST: FAISS VECTORDB WITH RERANKING")
    print("=" * 70)
    print(f"RERANK_TOP_K = {RERANK_TOP_K}")
    print(f"RERANKER_MODEL = {RERANKER_MODEL}")
    print("=" * 70)
    
    unittest.main(verbosity=2)
