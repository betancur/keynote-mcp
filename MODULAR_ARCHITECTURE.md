# Modular AppleScript Architecture

## Overview

The AppleScript files have been reorganized into a modular structure for better maintainability and updates. Instead of having one large `content.applescript` file, functionality is now split across specialized files.

## File Structure

```
src/applescript/
├── keynote_base.applescript          # Basic Keynote operations
├── presentation.applescript          # Presentation management  
├── slide.applescript                 # Slide operations
├── export.applescript                # Export functionality
├── text_content.applescript          # Text content management (NEW)
├── media_content.applescript         # Images and media (NEW)
├── shapes_tables.applescript         # Shapes and tables (NEW) 
├── formatting.applescript            # Text and object formatting (NEW)
├── object_management.applescript     # Object manipulation (NEW)
├── content_main.applescript          # Main orchestrator (NEW)
└── content.applescript               # Legacy file (to be deprecated)
```

## Modular Breakdown

### 1. text_content.applescript
**Purpose**: Handle all text-related content operations
- `addTextBox()` - Add text boxes
- `addTitle()` - Add titles with formatting
- `addSubtitle()` - Add subtitles
- `addBulletList()` - Create bullet point lists
- `addNumberedList()` - Create numbered lists
- `addCodeBlock()` - Add code blocks with monospace font
- `addQuote()` - Add quoted text with italic styling
- `editTextBox()` - Edit existing text content

### 2. media_content.applescript
**Purpose**: Handle multimedia content
- `addImage()` - Add images with positioning and sizing

### 3. shapes_tables.applescript
**Purpose**: Handle shapes and table operations
- `addShape()` - Add various shapes
- `addTable()` - Create tables
- `setTableCell()` - Set table cell content

### 4. formatting.applescript
**Purpose**: Handle text and object formatting
- `setTextStyle()` - Apply font styles, sizes, colors

### 5. object_management.applescript
**Purpose**: Handle object manipulation and statistics
- `positionObject()` - Move objects
- `resizeObject()` - Resize objects  
- `deleteObject()` - Remove objects
- `getSlideContentStats()` - Get content statistics

### 6. content_main.applescript
**Purpose**: Main orchestrator that loads and delegates to other modules
- Provides wrapper functions that call the appropriate module
- Maintains backward compatibility with existing API

## Benefits of Modular Structure

1. **Better Maintainability**: Each file focuses on a specific domain
2. **Easier Updates**: Changes to text operations don't affect media operations
3. **Reduced Complexity**: Smaller, more focused files are easier to understand
4. **Parallel Development**: Multiple developers can work on different modules
5. **Testing**: Individual modules can be tested in isolation
6. **Reusability**: Modules can be reused in other projects

## Python Integration

The Python `ContentTools` class has been updated to use the modular structure:

```python
class ContentTools:
    def __init__(self):
        self.runner = AppleScriptRunner()
        # Map functions to their respective script files
        self.script_files = {
            'addTextBox': 'text_content.applescript',
            'addImage': 'media_content.applescript',
            'addShape': 'shapes_tables.applescript',
            # ... etc
        }
    
    async def add_text_box(self, ...):
        result = await self.runner.run_function(
            script_file=self.script_files['addTextBox'],
            function_name='addTextBox',
            args=[...]
        )
```

## Migration Path

1. **Phase 1**: New modular files created (✅ Complete)
2. **Phase 2**: Python tools updated to use modular files (✅ Complete)
3. **Phase 3**: Test new structure thoroughly
4. **Phase 4**: Deprecate `content.applescript` once testing is complete
5. **Phase 5**: Update documentation and examples

## Usage Example

```python
# Old way (monolithic)
await runner.run_script("content", "addTextBox", args)

# New way (modular)
await runner.run_function("text_content.applescript", "addTextBox", args)
```

## Next Steps

1. Test the modular structure thoroughly
2. Update all Python tool files to use the new structure
3. Add comprehensive error handling for missing modules
4. Create integration tests for cross-module interactions
5. Update user documentation

## Notes

- All Chinese comments have been translated to English
- Function signatures remain unchanged for backward compatibility
- The `AppleScriptRunner` class has been enhanced with a `run_function()` method
- Error handling maintains the same patterns as before
