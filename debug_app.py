import streamlit as st
import json
import os
from dataclasses import dataclass
from typing import List, Optional

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

def debug_library_loading():
    st.title("🔍 Debug Library Loading")
    
    # Check if file exists
    data_file = "library_data.json"
    
    if os.path.exists(data_file):
        st.success(f"✅ File {data_file} exists")
        
        try:
            with open(data_file, 'r') as f:
                data = json.load(f)
            
            st.success("✅ JSON loaded successfully")
            
            books_data = data.get('books', [])
            st.info(f"📚 Found {len(books_data)} books in JSON")
            
            if books_data:
                st.write("**First book data:**")
                st.json(books_data[0])
                
                # Try to create Book objects
                try:
                    books = [Book(**book) for book in books_data]
                    st.success(f"✅ Created {len(books)} Book objects")
                    
                    # Display first few books
                    st.write("**First 3 books as objects:**")
                    for i, book in enumerate(books[:3]):
                        st.write(f"{i+1}. **{book.title}** by {book.author} ({book.genre})")
                        if book.summary:
                            st.write(f"   Summary: {book.summary[:100]}...")
                        st.write(f"   Borrowed: {book.is_borrowed}")
                        
                except Exception as e:
                    st.error(f"❌ Error creating Book objects: {e}")
                    st.write("**Raw book data structure:**")
                    for key, value in books_data[0].items():
                        st.write(f"- {key}: {type(value)} = {value}")
            else:
                st.warning("⚠️ No books found in JSON data")
                st.write("**Full data structure:**")
                st.json(data)
                
        except json.JSONDecodeError as e:
            st.error(f"❌ JSON decode error: {e}")
        except Exception as e:
            st.error(f"❌ Error reading file: {e}")
    else:
        st.error(f"❌ File {data_file} does not exist")
        st.write("**Current directory contents:**")
        try:
            files = os.listdir('.')
            for file in files:
                st.write(f"- {file}")
        except Exception as e:
            st.error(f"Error listing files: {e}")
    
    # Debug session state
    st.write("---")
    st.write("**Session State Debug:**")
    for key, value in st.session_state.items():
        if hasattr(value, '__dict__'):
            st.write(f"- {key}: {type(value).__name__} object")
            if hasattr(value, 'books'):
                st.write(f"  - Has {len(value.books)} books")
        else:
            st.write(f"- {key}: {type(value).__name__} = {str(value)[:100]}")

if __name__ == "__main__":
    debug_library_loading()