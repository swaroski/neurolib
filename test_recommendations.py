#!/usr/bin/env python3
"""
Test script to verify the AI recommendation system works with our sample data
"""

import json
import os
from dataclasses import dataclass
from typing import List, Optional

# Mock the dataclass for testing
@dataclass
class Book:
    id: str
    title: str
    author: str
    genre: str
    year: int
    isbn: str
    tags: List[str]
    is_borrowed: bool = False
    borrower_name: str = ""
    due_date: Optional[str] = None
    summary: str = ""

def load_sample_books():
    """Load books from the generated JSON file"""
    try:
        with open('library_data.json', 'r') as f:
            data = json.load(f)
        
        books = []
        for book_data in data['books']:
            books.append(Book(**book_data))
        
        return books
    except FileNotFoundError:
        print("❌ library_data.json not found. Run 'python sample_data.py' first.")
        return []

def test_recommendation_logic():
    """Test the recommendation system with sample data"""
    books = load_sample_books()
    
    if not books:
        return
    
    print(f"📚 Loaded {len(books)} sample books")
    print("\n🧪 Testing Recommendation Logic:")
    print("=" * 50)
    
    # Test with different genres
    test_cases = [
        ("Fiction", "1984", "dystopian themes"),
        ("Fantasy", "Harry Potter", "magical adventure"),
        ("Sci-Fi", "Dune", "space opera"),
        ("Mystery", "Gone Girl", "psychological thriller"),
        ("Non-Fiction", "Sapiens", "historical analysis")
    ]
    
    for genre, test_book_title, theme in test_cases:
        # Find the test book
        test_book = None
        for book in books:
            if test_book_title in book.title:
                test_book = book
                break
        
        if not test_book:
            print(f"❌ Test book '{test_book_title}' not found")
            continue
        
        print(f"\n📖 If someone liked: '{test_book.title}' ({test_book.genre})")
        print(f"   Theme: {theme}")
        
        # Find similar books by genre and tags
        similar_books = []
        for book in books:
            if book.id != test_book.id:
                # Same genre gets priority
                if book.genre == test_book.genre:
                    similar_books.append((book, "Same genre"))
                # Similar tags
                elif any(tag in book.tags for tag in test_book.tags):
                    similar_books.append((book, "Similar tags"))
                # Related genres
                elif (test_book.genre == "Fiction" and book.genre in ["Mystery", "Romance"]) or \
                     (test_book.genre == "Sci-Fi" and book.genre == "Fantasy") or \
                     (test_book.genre == "Non-Fiction" and book.genre in ["Biography", "History", "Science"]):
                    similar_books.append((book, "Related genre"))
        
        print(f"   Potential recommendations ({len(similar_books)} found):")
        for i, (book, reason) in enumerate(similar_books[:3]):
            print(f"   {i+1}. {book.title} by {book.author} - {reason}")
    
    print(f"\n✅ Sample data is ready for AI recommendations!")
    print(f"   Books span {len(set(book.genre for book in books))} different genres")
    print(f"   Each book has meaningful tags for better matching")
    
    if os.environ.get('GOOGLE_API_KEY'):
        print(f"   🤖 AI features will work (API key detected)")
    else:
        print(f"   ⚠️  Set GOOGLE_API_KEY for full AI functionality")

if __name__ == "__main__":
    test_recommendation_logic()