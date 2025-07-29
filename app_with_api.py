import streamlit as st
import pandas as pd
import json
import requests
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict
import google.generativeai as genai
import os
import base64
from io import BytesIO
import time

# Configure page with custom styling
st.set_page_config(
    page_title="📚 BookNest - AI Library Manager",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern UI (simplified for debugging)
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    .book-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
    }
    
    .book-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 0.5rem;
    }
    
    .book-author {
        color: #4a5568;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .book-meta {
        color: #718096;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    
    .status-available {
        background: #c6f6d5;
        color: #22543d;
        padding: 0.25rem 0.5rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .status-borrowed {
        background: #fed7d7;
        color: #742a2a;
        padding: 0.25rem 0.5rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

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
    cover_url: str = ""

class OpenLibraryAPI:
    """Interface to Open Library API"""
    
    def __init__(self):
        self.base_url = "https://openlibrary.org"
        self.covers_url = "https://covers.openlibrary.org/b"
    
    def search_books(self, query: str, limit: int = 10) -> List[Dict]:
        """Search for books using Open Library API"""
        try:
            url = f"{self.base_url}/search.json"
            params = {
                'q': query,
                'limit': limit,
                'fields': 'key,title,author_name,first_publish_year,isbn,subject,cover_i'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return data.get('docs', [])
            
        except Exception as e:
            st.error(f"Error searching Open Library: {e}")
            return []
    
    def get_book_details(self, work_key: str) -> Dict:
        """Get detailed book information"""
        try:
            # Remove /works/ prefix if present
            work_key = work_key.replace('/works/', '')
            url = f"{self.base_url}/works/{work_key}.json"
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            st.error(f"Error getting book details: {e}")
            return {}
    
    def get_cover_url(self, cover_id: int, size: str = "M") -> str:
        """Get book cover URL"""
        if cover_id:
            return f"{self.covers_url}/id/{cover_id}-{size}.jpg"
        return ""
    
    def convert_to_book(self, ol_book: Dict) -> Book:
        """Convert Open Library book data to our Book format"""
        try:
            # Extract basic info
            title = ol_book.get('title', 'Unknown Title')
            authors = ol_book.get('author_name', ['Unknown Author'])
            author = ', '.join(authors[:2])  # Take first 2 authors
            year = ol_book.get('first_publish_year', 2000)
            
            # Get ISBN
            isbns = ol_book.get('isbn', [])
            isbn = isbns[0] if isbns else f"OL-{ol_book.get('key', '').replace('/works/', '')}"
            
            # Get subjects for genre and tags
            subjects = ol_book.get('subject', [])
            genre = self._determine_genre(subjects)
            tags = subjects[:5]  # Take first 5 subjects as tags
            
            # Get cover URL
            cover_id = ol_book.get('cover_i')
            cover_url = self.get_cover_url(cover_id) if cover_id else ""
            
            # Generate unique ID
            book_id = f"OL-{hash(title + author) % 10000:04d}"
            
            return Book(
                id=book_id,
                title=title,
                author=author,
                genre=genre,
                year=int(year) if year else 2000,
                isbn=isbn,
                tags=tags,
                cover_url=cover_url
            )
            
        except Exception as e:
            st.error(f"Error converting book data: {e}")
            return None
    
    def _determine_genre(self, subjects: List[str]) -> str:
        """Determine genre from subjects"""
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
        
        return 'Fiction'  # Default genre

class LibraryManager:
    def __init__(self):
        self.data_file = "library_data.json"
        self.books = []
        self.borrowing_history = []
        self.load_data()
        
    def load_data(self):
        """Load data with better error handling"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data_dict = json.load(f)
                
                books_data = data_dict.get('books', [])
                self.books = []
                
                for book_data in books_data:
                    try:
                        # Ensure all required fields exist
                        if not all(key in book_data for key in ['id', 'title', 'author', 'genre', 'year', 'isbn', 'tags']):
                            st.warning(f"Skipping incomplete book: {book_data.get('title', 'Unknown')}")
                            continue
                        
                        # Add cover_url if missing
                        if 'cover_url' not in book_data:
                            book_data['cover_url'] = ""
                        
                        book = Book(**book_data)
                        self.books.append(book)
                        
                    except Exception as e:
                        st.error(f"Error loading book {book_data.get('title', 'Unknown')}: {e}")
                        continue
                
                self.borrowing_history = data_dict.get('borrowing_history', [])
                
                if self.books:
                    st.success(f"✅ Loaded {len(self.books)} books successfully!")
                else:
                    st.warning("⚠️ No valid books found in data file")
                    
            else:
                st.info("📚 No library data found. You can add books manually or import from Open Library.")
                self.books = []
                self.borrowing_history = []
                
        except Exception as e:
            st.error(f"❌ Error loading library data: {e}")
            self.books = []
            self.borrowing_history = []
            
    def save_data(self):
        """Save data with error handling"""
        try:
            data = {
                'books': [asdict(book) for book in self.books],
                'borrowing_history': self.borrowing_history
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            st.error(f"Error saving data: {e}")
    
    def add_book(self, book: Book):
        self.books.append(book)
        self.save_data()
    
    def update_book(self, book_id: str, updated_book: Book):
        for i, book in enumerate(self.books):
            if book.id == book_id:
                self.books[i] = updated_book
                break
        self.save_data()
    
    def delete_book(self, book_id: str):
        self.books = [book for book in self.books if book.id != book_id]
        self.save_data()

class AIAssistant:
    def __init__(self):
        # Configure Gemini AI
        if 'GOOGLE_API_KEY' in st.secrets:
            genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        elif 'GOOGLE_API_KEY' in os.environ:
            genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        else:
            st.warning("⚠️ Please set GOOGLE_API_KEY for AI features")
            self.model = None
    
    def generate_book_summary(self, title: str, author: str, genre: str, year: int = None) -> str:
        if not self.model:
            return "AI features require GOOGLE_API_KEY to be set."
        
        try:
            year_info = f" published in {year}" if year else ""
            prompt = f"""Generate a compelling 2-3 sentence summary for the book '{title}' by {author}{year_info} in the {genre} genre. 

Focus on:
- The main plot or central theme
- What makes this book noteworthy or appealing
- The book's impact or significance if it's well-known

Keep it engaging and informative for library users deciding whether to read it."""
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Could not generate summary: {str(e)}"

def render_book_card(book: Book, show_actions: bool = True):
    """Render a book card with improved styling"""
    
    # Status badge
    status_class = "status-borrowed" if book.is_borrowed else "status-available"
    status_text = "BORROWED" if book.is_borrowed else "AVAILABLE"
    
    # Book card HTML
    card_html = f"""
    <div class="book-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
            <div>
                <div class="book-title">{book.title}</div>
                <div class="book-author">by {book.author}</div>
                <div class="book-meta">
                    {book.genre} • {book.year} • ISBN: {book.isbn}
                </div>
                {f'<div style="margin-top: 0.5rem;">Tags: {", ".join(book.tags[:3])}</div>' if book.tags else ''}
                {f'<div style="margin-top: 0.5rem; font-style: italic;">{book.summary}</div>' if book.summary else ''}
                {f'<div style="margin-top: 0.5rem; color: #e53e3e;">Due: {book.due_date} | Borrower: {book.borrower_name}</div>' if book.is_borrowed else ''}
            </div>
            <span class="{status_class}">{status_text}</span>
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)
    
    if show_actions:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("📝 Edit", key=f"edit_{book.id}"):
                st.session_state[f"editing_{book.id}"] = True
        with col2:
            if st.button("🤖 AI Summary", key=f"summary_{book.id}"):
                if 'ai_assistant' in st.session_state:
                    with st.spinner("Generating summary..."):
                        summary = st.session_state.ai_assistant.generate_book_summary(
                            book.title, book.author, book.genre, book.year
                        )
                        book.summary = summary
                        st.session_state.library_manager.update_book(book.id, book)
                        st.success("Summary generated!")
                        st.rerun()
        with col3:
            if not book.is_borrowed:
                if st.button("📤 Check Out", key=f"checkout_{book.id}"):
                    st.session_state[f"checkout_{book.id}"] = True
        with col4:
            if st.button("🗑️ Delete", key=f"delete_{book.id}"):
                st.session_state.library_manager.delete_book(book.id)
                st.success("Book deleted!")
                st.rerun()

def main():
    st.title("🏠 BookNest - AI Library Manager")
    st.markdown("*Your intelligent library management system with Open Library integration*")
    
    # Initialize managers
    if 'library_manager' not in st.session_state:
        st.session_state.library_manager = LibraryManager()
    
    if 'ai_assistant' not in st.session_state:
        st.session_state.ai_assistant = AIAssistant()
    
    if 'ol_api' not in st.session_state:
        st.session_state.ol_api = OpenLibraryAPI()
    
    library_manager = st.session_state.library_manager
    ai_assistant = st.session_state.ai_assistant
    ol_api = st.session_state.ol_api
    
    # Stats dashboard
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Books", len(library_manager.books))
    with col2:
        borrowed = sum(1 for book in library_manager.books if book.is_borrowed)
        st.metric("Borrowed", borrowed)
    with col3:
        available = len(library_manager.books) - borrowed
        st.metric("Available", available)
    with col4:
        genres = len(set(book.genre for book in library_manager.books))
        st.metric("Genres", genres)
    
    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📚 My Library", "➕ Add Books", "🌐 Import from Open Library", "📊 Analytics"])
    
    with tab1:
        st.subheader("📚 Your Library Collection")
        
        if library_manager.books:
            # Search and filter
            col1, col2 = st.columns([3, 1])
            with col1:
                search_query = st.text_input("🔍 Search books...", placeholder="Title, author, or genre")
            with col2:
                filter_status = st.selectbox("Filter", ["All", "Available", "Borrowed"])
            
            # Apply filters
            filtered_books = library_manager.books
            
            if search_query:
                filtered_books = [
                    book for book in filtered_books
                    if (search_query.lower() in book.title.lower() or
                        search_query.lower() in book.author.lower() or
                        search_query.lower() in book.genre.lower())
                ]
            
            if filter_status == "Available":
                filtered_books = [book for book in filtered_books if not book.is_borrowed]
            elif filter_status == "Borrowed":
                filtered_books = [book for book in filtered_books if book.is_borrowed]
            
            st.write(f"Showing {len(filtered_books)} of {len(library_manager.books)} books")
            
            # Display books
            for book in filtered_books:
                render_book_card(book)
                
        else:
            st.info("📖 No books in your library yet. Add books manually or import from Open Library!")
    
    with tab2:
        st.subheader("➕ Add New Book")
        
        with st.form("add_book_form"):
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Title*")
                author = st.text_input("Author*")
                genre = st.selectbox("Genre*", [
                    "Fiction", "Non-Fiction", "Mystery", "Romance", "Sci-Fi", 
                    "Fantasy", "Biography", "History", "Science", "Self-Help"
                ])
            with col2:
                year = st.number_input("Year", min_value=1000, max_value=2024, value=2023)
                isbn = st.text_input("ISBN")
                tags = st.text_input("Tags (comma-separated)")
            
            generate_summary = st.checkbox("🤖 Generate AI summary")
            submitted = st.form_submit_button("➕ Add Book")
            
            if submitted and title and author and genre:
                book_id = f"{len(library_manager.books) + 1:04d}"
                tags_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
                
                summary = ""
                if generate_summary:
                    with st.spinner("Generating AI summary..."):
                        summary = ai_assistant.generate_book_summary(title, author, genre, year)
                
                new_book = Book(
                    id=book_id,
                    title=title,
                    author=author,
                    genre=genre,
                    year=year,
                    isbn=isbn,
                    tags=tags_list,
                    summary=summary
                )
                
                library_manager.add_book(new_book)
                st.success(f"✅ Added '{title}' to your library!")
                st.rerun()
    
    with tab3:
        st.subheader("🌐 Import Books from Open Library")
        st.write("Search and import books from the world's largest open book database!")
        
        # Search interface
        col1, col2 = st.columns([3, 1])
        with col1:
            search_query = st.text_input("Search Open Library", placeholder="e.g. 'Harry Potter', 'Isaac Asimov', 'science fiction'")
        with col2:
            search_limit = st.selectbox("Results", [5, 10, 20], index=1)
        
        if st.button("🔍 Search Open Library") and search_query:
            with st.spinner("Searching Open Library..."):
                results = ol_api.search_books(search_query, search_limit)
                st.session_state['search_results'] = results
        
        # Display search results
        if 'search_results' in st.session_state and st.session_state.search_results:
            st.write(f"Found {len(st.session_state.search_results)} results:")
            
            for i, result in enumerate(st.session_state.search_results):
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    
                    with col1:
                        title = result.get('title', 'Unknown Title')
                        authors = result.get('author_name', ['Unknown Author'])
                        author = ', '.join(authors[:2])
                        year = result.get('first_publish_year', 'Unknown')
                        subjects = result.get('subject', [])[:3]
                        
                        st.write(f"**{title}**")
                        st.write(f"by {author} ({year})")
                        if subjects:
                            st.write(f"Subjects: {', '.join(subjects)}")
                    
                    with col2:
                        if st.button("➕ Import", key=f"import_{i}"):
                            book = ol_api.convert_to_book(result)
                            if book:
                                # Generate unique ID for our system
                                book.id = f"{len(library_manager.books) + 1:04d}"
                                
                                # Generate AI summary if possible
                                if ai_assistant.model:
                                    with st.spinner("Generating AI summary..."):
                                        book.summary = ai_assistant.generate_book_summary(
                                            book.title, book.author, book.genre, book.year
                                        )
                                
                                library_manager.add_book(book)
                                st.success(f"✅ Imported '{book.title}'!")
                                st.rerun()
                            else:
                                st.error("Failed to import book")
                    
                    st.divider()
        
        # Quick import popular books
        st.write("---")
        st.write("**Quick Import Popular Books:**")
        
        popular_searches = [
            "Harry Potter series",
            "Lord of the Rings",
            "Agatha Christie",
            "Isaac Asimov Foundation",
            "George Orwell 1984"
        ]
        
        cols = st.columns(len(popular_searches))
        for i, search in enumerate(popular_searches):
            with cols[i]:
                if st.button(search, key=f"popular_{i}"):
                    with st.spinner(f"Importing {search}..."):
                        results = ol_api.search_books(search, 3)
                        imported = 0
                        for result in results:
                            book = ol_api.convert_to_book(result)
                            if book:
                                book.id = f"{len(library_manager.books) + 1:04d}"
                                if ai_assistant.model:
                                    book.summary = ai_assistant.generate_book_summary(
                                        book.title, book.author, book.genre, book.year
                                    )
                                library_manager.add_book(book)
                                imported += 1
                        
                        if imported > 0:
                            st.success(f"✅ Imported {imported} books!")
                            st.rerun()
                        else:
                            st.error("No books imported")
    
    with tab4:
        st.subheader("📊 Library Analytics")
        
        if library_manager.books:
            # Genre distribution
            genres = {}
            for book in library_manager.books:
                genres[book.genre] = genres.get(book.genre, 0) + 1
            
            if genres:
                st.write("**Genre Distribution:**")
                genre_df = pd.DataFrame(list(genres.items()), columns=['Genre', 'Count'])
                st.bar_chart(genre_df.set_index('Genre'))
            
            # Recent additions
            st.write("**Recent Additions:**")
            recent_books = library_manager.books[-5:]
            for book in reversed(recent_books):
                st.write(f"• **{book.title}** by {book.author} ({book.genre})")
                
        else:
            st.info("Add some books to see analytics!")

if __name__ == "__main__":
    main()