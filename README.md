# Lovable Clone with Gemini AI

A web application that ## Usage

### Initial Generation
1. **Generate a website:** Enter a descriptive prompt like:
   - "create a personal blog website for cars. I visit different cars and post photos and some details about them"
   - "build a portfolio website for a photographer"
   - "make a landing page for a coffee shop with warm colors"

2. **Preview:** See your website in the preview iframe immediately
3. **History:** Your prompt is automatically added to the history section (non-editable)
4. **Clean slate:** The text area is cleared for your next prompt

### Refinement Process
5. **Refine:** Click "Refine Further" and enter modification requests like:
   - "make it more modern with better colors"
   - "change the background to blue"
   - "add a contact form"
   - "make the typography more elegant"

6. **Important:** For refinements, you **don't need to repeat the original prompt**. Just describe what you want to change:
   - ✅ Good: "make it more modern"
   - ❌ Avoid: "create a personal blog website for cars... make it more modern" (too long and repetitive)

### Export & Share
7. **Download:** Click "Download ZIP" to get all website files in a ZIP archive
8. **Open in new tab:** Click the "Open in New Tab" button to view the full website

### Pro Tips for Better Results
- **Be specific but concise** in refinements
- **Use design terminology**: "modern", "clean", "professional", "vibrant"
- **Request specific changes**: "darker header", "larger fonts", "rounded corners"
- **Ask for features**: "contact form", "gallery", "navigation menu"
- **Check history** to see what prompts you've used beforetes websites from natural language prompts using Google's Gemini AI, similar to Lovable.

## Features

- 🚀 Generate complete websites from simple text prompts
- 🔄 Iterative refinement - continue improving your website with additional prompts
- 👀 Live preview within the app using iframes  
- 🌐 Open generated websites in new tabs
- 💅 Clean, responsive UI with loading states
- 📱 Mobile-friendly design

## Lovable Clone - AI Website Builder

A simple website builder powered by Google's Gemini AI, inspired by Lovable. Generate websites from natural language prompts and refine them iteratively.

## Features

- 🤖 AI-powered website generation using Google Gemini
- 🎨 Modern, responsive designs
- 🔄 Iterative refinement - keep improving your website
- 👀 Live preview with iframe
- � Prompt history tracking - see all your previous prompts
- 💾 Download websites as ZIP files
- �🚀 Open generated sites in new tabs
- 📱 Mobile-friendly interface

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Get a Gemini API Key:**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the key

3. **Create environment file:**
   ```bash
   cp env.example .env
   ```
   Then edit `.env` and add your API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

4. **Run the application:**
   ```bash
   python server.py
   ```

5. **Open in browser:**
   Navigate to `http://localhost:5001`

## Usage

1. **Generate a website:** Enter a prompt like "create a portfolio website for a photographer"
2. **Preview:** See your website in the preview iframe
3. **Refine:** Click "Refine Further" and add modifications like "make the background blue" or "add a contact form"
4. **Open in new tab:** Click the "Open in New Tab" button to see the full website

## Project Structure

```
├── server.py              # Flask web server
├── src/
│   └── main.py           # AI processing logic
├── site/                 # Landing page files
│   ├── index.html
│   └── style.css
└── output/               # Generated websites
    ├── index.html
    └── style.css
```

## How it Works

1. **User Input:** User enters a prompt on the landing page
2. **AI Processing:** Prompt is sent to Gemini AI with context and formatting instructions
3. **Response Parsing:** AI response is parsed to extract HTML/CSS files
4. **File Generation:** Files are saved to the `output/` directory
5. **Preview:** Website is displayed in an iframe for immediate feedback
6. **Iteration:** Users can refine the website with additional prompts

## API Endpoints

- `GET /` - Main landing page
- `POST /generate` - Generate website from prompt
- `GET /download-zip` - Download generated website as ZIP file
- `GET /site/<path>` - Serve landing page assets
- `GET /output/<path>` - Serve generated website files

## Examples

Try these prompts:
- "Create a landing page for a coffee shop with warm colors"
- "Build a portfolio website for a graphic designer"
- "Make a blog about sustainable living with green theme"
- "Create a restaurant website with menu and contact info"

Then refine with:
- "Make the header darker"
- "Add a contact form"
- "Change the font to serif"
- "Add social media links"

## Technologies

- **Backend:** Python, Flask
- **AI:** Google Gemini 1.5 Flash
- **Frontend:** HTML, CSS, JavaScript (Vanilla)
- **Styling:** Modern CSS with flexbox/grid

## Limitations

- Generates static websites only (HTML/CSS/JS)
- No backend functionality
- Limited to files that fit in AI context window
- Requires internet connection for AI generation

## Contributing

Feel free to contribute by:
- Improving the parsing logic
- Adding more UI features
- Enhancing error handling
- Adding export functionality

## License

MIT License - Feel free to use and modify as needed.

4. **Open your browser:**
   Navigate to `http://127.0.0.1:5000`

## How It Works

1. **Enter a Prompt**: Describe the website you want to create
   - Example: "Create a landing page for a coffee shop with menu and contact info"

2. **Generate**: The app sends your prompt to Gemini AI which generates HTML, CSS, and potentially JavaScript files

3. **Preview**: The generated website appears in an embedded iframe

4. **Refine**: Click "Refine Further" and enter additional instructions to improve the website
   - Example: "Make the background darker and add a newsletter signup"

5. **View**: Click "Open in New Tab" to see the full website
