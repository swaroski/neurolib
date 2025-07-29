#!/usr/bin/env python3
"""
Enhanced launcher script for BookNest - AI Library Management System
"""

import os
import sys
import subprocess

def main():
    print("🏠 Starting BookNest - AI Library Management System...")
    print("=" * 60)
    
    # Check if required dependencies are installed
    try:
        import streamlit
        import google.generativeai
        print("✅ All dependencies are installed")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return
    
    # Check for API key
    if not os.environ.get('GOOGLE_API_KEY'):
        print("\n⚠️  WARNING: GOOGLE_API_KEY not found in environment variables")
        print("AI features will not work without a valid API key.")
        print("\nTo set your API key:")
        print("export GOOGLE_API_KEY='your-api-key-here'")
        print("\nOr create .streamlit/secrets.toml with:")
        print("GOOGLE_API_KEY = 'your-api-key-here'")
        
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            return
    else:
        print("✅ Google API key found")
    
    print("\n🏠 BookNest Enhanced Features:")
    print("┌─────────────────────────────────────────────┐")
    print("│ 📚 25 sample books pre-loaded               │")
    print("│ 🎨 Modern card-based UI design              │")
    print("│ 📊 Real-time stats dashboard               │")
    print("│ 🔍 Advanced search and filtering           │")
    print("│ 🤖 AI-powered book summaries               │")
    print("│ 💬 Floating AI librarian chatbot          │")
    print("│ ✅ Toast notifications for actions         │")
    print("│ 📱 Responsive mobile-friendly design       │")
    print("│ 🏷️ Status badges (Available/Borrowed/Overdue)│")
    print("│ 📈 Analytics and insights dashboard        │")
    print("└─────────────────────────────────────────────┘")
    
    print(f"\n🌐 Starting BookNest on http://localhost:8501")
    print("\n💡 Pro Tips:")
    print("• Use the floating 🤖 button for AI assistance")
    print("• Click on status badges to see book details")
    print("• Try the AI summary generator for new books")
    print("• Check the Insights tab for library analytics")
    
    print("\n🚀 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Launch Streamlit with enhanced app
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app_enhanced.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Thanks for using BookNest!")
        print("🌟 Your AI-powered library management system")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error starting BookNest: {e}")

if __name__ == "__main__":
    main()