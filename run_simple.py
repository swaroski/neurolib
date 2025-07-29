#!/usr/bin/env python3
"""
Simple launcher to test book loading
"""

import os
import sys
import subprocess

def main():
    print("🔍 Starting Simple BookNest (Debug Version)...")
    print("=" * 50)
    
    # Check current directory and files
    print(f"Current directory: {os.getcwd()}")
    
    if os.path.exists('library_data.json'):
        print("✅ library_data.json found")
        
        # Quick check of JSON content
        import json
        try:
            with open('library_data.json', 'r') as f:
                data = json.load(f)
            books = data.get('books', [])
            print(f"✅ JSON valid with {len(books)} books")
            
            if books:
                print(f"First book: {books[0]['title']} by {books[0]['author']}")
            else:
                print("❌ No books in JSON")
        except Exception as e:
            print(f"❌ JSON error: {e}")
    else:
        print("❌ library_data.json not found - will be created automatically")
    
    print("\n🚀 Starting simple app...")
    print("This version WILL show books if they exist!")
    print("Visit: http://localhost:8501")
    
    # Launch simple app
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "simple_app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Thanks for testing!")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()