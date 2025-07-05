# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Keynote-MCP is a Model Context Protocol (MCP) server that enables AI assistants to control Keynote presentations through AppleScript automation. The project features a modular architecture with theme-aware content management and comprehensive Python-AppleScript integration.

## Development Commands

### Testing
```bash
# Run server tests
python3 test_server.py

# Run modular architecture tests
python3 test_modular.py

# Check architecture integrity
python3 check_architecture.py
```

### Running the Server
```bash
# Start MCP server
python3 mcp_server.py

# Install dependencies
pip install -r requirements.txt
```

### Dependencies Management
- Python 3.8+ required
- Dependencies defined in `requirements.txt`
- Key dependencies: `mcp>=1.0.0`, `aiohttp`, `Pillow`, `python-dotenv`

## Architecture Overview

### Core Components

**Server Architecture:**
- `mcp_server.py`: Entry point for MCP clients
- `src/server.py`: Main MCP server implementation with KeynoteMCPServer class
- `src/tools/`: Modular tool implementations (presentation, slide, content, export)
- `src/utils/`: Utilities including AppleScriptRunner and error handling

**AppleScript Modular Structure:**
The AppleScript code is organized into specialized modules in `src/applescript/`:
- `keynote_base.applescript`: Core Keynote operations
- `presentation.applescript`: Presentation management
- `slide.applescript`: Slide operations
- `text_content.applescript`: Text content handling
- `media_content.applescript`: Image and media operations
- `shapes_tables.applescript`: Shapes and table operations
- `formatting.applescript`: Text and object formatting
- `object_management.applescript`: Object manipulation
- `export.applescript`: Export functionality

### Key Design Patterns

**Tool Organization:**
Each tool category is implemented as a separate class:
- `PresentationTools`: Create, open, save, close presentations
- `SlideTools`: Add, delete, move, duplicate slides
- `ContentTools`: Add text, images, theme-aware content
- `ExportTools`: PDF export, screenshots

**AppleScript Integration:**
- `AppleScriptRunner` class handles execution of AppleScript files
- Modular approach: each function can be in its own specialized file
- Both inline script execution and file-based execution supported
- Error handling through custom exception classes

**Theme-Aware Content:**
- New feature that uses Keynote's built-in design elements
- Functions like `set_slide_content()` and `get_slide_default_elements()`
- Professional styling with consistent theme application

## macOS Permissions

This project requires specific macOS permissions:
- **Accessibility**: Required for Terminal and Python
- **Automation**: Required for Python to control Keynote
- Configure in: System Preferences > Security & Privacy > Privacy

## Common Development Patterns

### Adding New Tools
1. Create tool class in `src/tools/`
2. Add corresponding AppleScript file(s) in `src/applescript/`
3. Register tool in `KeynoteMCPServer` class
4. Add error handling using custom exception classes

### AppleScript Development
- Use modular approach: split functionality into specific files
- Functions should return JSON-compatible results
- Handle errors gracefully with try-catch blocks
- Test with `AppleScriptRunner.run_function()` method

### Error Handling
Custom exception hierarchy:
- `KeynoteError`: Base exception
- `AppleScriptError`: AppleScript execution errors
- `FileOperationError`: File system errors
- `ParameterError`: Invalid parameters

## Testing Strategy

- `test_server.py`: Basic server functionality and tool loading
- `test_modular.py`: Modular architecture testing
- `check_architecture.py`: Architecture integrity verification
- AppleScript functions should be testable independently

## Configuration

### Environment Variables
- Optional `.env` file support
- Environment variables loaded automatically at startup
- Example configuration in `env.example`

### Claude Desktop Integration
Server configured in `claude_desktop_config.json`:
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

## Documentation

Comprehensive documentation available in `docs/`:
- `MODULAR_ARCHITECTURE.md`: Detailed architecture overview
- `THEME_AWARE_CONTENT.md`: Theme-aware content management
- `ROADMAP.md`: Future development plans
- `README.md`: Documentation index

## Platform Requirements

- **macOS only**: Uses AppleScript for Keynote automation
- **Keynote required**: Must be installed from App Store
- **Python 3.8+**: Required for MCP server functionality