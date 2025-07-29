#!/usr/bin/env python3
"""
Initialize BookNest with sample data
"""

import json
import os
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

def create_enhanced_sample_books():
    """Create an enhanced collection of 30 sample books with better summaries"""
    sample_books = [
        # Fiction - Classic Literature
        Book("0001", "To Kill a Mockingbird", "Harper Lee", "Fiction", 1960, "978-0-06-112008-4", 
             ["classic", "social-justice", "coming-of-age"], 
             summary="A powerful story of racial injustice and childhood innocence in the American South, told through the eyes of Scout Finch as her father defends a Black man falsely accused of rape."),
        
        Book("0002", "1984", "George Orwell", "Fiction", 1949, "978-0-452-28423-4", 
             ["dystopian", "political", "classic"], 
             summary="A chilling vision of a totalitarian future where Big Brother watches everything, exploring themes of surveillance, truth, and individual freedom in a world of perpetual war."),
        
        Book("0003", "Pride and Prejudice", "Jane Austen", "Romance", 1813, "978-0-14-143951-8", 
             ["classic", "romance", "regency"], 
             summary="The timeless story of Elizabeth Bennet and Mr. Darcy's complex courtship, filled with wit, social commentary, and one of literature's most satisfying romantic relationships."),
        
        Book("0004", "The Great Gatsby", "F. Scott Fitzgerald", "Fiction", 1925, "978-0-7432-7356-5", 
             ["classic", "american-dream", "jazz-age"], 
             summary="A tragic tale of love, wealth, and the corruption of the American Dream set in the roaring twenties, following Jay Gatsby's obsessive pursuit of Daisy Buchanan."),
        
        Book("0005", "The Catcher in the Rye", "J.D. Salinger", "Fiction", 1951, "978-0-316-76948-0", 
             ["classic", "coming-of-age", "americana"], 
             summary="Holden Caulfield's iconic journey through New York City, exploring themes of alienation, identity, and the loss of innocence in post-war America."),
        
        # Fantasy & Adventure
        Book("0006", "Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "Fantasy", 1997, "978-0-439-70818-8", 
             ["magic", "young-adult", "adventure"], 
             summary="A young wizard discovers his magical heritage and begins his journey at Hogwarts School, launching one of the most beloved fantasy series of all time."),
        
        Book("0007", "The Lord of the Rings", "J.R.R. Tolkien", "Fantasy", 1954, "978-0-544-00341-5", 
             ["epic", "adventure", "middle-earth"], 
             summary="The epic quest to destroy the One Ring and save Middle-earth from darkness, featuring hobbits, wizards, and the ultimate battle between good and evil."),
        
        Book("0008", "A Game of Thrones", "George R.R. Martin", "Fantasy", 1996, "978-0-553-10354-0", 
             ["politics", "medieval", "dragons"], 
             summary="Political intrigue and power struggles in the Seven Kingdoms of Westeros, where noble families play the deadly game of thrones while an ancient evil awakens."),
        
        Book("0009", "The Name of the Wind", "Patrick Rothfuss", "Fantasy", 2007, "978-0-7564-0474-1", 
             ["magic", "music", "storytelling"], 
             summary="The legendary tale of Kvothe, told by the man himself—a story of magic, music, and the making of a legend in a beautifully crafted fantasy world."),
        
        Book("0010", "The Hobbit", "J.R.R. Tolkien", "Fantasy", 1937, "978-0-547-92822-7", 
             ["adventure", "dwarves", "dragon"], 
             summary="Bilbo Baggins' unexpected adventure with thirteen dwarves to reclaim their homeland from the dragon Smaug, setting the stage for the Lord of the Rings."),
        
        # Science Fiction
        Book("0011", "Dune", "Frank Herbert", "Sci-Fi", 1965, "978-0-441-17271-9", 
             ["space-opera", "politics", "ecology"], 
             summary="Epic tale of politics, religion, and ecology on the desert planet Arrakis, following Paul Atreides as he becomes a messianic leader in a complex galactic empire."),
        
        Book("0012", "The Hitchhiker's Guide to the Galaxy", "Douglas Adams", "Sci-Fi", 1979, "978-0-345-39180-3", 
             ["humor", "space", "adventure"], 
             summary="A hilarious journey through space with Arthur Dent and his alien friend Ford Prefect, featuring towels, paranoid androids, and the answer to life, the universe, and everything."),
        
        Book("0013", "Foundation", "Isaac Asimov", "Sci-Fi", 1951, "978-0-553-29335-0", 
             ["space", "mathematics", "empire"], 
             summary="The rise and fall of a galactic empire, guided by the science of psychohistory and Hari Seldon's plan to preserve knowledge through a coming dark age."),
        
        Book("0014", "Neuromancer", "William Gibson", "Sci-Fi", 1984, "978-0-441-56956-6", 
             ["cyberpunk", "technology", "virtual-reality"], 
             summary="The cyberpunk masterpiece that defined a genre, following console cowboy Case as he's hired for the ultimate hack in cyberspace."),
        
        Book("0015", "The Martian", "Andy Weir", "Sci-Fi", 2011, "978-0-553-41802-6", 
             ["mars", "survival", "science"], 
             summary="Mark Watney's incredible survival story on Mars, combining hard science with humor as he 'sciences the hell' out of impossible problems."),
        
        # Mystery & Thriller
        Book("0016", "The Murder of Roger Ackroyd", "Agatha Christie", "Mystery", 1926, "978-0-06-207350-4", 
             ["detective", "classic", "whodunit"], 
             summary="Hercule Poirot investigates a shocking murder with an unexpected twist that revolutionized the mystery genre and remains controversial to this day."),
        
        Book("0017", "The Girl with the Dragon Tattoo", "Stieg Larsson", "Mystery", 2005, "978-0-307-94930-4", 
             ["thriller", "crime", "sweden"], 
             summary="A journalist and a hacker uncover dark family secrets in Sweden, launching the acclaimed Millennium trilogy with unforgettable characters."),
        
        Book("0018", "Gone Girl", "Gillian Flynn", "Mystery", 2012, "978-0-307-58836-4", 
             ["psychological", "thriller", "marriage"], 
             summary="A marriage's dark secrets are revealed when Amy Dunne mysteriously disappears on her fifth wedding anniversary, leaving her husband Nick as the prime suspect."),
        
        Book("0019", "The Silent Patient", "Alex Michaelides", "Mystery", 2019, "978-1-250-30170-7", 
             ["psychological", "thriller", "art"], 
             summary="A psychotherapist becomes obsessed with treating a woman who refuses to speak after allegedly murdering her husband, leading to a shocking conclusion."),
        
        Book("0020", "In the Woods", "Tana French", "Mystery", 2007, "978-0-670-03860-2", 
             ["detective", "psychological", "ireland"], 
             summary="A haunting detective story set in Ireland, where a child's murder echoes a detective's own traumatic past, blending mystery with literary fiction."),
        
        # Non-Fiction & Biography
        Book("0021", "Sapiens", "Yuval Noah Harari", "Non-Fiction", 2011, "978-0-06-231609-7", 
             ["history", "anthropology", "evolution"], 
             summary="A sweeping look at the history and impact of Homo sapiens on Earth, from the Stone Age to the present, exploring how we became the dominant species."),
        
        Book("0022", "Educated", "Tara Westover", "Biography", 2018, "978-0-399-59050-4", 
             ["memoir", "education", "family"], 
             summary="A powerful memoir about education's transformative power, following Tara's journey from a survivalist family in Idaho to earning a PhD from Cambridge."),
        
        Book("0023", "The Immortal Life of Henrietta Lacks", "Rebecca Skloot", "Science", 2010, "978-1-4000-5217-2", 
             ["medical", "ethics", "biography"], 
             summary="The incredible story of cells that revolutionized medical science and the African American woman behind them, exploring ethics, race, and scientific progress."),
        
        Book("0024", "Becoming", "Michelle Obama", "Biography", 2018, "978-1-5247-6313-8", 
             ["memoir", "politics", "inspiration"], 
             summary="The former First Lady's powerful memoir of her journey from Chicago's South Side to the White House, sharing personal stories of triumph and resilience."),
        
        Book("0025", "Atomic Habits", "James Clear", "Self-Help", 2018, "978-0-7352-1129-2", 
             ["productivity", "habits", "psychology"], 
             summary="A proven system for building good habits and breaking bad ones, showing how small changes can create remarkable results over time."),
        
        # Additional Diverse Selections
        Book("0026", "Where the Crawdads Sing", "Delia Owens", "Fiction", 2018, "978-0-7352-1909-0", 
             ["nature", "mystery", "coming-of-age"], 
             summary="Kya the 'Marsh Girl' grows up isolated in North Carolina's coastal marshes, weaving together a murder mystery with a beautiful coming-of-age story."),
        
        Book("0027", "The Seven Husbands of Evelyn Hugo", "Taylor Jenkins Reid", "Fiction", 2017, "978-1-5011-3981-6", 
             ["hollywood", "lgbtq", "secrets"], 
             summary="Reclusive Hollywood icon Evelyn Hugo finally tells her life story, revealing the truth about her seven marriages and the price of fame and love."),
        
        Book("0028", "Circe", "Madeline Miller", "Fantasy", 2018, "978-0-316-55633-4", 
             ["mythology", "greek-gods", "feminism"], 
             summary="The enchanting story of Circe, the banished witch of Greek mythology, as she discovers her powers and finds her voice in a world of gods and monsters."),
        
        Book("0029", "The Thursday Murder Club", "Richard Osman", "Mystery", 2020, "978-0-241-42525-6", 
             ["cozy-mystery", "elderly", "friendship"], 
             summary="Four retirees in a peaceful retirement village meet weekly to investigate cold cases, until they find themselves in the middle of a real murder mystery."),
        
        Book("0030", "Klara and the Sun", "Kazuo Ishiguro", "Sci-Fi", 2021, "978-0-571-36487-1", 
             ["artificial-intelligence", "humanity", "love"], 
             summary="From the perspective of an artificial friend, this touching story explores what it means to love and be human in a world of advancing technology.")
    ]
    
    # Add some borrowed books for demonstration
    sample_books[2].is_borrowed = True  # Pride and Prejudice
    sample_books[2].borrower_name = "Alice Johnson"
    sample_books[2].due_date = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
    
    sample_books[11].is_borrowed = True  # Hitchhiker's Guide
    sample_books[11].borrower_name = "Bob Smith"
    sample_books[11].due_date = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
    
    sample_books[22].is_borrowed = True  # Immortal Life of Henrietta Lacks
    sample_books[22].borrower_name = "Carol Davis"
    sample_books[22].due_date = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")  # Overdue
    
    sample_books[16].is_borrowed = True  # Girl with Dragon Tattoo
    sample_books[16].borrower_name = "David Wilson"
    sample_books[16].due_date = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")  # Overdue
    
    return sample_books

def create_enhanced_history():
    """Create enhanced borrowing history"""
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
            'book_id': '0013',
            'book_title': 'Foundation',
            'borrower_name': 'Jane Smith',
            'checkout_date': '2024-01-20',
            'return_date': '2024-02-03',
            'action': 'checkin'
        },
        {
            'book_id': '0004',
            'book_title': 'The Great Gatsby',
            'borrower_name': 'Mike Wilson',
            'checkout_date': '2024-01-25',
            'return_date': '2024-02-08',
            'action': 'checkin'
        },
        {
            'book_id': '0007',
            'book_title': 'The Lord of the Rings',
            'borrower_name': 'Sarah Brown',
            'checkout_date': '2024-02-01',
            'return_date': '2024-02-15',
            'action': 'checkin'
        },
        {
            'book_id': '0021',
            'book_title': 'Sapiens',
            'borrower_name': 'Tom Anderson',
            'checkout_date': '2024-02-05',
            'return_date': '2024-02-19',
            'action': 'checkin'
        }
    ]
    return history

def initialize_booknest():
    """Initialize BookNest with enhanced sample data"""
    print("🏠 Initializing BookNest with enhanced sample data...")
    
    books = create_enhanced_sample_books()
    history = create_enhanced_history()
    
    data = {
        'books': [asdict(book) for book in books],
        'borrowing_history': history
    }
    
    # Backup existing data if it exists
    if os.path.exists('library_data.json'):
        print("📋 Backing up existing data...")
        import shutil
        shutil.copy('library_data.json', 'library_data_backup.json')
    
    # Write new enhanced data
    with open('library_data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ BookNest initialized with {len(books)} books!")
    print("\n📚 Sample collection includes:")
    
    genres = {}
    borrowed_count = 0
    overdue_count = 0
    
    for book in books:
        genres[book.genre] = genres.get(book.genre, 0) + 1
        if book.is_borrowed:
            borrowed_count += 1
            if book.due_date and datetime.strptime(book.due_date, "%Y-%m-%d") < datetime.now():
                overdue_count += 1
    
    for genre, count in sorted(genres.items()):
        print(f"  • {genre}: {count} books")
    
    print(f"\n📊 Library Statistics:")
    print(f"  • Total books: {len(books)}")
    print(f"  • Currently borrowed: {borrowed_count}")
    print(f"  • Overdue books: {overdue_count}")
    print(f"  • Borrowing history entries: {len(history)}")
    
    print(f"\n🚀 Ready to launch BookNest!")
    print(f"   Run: python run_enhanced.py")

if __name__ == "__main__":
    initialize_booknest()