# 🏠 BookNest - AI-Powered Library Management System

A modern, intelligent library management system with beautiful UI/UX, built with Streamlit and powered by Google's Gemini AI. Perfect for personal, school, or small community libraries.

```
  ╔══════════════════════════════════════╗
  ║            📚 BookNest 🏠            ║
  ║        AI Library Management         ║
  ╚══════════════════════════════════════╝
```

## ✨ Features

### 📘 Core Library Management
- **Book Management**: Add, edit, and delete books with comprehensive metadata
- **Check-In/Check-Out**: Track borrowed books with due dates and borrower information
- **Smart Search**: Real-time search by title, author, genre, or tags with filtering options
- **Status Tracking**: Visual indicators for available vs. borrowed books

### 🤖 AI-Powered Features (Gemini AI)
- **📖 Book Summary Generator**: Automatically generate engaging book summaries
- **📚 Reading Recommendations**: Get personalized book suggestions based on your collection
- **🧠 Smart Library Insights**: AI analysis of your collection with trends and recommendations
- **📊 Intelligent Analytics**: Data-driven insights about your library usage

### 🌐 Open Library Integration
- **🔍 Search & Import**: Search millions of books from Open Library database
- **📚 Real Book Data**: Import books with accurate metadata, covers, and descriptions
- **⚡ Quick Import**: One-click import buttons for popular book series
- **🏷️ Auto-Categorization**: Automatic genre classification and tagging
- **📖 Cover Images**: Real book covers from Open Library's collection

### 🎨 Enhanced User Experience
- **Modern Card-Based Layout**: Netflix/Open Library inspired design with book cover thumbnails
- **Status Badges**: Color-coded availability indicators (Available/Borrowed/Overdue)
- **Toast Notifications**: Real-time feedback for all user actions
- **Responsive Design**: Mobile-friendly interface that works on all devices
- **Interactive Elements**: Hover effects, smooth transitions, and visual feedback
- **Stats Dashboard**: Real-time overview of library metrics and activity
- **Floating AI Chat**: Always-available AI librarian assistant
- **Clean Navigation**: Icon-based tabs with intuitive organization

## 🚀 Quick Start

### 🌐 **Try Online (Recommended)**
**Live Demo**: [https://neurolib.streamlit.app/](https://neurolib.streamlit.app/)

The app automatically loads with 20 sample books including classics, sci-fi, mystery, and more! 

### 🏠 **Local Development**

#### Prerequisites
- Python 3.8+ (Recommended: Python 3.11+)
- Google API Key for Gemini AI (optional, for AI features)

#### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd neurolib
   ```

2. **Set up environment** (see Setup section below for details)

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Gemini AI** (Optional):
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Set it as an environment variable:
     ```bash
     export GOOGLE_API_KEY="your-api-key-here"
     ```
   - Or create a `.streamlit/secrets.toml` file:
     ```toml
     GOOGLE_API_KEY = "your-api-key-here"
     ```

5. **Run the application**:
   ```bash
   # Main application (works both locally and on Streamlit Cloud)
   streamlit run app.py
   
   # Or use launcher scripts for local development
   python run_api_version.py      # With Open Library integration
   python run_enhanced.py         # Enhanced UI version
   ```

6. **Open your browser** to `http://localhost:8501`

### 📚 Sample Data
The system comes pre-loaded with **30 diverse books** including detailed summaries:
- **Fiction**: To Kill a Mockingbird, 1984, The Great Gatsby
- **Fantasy**: Harry Potter, Lord of the Rings, Game of Thrones
- **Sci-Fi**: Dune, Foundation, Hitchhiker's Guide
- **Mystery**: Agatha Christie, Gone Girl, The Silent Patient
- **Non-Fiction**: Sapiens, Educated, Atomic Habits
- **Recent Bestsellers**: Where the Crawdads Sing, The Seven Husbands of Evelyn Hugo
- **Classic Literature**: The Catcher in the Rye, Neuromancer, The Hobbit
- **And many more across 9 different genres!**

**Features of Sample Data:**
- ✅ All 30 books include detailed AI-generated summaries
- 🔴 4 books are currently "borrowed" (2 are overdue for demo)
- 📊 Balanced across genres for testing recommendations
- 📋 5 borrowing history entries to demo analytics

**Quick Setup:** If needed, run `python init_booknest.py` to refresh the sample data.

## ⚙️ Setup

### 🐍 **Local Python Environment**

Choose your preferred method to set up a local Python environment:

#### **Option 1: Using uv (modern Python environment manager)**
```bash
# Create a new virtual environment with uv
uv venv

# Activate it
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies from requirements.txt
uv pip install -r requirements.txt

# Install additional dependencies for enhanced features
uv pip install requests jupyter
```

#### **Option 2: Using python -m venv (standard)**
```bash
# Create a virtual environment
python -m venv .venv

# Activate it
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Install additional dependencies
pip install requests jupyter
```

#### **Option 3: Using conda**
```bash
# Create conda environment
conda create -n booknest python=3.11

# Activate environment
conda activate booknest

# Install dependencies
pip install -r requirements.txt
```

### 🚀 **Streamlit Cloud Deployment**

To deploy your own version on Streamlit Cloud:

1. **Fork this repository** to your GitHub account
2. **Connect to Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Deploy from your forked repository
3. **Configure secrets** (optional, for AI features):
   - In Streamlit Cloud dashboard, go to "Secrets"
   - Add: `GOOGLE_API_KEY = "your-api-key-here"`
4. **Your app will be available** at `https://your-app-name.streamlit.app/`

## 📖 Usage Guide

### 🏠 BookNest Enhanced Interface

#### Navigation
- **📚 My Books**: Browse your collection with beautiful card layouts
- **➕ Add Book**: Clean form with AI summary generation
- **🔍 Search**: Advanced filtering and real-time search
- **📊 Insights**: Analytics dashboard with AI-powered insights

#### Managing Books
1. Navigate to **📚 My Books** to see your collection in card format
2. Use **➕ Add Book** tab for a streamlined book addition process
3. Each book card shows:
   - Book cover placeholder with title
   - Status badge (Available/Borrowed/Overdue)
   - Metadata (genre, year, ISBN, tags)
   - Action buttons (Check Out/In, Edit, AI Summary, Delete)
4. Real-time stats dashboard shows library overview

### Check-In/Check-Out
1. Go to **🔄 Check-In/Out**
2. **Check Out**: Select an available book, enter borrower name, and set loan period
3. **Check In**: Select a borrowed book to return it
4. Monitor overdue books in the status overview

### Search & Browse
1. Visit **🔍 Search & Browse**
2. Use the search bar for real-time filtering
3. Apply additional filters by availability status or genre
4. Browse your entire collection with detailed information

### 🤖 AI Features
1. **Floating AI Librarian**: Click the 🤖 button for instant AI assistance
2. **Book Summaries**: Generate summaries directly from book cards
3. **Smart Recommendations**: Get personalized suggestions based on any book
4. **Library Insights**: AI analysis in the 📊 Insights tab
5. **Chat Interface**: Ask questions like "Which sci-fi books do you recommend?" or "What books are overdue?"

### 🌐 Open Library Integration
1. **Search & Import**: Use the "Import from Open Library" tab
2. **Search Any Book**: Search by title, author, series, or genre
3. **One-Click Import**: Click "Import" on any search result
4. **Quick Import Buttons**: Popular series like Harry Potter, Lord of the Rings
5. **Automatic Enhancement**: All imported books get AI summaries and genre classification
6. **Real Book Covers**: Imported books include actual cover images from Open Library

### Analytics
1. Check **📊 Analytics** for data insights
2. View collection statistics and genre distribution
3. Monitor recent borrowing activity
4. Track overdue items and library usage patterns

## 🛠️ Technical Details

### Architecture
- **Frontend**: Streamlit for interactive web interface
- **Data Storage**: JSON-based persistence (easily upgradeable to database)
- **AI Integration**: Google Gemini AI for intelligent features
- **State Management**: Streamlit session state for real-time updates

### File Structure
```
booknest/
├── app.py              # Original application
├── app_enhanced.py     # Enhanced UI version (recommended)
├── requirements.txt    # Python dependencies  
├── run_app.py         # Original launcher
├── run_enhanced.py    # Enhanced launcher (recommended)
├── init_booknest.py   # Initialize with 30 sample books
├── check_library.py   # Check library status quickly
├── sample_data.py     # Original sample data generator
├── test_recommendations.py # Test recommendation system
├── logo.txt           # Branding and logo information
├── README.md          # This file
├── .gitignore        # Git ignore rules
└── library_data.json # Data storage (auto-generated)
```

### Data Models
- **Book**: Comprehensive book metadata with borrowing status
- **Library Data**: Books collection with borrowing history
- **AI Assistant**: Gemini AI integration for intelligent features

## 🎯 Key Features Implemented

✅ **All Required Features**:
- Book Management (Add/Edit/Delete)
- Check-In/Check-Out system
- Search functionality
- AI-powered book summaries
- Reading recommendations
- Smart search capabilities
- AI insights and analytics

✅ **Enhanced UI/UX Features**:
- **Card-based design** inspired by Netflix/Open Library
- **Status badges** with color coding and animations
- **Toast notifications** for instant feedback
- **Floating AI chatbot** always available
- **Real-time stats dashboard** with metrics
- **Mobile-responsive design** for all devices
- **Interactive elements** with hover effects
- **Modern color scheme** with professional branding
- **Smooth transitions** and visual feedback
- **Intuitive navigation** with icon-based tabs

## 🚀 Deployment

### Streamlit Cloud
1. Push your code to GitHub
2. Connect to [Streamlit Cloud](https://streamlit.io/cloud)
3. Add your `GOOGLE_API_KEY` in the secrets section
4. Deploy and share your live URL

### Other Platforms
- **Replit**: Import repository and set environment variables
- **Vercel**: Deploy with environment variables configured
- **Heroku**: Use Procfile with environment variables

## 🔒 Security Notes

- Never commit API keys to version control
- Use environment variables or Streamlit secrets for sensitive data
- The `.gitignore` file excludes sensitive files and data

## 🤝 Contributing

Feel free to enhance this library system with additional features like:
- User authentication
- Advanced reporting
- Email notifications for overdue books
- Barcode scanning
- Multi-library support

## 📝 License

This project is open source and available under the MIT License.
