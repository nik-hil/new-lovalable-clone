# Lovable Clone - AI Website Generator

A powerful AI-driven website generator that creates complete full-stack web applications using Gemini AI. Simply describe your vision, and watch as beautiful, functional websites come to life with backend APIs, databases, and modern frontend designs.

## 🌟 Features

### 🤖 **Smart AI Generation**
- **Intelligent Backend Detection**: Automatically identifies when your prompt needs backend functionality
- **Full-Stack Applications**: Generates complete Flask APIs with MySQL databases for data-driven sites
- **Modern Frontend Design**: Creates responsive, beautiful websites with contemporary styling
- **Iterative Generation**: Uses validation loops to ensure all required files are generated

### 🎯 **Website Types Supported**
- **E-commerce Sites**: Product catalogs, shopping carts, order management
- **Business Websites**: Service listings, contact forms, appointment booking
- **Content Management**: Blogs, news sites, portfolio galleries
- **User Systems**: Registration, authentication, user dashboards
- **Static Sites**: Landing pages, brochures, informational sites

### 🔧 **Generated Files**
- `index.html` - Vue.js application structure
- `App.vue` - Main Vue.js component with reactive features
- `main.js` - Vue.js application initialization
- `style.css` - Modern CSS with vibrant gradients and glassmorphism
- `app.py` - Complete Flask backend with RESTful APIs (for full-stack apps)
- `database.py` - MySQL connection and helper functions (for data-driven sites)
- `schema.sql` - Database schema and sample data (for backend apps)
- `.env.example` - Environment configuration template

### 🚀 **Advanced Features**
- **Real-time Preview**: Instant preview with iframe and new tab options
- **Project History**: Track all prompts and iterations
- **File Validation**: Ensures all required files are generated
- **Error Handling**: Comprehensive error reporting and recovery
- **ZIP Export**: Download complete projects as ZIP files
- **Database Integration**: Automatic schema execution and table creation

## 🛠️ Installation & Setup

### Prerequisites
- Docker and Docker Compose
- Gemini AI API key

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd new-lovalable-clone
   ```

2. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env and add your Gemini API key:
   GEMINI_API_KEY=your_actual_api_key_here
   ```

3. **Start the development environment**
   ```bash
   ./docker-dev.sh up
   ```

4. **Access the application**
   - Vue.js Frontend: http://localhost:8080 (Main Interface)
   - Flask Backend: http://localhost:5001 (API Server)
   - Test Server: http://localhost:5002 (Generated Sites)
   - MySQL: localhost:3306 (Database)

### Development Commands

```bash
# Start full development environment (recommended)
./docker-dev.sh up

# Start only Vue.js frontend
./docker-dev.sh frontend

# Start only Flask backend  
./docker-dev.sh backend

# Vue.js specific commands
./docker-dev.sh vue dev      # Start Vue.js dev server
./docker-dev.sh vue build    # Build for production
./docker-dev.sh vue install  # Install dependencies

# Other commands
./docker-dev.sh build        # Build Docker containers
./docker-dev.sh logs         # View backend logs
./docker-dev.sh logs frontend # View frontend logs
./docker-dev.sh shell        # Open backend shell
./docker-dev.sh shell frontend # Open frontend shell
./docker-dev.sh test         # Run test suite
./docker-dev.sh mysql        # Access MySQL shell
./docker-dev.sh clean        # Clean up everything
```

## 🎨 Usage Examples

### Example Prompts

**E-commerce Store:**
```
"Create a flower shop where customers can browse flowers and place orders"
```
*Generates: Product catalog, shopping cart, order management system, admin dashboard*

**Business Website:**
```
"Build a restaurant website with online menu and reservation system"
```
*Generates: Menu display, reservation booking, contact forms, location info*

**Content Platform:**
```
"Make a blog website for tech reviews with user comments"
```
*Generates: Article management, comment system, user authentication, admin panel*

**Service Business:**
```
"Create a photography portfolio with client booking system"
```
*Generates: Gallery display, booking calendar, client management, contact forms*

### Website Refinement

After generating a website, you can refine it with additional prompts:
- "Make it more modern and minimalist"
- "Add a dark mode toggle"
- "Improve the mobile design"
- "Add more interactive animations"

## 🏗️ Architecture

### Frontend (Landing Page)
- **Framework**: Vue.js 3 with Composition API
- **Build Tool**: Vue CLI with Webpack
- **Styling**: Modern CSS with glassmorphism, neumorphism, and vibrant gradients
- **Features**: Real-time preview, reactive state management, modern animations
- **Development**: Hot reload with proxy to Flask backend

### Backend (API & Generated Applications)
- **Framework**: Flask (Python) with CORS enabled
- **Database**: MySQL 8.0
- **APIs**: RESTful endpoints with proxy support for Vue.js frontend
- **Authentication**: Session-based (when needed)
- **Generated Sites**: Vue.js applications with modern aesthetics

### Infrastructure
- **Containerization**: Docker with Docker Compose
- **Development**: Hot reload and live debugging
- **Database**: Persistent MySQL with initialization scripts
- **File Storage**: Local filesystem with volume mounting

## 🧪 Testing

### Run Tests
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

### Test Categories
- **Unit Tests**: Core functionality testing
- **Integration Tests**: API endpoint testing
- **File Generation Tests**: Validation of generated files
- **Backend Detection Tests**: Smart prompt analysis
- **Error Handling Tests**: Edge cases and error scenarios

## 📁 Project Structure

```
new-lovalable-clone/
├── src/                      # Core application code
│   ├── main.py              # AI generation logic (Vue.js focused)
│   ├── server.py            # Flask API server with CORS
│   └── database.py          # Database management
├── frontend/                # Vue.js frontend application
│   ├── src/
│   │   ├── App.vue          # Main Vue.js component
│   │   ├── main.js          # Vue.js entry point
│   │   ├── router/          # Vue Router configuration
│   │   ├── views/           # Vue.js page components
│   │   └── styles/          # Global CSS utilities
│   ├── public/              # Static assets
│   ├── package.json         # Node.js dependencies
│   └── vue.config.js        # Vue.js configuration with proxy
├── site/                    # Legacy HTML (fallback)
├── output/                  # Generated Vue.js applications
├── tests/                   # Test suite (updated for Vue.js)
├── mysql-init/              # Database initialization
├── docker-compose.yml       # Container orchestration (Node.js + Python)
├── Dockerfile              # Container definition (Node.js base)
├── requirements.txt         # Python dependencies (includes Flask-CORS)
├── package.json             # Root Node.js configuration
└── docker-dev.sh           # Development scripts (Vue.js commands)
```

## 🔧 Configuration

### Environment Variables
```bash
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Database (for generated applications)
DB_HOST=mysql
DB_USER=lovable_user
DB_PASSWORD=lovable_password
DB_NAME=lovable_db

# Flask
FLASK_ENV=development
FLASK_DEBUG=1
```

### Database Configuration
- **Host**: mysql (Docker service name)
- **Port**: 3306
- **Database**: lovable_db
- **User**: lovable_user
- **Password**: lovable_password

## 🔍 API Reference

### Main Endpoints

#### Generate Website
```http
POST /generate
Content-Type: application/x-www-form-urlencoded

prompt=your_website_description
```

**Response:**
```json
{
  "preview_url": "/output/index.html",
  "new_tab_url": "http://localhost:5001/output/index.html",
  "files_generated": ["index.html", "style.css", "app.py", "database.py", "schema.sql", "script.js", ".env.example"],
  "message": "Successfully generated 7 files"
}
```

#### Clear All Data
```http
POST /api/clear-all
```

#### Download Project
```http
GET /download-zip
```

#### Health Check
```http
GET /api/health
```

## 🚨 Troubleshooting

### Common Issues

**Container won't start:**
```bash
# Check container status
docker-compose ps

# View logs
./docker-dev.sh logs

# Rebuild containers
./docker-dev.sh clean && ./docker-dev.sh build && ./docker-dev.sh up
```

**API quota exceeded:**
- Gemini API has rate limits
- Wait for quota reset (usually 24 hours)
- Check your API key and billing status

**Database connection errors:**
```bash
# Restart MySQL container
docker-compose restart mysql

# Check MySQL logs
docker-compose logs mysql
```

**Port conflicts:**
```bash
# Check what's using port 5001
lsof -i :5001

# Stop conflicting processes or change ports in docker-compose.yml
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Add tests for new features
- Update documentation
- Use meaningful commit messages

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Gemini AI** for powering the website generation
- **Flask** for the robust web framework
- **MySQL** for reliable data storage
- **Docker** for containerization

## 📞 Support

- **Issues**: Report bugs and feature requests on GitHub Issues
- **Documentation**: Check this README and inline code comments
- **Community**: Join discussions in GitHub Discussions

---

**Built with ❤️ using AI and modern web technologies**
