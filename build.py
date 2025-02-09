import os
import shutil
import subprocess
import sys

def clean_builds():
    """Clean previous build artifacts."""
    dirs_to_clean = ['build', 'dist']
    files_to_clean = ['*.spec']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Cleaned {dir_name}/")

    for pattern in files_to_clean:
        for file in os.listdir('.'):
            if file.endswith('.spec') and file != 'chatbot.spec':
                os.remove(file)
                print(f"Cleaned {file}")

def build_executable():
    """Build the executable using PyInstaller."""
    print("Building executable...")
    
    # Ensure resources directory exists
    os.makedirs('chatbot/resources', exist_ok=True)
    
    # Run PyInstaller
    result = subprocess.run([
        'pyinstaller',
        '--clean',
        '--noconfirm',
        'chatbot.spec'
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Build failed!")
        print("Error output:")
        print(result.stderr)
        sys.exit(1)
    
    print("Build completed successfully!")
    print(f"Executable can be found in {os.path.abspath('dist/ChatBot.exe')}")

if __name__ == '__main__':
    clean_builds()
    build_executable()