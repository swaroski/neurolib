import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict
import google.generativeai as genai
import os
import base64
from io import BytesIO

# Configure page with custom styling
st.set_page_config(
    page_title="📚 BookNest - AI Library Manager",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom color scheme */
    :root {
        --primary-color: #2E86AB;
        --secondary-color: #A23B72;
        --accent-color: #F18F01;
        --success-color: #C73E1D;
        --background-light: #F5F7FA;
        --text-dark: #2D3748;
        --border-color: #E2E8F0;
    }
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(46, 134, 171, 0.2);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0.5rem 0 0 0;
    }
    
    /* Navigation tabs */
    .nav-tabs {
        display: flex;
        gap: 1rem;
        margin-bottom: 2rem;
        flex-wrap: wrap;
    }
    
    .nav-tab {
        background: white;
        border: 2px solid var(--border-color);
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        color: var(--text-dark);
        text-decoration: none;
        transition: all 0.3s ease;
        cursor: pointer;
        flex: 1;
        text-align: center;
        min-width: 150px;
    }
    
    .nav-tab:hover {
        border-color: var(--primary-color);
        background: var(--primary-color);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(46, 134, 171, 0.2);
    }
    
    .nav-tab.active {
        background: var(--primary-color);
        border-color: var(--primary-color);
        color: white;
        box-shadow: 0 4px 12px rgba(46, 134, 171, 0.3);
    }
    
    /* Book card styling */
    .book-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .book-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
        border-color: var(--primary-color);
    }
    
    .book-cover {
        width: 80px;
        height: 120px;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 0.8rem;
        text-align: center;
        margin-right: 1rem;
        flex-shrink: 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    .book-info {
        flex: 1;
    }
    
    .book-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: var(--text-dark);
        margin-bottom: 0.5rem;
        line-height: 1.3;
    }
    
    .book-author {
        color: var(--secondary-color);
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .book-meta {
        color: #718096;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    
    .book-summary {
        color: var(--text-dark);
        font-size: 0.9rem;
        line-height: 1.5;
        margin-top: 0.5rem;
    }
    
    /* Status badges */
    .status-badge {
        position: absolute;
        top: 1rem;
        right: 1rem;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-available {
        background: #C6F6D5;
        color: #22543D;
        border: 1px solid #9AE6B4;
    }
    
    .status-borrowed {
        background: #FED7D7;
        color: #742A2A;
        border: 1px solid #FC8181;
    }
    
    .status-overdue {
        background: #FFEAA7;
        color: #8B4513;
        border: 1px solid #FDCB6E;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    /* Action buttons */
    .action-buttons {
        display: flex;
        gap: 0.5rem;
        margin-top: 1rem;
        flex-wrap: wrap;
    }
    
    .btn {
        padding: 0.5rem 1rem;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.9rem;
    }
    
    .btn-primary {
        background: var(--primary-color);
        color: white;
    }
    
    .btn-primary:hover {
        background: #2A7A9B;
        transform: translateY(-1px);
    }
    
    .btn-secondary {
        background: var(--background-light);
        color: var(--text-dark);
        border: 1px solid var(--border-color);
    }
    
    .btn-secondary:hover {
        background: var(--border-color);
    }
    
    .btn-success {
        background: #48BB78;
        color: white;
    }
    
    .btn-warning {
        background: var(--accent-color);
        color: white;
    }
    
    .btn-danger {
        background: var(--success-color);
        color: white;
    }
    
    /* Stats cards */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid var(--border-color);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary-color);
        line-height: 1;
    }
    
    .stat-label {
        color: #718096;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    /* Search and filters */
    .search-section {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid var(--border-color);
    }
    
    /* AI Chat Interface */
    .ai-chat-button {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, var(--accent-color), var(--secondary-color));
        border-radius: 50%;
        border: none;
        color: white;
        font-size: 1.5rem;
        cursor: pointer;
        box-shadow: 0 8px 32px rgba(241, 143, 1, 0.3);
        transition: all 0.3s ease;
        z-index: 1000;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .ai-chat-button:hover {
        transform: scale(1.1);
        box-shadow: 0 12px 40px rgba(241, 143, 1, 0.4);
    }
    
    .ai-chat-panel {
        position: fixed;
        bottom: 6rem;
        right: 2rem;
        width: 350px;
        height: 400px;
        background: white;
        border-radius: 16px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
        border: 1px solid var(--border-color);
        z-index: 1000;
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }
    
    .ai-chat-header {
        background: linear-gradient(135deg, var(--accent-color), var(--secondary-color));
        color: white;
        padding: 1rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .ai-chat-content {
        flex: 1;
        padding: 1rem;
        overflow-y: auto;
    }
    
    /* Toast notifications */
    .toast {
        position: fixed;
        top: 2rem;
        right: 2rem;
        background: white;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
        border-left: 4px solid var(--primary-color);
        z-index: 1001;
        animation: slideIn 0.3s ease;
    }
    
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .toast-success {
        border-left-color: #48BB78;
    }
    
    .toast-error {
        border-left-color: var(--success-color);
    }
    
    .toast-warning {
        border-left-color: var(--accent-color);
    }
    
    /* Genre tags */
    .genre-tags {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin-top: 0.5rem;
    }
    
    .genre-tag {
        background: var(--background-light);
        color: var(--text-dark);
        padding: 0.25rem 0.75rem;
        border-radius: 16px;
        font-size: 0.8rem;
        border: 1px solid var(--border-color);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .book-card {
            padding: 1rem;
        }
        
        .book-cover {
            width: 60px;
            height: 90px;
            font-size: 0.7rem;
        }
        
        .main-header h1 {
            font-size: 2rem;
        }
        
        .nav-tabs {
            flex-direction: column;
        }
        
        .ai-chat-panel {
            width: calc(100vw - 2rem);
            right: 1rem;
        }
        
        .stats-grid {
            grid-template-columns: repeat(2, 1fr);
        }
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

@dataclass
class LibraryData:
    books: List[Book]
    borrowing_history: List[Dict]

class LibraryManager:
    def __init__(self):
        self.data_file = "library_data.json"
        self.load_data()
        
    def load_data(self):
        try:
            with open(self.data_file, 'r') as f:
                data_dict = json.load(f)
                books_data = data_dict.get('books', [])
                self.books = [Book(**book) for book in books_data]
                self.borrowing_history = data_dict.get('borrowing_history', [])
        except FileNotFoundError:
            self.books = []
            self.borrowing_history = []
            
    def save_data(self):
        data = {
            'books': [asdict(book) for book in self.books],
            'borrowing_history': self.borrowing_history
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
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
    
    def check_out_book(self, book_id: str, borrower_name: str, days: int = 14):
        for book in self.books:
            if book.id == book_id:
                book.is_borrowed = True
                book.borrower_name = borrower_name
                book.due_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
                
                self.borrowing_history.append({
                    'book_id': book_id,
                    'book_title': book.title,
                    'borrower_name': borrower_name,
                    'checkout_date': datetime.now().strftime("%Y-%m-%d"),
                    'due_date': book.due_date,
                    'action': 'checkout'
                })
                break
        self.save_data()
    
    def check_in_book(self, book_id: str):
        for book in self.books:
            if book.id == book_id:
                book.is_borrowed = False
                borrower_name = book.borrower_name
                book.borrower_name = ""
                book.due_date = None
                
                self.borrowing_history.append({
                    'book_id': book_id,
                    'book_title': book.title,
                    'borrower_name': borrower_name,
                    'return_date': datetime.now().strftime("%Y-%m-%d"),
                    'action': 'checkin'
                })
                break
        self.save_data()

class AIAssistant:
    def __init__(self):
        # Configure Gemini AI
        if 'GOOGLE_API_KEY' in st.secrets:
            genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])
        elif 'GOOGLE_API_KEY' in os.environ:
            genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
        else:
            st.warning("Please set GOOGLE_API_KEY in secrets or environment variables")
            return
            
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def generate_book_summary(self, title: str, author: str, genre: str, year: int = None) -> str:
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
    
    def get_reading_recommendations(self, books: List[Book], current_book: Book) -> List[str]:
        try:
            # Filter out the current book and create a comprehensive list
            other_books = [book for book in books if book.id != current_book.id]
            
            # Include more books and better formatting
            book_list = "\n".join([
                f"- {book.title} by {book.author} | Genre: {book.genre} | Tags: {', '.join(book.tags) if book.tags else 'None'}"
                for book in other_books[:20]  # Show up to 20 books for better recommendations
            ])
            
            prompt = f"""Based on this library collection:
{book_list}

A reader just finished and enjoyed: '{current_book.title}' by {current_book.author}
- Genre: {current_book.genre}
- Tags: {', '.join(current_book.tags) if current_book.tags else 'None'}
- Summary: {current_book.summary[:100] if current_book.summary else 'No summary available'}

Please recommend exactly 3 books from the above collection that this reader would likely enjoy next. For each recommendation:
1. State the book title and author clearly
2. Explain in 1-2 sentences why it's similar or would appeal to someone who liked the reference book
3. Mention specific themes, genres, or elements that connect them

Format your response as:
**Book Title** by Author Name
Explanation here.

**Book Title** by Author Name  
Explanation here.

**Book Title** by Author Name
Explanation here."""
            
            response = self.model.generate_content(prompt)
            return [line.strip() for line in response.text.strip().split('\n') if line.strip()]
        except Exception as e:
            return [f"Could not generate recommendations: {str(e)}"]
    
    def get_library_insights(self, books: List[Book]) -> str:
        try:
            genre_counts = {}
            for book in books:
                genre_counts[book.genre] = genre_counts.get(book.genre, 0) + 1
            
            stats = f"Total books: {len(books)}\n"
            stats += f"Genre distribution: {dict(list(genre_counts.items())[:5])}\n"
            stats += f"Currently borrowed: {sum(1 for book in books if book.is_borrowed)}"
            
            prompt = f"""Analyze this library data and provide 2-3 interesting insights:
{stats}

Focus on trends, popular genres, or recommendations for collection development."""
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Could not generate insights: {str(e)}"
    
    def chat_with_librarian(self, question: str, books: List[Book]) -> str:
        try:
            book_context = f"Library has {len(books)} books across genres: {', '.join(set(book.genre for book in books))}"
            
            prompt = f"""You are a helpful AI librarian assistant for BookNest. 
Context: {book_context}

User question: {question}

Provide a helpful, friendly response. If the question is about book recommendations, be specific. 
If it's about library operations, be practical. Keep responses concise but informative."""
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Sorry, I'm having trouble connecting right now: {str(e)}"

def show_toast(message: str, toast_type: str = "success"):
    """Show toast notification"""
    toast_class = f"toast-{toast_type}"
    icon = {"success": "✅", "error": "❌", "warning": "⚠️"}.get(toast_type, "ℹ️")
    
    st.markdown(f"""
    <div class="toast {toast_class}">
        <strong>{icon} {message}</strong>
    </div>
    <script>
        setTimeout(function() {{
            const toast = document.querySelector('.toast');
            if (toast) toast.remove();
        }}, 3000);
    </script>
    """, unsafe_allow_html=True)

def render_book_card(book: Book, library_manager: LibraryManager, show_actions: bool = True):
    """Render a modern book card"""
    
    # Determine status
    is_overdue = False
    if book.is_borrowed and book.due_date:
        is_overdue = datetime.strptime(book.due_date, "%Y-%m-%d") < datetime.now()
    
    status_class = "status-overdue" if is_overdue else ("status-borrowed" if book.is_borrowed else "status-available")
    status_text = "OVERDUE" if is_overdue else ("BORROWED" if book.is_borrowed else "AVAILABLE")
    
    # Generate book cover placeholder
    cover_text = f"{book.title[:15]}..." if len(book.title) > 15 else book.title
    
    card_html = f"""
    <div class="book-card">
        <div class="status-badge {status_class}">{status_text}</div>
        <div style="display: flex; align-items: flex-start;">
            <div class="book-cover">
                📚<br>{cover_text}
            </div>
            <div class="book-info">
                <div class="book-title">{book.title}</div>
                <div class="book-author">by {book.author}</div>
                <div class="book-meta">
                    {book.genre} • {book.year} • ISBN: {book.isbn}
                </div>
                <div class="genre-tags">
                    {''.join([f'<span class="genre-tag">{tag}</span>' for tag in book.tags[:3]])}
                </div>
                {f'<div class="book-summary">{book.summary}</div>' if book.summary else ''}
                {f'<div style="margin-top: 0.5rem; color: #E53E3E; font-weight: 600;">Due: {book.due_date} | Borrower: {book.borrower_name}</div>' if book.is_borrowed else ''}
            </div>
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)
    
    if show_actions:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if not book.is_borrowed:
                if st.button("📤 Check Out", key=f"checkout_{book.id}", help="Check out this book"):
                    st.session_state[f"checkout_modal_{book.id}"] = True
            else:
                if st.button("📥 Check In", key=f"checkin_{book.id}", help="Return this book"):
                    library_manager.check_in_book(book.id)
                    show_toast(f"'{book.title}' has been returned successfully!")
                    st.rerun()
        
        with col2:
            if st.button("✏️ Edit", key=f"edit_{book.id}", help="Edit book details"):
                st.session_state[f"edit_modal_{book.id}"] = True
        
        with col3:
            if st.button("🤖 AI Summary", key=f"summary_{book.id}", help="Generate AI summary"):
                if 'ai_assistant' in st.session_state:
                    with st.spinner("Generating summary..."):
                        summary = st.session_state.ai_assistant.generate_book_summary(
                            book.title, book.author, book.genre, book.year
                        )
                        book.summary = summary
                        library_manager.update_book(book.id, book)
                        show_toast("Summary generated successfully!")
                        st.rerun()
        
        with col4:
            if st.button("🗑️ Delete", key=f"delete_{book.id}", help="Delete this book"):
                library_manager.delete_book(book.id)
                show_toast(f"'{book.title}' has been deleted", "warning")
                st.rerun()
        
        # Checkout modal
        if st.session_state.get(f"checkout_modal_{book.id}", False):
            with st.form(f"checkout_form_{book.id}"):
                st.write(f"**Check out: {book.title}**")
                borrower_name = st.text_input("Borrower name", key=f"borrower_{book.id}")
                days = st.number_input("Loan period (days)", min_value=1, max_value=90, value=14, key=f"days_{book.id}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("✅ Confirm Checkout"):
                        if borrower_name:
                            library_manager.check_out_book(book.id, borrower_name, days)
                            show_toast(f"'{book.title}' checked out to {borrower_name}")
                            st.session_state[f"checkout_modal_{book.id}"] = False
                            st.rerun()
                        else:
                            st.error("Please enter borrower name")
                
                with col2:
                    if st.form_submit_button("❌ Cancel"):
                        st.session_state[f"checkout_modal_{book.id}"] = False
                        st.rerun()

def render_stats_dashboard(library_manager: LibraryManager):
    """Render statistics dashboard"""
    books = library_manager.books
    total_books = len(books)
    borrowed_books = sum(1 for book in books if book.is_borrowed)
    available_books = total_books - borrowed_books
    overdue_books = sum(1 for book in books if book.is_borrowed and book.due_date and 
                       datetime.strptime(book.due_date, "%Y-%m-%d") < datetime.now())
    
    stats_html = f"""
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-number">{total_books}</div>
            <div class="stat-label">Total Books</div>
        </div>
        <div class="stat-card">
            <div class="stat-number" style="color: #48BB78;">{available_books}</div>
            <div class="stat-label">Available</div>
        </div>
        <div class="stat-card">
            <div class="stat-number" style="color: #ED8936;">{borrowed_books}</div>
            <div class="stat-label">Borrowed</div>
        </div>
        <div class="stat-card">
            <div class="stat-number" style="color: #E53E3E;">{overdue_books}</div>
            <div class="stat-label">Overdue</div>
        </div>
    </div>
    """
    
    st.markdown(stats_html, unsafe_allow_html=True)

def render_ai_chat():
    """Render floating AI chat interface"""
    if 'chat_open' not in st.session_state:
        st.session_state.chat_open = False
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Chat button
    chat_button_html = """
    <button class="ai-chat-button" onclick="toggleChat()">
        🤖
    </button>
    
    <script>
        function toggleChat() {
            // This would toggle the chat panel
            // For now, we'll use Streamlit's session state
        }
    </script>
    """
    
    st.markdown(chat_button_html, unsafe_allow_html=True)
    
    # Chat toggle button
    if st.button("💬 Ask AI Librarian", key="chat_toggle"):
        st.session_state.chat_open = not st.session_state.chat_open
    
    # Chat panel
    if st.session_state.chat_open:
        with st.container():
            st.markdown("""
            <div style="background: white; border-radius: 16px; padding: 1rem; margin: 1rem 0; box-shadow: 0 8px 32px rgba(0,0,0,0.1);">
                <div style="background: linear-gradient(135deg, #F18F01, #A23B72); color: white; padding: 1rem; border-radius: 12px; margin-bottom: 1rem;">
                    <h4 style="margin: 0;">🤖 AI Librarian Assistant</h4>
                    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Ask me anything about your library!</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Chat history
            for msg in st.session_state.chat_history[-5:]:  # Show last 5 messages
                if msg['role'] == 'user':
                    st.write(f"**You:** {msg['content']}")
                else:
                    st.write(f"**AI Librarian:** {msg['content']}")
            
            # Chat input
            user_input = st.text_input("Ask a question...", key="chat_input", placeholder="e.g., 'Recommend a sci-fi book' or 'Which books are overdue?'")
            
            if st.button("Send", key="send_chat") and user_input:
                if 'ai_assistant' in st.session_state and 'library_manager' in st.session_state:
                    # Add user message
                    st.session_state.chat_history.append({'role': 'user', 'content': user_input})
                    
                    # Get AI response
                    with st.spinner("AI Librarian is thinking..."):
                        response = st.session_state.ai_assistant.chat_with_librarian(
                            user_input, st.session_state.library_manager.books
                        )
                        st.session_state.chat_history.append({'role': 'assistant', 'content': response})
                    
                    st.rerun()
                else:
                    st.error("AI Assistant not available. Please check your API key.")

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏠 BookNest</h1>
        <p>Your AI-Powered Library Management System</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize managers
    if 'library_manager' not in st.session_state:
        st.session_state.library_manager = LibraryManager()
    
    if 'ai_assistant' not in st.session_state:
        st.session_state.ai_assistant = AIAssistant()
    
    library_manager = st.session_state.library_manager
    ai_assistant = st.session_state.ai_assistant
    
    # Navigation
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "My Books"
    
    # Navigation tabs
    col1, col2, col3, col4 = st.columns(4)
    
    pages = ["📚 My Books", "➕ Add Book", "🔍 Search", "📊 Insights"]
    
    for i, (col, page) in enumerate(zip([col1, col2, col3, col4], pages)):
        with col:
            if st.button(page, key=f"nav_{i}", use_container_width=True):
                st.session_state.current_page = page
    
    # Stats dashboard
    render_stats_dashboard(library_manager)
    
    # Page content
    if st.session_state.current_page == "📚 My Books":
        st.subheader("📚 Your Library Collection")
        
        if library_manager.books:
            # Filter options
            with st.expander("🔧 Filter Options", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    filter_status = st.selectbox("Filter by status", ["All", "Available", "Borrowed", "Overdue"])
                with col2:
                    filter_genre = st.selectbox("Filter by genre", ["All"] + list(set(book.genre for book in library_manager.books)))
            
            # Apply filters
            filtered_books = library_manager.books
            
            if filter_status != "All":
                if filter_status == "Available":
                    filtered_books = [book for book in filtered_books if not book.is_borrowed]
                elif filter_status == "Borrowed":
                    filtered_books = [book for book in filtered_books if book.is_borrowed]
                elif filter_status == "Overdue":
                    filtered_books = [book for book in filtered_books if book.is_borrowed and book.due_date and 
                                    datetime.strptime(book.due_date, "%Y-%m-%d") < datetime.now()]
            
            if filter_genre != "All":
                filtered_books = [book for book in filtered_books if book.genre == filter_genre]
            
            st.write(f"Showing {len(filtered_books)} of {len(library_manager.books)} books")
            
            # Display books
            for book in filtered_books:
                render_book_card(book, library_manager)
                
        else:
            st.info("📖 No books in your library yet. Add your first book using the 'Add Book' tab!")
    
    elif st.session_state.current_page == "➕ Add Book":
        st.subheader("➕ Add New Book")
        
        with st.form("add_book_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("📖 Title*", placeholder="Enter book title")
                author = st.text_input("✍️ Author*", placeholder="Enter author name")
                genre = st.selectbox("📂 Genre*", [
                    "Fiction", "Non-Fiction", "Mystery", "Romance", "Sci-Fi", 
                    "Fantasy", "Biography", "History", "Science", "Self-Help"
                ])
            with col2:
                year = st.number_input("📅 Year", min_value=1000, max_value=2024, value=2023)
                isbn = st.text_input("🔢 ISBN", placeholder="978-0-123456-78-9")
                tags = st.text_input("🏷️ Tags", placeholder="classic, adventure, must-read (comma separated)")
            
            generate_summary = st.checkbox("🤖 Generate AI summary automatically")
            submitted = st.form_submit_button("➕ Add Book to Library", use_container_width=True)
            
            if submitted and title and author and genre:
                book_id = f"{len(library_manager.books) + 1:04d}"
                tags_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
                
                summary = ""
                if generate_summary:
                    with st.spinner("🤖 Generating AI summary..."):
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
                show_toast(f"📚 '{title}' added to your library!")
                st.rerun()
            elif submitted:
                st.error("⚠️ Please fill in all required fields (marked with *)")
    
    elif st.session_state.current_page == "🔍 Search":
        st.subheader("🔍 Search & Browse")
        
        # Search interface
        search_query = st.text_input("🔍 Search books...", placeholder="Enter title, author, genre, or tags")
        
        col1, col2 = st.columns(2)
        with col1:
            search_filter = st.selectbox("📊 Filter by availability", ["All", "Available", "Borrowed"])
        with col2:
            genres = list(set(book.genre for book in library_manager.books))
            selected_genres = st.multiselect("📂 Filter by genres", genres)
        
        # Filter books based on search
        filtered_books = library_manager.books
        
        if search_query:
            filtered_books = [
                book for book in filtered_books
                if (search_query.lower() in book.title.lower() or
                    search_query.lower() in book.author.lower() or
                    search_query.lower() in book.genre.lower() or
                    any(search_query.lower() in tag.lower() for tag in book.tags))
            ]
        
        if search_filter == "Available":
            filtered_books = [book for book in filtered_books if not book.is_borrowed]
        elif search_filter == "Borrowed":
            filtered_books = [book for book in filtered_books if book.is_borrowed]
        
        if selected_genres:
            filtered_books = [book for book in filtered_books if book.genre in selected_genres]
        
        st.write(f"📊 Found {len(filtered_books)} books")
        
        # Display results
        for book in filtered_books:
            render_book_card(book, library_manager, show_actions=False)
    
    elif st.session_state.current_page == "📊 Insights":
        st.subheader("📊 Library Analytics & AI Insights")
        
        if library_manager.books:
            # Genre distribution chart
            genre_counts = {}
            for book in library_manager.books:
                genre_counts[book.genre] = genre_counts.get(book.genre, 0) + 1
            
            if genre_counts:
                st.write("📈 **Genre Distribution**")
                genre_df = pd.DataFrame(list(genre_counts.items()), columns=['Genre', 'Count'])
                st.bar_chart(genre_df.set_index('Genre'))
            
            # AI Insights
            st.write("🤖 **AI Library Analysis**")
            if st.button("Generate AI Insights", use_container_width=True):
                with st.spinner("🤖 Analyzing your library..."):
                    insights = ai_assistant.get_library_insights(library_manager.books)
                    st.info(insights)
            
            # Recent activity
            st.write("📅 **Recent Activity**")
            if library_manager.borrowing_history:
                recent_history = sorted(library_manager.borrowing_history, 
                                      key=lambda x: x.get('checkout_date', x.get('return_date', '')), 
                                      reverse=True)[:10]
                
                for activity in recent_history:
                    if activity['action'] == 'checkout':
                        st.write(f"📤 {activity['checkout_date']}: **{activity['book_title']}** checked out to {activity['borrower_name']}")
                    else:
                        st.write(f"📥 {activity['return_date']}: **{activity['book_title']}** returned by {activity['borrower_name']}")
            else:
                st.info("No borrowing activity yet")
        else:
            st.info("📖 Add some books first to see insights and analytics")
    
    # AI Chat Interface
    render_ai_chat()

if __name__ == "__main__":
    main()