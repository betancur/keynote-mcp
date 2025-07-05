# Keynote-MCP

# Keynote-MCP

A Model Context Protocol (MCP) server that enables AI assistants to control Keynote presentations through AppleScript automation.

## Features
- **Presentation Management**: Create, open, save, close presentations  
- **Slide Operations**: Add, delete, duplicate, move slides
- **Content Management**: Add text and images to slides
- **Export Functions**: Screenshots, PDF export
- **Unsplash Integration**: High-quality images (optional)

## Quick Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Grant macOS permissions**
   - System Preferences > Security & Privacy > Privacy
   - Add Terminal and Python to **Accessibility** permissions  
   - Add Python to **Automation** permissions for Keynote

3. **Configure Claude Desktop**
   Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "keynote": {
         "command": "python3",
         "args": ["/path/to/keynote-mcp/mcp_server.py"]
       }
     }
   }
   ```

4. **Test the server**
   ```bash
   python3 test_server.py
   ```

## Optional: Unsplash Images

1. Get API key from [Unsplash Developers](https://unsplash.com/developers)
2. Create `.env` file: `UNSPLASH_KEY=your_api_key`

## Available Tools (23 total)

- `create_presentation` - Create new presentation
- `open_presentation` - Open existing presentation  
- `save_presentation` - Save presentation
- `close_presentation` - Close presentation
- `add_slide` - Add new slide
- `delete_slide` - Delete slide
- `add_text_box` - Add text to slide
- `add_image` - Add image to slide
- `screenshot_slide` - Take slide screenshot
- `export_pdf` - Export as PDF
- And more...

## License
MIT License
