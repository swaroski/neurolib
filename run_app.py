#!/usr/bin/env python3
"""
Quick launcher script for the AI Library Management System
"""

import os
import sys
import subprocess

def main():
    print("🚀 Starting AI-Powered Library Management System...")
    print("=" * 50)
    
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
    
    print("\n📚 Features available:")
    print("- 25 sample books already loaded")
    print("- Book management (Add/Edit/Delete)")
    print("- Check-in/Check-out system")
    print("- Advanced search and filtering")
    print("- AI-powered book summaries")
    print("- Intelligent reading recommendations")
    print("- Library analytics and insights")
    
    print(f"\n🌐 Starting server on http://localhost:8501")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Launch Streamlit
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Thanks for using the AI Library Management System!")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error starting the application: {e}")

if __name__ == "__main__":
    main()