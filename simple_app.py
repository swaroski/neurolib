import streamlit as st
import json
import os

st.set_page_config(page_title="📚 BookNest - Simple", layout="wide")

st.title("📚 BookNest Library")
st.write("**Debug Version - Ensuring Books Load**")

# Debug info
st.write(f"**Current directory:** {os.getcwd()}")
st.write(f"**Files in directory:** {[f for f in os.listdir('.') if 'json' in f or 'py' in f]}")

# Force initialize if no data
if not os.path.exists('library_data.json'):
    st.error("❌ No library_data.json found. Initializing with sample books...")
    
    # Run initialization
    import subprocess
    import sys
    result = subprocess.run([sys.executable, "init_booknest.py"], capture_output=True, text=True)
    
    if result.returncode == 0:
        st.success("✅ Sample books created!")
    else:
        st.error(f"Failed to create sample books: {result.stderr}")

# Try to load books
try:
    with open('library_data.json', 'r') as f:
        data = json.load(f)
    
    books = data.get('books', [])
    
    st.success(f"✅ **Loaded {len(books)} books successfully!**")
    
    if books:
        # Show quick stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Books", len(books))
        with col2:
            borrowed = sum(1 for book in books if book.get('is_borrowed', False))
            st.metric("Borrowed", borrowed)
        with col3:
            genres = len(set(book.get('genre', 'Unknown') for book in books))
            st.metric("Genres", genres)
        
        st.subheader("📚 Your Library Collection")
        
        # Display books in a simple list
        for i, book in enumerate(books[:10]):  # Show first 10 books
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    # Status indicator
                    status = "🔴 BORROWED" if book.get('is_borrowed', False) else "🟢 AVAILABLE"
                    
                    st.write(f"**{i+1}. {book.get('title', 'No Title')}**")
                    st.write(f"by {book.get('author', 'Unknown Author')} | {book.get('genre', 'Unknown')} | {book.get('year', 'Unknown')}")
                    
                    if book.get('summary'):
                        st.write(f"*{book['summary'][:100]}...*")
                
                with col2:
                    st.write(status)
                    if book.get('is_borrowed') and book.get('borrower_name'):
                        st.write(f"Borrower: {book['borrower_name']}")
                
                st.divider()
        
        if len(books) > 10:
            st.info(f"Showing first 10 of {len(books)} books")
            
    else:
        st.error("❌ Books array is empty!")
        st.write("**Debug - Raw data structure:**")
        st.json(data)
        
except FileNotFoundError:
    st.error("❌ library_data.json still not found!")
    
except json.JSONDecodeError as e:
    st.error(f"❌ JSON parsing error: {e}")
    
except Exception as e:
    st.error(f"❌ Unexpected error: {e}")
    st.exception(e)

# Manual refresh button
if st.button("🔄 Reload Books"):
    st.rerun()