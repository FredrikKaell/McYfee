#!/bin/bash

###############################################################################
# McYfee Deployment Script
# Deploys McYfee project with environment setup and service configuration
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Find project root (directory containing src/ and requirements.txt)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# If script is in scripts/ subdirectory, go up one level
if [[ "$(basename "$SCRIPT_DIR")" == "scripts" ]]; then
    PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
else
    PROJECT_DIR="$SCRIPT_DIR"
fi

# Verify we're in the right place
if [ ! -f "$PROJECT_DIR/pyproject.toml" ] || [ ! -d "$PROJECT_DIR/src" ]; then
    log_error() {
        echo -e "${RED}[ERROR]${NC} $1"
    }
    log_error "Could not find project root!"
    log_error "Expected to find pyproject.toml and src/ directory"
    log_error "Current location: $PROJECT_DIR"
    exit 1
fi

# Configuration
PROJECT_NAME="mcyfee"
VENV_DIR="$PROJECT_DIR/.venv"
LOG_DIR="$PROJECT_DIR/logs/"

# Detect OS
OS_TYPE="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS_TYPE="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS_TYPE="macos"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "win32" ]]; then
    OS_TYPE="windows"
fi

###############################################################################
# Helper Functions
###############################################################################

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

###############################################################################
# Pre-deployment Checks
###############################################################################

check_requirements() {
    log_info "Checking system requirements..."
    log_info "Detected OS: $OS_TYPE"
    
    # Only check for root on Linux/macOS
    if [[ "$OS_TYPE" == "linux" ]] || [[ "$OS_TYPE" == "macos" ]]; then
        if [[ $EUID -ne 0 ]]; then
            log_warning "Not running as root. Some operations may require sudo."
            log_info "Continue anyway? [y/N]"
            read -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                log_error "Deployment cancelled. Run with: sudo ./setup.sh"
                exit 1
            fi
        fi
    fi
    
    # Check Python version
    if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
        log_error "Python 3 is not installed"
        exit 1
    fi
    
    # Detect Python command (prioritize py launcher on Windows, then python3, then python)
    if [[ "$OS_TYPE" == "windows" ]] && command -v py &> /dev/null; then
        PYTHON_CMD="py"
    elif command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        log_error "Python 3 is not installed"
        exit 1
    fi
    
    PYTHON_VERSION=$($PYTHON_CMD --version | cut -d' ' -f2 | cut -d'.' -f1-2)
    log_info "Found Python $PYTHON_VERSION (using $PYTHON_CMD)"
    
    # Check optional commands (don't fail if missing)
    if [[ "$OS_TYPE" != "windows" ]]; then
        for cmd in git systemctl mysql; do
            if ! command -v $cmd &> /dev/null; then
                log_warning "$cmd is not installed"
            fi
        done
    fi
    
    log_success "Requirements check passed"
}

###############################################################################
# Python Environment
###############################################################################

setup_python_env() {
    log_info "Setting up Python virtual environment and installing project..."
    
    # Create virtual environment
    $PYTHON_CMD -m venv $VENV_DIR
    
    # Detect activation script based on OS
    if [[ "$OS_TYPE" == "windows" ]]; then
        ACTIVATE_SCRIPT="$VENV_DIR/Scripts/activate"
    else
        ACTIVATE_SCRIPT="$VENV_DIR/bin/activate"
    fi
    
    if [ ! -f "$ACTIVATE_SCRIPT" ]; then
        log_error "Virtual environment creation failed"
        exit 1
    fi
    
    # Activate and install dependencies
    log_info "Activating virtual environment..."
    source "$ACTIVATE_SCRIPT"
    
    log_info "Upgrading pip..."
    if [[ "$OS_TYPE" == "windows" ]]; then
        # Windows: Use python -m pip to avoid file locking
        PYTHON_VENV="$VENV_DIR/Scripts/python.exe"
        "$PYTHON_VENV" -m pip install --upgrade pip 2>&1 | grep -v "WARNING" || {
            log_warning "Pip upgrade skipped (file locked - this is OK on Windows)"
        }
    else
        pip install --upgrade pip
    fi
    
    if [[ "$OS_TYPE" == "windows" ]]; then
        "$PYTHON_VENV" -m pip install -e "$PROJECT_DIR"
    else
        pip install -e .
    fi
    
    deactivate
    
    log_success "Python virtual environment and project with dependencies ready"
}

###############################################################################
# Environment Configuration
###############################################################################

setup_env_file() {
    log_info "Setting up environment file..."
    
    if [ ! -f "$PROJECT_DIR/.env" ]; then
        if [ -f "$PROJECT_DIR/.env.template" ]; then
            cp $PROJECT_DIR/.env.template $PROJECT_DIR/.env
            log_warning "Created .env from .env.template - EDIT THIS FILE!"
            log_warning "Set environmental variables in $PROJECT_DIR/.env"
        else
            log_warning ".env.template not found. Creating basic .env..."
            cat > $PROJECT_DIR/.env << 'EOF'
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=mcyfee_user
DB_PASS=CHANGE_ME
DB_NAME=mcyfee
EOF
            log_warning "Created basic .env template - EDIT THIS FILE!"
        fi
    else
        log_info ".env file already exists"
    fi
    
    # Secure .env file (skip on Windows)
    if [[ "$OS_TYPE" != "windows" ]]; then
        chmod 600 $PROJECT_DIR/.env
        if [[ $EUID -eq 0 ]] && [ ! -z "$SUDO_USER" ]; then
            chown $SUDO_USER:$SUDO_USER $PROJECT_DIR/.env
        fi
    fi
    
    log_success ".env file ready"
}

###############################################################################
# Database Setup
###############################################################################

setup_database() {
    log_info "Database setup information..."
    
    if [ -f "$PROJECT_DIR/scripts/setup_db.sql" ]; then
        log_info "Found database schema file: scripts/setup_db.sql"
        
        if command -v mysql &> /dev/null; then
            log_info "MySQL client detected"
            log_warning "To deploy database, run: mysql -u root -p < $PROJECT_DIR/scripts/setup_db.sql"
        else
            log_warning "MySQL client not found. Install MySQL to set up database."
        fi
    else
        log_warning "No database schema file found at scripts/setup_db.sql"
    fi
}

###############################################################################
# Post-deployment
###############################################################################

post_deploy_info() {
    echo
    log_success "========================================="
    log_success "McYfee Deployment Complete!"
    log_success "========================================="
    echo
    
    log_info "Platform: $OS_TYPE"
    log_info "Python:   $PYTHON_CMD ($PYTHON_VERSION)"
    echo
    
    log_info "Next steps:"
    echo
    
    if [ -f "$PROJECT_DIR/scripts/setup_db.sql" ]; then
        echo "  1. Setup database:"
        if [[ "$OS_TYPE" == "windows" ]]; then
            echo "     Run setup_db.sql in your MySQL client"
        else
            echo "     mysql -u root -p < $PROJECT_DIR/scripts/setup_db.sql"
        fi
    fi
    
    echo "  2. Edit configuration:"
    if [[ "$OS_TYPE" == "windows" ]]; then
        echo "     notepad $PROJECT_DIR\\.env"
    else
        echo "     nano $PROJECT_DIR/.env"
    fi
    
    echo
    echo "  3. Activate virtual environment:"
    if [[ "$OS_TYPE" == "windows" ]]; then
        echo "     source .venv\\Scripts\\activate"
    else
        echo "     source .venv/bin/activate"
    fi
    
    echo
    echo "  4. Run application:"
    echo "     mcyfee"
    echo
    
    log_info "Files:"
    echo "  Project:  $PROJECT_DIR"
    echo "  Config:   $PROJECT_DIR/.env"
    echo "  Venv:     $VENV_DIR"
    echo
    
    if [[ "$OS_TYPE" == "linux" ]]; then
        log_info "For production deployment setup tracker to run in systemd service or run in cron."
        echo "  See deployment documentation"
    fi
}

###############################################################################
# Main Deployment Flow
###############################################################################

main() {
    echo
    log_info "========================================="
    log_info "McYfee Deployment Script"
    log_info "========================================="
    echo
    
    check_requirements
    setup_python_env
    setup_env_file
    setup_database
    post_deploy_info
}

# Run deployment
main