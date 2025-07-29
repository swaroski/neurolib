import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict
import google.generativeai as genai
import os

# Configure page
st.set_page_config(
    page_title="📚 AI Library Manager",
    page_icon="📚",
    layout="wide"
)

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
        # Initialize with sample books if running on Streamlit Cloud
        if 'library_books' not in st.session_state:
            st.session_state.library_books = self.create_sample_books()
        if 'borrowing_history' not in st.session_state:
            st.session_state.borrowing_history = []
        
        # Try to load from file if it exists (for local development)
        self.load_data()
    
    def create_sample_books(self):
        """Create sample books for Streamlit Cloud"""
        return [
            Book("0001", "To Kill a Mockingbird", "Harper Lee", "Fiction", 1960, "978-0-06-112008-4", 
                 ["classic", "social-justice", "coming-of-age"], 
                 summary="A powerful story of racial injustice and childhood innocence in the American South."),
            
            Book("0002", "1984", "George Orwell", "Fiction", 1949, "978-0-452-28423-4", 
                 ["dystopian", "political", "classic"], 
                 summary="A chilling vision of a totalitarian future where Big Brother watches everything."),
            
            Book("0003", "Pride and Prejudice", "Jane Austen", "Romance", 1813, "978-0-14-143951-8", 
                 ["classic", "romance", "regency"], is_borrowed=True, borrower_name="Alice Johnson",
                 due_date=(datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
                 summary="The timeless story of Elizabeth Bennet and Mr. Darcy's complex courtship."),
            
            Book("0004", "The Great Gatsby", "F. Scott Fitzgerald", "Fiction", 1925, "978-0-7432-7356-5", 
                 ["classic", "american-dream", "jazz-age"], 
                 summary="A tragic tale of love, wealth, and the corruption of the American Dream."),
            
            Book("0005", "Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "Fantasy", 1997, "978-0-439-70818-8", 
                 ["magic", "young-adult", "adventure"], 
                 summary="A young wizard discovers his magical heritage and begins his journey at Hogwarts."),
            
            Book("0006", "Dune", "Frank Herbert", "Sci-Fi", 1965, "978-0-441-17271-9", 
                 ["space-opera", "politics", "ecology"], 
                 summary="Epic tale of politics, religion, and ecology on the desert planet Arrakis."),
            
            Book("0007", "The Hitchhiker's Guide to the Galaxy", "Douglas Adams", "Sci-Fi", 1979, "978-0-345-39180-3", 
                 ["humor", "space", "adventure"], is_borrowed=True, borrower_name="Bob Smith",
                 due_date=(datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d"),
                 summary="A hilarious journey through space with Arthur Dent and his alien friend Ford Prefect."),
            
            Book("0008", "The Murder of Roger Ackroyd", "Agatha Christie", "Mystery", 1926, "978-0-06-207350-4", 
                 ["detective", "classic", "whodunit"], 
                 summary="Hercule Poirot investigates a shocking murder with an unexpected twist."),
            
            Book("0009", "Sapiens", "Yuval Noah Harari", "Non-Fiction", 2011, "978-0-06-231609-7", 
                 ["history", "anthropology", "evolution"], 
                 summary="A sweeping look at the history and impact of Homo sapiens on Earth."),
            
            Book("0010", "The Lord of the Rings", "J.R.R. Tolkien", "Fantasy", 1954, "978-0-544-00341-5", 
                 ["epic", "adventure", "middle-earth"], 
                 summary="The epic quest to destroy the One Ring and save Middle-earth from darkness."),
            
            Book("0011", "Gone Girl", "Gillian Flynn", "Mystery", 2012, "978-0-307-58836-4", 
                 ["psychological", "thriller", "marriage"], 
                 summary="A marriage's dark secrets are revealed when Amy Dunne mysteriously disappears."),
            
            Book("0012", "Educated", "Tara Westover", "Biography", 2018, "978-0-399-59050-4", 
                 ["memoir", "education", "family"], 
                 summary="A powerful memoir about education's transformative power."),
            
            Book("0013", "The Martian", "Andy Weir", "Sci-Fi", 2011, "978-0-553-41802-6", 
                 ["mars", "survival", "science"], 
                 summary="Mark Watney's incredible survival story on Mars."),
            
            Book("0014", "Atomic Habits", "James Clear", "Self-Help", 2018, "978-0-7352-1129-2", 
                 ["productivity", "habits", "psychology"], 
                 summary="A proven system for building good habits and breaking bad ones."),
            
            Book("0015", "Where the Crawdads Sing", "Delia Owens", "Fiction", 2018, "978-0-7352-1909-0", 
                 ["nature", "mystery", "coming-of-age"], is_borrowed=True, borrower_name="Carol Davis",
                 due_date=(datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),  # Overdue
                 summary="Kya the 'Marsh Girl' grows up isolated in North Carolina's coastal marshes."),
            
            Book("0016", "The Silent Patient", "Alex Michaelides", "Mystery", 2019, "978-1-250-30170-7", 
                 ["psychological", "thriller", "art"], 
                 summary="A psychotherapist becomes obsessed with treating a woman who refuses to speak."),
            
            Book("0017", "Circe", "Madeline Miller", "Fantasy", 2018, "978-0-316-55633-4", 
                 ["mythology", "greek-gods", "feminism"], 
                 summary="The enchanting story of Circe, the banished witch of Greek mythology."),
            
            Book("0018", "Becoming", "Michelle Obama", "Biography", 2018, "978-1-5247-6313-8", 
                 ["memoir", "politics", "inspiration"], 
                 summary="The former First Lady's powerful memoir of her journey to the White House."),
            
            Book("0019", "The Seven Husbands of Evelyn Hugo", "Taylor Jenkins Reid", "Fiction", 2017, "978-1-5011-3981-6", 
                 ["hollywood", "lgbtq", "secrets"], 
                 summary="Reclusive Hollywood icon Evelyn Hugo finally tells her life story."),
            
            Book("0020", "Klara and the Sun", "Kazuo Ishiguro", "Sci-Fi", 2021, "978-0-571-36487-1", 
                 ["artificial-intelligence", "humanity", "love"], 
                 summary="From the perspective of an artificial friend, exploring what it means to be human.")
        ]
        
    def load_data(self):
        try:
            with open(self.data_file, 'r') as f:
                data_dict = json.load(f)
                books_data = data_dict.get('books', [])
                # Only load from file if session state is empty
                if not st.session_state.library_books:
                    st.session_state.library_books = [Book(**book) for book in books_data]
                if not st.session_state.borrowing_history:
                    st.session_state.borrowing_history = data_dict.get('borrowing_history', [])
        except FileNotFoundError:
            # This is expected on Streamlit Cloud - we already have sample books
            pass
            
    @property
    def books(self):
        return st.session_state.library_books
    
    @property 
    def borrowing_history(self):
        return st.session_state.borrowing_history
    
    def save_data(self):
        # For Streamlit Cloud, data persists in session state
        # For local development, save to file
        try:
            data = {
                'books': [asdict(book) for book in self.books],
                'borrowing_history': self.borrowing_history
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except:
            pass  # Skip file saving on Streamlit Cloud
    
    def add_book(self, book: Book):
        st.session_state.library_books.append(book)
        self.save_data()
    
    def update_book(self, book_id: str, updated_book: Book):
        for i, book in enumerate(st.session_state.library_books):
            if book.id == book_id:
                st.session_state.library_books[i] = updated_book
                break
        self.save_data()
    
    def delete_book(self, book_id: str):
        st.session_state.library_books = [book for book in st.session_state.library_books if book.id != book_id]
        self.save_data()
    
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
        self.save_data()
    
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
    
    def get_simple_recommendations(self, books: List[Book], current_book: Book) -> List[Book]:
        """Get simple rule-based recommendations without AI"""
        other_books = [book for book in books if book.id != current_book.id]
        recommendations = []
        
        # 1. Same genre books
        genre_matches = [book for book in other_books if book.genre == current_book.genre]
        recommendations.extend(genre_matches[:2])
        
        # 2. Books with similar tags
        if current_book.tags and len(recommendations) < 3:
            tag_matches = []
            for book in other_books:
                if book not in recommendations and book.tags:
                    common_tags = set(current_book.tags) & set(book.tags)
                    if common_tags:
                        tag_matches.append((book, len(common_tags)))
            
            # Sort by number of common tags
            tag_matches.sort(key=lambda x: x[1], reverse=True)
            for book, _ in tag_matches[:3-len(recommendations)]:
                recommendations.append(book)
        
        # 3. Fill remaining with popular books (by author similarity or random)
        if len(recommendations) < 3:
            remaining = [book for book in other_books if book not in recommendations]
            recommendations.extend(remaining[:3-len(recommendations)])
        
        return recommendations[:3]
    
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

def main():
    st.title("📚 AI-Powered Library Management System")
    st.markdown("*Book Management • Check-In/Out • AI Summaries • Smart Recommendations • Open Library • Search • Analytics*")
    
    # Initialize managers
    if 'library_manager' not in st.session_state:
        st.session_state.library_manager = LibraryManager()
    
    if 'ai_assistant' not in st.session_state:
        st.session_state.ai_assistant = AIAssistant()
    
    library_manager = st.session_state.library_manager
    ai_assistant = st.session_state.ai_assistant
    
    # Show initialization success
    if len(library_manager.books) > 0:
        st.success(f"🎉 BookNest initialized with {len(library_manager.books)} sample books!")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", [
        "📖 Book Management", 
        "🔄 Check-In/Out", 
        "🔍 Search & Browse",
        "🤖 AI Features",
        "📊 Analytics"
    ])
    
    if page == "📖 Book Management":
        st.header("Book Management")
        
        # Add new book form
        with st.expander("➕ Add New Book", expanded=False):
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
                
                generate_summary = st.checkbox("Generate AI summary")
                submitted = st.form_submit_button("Add Book")
                
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
                    st.success(f"Added '{title}' to the library!")
                    st.rerun()
        
        # Display books
        st.subheader("Current Collection")
        if library_manager.books:
            for book in library_manager.books:
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        status_emoji = "🔴" if book.is_borrowed else "🟢"
                        st.write(f"{status_emoji} **{book.title}** by {book.author}")
                        st.write(f"*{book.genre} ({book.year})* | Tags: {', '.join(book.tags) if book.tags else 'None'}")
                        if book.summary:
                            st.write(f"📝 {book.summary}")
                        if book.is_borrowed:
                            st.write(f"📅 Due: {book.due_date} | Borrower: {book.borrower_name}")
                    
                    with col2:
                        if st.button("📚 Get Recommendations", key=f"recommend_{book.id}"):
                            st.session_state[f"show_recommendations_{book.id}"] = True
                    
                    with col3:
                        if st.button("Edit", key=f"edit_{book.id}"):
                            st.session_state[f"editing_{book.id}"] = True
                        if st.button("Delete", key=f"delete_{book.id}"):
                            library_manager.delete_book(book.id)
                            st.rerun()
                    
                    # Show recommendations
                    if st.session_state.get(f"show_recommendations_{book.id}", False):
                        st.write("---")
                        st.write(f"**📚 Books similar to '{book.title}':**")
                        
                        # Get recommendations (simple first, then AI if available)
                        recommendations = ai_assistant.get_simple_recommendations(library_manager.books, book)
                        
                        if recommendations:
                            for i, rec_book in enumerate(recommendations):
                                rec_col1, rec_col2 = st.columns([4, 1])
                                with rec_col1:
                                    status_emoji = "🔴" if rec_book.is_borrowed else "🟢"
                                    st.write(f"{status_emoji} **{rec_book.title}** by {rec_book.author}")
                                    st.write(f"*{rec_book.genre} ({rec_book.year})* | Tags: {', '.join(rec_book.tags) if rec_book.tags else 'None'}")
                                    
                                    # Show why it's recommended
                                    reasons = []
                                    if rec_book.genre == book.genre:
                                        reasons.append(f"Same genre ({book.genre})")
                                    if rec_book.tags and book.tags:
                                        common_tags = set(rec_book.tags) & set(book.tags)
                                        if common_tags:
                                            reasons.append(f"Similar themes: {', '.join(list(common_tags)[:2])}")
                                    
                                    if reasons:
                                        st.write(f"💡 *Recommended because: {', '.join(reasons)}*")
                                
                                with rec_col2:
                                    if not rec_book.is_borrowed:
                                        if st.button("📤 Check Out", key=f"checkout_rec_{rec_book.id}_{book.id}"):
                                            borrower_name = st.text_input("Borrower name:", key=f"borrower_rec_{rec_book.id}_{book.id}")
                                            if borrower_name:
                                                library_manager.check_out_book(rec_book.id, borrower_name)
                                                st.success(f"Checked out '{rec_book.title}' to {borrower_name}!")
                                                st.rerun()
                                    else:
                                        st.write("📅 Currently borrowed")
                            
                            # AI recommendations if available
                            if ai_assistant.model:
                                if st.button("🤖 Get AI Recommendations", key=f"ai_rec_{book.id}"):
                                    with st.spinner("Getting AI recommendations..."):
                                        ai_recs = ai_assistant.get_reading_recommendations(library_manager.books, book)
                                        st.write("**🤖 AI Recommendations:**")
                                        for rec in ai_recs:
                                            if rec.strip():
                                                st.write(rec)
                        else:
                            st.info("No recommendations available (need more books in library)")
                        
                        if st.button("❌ Hide Recommendations", key=f"hide_rec_{book.id}"):
                            st.session_state[f"show_recommendations_{book.id}"] = False
                            st.rerun()
                    
                    # Edit form
                    if st.session_state.get(f"editing_{book.id}", False):
                        with st.form(f"edit_form_{book.id}"):
                            edit_col1, edit_col2 = st.columns(2)
                            with edit_col1:
                                new_title = st.text_input("Title", value=book.title)
                                new_author = st.text_input("Author", value=book.author)
                                new_genre = st.selectbox("Genre", [
                                    "Fiction", "Non-Fiction", "Mystery", "Romance", "Sci-Fi", 
                                    "Fantasy", "Biography", "History", "Science", "Self-Help"
                                ], index=["Fiction", "Non-Fiction", "Mystery", "Romance", "Sci-Fi", 
                                         "Fantasy", "Biography", "History", "Science", "Self-Help"].index(book.genre))
                            with edit_col2:
                                new_year = st.number_input("Year", value=book.year)
                                new_isbn = st.text_input("ISBN", value=book.isbn)
                                new_tags = st.text_input("Tags", value=", ".join(book.tags))
                            
                            new_summary = st.text_area("Summary", value=book.summary)
                            
                            col_save, col_cancel = st.columns(2)
                            with col_save:
                                if st.form_submit_button("Save Changes"):
                                    updated_book = Book(
                                        id=book.id,
                                        title=new_title,
                                        author=new_author,
                                        genre=new_genre,
                                        year=new_year,
                                        isbn=new_isbn,
                                        tags=[tag.strip() for tag in new_tags.split(",") if tag.strip()],
                                        is_borrowed=book.is_borrowed,
                                        borrower_name=book.borrower_name,
                                        due_date=book.due_date,
                                        summary=new_summary
                                    )
                                    library_manager.update_book(book.id, updated_book)
                                    st.session_state[f"editing_{book.id}"] = False
                                    st.rerun()
                            
                            with col_cancel:
                                if st.form_submit_button("Cancel"):
                                    st.session_state[f"editing_{book.id}"] = False
                                    st.rerun()
                    
                    st.divider()
        else:
            st.info("No books in the library yet. Add your first book above!")
    
    elif page == "🔄 Check-In/Out":
        st.header("Check-In / Check-Out")
        
        available_books = [book for book in library_manager.books if not book.is_borrowed]
        borrowed_books = [book for book in library_manager.books if book.is_borrowed]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📤 Check Out Books")
            if available_books:
                book_options = {f"{book.title} by {book.author}": book.id for book in available_books}
                selected_book = st.selectbox("Select book to check out", list(book_options.keys()))
                borrower_name = st.text_input("Borrower name")
                days = st.number_input("Loan period (days)", min_value=1, max_value=90, value=14)
                
                if st.button("Check Out"):
                    if borrower_name:
                        library_manager.check_out_book(book_options[selected_book], borrower_name, days)
                        st.success(f"Checked out '{selected_book}' to {borrower_name}")
                        st.rerun()
                    else:
                        st.error("Please enter borrower name")
            else:
                st.info("No books available for checkout")
        
        with col2:
            st.subheader("📥 Check In Books")
            if borrowed_books:
                return_options = {f"{book.title} (Due: {book.due_date})": book.id for book in borrowed_books}
                selected_return = st.selectbox("Select book to return", list(return_options.keys()))
                
                if st.button("Check In"):
                    library_manager.check_in_book(return_options[selected_return])
                    st.success(f"Checked in '{selected_return.split(' (Due:')[0]}'")
                    st.rerun()
            else:
                st.info("No books currently checked out")
        
        # Show overdue books
        if borrowed_books:
            st.subheader("⚠️ Status Overview")
            overdue_books = []
            for book in borrowed_books:
                if book.due_date and datetime.strptime(book.due_date, "%Y-%m-%d") < datetime.now():
                    overdue_books.append(book)
            
            if overdue_books:
                st.error(f"**{len(overdue_books)} Overdue Books:**")
                for book in overdue_books:
                    st.write(f"- {book.title} (Due: {book.due_date}, Borrower: {book.borrower_name})")
            else:
                st.success("All borrowed books are current")
    
    elif page == "🔍 Search & Browse":
        st.header("Search & Browse")
        
        # Search interface
        search_col1, search_col2 = st.columns([3, 1])
        with search_col1:
            search_query = st.text_input("🔍 Search books...", placeholder="Enter title, author, genre, or tags")
        with search_col2:
            search_filter = st.selectbox("Filter by", ["All", "Available", "Borrowed"])
        
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
        
        # Genre filter
        genres = list(set(book.genre for book in library_manager.books))
        selected_genres = st.multiselect("Filter by genres", genres)
        if selected_genres:
            filtered_books = [book for book in filtered_books if book.genre in selected_genres]
        
        # Display results
        st.write(f"Found {len(filtered_books)} books")
        
        for book in filtered_books:
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    status = "🔴 Borrowed" if book.is_borrowed else "🟢 Available"
                    st.write(f"**{book.title}** by {book.author} | {status}")
                    st.write(f"*{book.genre} ({book.year})* | Tags: {', '.join(book.tags) if book.tags else 'None'}")
                    if book.summary:
                        st.write(f"📝 {book.summary}")
                    if book.is_borrowed:
                        st.write(f"📅 Due: {book.due_date} | Borrower: {book.borrower_name}")
                
                with col2:
                    if st.button("📚 Find Similar", key=f"search_recommend_{book.id}"):
                        st.session_state[f"search_show_recommendations_{book.id}"] = True
                
                # Show recommendations in search
                if st.session_state.get(f"search_show_recommendations_{book.id}", False):
                    st.write("---")
                    st.write(f"**📚 Books similar to '{book.title}':**")
                    
                    recommendations = ai_assistant.get_simple_recommendations(library_manager.books, book)
                    
                    if recommendations:
                        for rec_book in recommendations:
                            rec_status = "🔴 Borrowed" if rec_book.is_borrowed else "🟢 Available"
                            st.write(f"  {rec_status} **{rec_book.title}** by {rec_book.author} ({rec_book.genre})")
                            
                            # Show why it's recommended
                            reasons = []
                            if rec_book.genre == book.genre:
                                reasons.append(f"Same genre ({book.genre})")
                            if rec_book.tags and book.tags:
                                common_tags = set(rec_book.tags) & set(book.tags)
                                if common_tags:
                                    reasons.append(f"Similar themes: {', '.join(list(common_tags)[:2])}")
                            
                            if reasons:
                                st.write(f"    💡 *{', '.join(reasons)}*")
                    
                    if st.button("❌ Hide Similar Books", key=f"search_hide_rec_{book.id}"):
                        st.session_state[f"search_show_recommendations_{book.id}"] = False
                        st.rerun()
                
                st.divider()
    
    elif page == "🤖 AI Features":
        st.header("AI-Powered Features")
        
        tab1, tab2, tab3 = st.tabs(["📖 Book Summaries", "📚 Recommendations", "🧠 Library Insights"])
        
        with tab1:
            st.subheader("Generate Book Summary")
            if library_manager.books:
                books_without_summary = [book for book in library_manager.books if not book.summary]
                if books_without_summary:
                    book_options = {f"{book.title} by {book.author}": book for book in books_without_summary}
                    selected_book_title = st.selectbox("Select book for AI summary", list(book_options.keys()))
                    
                    if st.button("Generate Summary"):
                        selected_book = book_options[selected_book_title]
                        with st.spinner("Generating AI summary..."):
                            summary = ai_assistant.generate_book_summary(
                                selected_book.title, selected_book.author, selected_book.genre, selected_book.year
                            )
                            selected_book.summary = summary
                            library_manager.update_book(selected_book.id, selected_book)
                            st.success("Summary generated and saved!")
                            st.write(summary)
                            st.rerun()
                else:
                    st.info("All books already have summaries!")
            else:
                st.info("Add some books first to generate summaries")
        
        with tab2:
            st.subheader("Get Reading Recommendations")
            if len(library_manager.books) >= 2:
                book_options = {f"{book.title} by {book.author}": book for book in library_manager.books}
                selected_book_title = st.selectbox("Based on this book...", list(book_options.keys()), key="rec_book")
                
                if st.button("Get Recommendations"):
                    selected_book = book_options[selected_book_title]
                    with st.spinner("Generating recommendations..."):
                        recommendations = ai_assistant.get_reading_recommendations(library_manager.books, selected_book)
                        st.write("**AI Recommendations:**")
                        for rec in recommendations:
                            if rec.strip():
                                st.write(rec)
            else:
                st.info("Add at least 2 books to get recommendations")
        
        with tab3:
            st.subheader("Library Analytics & Insights")
            if library_manager.books:
                if st.button("Generate AI Insights"):
                    with st.spinner("Analyzing your library..."):
                        insights = ai_assistant.get_library_insights(library_manager.books)
                        st.write("**AI Library Analysis:**")
                        st.write(insights)
            else:
                st.info("Add some books first to get insights")
    
    elif page == "📊 Analytics":
        st.header("Library Analytics")
        
        if library_manager.books:
            # Basic stats
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Books", len(library_manager.books))
            with col2:
                borrowed_count = sum(1 for book in library_manager.books if book.is_borrowed)
                st.metric("Currently Borrowed", borrowed_count)
            with col3:
                available_count = len(library_manager.books) - borrowed_count
                st.metric("Available", available_count)
            with col4:
                overdue_count = sum(1 for book in library_manager.books 
                                   if book.is_borrowed and book.due_date and 
                                   datetime.strptime(book.due_date, "%Y-%m-%d") < datetime.now())
                st.metric("Overdue", overdue_count)
            
            # Genre distribution
            st.subheader("📈 Genre Distribution")
            genre_counts = {}
            for book in library_manager.books:
                genre_counts[book.genre] = genre_counts.get(book.genre, 0) + 1
            
            if genre_counts:
                genre_df = pd.DataFrame(list(genre_counts.items()), columns=['Genre', 'Count'])
                st.bar_chart(genre_df.set_index('Genre'))
            
            # Recent activity
            st.subheader("📅 Recent Activity")
            if library_manager.borrowing_history:
                recent_history = sorted(library_manager.borrowing_history, 
                                      key=lambda x: x.get('checkout_date', x.get('return_date', '')), 
                                      reverse=True)[:10]
                
                for activity in recent_history:
                    if activity['action'] == 'checkout':
                        st.write(f"📤 {activity['checkout_date']}: {activity['book_title']} checked out to {activity['borrower_name']}")
                    else:
                        st.write(f"📥 {activity['return_date']}: {activity['book_title']} returned by {activity['borrower_name']}")
            else:
                st.info("No borrowing activity yet")
        else:
            st.info("No books in library yet")

if __name__ == "__main__":
    main()