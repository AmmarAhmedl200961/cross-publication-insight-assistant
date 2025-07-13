"""
Setup script for Publication Assistant
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error during {description}: {str(e)}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True


def create_virtual_environment():
    """Create a virtual environment."""
    venv_path = Path("venv")
    if venv_path.exists():
        print("📁 Virtual environment already exists")
        return True
    
    return run_command(f"{sys.executable} -m venv venv", "Creating virtual environment")


def install_requirements():
    """Install required packages."""
    # Determine pip command based on platform
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\pip.exe"
    else:  # Unix/Linux/Mac
        pip_cmd = "venv/bin/pip"
    
    # Upgrade pip first
    if not run_command(f"{pip_cmd} install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install requirements
    return run_command(f"{pip_cmd} install -r requirements.txt", "Installing requirements")


def setup_environment_file():
    """Set up environment file from template."""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("📁 .env file already exists")
        return True
    
    if env_example.exists():
        # Copy example to .env
        with open(env_example, 'r') as src, open(env_file, 'w') as dst:
            content = src.read()
            dst.write(content)
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env file and add your API keys")
        return True
    else:
        print("❌ .env.example file not found")
        return False


def validate_setup():
    """Validate the installation."""
    print("\\n🔍 Validating installation...")
    
    # Check if venv exists
    venv_path = Path("venv")
    if not venv_path.exists():
        print("❌ Virtual environment not found")
        return False
    
    # Check if requirements are installed
    if os.name == 'nt':  # Windows
        python_cmd = "venv\\Scripts\\python.exe"
    else:  # Unix/Linux/Mac
        python_cmd = "venv/bin/python"
    
    check_cmd = f'{python_cmd} -c "import crewai, langchain_openai; print(\\"Dependencies OK\\")"'
    if not run_command(check_cmd, "Checking dependencies"):
        return False
    
    # Check environment file
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found")
        return False
    
    print("✅ Installation validation completed")
    return True


def main():
    """Main setup function."""
    print("🚀 Publication Assistant Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        print("❌ Failed to create virtual environment")
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("❌ Failed to install requirements")
        sys.exit(1)
    
    # Setup environment file
    if not setup_environment_file():
        print("❌ Failed to setup environment file")
        sys.exit(1)
    
    # Validate setup
    if not validate_setup():
        print("❌ Setup validation failed")
        sys.exit(1)
    
    print("\\n🎉 Setup completed successfully!")
    print("\\nNext steps:")
    print("1. Edit .env file and add your OpenAI API key")
    print("2. Optionally add your GitHub token for better rate limits")
    print("3. Activate virtual environment:")
    
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\activate")
    else:  # Unix/Linux/Mac
        print("   source venv/bin/activate")
    
    print("4. Run the system:")
    print('   python main.py --repo-url "https://github.com/owner/repo"')
    
    print("\\n📚 For more information, see README.md")


if __name__ == "__main__":
    main()
