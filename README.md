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
- `index.html` - Responsive frontend with modern design
- `style.css` - Beautiful styling with animations and effects
- `script.js` - Interactive JavaScript features
- `app.py` - Complete Flask backend with RESTful APIs
- `database.py` - MySQL connection and helper functions
- `schema.sql` - Database schema and sample data
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
   - Website: http://localhost:5001
   - MySQL: localhost:3306

### Development Commands

```bash
# Build containers
./docker-dev.sh build

# Start services
./docker-dev.sh up

# View logs
./docker-dev.sh logs

# Open shell in web container
./docker-dev.sh shell

# Access MySQL shell
./docker-dev.sh mysql

# Restart web container
./docker-dev.sh restart

# Clean up everything
./docker-dev.sh clean
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
- **Framework**: Vanilla HTML/CSS/JavaScript
- **Styling**: Modern CSS with animations and responsive design
- **Features**: Real-time preview, project history, file download

### Backend (Generated Applications)
- **Framework**: Flask (Python)
- **Database**: MySQL 8.0
- **APIs**: RESTful endpoints with CORS support
- **Authentication**: Session-based (when needed)

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
│   ├── main.py              # AI generation logic
│   ├── server.py            # Flask web server
│   └── database.py          # Database management
├── site/                    # Landing page frontend
│   ├── index.html           # Main interface
│   └── style.css            # Landing page styles
├── output/                  # Generated websites
├── tests/                   # Test suite
├── mysql-init/              # Database initialization
├── docker-compose.yml       # Container orchestration
├── Dockerfile              # Container definition
├── requirements.txt         # Python dependencies
└── docker-dev.sh           # Development scripts
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
