#!/usr/bin/env python3
"""
Test Open Library API integration
"""

import requests
import json
from dataclasses import dataclass
from typing import List

@dataclass
class Book:
    id: str
    title: str
    author: str
    genre: str
    year: int
    isbn: str
    tags: List[str]
    cover_url: str = ""

def test_open_library_api():
    print("🌐 Testing Open Library API Integration...")
    print("=" * 50)
    
    # Test basic search
    try:
        print("1. Testing basic search...")
        url = "https://openlibrary.org/search.json"
        params = {
            'q': 'Harry Potter',
            'limit': 3,
            'fields': 'key,title,author_name,first_publish_year,isbn,subject,cover_i'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        books = data.get('docs', [])
        
        print(f"✅ Found {len(books)} books")
        
        for i, book in enumerate(books):
            title = book.get('title', 'Unknown')
            authors = book.get('author_name', ['Unknown'])
            year = book.get('first_publish_year', 'Unknown')
            cover_id = book.get('cover_i')
            
            print(f"  {i+1}. {title}")
            print(f"     by {', '.join(authors[:2])}")
            print(f"     Year: {year}")
            print(f"     Cover ID: {cover_id}")
            
            # Test cover URL
            if cover_id:
                cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
                print(f"     Cover URL: {cover_url}")
        
        print("\n2. Testing genre classification...")
        test_subjects = ['fiction', 'mystery', 'science fiction', 'romance', 'biography']
        
        for subject in test_subjects:
            genre = determine_genre([subject])
            print(f"  '{subject}' -> {genre}")
        
        print("\n✅ Open Library API integration working!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

def determine_genre(subjects):
    """Test genre determination logic"""
    subjects_lower = [s.lower() for s in subjects]
    
    genre_keywords = {
        'Fiction': ['fiction', 'novel', 'literature'],
        'Mystery': ['mystery', 'detective', 'crime', 'thriller'],
        'Sci-Fi': ['science fiction', 'sci-fi', 'fantasy', 'dystopian'],
        'Romance': ['romance', 'love story'],
        'Biography': ['biography', 'memoir', 'autobiography'],
        'History': ['history', 'historical'],
        'Science': ['science', 'technology', 'physics', 'biology'],
        'Self-Help': ['self-help', 'psychology', 'philosophy']
    }
    
    for genre, keywords in genre_keywords.items():
        if any(keyword in ' '.join(subjects_lower) for keyword in keywords):
            return genre
    
    return 'Fiction'

def test_popular_books():
    """Test importing some popular books"""
    print("\n3. Testing popular book imports...")
    
    popular_queries = ['1984 Orwell', 'Pride Prejudice Austen', 'Dune Herbert']
    
    for query in popular_queries:
        try:
            print(f"\nSearching for: {query}")
            url = "https://openlibrary.org/search.json"
            params = {
                'q': query,
                'limit': 1,
                'fields': 'key,title,author_name,first_publish_year,isbn,subject'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            books = data.get('docs', [])
            
            if books:
                book = books[0]
                title = book.get('title', 'Unknown')
                authors = book.get('author_name', ['Unknown'])
                year = book.get('first_publish_year', 'Unknown')
                
                print(f"  ✅ Found: {title} by {', '.join(authors[:2])} ({year})")
            else:
                print(f"  ❌ No results for {query}")
                
        except Exception as e:
            print(f"  ❌ Error searching {query}: {e}")

if __name__ == "__main__":
    success = test_open_library_api()
    
    if success:
        test_popular_books()
        print("\n🚀 Ready to launch BookNest with Open Library!")
        print("   Run: python run_api_version.py")
    else:
        print("\n❌ API integration needs debugging")