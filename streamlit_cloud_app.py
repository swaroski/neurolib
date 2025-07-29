import streamlit as st
import pandas as pd
import json
import requests
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict
import google.generativeai as genai
import os

# Configure page
st.set_page_config(
    page_title="📚 BookNest - AI Library Manager",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .book-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
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

def create_sample_books():
    """Create sample books for Streamlit Cloud"""
    return [
        Book("0001", "To Kill a Mockingbird", "Harper Lee", "Fiction", 1960, "978-0-06-112008-4", 
             ["classic", "social-justice", "coming-of-age"], 
             summary="A powerful story of racial injustice and childhood innocence in the American South, told through the eyes of Scout Finch as her father defends a Black man falsely accused of rape."),
        
        Book("0002", "1984", "George Orwell", "Fiction", 1949, "978-0-452-28423-4", 
             ["dystopian", "political", "classic"], 
             summary="A chilling vision of a totalitarian future where Big Brother watches everything, exploring themes of surveillance, truth, and individual freedom in a world of perpetual war."),
        
        Book("0003", "Pride and Prejudice", "Jane Austen", "Romance", 1813, "978-0-14-143951-8", 
             ["classic", "romance", "regency"], is_borrowed=True, borrower_name="Alice Johnson",
             due_date=(datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
             summary="The timeless story of Elizabeth Bennet and Mr. Darcy's complex courtship, filled with wit, social commentary, and one of literature's most satisfying romantic relationships."),
        
        Book("0004", "The Great Gatsby", "F. Scott Fitzgerald", "Fiction", 1925, "978-0-7432-7356-5", 
             ["classic", "american-dream", "jazz-age"], 
             summary="A tragic tale of love, wealth, and the corruption of the American Dream set in the roaring twenties, following Jay Gatsby's obsessive pursuit of Daisy Buchanan."),
        
        Book("0005", "Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "Fantasy", 1997, "978-0-439-70818-8", 
             ["magic", "young-adult", "adventure"], 
             summary="A young wizard discovers his magical heritage and begins his journey at Hogwarts School, launching one of the most beloved fantasy series of all time."),
        
        Book("0006", "Dune", "Frank Herbert", "Sci-Fi", 1965, "978-0-441-17271-9", 
             ["space-opera", "politics", "ecology"], 
             summary="Epic tale of politics, religion, and ecology on the desert planet Arrakis, following Paul Atreides as he becomes a messianic leader in a complex galactic empire."),
        
        Book("0007", "The Hitchhiker's Guide to the Galaxy", "Douglas Adams", "Sci-Fi", 1979, "978-0-345-39180-3", 
             ["humor", "space", "adventure"], is_borrowed=True, borrower_name="Bob Smith",
             due_date=(datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d"),
             summary="A hilarious journey through space with Arthur Dent and his alien friend Ford Prefect, featuring towels, paranoid androids, and the answer to life, the universe, and everything."),
        
        Book("0008", "The Murder of Roger Ackroyd", "Agatha Christie", "Mystery", 1926, "978-0-06-207350-4", 
             ["detective", "classic", "whodunit"], 
             summary="Hercule Poirot investigates a shocking murder with an unexpected twist that revolutionized the mystery genre and remains controversial to this day."),
        
        Book("0009", "Sapiens", "Yuval Noah Harari", "Non-Fiction", 2011, "978-0-06-231609-7", 
             ["history", "anthropology", "evolution"], 
             summary="A sweeping look at the history and impact of Homo sapiens on Earth, from the Stone Age to the present, exploring how we became the dominant species."),
        
        Book("0010", "The Lord of the Rings", "J.R.R. Tolkien", "Fantasy", 1954, "978-0-544-00341-5", 
             ["epic", "adventure", "middle-earth"], 
             summary="The epic quest to destroy the One Ring and save Middle-earth from darkness, featuring hobbits, wizards, and the ultimate battle between good and evil."),
        
        Book("0011", "Gone Girl", "Gillian Flynn", "Mystery", 2012, "978-0-307-58836-4", 
             ["psychological", "thriller", "marriage"], 
             summary="A marriage's dark secrets are revealed when Amy Dunne mysteriously disappears on her fifth wedding anniversary, leaving her husband Nick as the prime suspect."),
        
        Book("0012", "Educated", "Tara Westover", "Biography", 2018, "978-0-399-59050-4", 
             ["memoir", "education", "family"], 
             summary="A powerful memoir about education's transformative power, following Tara's journey from a survivalist family in Idaho to earning a PhD from Cambridge."),
        
        Book("0013", "The Martian", "Andy Weir", "Sci-Fi", 2011, "978-0-553-41802-6", 
             ["mars", "survival", "science"], 
             summary="Mark Watney's incredible survival story on Mars, combining hard science with humor as he 'sciences the hell' out of impossible problems."),
        
        Book("0014", "Atomic Habits", "James Clear", "Self-Help", 2018, "978-0-7352-1129-2", 
             ["productivity", "habits", "psychology"], 
             summary="A proven system for building good habits and breaking bad ones, showing how small changes can create remarkable results over time."),
        
        Book("0015", "Where the Crawdads Sing", "Delia Owens", "Fiction", 2018, "978-0-7352-1909-0", 
             ["nature", "mystery", "coming-of-age"], is_borrowed=True, borrower_name="Carol Davis",
             due_date=(datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),  # Overdue
             summary="Kya the 'Marsh Girl' grows up isolated in North Carolina's coastal marshes, weaving together a murder mystery with a beautiful coming-of-age story."),
        
        Book("0016", "The Silent Patient", "Alex Michaelides", "Mystery", 2019, "978-1-250-30170-7", 
             ["psychological", "thriller", "art"], 
             summary="A psychotherapist becomes obsessed with treating a woman who refuses to speak after allegedly murdering her husband, leading to a shocking conclusion."),
        
        Book("0017", "Circe", "Madeline Miller", "Fantasy", 2018, "978-0-316-55633-4", 
             ["mythology", "greek-gods", "feminism"], 
             summary="The enchanting story of Circe, the banished witch of Greek mythology, as she discovers her powers and finds her voice in a world of gods and monsters."),
        
        Book("0018", "Becoming", "Michelle Obama", "Biography", 2018, "978-1-5247-6313-8", 
             ["memoir", "politics", "inspiration"], 
             summary="The former First Lady's powerful memoir of her journey from Chicago's South Side to the White House, sharing personal stories of triumph and resilience."),
        
        Book("0019", "The Seven Husbands of Evelyn Hugo", "Taylor Jenkins Reid", "Fiction", 2017, "978-1-5011-3981-6", 
             ["hollywood", "lgbtq", "secrets"], 
             summary="Reclusive Hollywood icon Evelyn Hugo finally tells her life story, revealing the truth about her seven marriages and the price of fame and love."),
        
        Book("0020", "Klara and the Sun", "Kazuo Ishiguro", "Sci-Fi", 2021, "978-0-571-36487-1", 
             ["artificial-intelligence", "humanity", "love"], 
             summary="From the perspective of an artificial friend, this touching story explores what it means to love and be human in a world of advancing technology.")
    ]

class LibraryManager:
    def __init__(self):
        # Initialize with sample books for Streamlit Cloud
        if 'library_books' not in st.session_state:
            st.session_state.library_books = create_sample_books()
        
        if 'borrowing_history' not in st.session_state:
            st.session_state.borrowing_history = [
                {
                    'book_id': '0001',
                    'book_title': 'To Kill a Mockingbird',
                    'borrower_name': 'John Doe',
                    'checkout_date': '2024-01-15',
                    'return_date': '2024-01-29',
                    'action': 'checkin'
                },
                {
                    'book_id': '0002',
                    'book_title': '1984',
                    'borrower_name': 'Jane Smith',
                    'checkout_date': '2024-01-20',
                    'return_date': '2024-02-03',
                    'action': 'checkin'
                }
            ]
    
    @property
    def books(self):
        return st.session_state.library_books
    
    def add_book(self, book: Book):
        st.session_state.library_books.append(book)
    
    def update_book(self, book_id: str, updated_book: Book):
        for i, book in enumerate(st.session_state.library_books):
            if book.id == book_id:
                st.session_state.library_books[i] = updated_book
                break
    
    def delete_book(self, book_id: str):
        st.session_state.library_books = [book for book in st.session_state.library_books if book.id != book_id]
    
    def check_out_book(self, book_id: str, borrower_name: str, days: int = 14):
        for book in st.session_state.library_books:
            if book.id == book_id:
                book.is_borrowed = True
                book.borrower_name = borrower_name
                book.due_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
                
                st.session_state.borrowing_history.append({
                    'book_id': book_id,
                    'book_title': book.title,
                    'borrower_name': borrower_name,
                    'checkout_date': datetime.now().strftime("%Y-%m-%d"),
                    'due_date': book.due_date,
                    'action': 'checkout'
                })
                break
    
    def check_in_book(self, book_id: str):
        for book in st.session_state.library_books:
            if book.id == book_id:
                book.is_borrowed = False
                borrower_name = book.borrower_name
                book.borrower_name = ""
                book.due_date = None
                
                st.session_state.borrowing_history.append({
                    'book_id': book_id,
                    'book_title': book.title,
                    'borrower_name': borrower_name,
                    'return_date': datetime.now().strftime("%Y-%m-%d"),
                    'action': 'checkin'
                })
                break

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
    
    def convert_to_book(self, ol_book: Dict, book_id: str) -> Book:
        """Convert Open Library book data to our Book format"""
        try:
            title = ol_book.get('title', 'Unknown Title')
            authors = ol_book.get('author_name', ['Unknown Author'])
            author = ', '.join(authors[:2])
            year = ol_book.get('first_publish_year', 2000)
            
            isbns = ol_book.get('isbn', [])
            isbn = isbns[0] if isbns else f"OL-{ol_book.get('key', '').replace('/works/', '')}"
            
            subjects = ol_book.get('subject', [])
            genre = self._determine_genre(subjects)
            tags = subjects[:5]
            
            cover_id = ol_book.get('cover_i')
            cover_url = f"{self.covers_url}/id/{cover_id}-M.jpg" if cover_id else ""
            
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
        
        return 'Fiction'

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
            st.info("💡 Add GOOGLE_API_KEY to Streamlit secrets for AI features")
            self.model = None
    
    def generate_book_summary(self, title: str, author: str, genre: str, year: int = None) -> str:
        if not self.model:
            return "AI features require GOOGLE_API_KEY to be configured in Streamlit secrets."
        
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

def render_book_card(book: Book):
    """Render a book card"""
    
    status_class = "status-borrowed" if book.is_borrowed else "status-available"
    status_text = "BORROWED" if book.is_borrowed else "AVAILABLE"
    
    # Check if overdue
    is_overdue = False
    if book.is_borrowed and book.due_date:
        try:
            due_date = datetime.strptime(book.due_date, "%Y-%m-%d")
            is_overdue = due_date < datetime.now()
        except:
            pass
    
    if is_overdue:
        status_text = "OVERDUE"
        status_class = "status-overdue"
    
    card_html = f"""
    <div class="book-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
            <div style="flex: 1;">
                <div class="book-title">{book.title}</div>
                <div class="book-author">by {book.author}</div>
                <div style="color: #718096; font-size: 0.9rem; margin-bottom: 0.5rem;">
                    {book.genre} • {book.year} • ISBN: {book.isbn}
                </div>
                {f'<div style="margin-bottom: 0.5rem;">Tags: {", ".join(book.tags[:3])}</div>' if book.tags else ''}
                {f'<div style="margin-top: 0.5rem; font-style: italic; color: #4a5568;">{book.summary}</div>' if book.summary else ''}
                {f'<div style="margin-top: 0.5rem; color: #e53e3e; font-weight: 600;">Due: {book.due_date} | Borrower: {book.borrower_name}</div>' if book.is_borrowed else ''}
            </div>
            <span class="{status_class}" style="margin-left: 1rem;">{status_text}</span>
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)

def main():
    st.title("🏠 BookNest - AI Library Manager")
    st.markdown("*Your intelligent library management system • Running on Streamlit Cloud*")
    
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
    
    # Show initialization success
    if len(library_manager.books) > 0:
        st.success(f"🎉 BookNest initialized with {len(library_manager.books)} sample books!")
    
    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📚 My Library", "➕ Add Books", "🌐 Import from Open Library", "📊 Analytics"])
    
    with tab1:
        st.subheader("📚 Your Library Collection")
        
        # Search and filter
        col1, col2 = st.columns([3, 1])
        with col1:
            search_query = st.text_input("🔍 Search books...", placeholder="Title, author, or genre")
        with col2:
            filter_status = st.selectbox("Filter", ["All", "Available", "Borrowed", "Overdue"])
        
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
        elif filter_status == "Overdue":
            overdue_books = []
            for book in filtered_books:
                if book.is_borrowed and book.due_date:
                    try:
                        due_date = datetime.strptime(book.due_date, "%Y-%m-%d")
                        if due_date < datetime.now():
                            overdue_books.append(book)
                    except:
                        pass
            filtered_books = overdue_books
        
        st.write(f"Showing {len(filtered_books)} of {len(library_manager.books)} books")
        
        # Display books
        for book in filtered_books:
            render_book_card(book)
            
            # Action buttons
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if not book.is_borrowed:
                    if st.button("📤 Check Out", key=f"checkout_{book.id}"):
                        borrower_name = st.text_input("Borrower name:", key=f"borrower_{book.id}")
                        if borrower_name:
                            library_manager.check_out_book(book.id, borrower_name)
                            st.success(f"Checked out to {borrower_name}!")
                            st.rerun()
                else:
                    if st.button("📥 Check In", key=f"checkin_{book.id}"):
                        library_manager.check_in_book(book.id)
                        st.success("Book returned!")
                        st.rerun()
            
            with col2:
                if st.button("🤖 AI Summary", key=f"summary_{book.id}"):
                    if ai_assistant.model:
                        with st.spinner("Generating summary..."):
                            summary = ai_assistant.generate_book_summary(
                                book.title, book.author, book.genre, book.year
                            )
                            book.summary = summary
                            library_manager.update_book(book.id, book)
                            st.success("Summary generated!")
                            st.rerun()
                    else:
                        st.warning("Add GOOGLE_API_KEY to secrets for AI features")
            
            with col3:
                if st.button("🗑️ Delete", key=f"delete_{book.id}"):
                    library_manager.delete_book(book.id)
                    st.success("Book deleted!")
                    st.rerun()
    
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
                if generate_summary and ai_assistant.model:
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
                            book_id = f"{len(library_manager.books) + 1:04d}"
                            book = ol_api.convert_to_book(result, book_id)
                            if book:
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
            
            # Recent activity
            st.write("**Recent Activity:**")
            recent_history = sorted(st.session_state.borrowing_history, 
                                  key=lambda x: x.get('checkout_date', x.get('return_date', '')), 
                                  reverse=True)[:5]
            
            for activity in recent_history:
                if activity['action'] == 'checkout':
                    st.write(f"📤 {activity['checkout_date']}: **{activity['book_title']}** checked out to {activity['borrower_name']}")
                else:
                    st.write(f"📥 {activity['return_date']}: **{activity['book_title']}** returned by {activity['borrower_name']}")
                    
        else:
            st.info("Add some books to see analytics!")
    
    # Footer
    st.markdown("---")
    st.markdown("*BookNest • Built with Streamlit & Powered by AI • [GitHub](https://github.com/your-repo)*")

if __name__ == "__main__":
    main()