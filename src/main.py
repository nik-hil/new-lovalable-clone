
import os
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def create_website(prompt: str):
    """
    This function takes a prompt and creates or modifies a website based on it.
    It reads existing files from the 'output' directory to provide context.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file or environment variables.")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

    # Check for existing files in the output directory
    existing_files = {}
    output_dir = "output"
    if os.path.exists(output_dir):
        for filename in os.listdir(output_dir):
            with open(os.path.join(output_dir, filename), "r") as f:
                existing_files[filename] = f.read()

    if existing_files:
        prompt_with_context = (
            "You are a professional web developer and UI/UX designer. Here are the existing files for a website:\n\n"
        )
        for filename, content in existing_files.items():
            prompt_with_context += f"**{filename}**:\n```\n{content}\n```\n\n"
        prompt_with_context += (
            f"Please improve and modify this website based on this request: '{prompt}'\n\n"
            "IMPORTANT DESIGN REQUIREMENTS:\n"
            "- Make the website MODERN, BEAUTIFUL, and VISUALLY APPEALING\n"
            "- Use modern CSS techniques (flexbox, grid, smooth animations, gradients)\n"
            "- Apply attractive color schemes and typography\n"
            "- Ensure responsive design for all devices\n"
            "- Add subtle animations and hover effects\n"
            "- Use proper spacing, shadows, and visual hierarchy\n"
            "- Make it look professional and polished\n\n"
            "Provide the complete, updated code for ALL files (even if only some changed).\n"
            "Format your response exactly like this:\n\n"
            "**index.html**:\n"
            "```html\n"
            "[complete HTML code here]\n"
            "```\n\n"
            "**style.css**:\n"
            "```css\n"
            "[complete CSS code here]\n"
            "```\n\n"
            "If you need JavaScript for interactions, add:\n"
            "**script.js**:\n"
            "```javascript\n"
            "[complete JavaScript code here]\n"
            "```"
        )
    else:
        prompt_with_context = (
            f"You are a professional web developer and UI/UX designer. Create a stunning, modern website based on this prompt: '{prompt}'\n\n"
            "IMPORTANT DESIGN REQUIREMENTS:\n"
            "- Make the website MODERN, BEAUTIFUL, and VISUALLY APPEALING\n"
            "- Use contemporary design trends (clean layouts, attractive colors, modern typography)\n"
            "- Apply CSS techniques like flexbox, grid, smooth animations, gradients, shadows\n"
            "- Ensure fully responsive design for mobile, tablet, and desktop\n"
            "- Add subtle animations, hover effects, and micro-interactions\n"
            "- Use proper spacing, visual hierarchy, and professional aesthetics\n"
            "- Make it look like a premium, professional website\n"
            "- Include relevant, high-quality content related to the prompt\n\n"
            "Format your response exactly like this:\n\n"
            "**index.html**:\n"
            "```html\n"
            "[complete HTML code here]\n"
            "```\n\n"
            "**style.css**:\n"
            "```css\n"
            "[complete CSS code here]\n"
            "```\n\n"
            "If you need JavaScript for interactions, add:\n"
            "**script.js**:\n"
            "```javascript\n"
            "[complete JavaScript code here]\n"
            "```\n\n"
            "CONTENT GUIDELINES:\n"
            "- Include relevant, realistic content (don't use Lorem ipsum)\n"
            "- Add appropriate headings, descriptions, and calls-to-action\n"
            "- Make content engaging and relevant to the topic\n"
            "- Use semantic HTML structure for accessibility"
        )

    response = model.generate_content(prompt_with_context)

    # Parse the response and write to files
    file_contents = parse_gemini_response(response.text)
    
    if not file_contents:
        return {"error": "Could not parse the response from the AI. No files were created."}

    for filename, content in file_contents.items():
        # Ensure the output directory exists
        os.makedirs("output", exist_ok=True)
        with open(os.path.join("output", filename), "w") as f:
            f.write(content)
    
    return {"files": list(file_contents.keys())}

def parse_gemini_response(response_text):
    """
    Parses the Gemini API response to extract file names and their content.
    This version is more robust to variations in filename markers.
    """
    files = {}
    
    # Pattern to match **filename.ext:** followed by code block
    pattern1 = re.compile(
        r"\*\*([\w.-]+)\*\*:?\s*\n\n```(?:\w+)?\n(.*?)\n```",
        re.DOTALL
    )
    
    matches = pattern1.findall(response_text)
    
    for filename, content in matches:
        if filename:
            files[filename.strip()] = content.strip()

    # Alternative pattern for other formats like --- filename --- 
    if not files:
        alt_pattern = re.compile(
            r"---\s*([\w.-]+)\s*---\s*\n```(?:\w+)?\n(.*?)\n```",
            re.DOTALL
        )
        matches = alt_pattern.findall(response_text)
        for filename, content in matches:
            if filename:
                files[filename.strip()] = content.strip()

    # Fallback for cases where the filename is not explicitly marked
    if not files:
        # Find all code blocks
        code_blocks = re.findall(r"```(?:\w+)?\n([\s\S]*?)\n```", response_text)
        if len(code_blocks) >= 1:
            # Try to infer filenames based on content
            for i, content in enumerate(code_blocks):
                content = content.strip()
                if "<!DOCTYPE html>" in content or "<html>" in content:
                    files["index.html"] = content
                elif "body\s*{" in content or re.search(r"[.#]\w+\s*{", content):
                    files["style.css"] = content
                elif "function" in content or "const" in content or "var" in content:
                    files["script.js"] = content
                else:
                    # Generic filename if we can't determine
                    files[f"file_{i+1}.txt"] = content
    
    return files


if __name__ == "__main__":
    # This block is for testing purposes only
    # To run, use the server.py file
    pass

