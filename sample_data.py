import json
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
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

def create_sample_books():
    """Create a diverse collection of 25 sample books"""
    sample_books = [
        # Fiction
        Book("0001", "To Kill a Mockingbird", "Harper Lee", "Fiction", 1960, "978-0-06-112008-4", 
             ["classic", "social justice", "coming-of-age"], summary="A powerful story of racial injustice and childhood innocence in the American South."),
        
        Book("0002", "1984", "George Orwell", "Fiction", 1949, "978-0-452-28423-4", 
             ["dystopian", "political", "classic"], summary="A chilling vision of a totalitarian future where Big Brother watches everything."),
        
        Book("0003", "Pride and Prejudice", "Jane Austen", "Romance", 1813, "978-0-14-143951-8", 
             ["classic", "romance", "regency"], summary="The timeless story of Elizabeth Bennet and Mr. Darcy's complex courtship."),
        
        Book("0004", "The Great Gatsby", "F. Scott Fitzgerald", "Fiction", 1925, "978-0-7432-7356-5", 
             ["classic", "american-dream", "jazz-age"], summary="A tragic tale of love, wealth, and the corruption of the American Dream."),
        
        Book("0005", "Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "Fantasy", 1997, "978-0-439-70818-8", 
             ["magic", "young-adult", "adventure"], summary="A young wizard discovers his magical heritage and begins his journey at Hogwarts."),
        
        # Science Fiction
        Book("0006", "Dune", "Frank Herbert", "Sci-Fi", 1965, "978-0-441-17271-9", 
             ["space-opera", "politics", "ecology"], summary="Epic tale of politics, religion, and ecology on the desert planet Arrakis."),
        
        Book("0007", "The Hitchhiker's Guide to the Galaxy", "Douglas Adams", "Sci-Fi", 1979, "978-0-345-39180-3", 
             ["humor", "space", "adventure"], summary="A hilarious journey through space with an unwitting human and his alien friend."),
        
        Book("0008", "Foundation", "Isaac Asimov", "Sci-Fi", 1951, "978-0-553-29335-0", 
             ["space", "mathematics", "empire"], summary="The rise and fall of a galactic empire, guided by the science of psychohistory."),
        
        # Mystery
        Book("0009", "The Murder of Roger Ackroyd", "Agatha Christie", "Mystery", 1926, "978-0-06-207350-4", 
             ["detective", "classic", "whodunit"], summary="Hercule Poirot investigates a shocking murder with an unexpected twist."),
        
        Book("0010", "The Girl with the Dragon Tattoo", "Stieg Larsson", "Mystery", 2005, "978-0-307-94930-4", 
             ["thriller", "crime", "sweden"], summary="A journalist and a hacker uncover dark family secrets in Sweden."),
        
        Book("0011", "Gone Girl", "Gillian Flynn", "Mystery", 2012, "978-0-307-58836-4", 
             ["psychological", "thriller", "marriage"], summary="A marriage's dark secrets are revealed when a wife mysteriously disappears."),
        
        # Non-Fiction
        Book("0012", "Sapiens", "Yuval Noah Harari", "Non-Fiction", 2011, "978-0-06-231609-7", 
             ["history", "anthropology", "evolution"], summary="A sweeping look at the history and impact of Homo sapiens on Earth."),
        
        Book("0013", "Educated", "Tara Westover", "Biography", 2018, "978-0-399-59050-4", 
             ["memoir", "education", "family"], summary="A powerful memoir about education's transformative power and family loyalty."),
        
        Book("0014", "The Immortal Life of Henrietta Lacks", "Rebecca Skloot", "Science", 2010, "978-1-4000-5217-2", 
             ["medical", "ethics", "biography"], summary="The story of cells that revolutionized medical science and the woman behind them."),
        
        # Fantasy
        Book("0015", "The Lord of the Rings", "J.R.R. Tolkien", "Fantasy", 1954, "978-0-544-00341-5", 
             ["epic", "adventure", "middle-earth"], summary="The epic quest to destroy the One Ring and save Middle-earth from darkness."),
        
        Book("0016", "A Game of Thrones", "George R.R. Martin", "Fantasy", 1996, "978-0-553-10354-0", 
             ["politics", "medieval", "dragons"], summary="Political intrigue and power struggles in the Seven Kingdoms of Westeros."),
        
        Book("0017", "The Name of the Wind", "Patrick Rothfuss", "Fantasy", 2007, "978-0-7564-0474-1", 
             ["magic", "music", "storytelling"], summary="The legendary tale of Kvothe, told by the man himself."),
        
        # Self-Help
        Book("0018", "Atomic Habits", "James Clear", "Self-Help", 2018, "978-0-7352-1129-2", 
             ["productivity", "habits", "psychology"], summary="A proven system for building good habits and breaking bad ones."),
        
        Book("0019", "The 7 Habits of Highly Effective People", "Stephen Covey", "Self-Help", 1989, "978-1-982-13761-9", 
             ["leadership", "productivity", "success"], summary="Timeless principles for personal and professional effectiveness."),
        
        # History
        Book("0020", "The Guns of August", "Barbara Tuchman", "History", 1962, "978-0-345-47609-8", 
             ["world-war-1", "politics", "military"], summary="A masterful account of the first month of World War I."),
        
        Book("0021", "A People's History of the United States", "Howard Zinn", "History", 1980, "978-0-06-083865-2", 
             ["american-history", "social-justice", "politics"], summary="American history told from the perspective of ordinary people and marginalized groups."),
        
        # More diverse genres
        Book("0022", "The Alchemist", "Paulo Coelho", "Fiction", 1988, "978-0-06-112241-5", 
             ["philosophy", "adventure", "spiritual"], summary="A shepherd's journey to find treasure leads to self-discovery."),
        
        Book("0023", "Becoming", "Michelle Obama", "Biography", 2018, "978-1-5247-6313-8", 
             ["memoir", "politics", "inspiration"], summary="The former First Lady's powerful memoir of her journey from Chicago to the White House."),
        
        Book("0024", "The Silent Patient", "Alex Michaelides", "Mystery", 2019, "978-1-250-30170-7", 
             ["psychological", "thriller", "art"], summary="A psychotherapist becomes obsessed with treating a woman who refuses to speak."),
        
        Book("0025", "Where the Crawdads Sing", "Delia Owens", "Fiction", 2018, "978-0-7352-1909-0", 
             ["nature", "mystery", "coming-of-age"], summary="A nature-loving girl grows up isolated in the marshes of North Carolina.")
    ]
    
    # Add some borrowed books for testing
    sample_books[2].is_borrowed = True  # Pride and Prejudice
    sample_books[2].borrower_name = "Alice Johnson"
    sample_books[2].due_date = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
    
    sample_books[6].is_borrowed = True  # Hitchhiker's Guide
    sample_books[6].borrower_name = "Bob Smith"
    sample_books[6].due_date = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
    
    sample_books[13].is_borrowed = True  # Immortal Life of Henrietta Lacks
    sample_books[13].borrower_name = "Carol Davis"
    sample_books[13].due_date = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")  # Overdue
    
    return sample_books

def create_sample_history():
    """Create sample borrowing history"""
    history = [
        {
            'book_id': '0001',
            'book_title': 'To Kill a Mockingbird',
            'borrower_name': 'John Doe',
            'checkout_date': '2024-01-15',
            'return_date': '2024-01-29',
            'action': 'checkin'
        },
        {
            'book_id': '0008',
            'book_title': 'Foundation',
            'borrower_name': 'Jane Smith',
            'checkout_date': '2024-01-20',
            'return_date': '2024-02-03',
            'action': 'checkin'
        },
        {
            'book_id': '0002',
            'book_title': '1984',
            'borrower_name': 'Mike Wilson',
            'checkout_date': '2024-01-25',
            'return_date': '2024-02-08',
            'action': 'checkin'
        }
    ]
    return history

def populate_library():
    """Create and save sample library data"""
    books = create_sample_books()
    history = create_sample_history()
    
    data = {
        'books': [asdict(book) for book in books],
        'borrowing_history': history
    }
    
    with open('library_data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Created library with {len(books)} books and {len(history)} history entries")
    print("Sample books include:")
    for book in books[:5]:
        status = "🔴 Borrowed" if book.is_borrowed else "🟢 Available"
        print(f"  {status} {book.title} by {book.author} ({book.genre})")
    print("  ... and 20 more books!")

if __name__ == "__main__":
    populate_library()