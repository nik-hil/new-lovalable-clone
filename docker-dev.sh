#!/bin/bash

# Development scripts for Lovable Clone

echo "Lovable Clone Docker Development Helper"
echo "======================================"

case "$1" in
    "build")
        echo "Building Docker containers..."
        docker-compose build
        ;;
    "up")
        echo "Starting development environment..."
        docker-compose up -d
        echo "Application running at: http://localhost:5001"
        echo "MySQL available at: localhost:3306"
        ;;
    "down")
        echo "Stopping containers..."
        docker-compose down
        ;;
    "logs")
        echo "Showing logs..."
        docker-compose logs -f web
        ;;
    "shell")
        echo "Opening shell in web container..."
        docker-compose exec web bash
        ;;
    "mysql")
        echo "Opening MySQL shell..."
        docker-compose exec mysql mysql -u lovable_user -plovable_pass lovable_db
        ;;
    "restart")
        echo "Restarting web container..."
        docker-compose restart web
        ;;
    "clean")
        echo "Cleaning up containers and volumes..."
        docker-compose down -v
        docker system prune -f
        ;;
    *)
        echo "Usage: $0 {build|up|down|logs|shell|mysql|restart|clean}"
        echo ""
        echo "Commands:"
        echo "  build   - Build Docker containers"
        echo "  up      - Start the development environment"
        echo "  down    - Stop containers"
        echo "  logs    - Show web container logs"
        echo "  shell   - Open bash shell in web container"
        echo "  mysql   - Open MySQL shell"
        echo "  restart - Restart web container"
        echo "  clean   - Clean up containers and volumes"
        ;;
esac
