#!/bin/bash

# WebVuln Docker Manager
# Usage: ./start.sh [clean|quick|stop|logs|restart]

set -e

PROJECT_NAME="webvuln"
COMPOSE_FILE="docker-compose.yml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  $1${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
}

print_step() {
    echo -e "${YELLOW}[+]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Stop and remove all containers
stop_containers() {
    print_step "Stopping all containers..."
    docker compose -f "$COMPOSE_FILE" down 2>/dev/null || true
    print_success "Containers stopped"
}

# Remove all project images (clean rebuild)
remove_images() {
    print_step "Removing old Docker images..."
    docker images | grep "$PROJECT_NAME" | awk '{print $3}' | xargs -r docker rmi -f 2>/dev/null || true
    # Also remove build cache
    docker builder prune -f >/dev/null 2>&1 || true
    print_success "Images removed"
}

# Build and start services
build_and_start() {
    local rebuild_type="$1"

    print_step "Building Docker images ($rebuild_type)..."
    if [ "$rebuild_type" = "full" ]; then
        docker compose -f "$COMPOSE_FILE" build --no-cache --pull
    else
        docker compose -f "$COMPOSE_FILE" build
    fi
    print_success "Build complete"

    print_step "Starting services..."
    docker compose -f "$COMPOSE_FILE" up -d
    print_success "Services started"

    echo ""
    print_header "Services Available"
    echo -e "  SQLI  → ${GREEN}http://localhost:1111${NC}"
    echo -e "  XSS   → ${GREEN}http://localhost:1112${NC}"
    echo -e "  SSTI  → ${GREEN}http://localhost:1113${NC}"
    echo ""
    print_step "Use './start.sh logs' to view logs"
}

# Show logs
show_logs() {
    docker compose -f "$COMPOSE_FILE" logs -f
}

# Restart services
restart_services() {
    print_step "Restarting services..."
    docker compose -f "$COMPOSE_FILE" restart
    print_success "Services restarted"
}

# Main script logic
case "${1:-quick}" in
    clean)
        print_header "Clean Rebuild (Full Reset)"
        stop_containers
        remove_images
        build_and_start "full"
        ;;
    quick)
        print_header "Quick Start (Code Update)"
        stop_containers
        build_and_start "quick"
        ;;
    stop)
        print_header "Stop Services"
        stop_containers
        ;;
    restart)
        print_header "Restart Services"
        restart_services
        ;;
    logs)
        print_header "Service Logs"
        show_logs
        ;;
    *)
        echo "Usage: $0 [clean|quick|stop|restart|logs]"
        echo ""
        echo "  clean   - Remove images and rebuild from scratch (slow, fresh environment)"
        echo "  quick   - Rebuild with code changes only (fast, uses cached layers)"
        echo "  stop    - Stop all services"
        echo "  restart - Restart services without rebuild"
        echo "  logs    - Show and follow service logs"
        echo ""
        echo "Default: quick"
        exit 1
        ;;
esac
