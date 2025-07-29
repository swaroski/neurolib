#!/usr/bin/env python3
"""
Quick script to check BookNest library contents
"""

import json
from datetime import datetime

def check_library():
    try:
        with open('library_data.json', 'r') as f:
            data = json.load(f)
        
        books = data.get('books', [])
        history = data.get('borrowing_history', [])
        
        print("🏠 BookNest Library Status")
        print("=" * 50)
        print(f"📚 Total Books: {len(books)}")
        print(f"📋 History Entries: {len(history)}")
        
        # Count by genre
        genres = {}
        borrowed_count = 0
        overdue_count = 0
        with_summaries = 0
        
        for book in books:
            genre = book.get('genre', 'Unknown')
            genres[genre] = genres.get(genre, 0) + 1
            
            if book.get('is_borrowed', False):
                borrowed_count += 1
                due_date = book.get('due_date')
                if due_date and datetime.strptime(due_date, "%Y-%m-%d") < datetime.now():
                    overdue_count += 1
            
            if book.get('summary', '').strip():
                with_summaries += 1
        
        print(f"🔴 Currently Borrowed: {borrowed_count}")
        print(f"⚠️  Overdue Books: {overdue_count}")
        print(f"📝 Books with Summaries: {with_summaries}")
        
        print(f"\n📊 Genre Distribution:")
        for genre, count in sorted(genres.items()):
            print(f"  • {genre}: {count} books")
        
        print(f"\n📚 Sample Books:")
        for i, book in enumerate(books[:5]):
            status = "🔴 BORROWED" if book.get('is_borrowed') else "🟢 AVAILABLE"
            summary_status = "✅" if book.get('summary', '').strip() else "❌"
            print(f"  {i+1}. {book['title']} by {book['author']} {status} Summary:{summary_status}")
        
        if len(books) > 5:
            print(f"  ... and {len(books) - 5} more books!")
        
        print(f"\n🚀 BookNest is ready with {len(books)} books!")
        print("   Run: python run_enhanced.py")
        
    except FileNotFoundError:
        print("❌ library_data.json not found!")
        print("   Run: python init_booknest.py")
    except Exception as e:
        print(f"❌ Error reading library data: {e}")

if __name__ == "__main__":
    check_library()