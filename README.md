# Lovable Clone with Gemini AI

A web application that creates websites from natural language prompts using Google's Gemini AI, similar to Lovable.

## Features

- 🚀 Generate complete websites from simple text prompts
- 🔄 Iterative refinement - continue improving your website with additional prompts
- 👀 Live preview within the app using iframes  
- 🌐 Open generated websites in new tabs
- 💾 Download websites as ZIP files
- 📝 Prompt history tracking with timestamps
- 💅 Clean, responsive UI with loading states and spinning animations
- 📱 Mobile-friendly design
- 🐳 Docker development environment

## Setup

### Docker Development Setup (Recommended)

1. Set up your Google Gemini API key:
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a `.env` file in the root directory:
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```

2. Use the Docker helper script:
   ```bash
   # Build the containers
   ./docker-dev.sh build
   
   # Start the development environment
   ./docker-dev.sh up
   
   # Stop the environment
   ./docker-dev.sh down
   
   # View logs
   ./docker-dev.sh logs
   ```

3. Access the application:
   - **Lovable Clone**: http://localhost:5001

### Manual Setup (Alternative)

1. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your Google Gemini API key:
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Set it as an environment variable:
     ```bash
     export GOOGLE_API_KEY="your_api_key_here"
     ```
   - Or create a `.env` file in the root directory:
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```

3. Run the application:
   ```bash
   cd src
   python server.py
   ```

4. Open your browser and go to `http://localhost:5001`

## Usage

### Initial Generation
1. **Generate a website:** Enter a descriptive prompt like:
   - "create a personal blog website for cars. I visit different cars and post photos and some details about them"
   - "build a portfolio website for a photographer"
   - "make a landing page for a coffee shop with warm colors"

2. **Preview:** See your website in the preview iframe immediately
3. **History:** Your prompt is automatically added to the history section (non-editable)
4. **Clean slate:** The text area is cleared for your next prompt
5. **Loading animation:** Watch the spinning hourglass ⏳ while your website is being generated

### Refinement Process
6. **Refine:** Click "Refine Further" and enter modification requests like:
   - "make it more modern with better colors"
   - "change the background to blue"
   - "add a contact form"
   - "make the typography more elegant"

7. **Important:** For refinements, you **don't need to repeat the original prompt**. Just describe what you want to change:
   - ✅ Good: "make it more modern"
   - ❌ Avoid: "create a personal blog website for cars... make it more modern" (too long and repetitive)

### Export & Share
8. **Download:** Click "Download ZIP" to get all website files in a ZIP archive
9. **Open in new tab:** Click the "Open in New Tab" button to view the full website

### Pro Tips for Better Results
- **Be specific but concise** in refinements
- **Use design terminology**: "modern", "clean", "professional", "vibrant"
- **Request specific changes**: "darker header", "larger fonts", "rounded corners"
- **Ask for features**: "contact form", "gallery", "navigation menu"
- **Check history** to see what prompts you've used before

## Technology Stack

- **Backend**: Python Flask with Google Gemini AI integration
- **AI Model**: Google Gemini 1.5 Flash for website generation
- **Frontend**: HTML/CSS/JavaScript with responsive design and animations
- **Infrastructure**: Docker containerization with volume mounting
- **Features**: ZIP file generation, prompt history, live preview, spinning loading animations

## Development

### Project Structure

```
├── src/
│   ├── server.py          # Main Flask application (moved from root)
│   └── main.py            # AI processing and response parsing
├── site/                  # Frontend files
│   ├── index.html         # Main interface with spinning animations
│   └── style.css          # Responsive styling with CSS animations
├── output/                # Generated website files
├── tests/                 # Test files
├── docker-compose.yml     # Docker services configuration
├── Dockerfile             # Container build instructions
├── docker-dev.sh          # Development helper script
└── requirements.txt       # Python dependencies
```

### Recent Updates

**✅ File Structure Reorganization:**
- Moved `server.py` from root to `src/` folder for better organization
- Updated Dockerfile and all imports accordingly
- Tests and other files updated to reflect new structure

**✅ UI/UX Improvements:**
- Added spinning animation to hourglass (⏳) loading indicator
- CSS keyframe animations provide visual feedback during generation
- Improved user experience with clear loading states

**✅ Docker Simplification:**
- Removed phpMyAdmin dependency (was only needed for database administration)
- Streamlined docker-compose.yml for simpler deployment
- Focus on core functionality without unnecessary database tools

### Docker Commands

```bash
# Start all services
./docker-dev.sh up

# Build containers
./docker-dev.sh build

# Stop services
./docker-dev.sh down

# View logs
./docker-dev.sh logs

# Check status
docker-compose ps
```

## Environment Variables

Create a `.env` file with:

```env
GOOGLE_API_KEY=your_google_api_key_here
FLASK_ENV=development
```

## Running Tests

```bash
# Run tests locally
pytest tests/

# Run tests in Docker
docker-compose exec web pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with the Docker environment
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).
