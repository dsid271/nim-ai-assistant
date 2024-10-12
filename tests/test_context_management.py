import pytest
import numpy as np
from src.context_management import ContextTracker, VectorStore

def test_context_tracker():
    tracker = ContextTracker(max_history=3)
    
    tracker.add_interaction("Hello", "Hi there!")
    tracker.add_interaction("How are you?", "I'm doing well, thanks for asking!")
    tracker.add_interaction("What's the weather like?", "I'm sorry, I don't have real-time weather information.")
    
    context = tracker.get_context()
    assert len(context.split("\n")) == 6  # 3 interactions * 2 lines each
    
    # Test that the oldest interaction is removed when max_history is exceeded
    tracker.add_interaction("One more question", "Sure, go ahead!")
    context = tracker.get_context()
    assert "Hello" not in context
    assert "One more question" in context

def test_vector_store():
    vector_store = VectorStore(dimension=5)
    
    # Add some test data
    vector_store.add_text("Hello world", np.array([1, 2, 3, 4, 5]))
    vector_store.add_text("OpenAI GPT", np.array([2, 3, 4, 5, 6]))
    vector_store.add_text("Vector databases", np.array([3, 4, 5, 6, 7]))
    
    # Test search functionality
    query_vector = np.array([1, 2, 3, 4, 5])
    results = vector_store.search(query_vector, k=2)
    
    assert len(results) == 2
    assert results[0]["text"] == "Hello world"
    assert results[1]["text"] == "OpenAI GPT"
    
    # Test adding vector with wrong dimension
    with pytest.raises(ValueError):
        vector_store.add_text("Wrong dimension", np.array([1, 2, 3]))

def test_vector_store_empty_search():
    vector_store = VectorStore(dimension=3)
    
    # Search in an empty store
    query_vector = np.array([1, 2, 3])
    results = vector_store.search(query_vector, k=5)
    
    assert len(results) == 0

def test_vector_store_fewer_results():
    vector_store = VectorStore(dimension=3)
    
    vector_store.add_text("Text 1", np.array([1, 2, 3]))
    vector_store.add_text("Text 2", np.array([4, 5, 6]))
    
    query_vector = np.array([1, 2, 3])
    results = vector_store.search(query_vector, k=5)
    
    assert len(results) == 2  # Only 2 items in store, so should return 2 results even though k=5
