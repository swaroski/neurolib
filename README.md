# 📚 AI-Powered Library Management System

A modern, intelligent library management system built with Streamlit and powered by Google's Gemini AI. Perfect for personal, school, or small community libraries.

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

### 🎨 User Experience
- **Clean, Intuitive Interface**: Beautiful Streamlit-based UI with emojis and clear navigation
- **Real-time Updates**: Instant feedback and automatic data persistence
- **Responsive Design**: Works seamlessly across different screen sizes
- **Visual Status Indicators**: Easy-to-understand book availability status

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Google API Key for Gemini AI

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd neurolib
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Gemini AI**:
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Set it as an environment variable:
     ```bash
     export GOOGLE_API_KEY="your-api-key-here"
     ```
   - Or create a `.streamlit/secrets.toml` file:
     ```toml
     GOOGLE_API_KEY = "your-api-key-here"
     ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** to `http://localhost:8501`

## 📖 Usage Guide

### Managing Books
1. Navigate to **📖 Book Management**
2. Use **➕ Add New Book** to add books with optional AI summary generation
3. Edit or delete existing books using the action buttons
4. All changes are automatically saved

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

### AI Features
1. Access **🤖 AI Features** for intelligent capabilities
2. **Book Summaries**: Generate AI-powered summaries for your books
3. **Recommendations**: Get personalized reading suggestions
4. **Library Insights**: Receive AI analysis of your collection

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
neurolib/
├── app.py              # Main application
├── requirements.txt    # Python dependencies
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

✅ **Bonus Features**:
- Visual status indicators
- Overdue book tracking
- Borrowing history
- Genre-based filtering
- Real-time search
- Comprehensive analytics dashboard
- Beautiful, polished UI

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
