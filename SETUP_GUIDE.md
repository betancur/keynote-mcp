# Keynote-MCP Server Setup Guide

## 🛠️ Installation & Configuration

### 1. Install Dependencies

```bash
cd /Users/betancur/Desktop/Work/mcpServers/keynote-mcp
pip3 install -r requirements.txt
```

### 2. Grant macOS Permissions

**IMPORTANT**: You must grant the following permissions in System Preferences > Security & Privacy > Privacy:

1. **Accessibility**:
   - Add your Terminal app
   - Add Python (usually at `/usr/bin/python3`)

2. **Automation**:
   - Allow Python to control Keynote

### 3. Configure Claude Desktop

Add this configuration to your Claude Desktop config file (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "keynote": {
      "command": "python3",
      "args": ["/Users/betancur/Desktop/Work/mcpServers/keynote-mcp/mcp_server.py"],
      "env": {
        "UNSPLASH_KEY": ""
      }
    }
  }
}
```

### 4. Optional: Unsplash Integration

If you want to use Unsplash images:

1. Get an API key from [Unsplash Developers](https://unsplash.com/developers)
2. Create a `.env` file in the project root:
   ```
   UNSPLASH_KEY=your_unsplash_access_key_here
   ```

### 5. Test the Server

```bash
cd /Users/betancur/Desktop/Work/mcpServers/keynote-mcp
python3 mcp_server.py
```

If you see JSON output starting with `{"jsonrpc": "2.0", ...}`, the server is working correctly.

## 🔧 Troubleshooting

### Common Issues

1. **JSON Parse Errors**: 
   - Make sure you're using `mcp_server.py` not `start_server.py`
   - Ensure no print statements are being output to stdout

2. **Permission Denied**:
   - Check that Accessibility and Automation permissions are granted
   - Make sure Keynote is in your Applications folder

3. **Python Path Issues**:
   - Use full path to python3: `/usr/bin/python3`
   - Or use the python3 in your PATH

4. **Module Not Found**:
   - Ensure all dependencies are installed: `pip3 install -r requirements.txt`

### Testing the Connection

1. Start Claude Desktop
2. Look for "keynote" in the MCP servers list
3. Try asking: "Create a new presentation called 'Test'"

## 📚 Available Tools

The server provides 29+ tools for:
- **Presentation Management**: Create, open, save, close presentations
- **Slide Operations**: Add, delete, move, duplicate slides  
- **Content Management**: Add text, images, shapes
- **Export Functions**: Screenshots, PDF export
- **Unsplash Integration**: High-quality images (optional)

## 🆘 Getting Help

If you encounter issues:
1. Check the troubleshooting section above
2. Verify macOS permissions are correctly set
3. Test the server directly with `python3 mcp_server.py`
4. Check Claude Desktop logs for connection errors
