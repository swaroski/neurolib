#!/usr/bin/env python3
"""
BookNest with Open Library API Integration
"""

import os
import sys
import subprocess

def main():
    print("🏠 Starting BookNest with Open Library Integration...")
    print("=" * 60)
    
    # Check if required dependencies are installed
    try:
        import streamlit
        import requests
        import google.generativeai
        print("✅ All dependencies are installed")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Installing requests...")
        subprocess.run([sys.executable, "-m", "pip", "install", "requests"])
        return
    
    # Check for API key
    if not os.environ.get('GOOGLE_API_KEY'):
        print("\n⚠️  GOOGLE_API_KEY not found (AI features will be limited)")
        print("To enable AI features:")
        print("export GOOGLE_API_KEY='your-api-key-here'")
    else:
        print("✅ Google API key found - AI features enabled")
    
    print("\n🌐 BookNest with Open Library Features:")
    print("┌─────────────────────────────────────────────┐")
    print("│ 📚 Load existing 30 sample books            │")
    print("│ 🌐 Search & import from Open Library        │")
    print("│ 📖 Real book covers and metadata            │")
    print("│ 🤖 AI-powered book summaries                │")
    print("│ 🔍 Advanced search functionality            │")
    print("│ 📊 Library analytics and insights           │")
    print("│ ➕ Manual book addition                     │")
    print("│ 📱 Clean, responsive interface              │")
    print("└─────────────────────────────────────────────┘")
    
    print(f"\n🌐 Starting BookNest on http://localhost:8501")
    print("\n💡 Features:")
    print("• Your existing 30 books will load automatically")
    print("• Search millions of books on Open Library")
    print("• Import books with one click")
    print("• Quick import buttons for popular series")
    print("• AI summaries for all imported books")
    
    print("\n🚀 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Launch Streamlit with API-integrated app
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app_with_api.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Thanks for using BookNest!")
        print("🌟 Your AI-powered library with Open Library integration")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error starting BookNest: {e}")

if __name__ == "__main__":
    main()