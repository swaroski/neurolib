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
    
    def generate_book_summary(self, title: str, author: str, genre: str) -> str:
        try:
            prompt = f"Generate a concise 2-3 sentence summary for a book titled '{title}' by {author} in the {genre} genre. Focus on what makes this book interesting."
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Could not generate summary: {str(e)}"
    
    def get_reading_recommendations(self, books: List[Book], current_book: Book) -> List[str]:
        try:
            book_list = "\n".join([f"- {book.title} by {book.author} ({book.genre})" for book in books[:10]])
            prompt = f"""Based on this library collection:
{book_list}

Someone enjoyed '{current_book.title}' by {current_book.author} ({current_book.genre}).
Recommend 3 similar books from this collection and explain why in 1-2 sentences each."""
            
            response = self.model.generate_content(prompt)
            return response.text.strip().split('\n')
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

def main():
    st.title("📚 AI-Powered Library Management System")
    st.markdown("*Manage your library with intelligent features powered by Gemini AI*")
    
    # Initialize managers
    if 'library_manager' not in st.session_state:
        st.session_state.library_manager = LibraryManager()
    
    if 'ai_assistant' not in st.session_state:
        st.session_state.ai_assistant = AIAssistant()
    
    library_manager = st.session_state.library_manager
    ai_assistant = st.session_state.ai_assistant
    
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
                            summary = ai_assistant.generate_book_summary(title, author, genre)
                    
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
                        if st.button("Edit", key=f"edit_{book.id}"):
                            st.session_state[f"editing_{book.id}"] = True
                    
                    with col3:
                        if st.button("Delete", key=f"delete_{book.id}"):
                            library_manager.delete_book(book.id)
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
                col1, col2 = st.columns([4, 1])
                with col1:
                    status = "🔴 Borrowed" if book.is_borrowed else "🟢 Available"
                    st.write(f"**{book.title}** by {book.author} | {status}")
                    st.write(f"*{book.genre} ({book.year})* | Tags: {', '.join(book.tags) if book.tags else 'None'}")
                    if book.summary:
                        st.write(f"📝 {book.summary}")
                with col2:
                    if book.is_borrowed:
                        st.write(f"Due: {book.due_date}")
                        st.write(f"Borrower: {book.borrower_name}")
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
                                selected_book.title, selected_book.author, selected_book.genre
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