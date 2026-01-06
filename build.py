#!/usr/bin/env python3
"""
Simple build script for Auto Typing Tool
Creates a standalone executable using PyInstaller
"""

import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """Build the Auto Typing Tool executable."""
    print("🔨 Building Auto Typing Tool...")
    
    # Check if we're in the right directory
    if not os.path.exists("src/main.py"):
        print("❌ Error: src/main.py not found. Make sure you're in the project directory.")
        sys.exit(1)
    
    # Use the virtual environment's pyinstaller if available
    venv_pyinstaller = "./Auto-Typing-Bot-Python/bin/pyinstaller"
    if os.path.exists(venv_pyinstaller):
        pyinstaller_cmd = venv_pyinstaller
        print("📦 Using virtual environment PyInstaller")
    else:
        pyinstaller_cmd = "pyinstaller"
        print("📦 Using system PyInstaller")
    
    try:
        # Clean previous builds
        print("🧹 Cleaning previous builds...")
        for folder in ["build", "dist"]:
            if os.path.exists(folder):
                subprocess.run(["rm", "-rf", folder], check=False)
        
        # Remove old spec file
        spec_files = [f for f in os.listdir(".") if f.endswith(".spec")]
        for spec_file in spec_files:
            os.remove(spec_file)
            print(f"🗑️  Removed old spec file: {spec_file}")
        
        # Run PyInstaller command
        cmd = [
            pyinstaller_cmd,
            "--onedir",
            "--windowed", 
            "--name", "Auto-Typing-Tool",
            "--paths=src",
            "--hidden-import=pattern_matcher",
            "--hidden-import=pause_directive",
            "--hidden-import=help_window",
            "--hidden-import=code_patterns",
            "src/main.py"
        ]
        
        print(f"⚡ Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("✅ Build completed successfully!")
        
        # Check if executable was created and show info
        exe_path = Path("dist") / "Auto-Typing-Tool"
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / 1024 / 1024
            print(f"📦 Executable created: {exe_path}")
            print(f"📊 File size: {size_mb:.1f} MB")
            print(f"🎯 You can now run: ./dist/Auto-Typing-Tool")
        else:
            print("⚠️  Executable not found in expected location")
            
        # Show any warnings from PyInstaller
        if result.stderr and "WARNING" in result.stderr:
            print("\n📋 Build warnings:")
            for line in result.stderr.split('\n'):
                if "WARNING" in line:
                    print(f"  ⚠️  {line.strip()}")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed with exit code {e.returncode}")
        print(f"Error output: {e.stderr}")
        if "command not found" in str(e) or "No such file" in str(e):
            print("\n💡 PyInstaller not found. Install with:")
            if os.path.exists("./Auto-Typing-Bot-Python/bin/pip"):
                print("  ./Auto-Typing-Bot-Python/bin/pip install pyinstaller")
            else:
                print("  pip install pyinstaller")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ PyInstaller not found.")
        print("\n💡 Install PyInstaller with:")
        if os.path.exists("./Auto-Typing-Bot-Python/bin/pip"):
            print("  ./Auto-Typing-Bot-Python/bin/pip install pyinstaller")
        else:
            print("  pip install pyinstaller")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Build cancelled by user")
        sys.exit(1)

def main():
    """Main entry point."""
    print("=" * 50)
    print("  AUTO TYPING TOOL - BUILD SCRIPT")
    print("=" * 50)
    
    # Show current directory
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Check for required files
    required_files = ["src/main.py"]
    print(f"📁 required files: {required_files}")
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        sys.exit(1)
    
    build_app()
    
    print("\n" + "=" * 50)
    print("🎉 Build process completed!")
    print("=" * 50)

if __name__ == "__main__":
    main()