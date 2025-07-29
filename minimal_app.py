import streamlit as st
import json

st.title("📚 Minimal BookNest Test")

# Direct path check
import os
current_dir = os.getcwd()
st.write(f"**Working directory:** {current_dir}")

files = os.listdir('.')
json_files = [f for f in files if f.endswith('.json')]
st.write(f"**JSON files found:** {json_files}")

# Try to read the file
if 'library_data.json' in json_files:
    st.success("✅ library_data.json found!")
    
    try:
        # Read file
        with open('library_data.json', 'r') as f:
            content = f.read()
        
        st.write(f"**File size:** {len(content)} characters")
        
        # Parse JSON
        data = json.loads(content)
        st.write(f"**JSON keys:** {list(data.keys())}")
        
        # Get books
        books = data.get('books', [])
        st.write(f"**Number of books:** {len(books)}")
        
        if books:
            st.success(f"🎉 SUCCESS! Found {len(books)} books!")
            
            # Show first 5 books
            st.subheader("First 5 Books:")
            for i, book in enumerate(books[:5]):
                st.write(f"**{i+1}. {book['title']}** by {book['author']}")
                st.write(f"   Genre: {book['genre']} | Year: {book['year']}")
                if book.get('summary'):
                    st.write(f"   Summary: {book['summary'][:100]}...")
                st.write("---")
                
        else:
            st.error("❌ Books array is empty!")
            st.write("**Data structure:**")
            st.json(data)
            
    except json.JSONDecodeError as e:
        st.error(f"❌ JSON parsing failed: {e}")
        st.write("**Raw file content (first 500 chars):**")
        with open('library_data.json', 'r') as f:
            st.code(f.read()[:500])
            
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
        
else:
    st.error("❌ library_data.json not found!")
    st.write("**Available files:**", files)
    
    # Try to create it
    if st.button("Create Sample Data"):
        sample_books = [
            {
                "id": "001",
                "title": "Test Book 1",
                "author": "Test Author",
                "genre": "Fiction",
                "year": 2023,
                "isbn": "123456789",
                "tags": ["test"],
                "is_borrowed": False,
                "borrower_name": "",
                "due_date": None,
                "summary": "This is a test book to verify the system works."
            },
            {
                "id": "002", 
                "title": "Test Book 2",
                "author": "Another Author",
                "genre": "Mystery",
                "year": 2023,
                "isbn": "987654321",
                "tags": ["test", "mystery"],
                "is_borrowed": True,
                "borrower_name": "John Doe",
                "due_date": "2024-01-01",
                "summary": "Another test book to verify borrowing works."
            }
        ]
        
        test_data = {
            "books": sample_books,
            "borrowing_history": []
        }
        
        with open('library_data.json', 'w') as f:
            json.dump(test_data, f, indent=2)
            
        st.success("✅ Created test data! Refresh the page.")
        st.rerun()