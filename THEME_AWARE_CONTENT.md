# Theme-Aware Content Management

## Overview

The Keynote MCP now supports theme-aware content management, which uses the default elements provided by slide layouts instead of creating new text boxes from scratch.

## Why Use Theme Elements?

### Benefits
- **Consistent Design**: Maintains the theme's visual consistency
- **Automatic Formatting**: Uses theme's predefined fonts, colors, and styles
- **Better Performance**: No need to manually position elements
- **Professional Look**: Follows design best practices

### Example Comparison

**Old Approach (Manual)**:
```applescript
-- Creates a new text box, requiring manual positioning and styling
set newTitle to make new text item with properties {object text:"My Title"}
set position of newTitle to {100, 100}
set size of object text of newTitle to 36
set font style of object text of newTitle to bold
```

**New Approach (Theme-Aware)**:
```applescript
-- Uses the theme's predefined title element
set the object text of the default title item to "My Title"
```

## Available Default Elements

### Common Elements in Keynote Layouts

1. **Default Title Item** - Main slide title
2. **Default Body Item** - Main content area
3. **Additional Text Items** - Subtitle, footer, etc. (layout-dependent)

### Layout-Specific Availability

- **Title & Subtitle Layout**: Has both title and body items
- **Title & Content Layout**: Has title and body items  
- **Section Header Layout**: Has title item only
- **Blank Layout**: No default items (falls back to manual creation)

## Updated Functions

### 1. `setSlideContent()` (Recommended)
```python
# Set both title and content using theme elements
await content_tools.set_slide_content(
    slide_number=1,
    title="Automation Capabilities", 
    body="• Created from Swift app\n• Using AppleScript\n• Programmatic content"
)
```

### 2. Enhanced `addTitle()`
```python
# Now tries default title item first, falls back to manual creation
await content_tools.add_title(slide_number=1, title="My Title")
```

### 3. Enhanced `addSubtitle()` / `addBulletList()`
```python
# Uses default body item when available
await content_tools.add_bullet_list(
    slide_number=1, 
    items=["Point 1", "Point 2", "Point 3"]
)
```

### 4. `getSlideDefaultElements()`
```python
# Check what elements are available in a slide
result = await content_tools.get_slide_default_elements(slide_number=1)
# Returns: "Available default elements: title, body"
```

## Best Practices

### 1. Check Available Elements First
```python
# Check what's available before adding content
elements = await content_tools.get_slide_default_elements(slide_number=1)
```

### 2. Use `setSlideContent()` for Standard Layouts
```python
# Preferred method for most slides
await content_tools.set_slide_content(
    slide_number=1,
    title="Section Title",
    body="Main content here"
)
```

### 3. Manual Creation for Complex Layouts
```python
# Use manual positioning for specific design needs
await content_tools.add_text_box(
    slide_number=1,
    text="Custom positioned text",
    x=500, y=300
)
```

### 4. Fallback Behavior
All enhanced functions automatically fall back to manual creation if no default elements are available, ensuring compatibility with all layout types.

## Implementation Details

### AppleScript Level
```applescript
-- Primary approach: Use theme elements
try
    set the object text of the default title item to titleText
on error
    -- Fallback: Create manual text box
    set newTitle to make new text item with properties {object text:titleText}
    -- Apply manual positioning and styling
end try
```

### Python Level
```python
# Map functions to modular AppleScript files
self.script_files = {
    'setSlideContent': 'text_content.applescript',
    'getSlideDefaultElements': 'text_content.applescript'
}
```

## Migration Path

1. **Existing Code**: Continues to work with enhanced fallback behavior
2. **New Code**: Should prefer `setSlideContent()` when possible
3. **Complex Layouts**: Use manual positioning as needed

## Error Handling

- **No Default Elements**: Automatically falls back to manual creation
- **Invalid Layouts**: Graceful error handling with informative messages
- **Theme Compatibility**: Works with all Keynote themes

This approach provides the best of both worlds: automatic theme compliance when possible, with full manual control when needed.
