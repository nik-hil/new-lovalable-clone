#!/bin/bash

# Development scripts for Lovable Clone Vue.js Edition

echo "Lovable Clone Vue.js - Docker Development Helper"
echo "==============================================="

case "$1" in
    "build")
        echo "Building Docker containers..."
        docker-compose build
        ;;
    "up")
        echo "Starting development environment..."
        docker-compose up -d
        echo ""
        echo "🚀 Application URLs:"
        echo "   Vue.js Frontend: http://localhost:8080"
        echo "   Flask Backend:   http://localhost:5001"
        echo "   Test Server:     http://localhost:5002"
        echo "   MySQL:           localhost:3306"
        echo ""
        echo "Starting Vue.js frontend..."
        cd frontend && npm run serve &
        echo "Vue.js dev server starting in background..."
        ;;
    "frontend")
        echo "Starting Vue.js frontend only..."
        cd frontend && npm run serve
        ;;
    "backend")
        echo "Starting Flask backend only..."
        docker-compose up -d mysql web
        ;;
    "down")
        echo "Stopping containers..."
        docker-compose down
        # Also stop Vue.js dev server if running
        pkill -f "vue-cli-service serve" 2>/dev/null || true
        ;;
    "logs")
        if [ "$2" = "frontend" ]; then
            echo "Showing Vue.js frontend logs..."
            # Vue.js logs are shown in the terminal where it's running
            echo "Check the terminal where 'npm run serve' is running"
        else
            echo "Showing Flask backend logs..."
            docker-compose logs -f web
        fi
        ;;
    "shell")
        if [ "$2" = "frontend" ]; then
            echo "Opening shell in frontend directory..."
            cd frontend && bash
        else
            echo "Opening shell in web container..."
            docker-compose exec web bash
        fi
        ;;
    "vue")
        echo "Vue.js commands:"
        echo "  build    - Build Vue.js for production"
        echo "  dev      - Start Vue.js dev server"
        echo "  install  - Install Vue.js dependencies"
        echo ""
        case "$2" in
            "build")
                cd frontend && npm run build
                ;;
            "dev")
                cd frontend && npm run serve
                ;;
            "install")
                cd frontend && npm install
                ;;
            *)
                echo "Usage: $0 vue {build|dev|install}"
                ;;
        esac
        ;;
    "mysql")
        echo "Opening MySQL shell..."
        docker-compose exec mysql mysql -u lovable_user -plovable_password lovable_db
        ;;
    "restart")
        echo "Restarting web container..."
        docker-compose restart web
        ;;
    "test")
        echo "Running tests..."
        docker-compose exec web python3 -m pytest tests/ -v
        ;;
    "clean")
        echo "Cleaning up containers and volumes..."
        docker-compose down -v
        docker system prune -f
        # Clean Vue.js build files
        rm -rf frontend/dist frontend/node_modules/.cache
        ;;
    *)
        echo "Usage: $0 {build|up|frontend|backend|down|logs|shell|vue|mysql|restart|test|clean}"
        echo ""
        echo "Main Commands:"
        echo "  build     - Build Docker containers"
        echo "  up        - Start full development environment (Docker + Vue.js)"
        echo "  frontend  - Start Vue.js frontend only"
        echo "  backend   - Start Flask backend only" 
        echo "  down      - Stop all services"
        echo ""
        echo "Development Commands:"
        echo "  logs      - Show logs (add 'frontend' or 'backend')"
        echo "  shell     - Open shell (add 'frontend' for frontend directory)"
        echo "  vue       - Vue.js specific commands (build|dev|install)"
        echo "  test      - Run test suite"
        echo ""
        echo "Utility Commands:"
        echo "  mysql     - Open MySQL shell"
        echo "  restart   - Restart backend container"
        echo "  clean     - Clean up containers, volumes, and caches"
        echo ""
        echo "🚀 Quick Start:"
        echo "  ./docker-dev.sh up      # Start everything"
        echo "  ./docker-dev.sh frontend # Start just Vue.js frontend"
        ;;
esac
