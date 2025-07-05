# Keynote MCP Documentation

This directory contains comprehensive documentation for the Keynote Model Context Protocol (MCP) server.

## 📚 Documentation Index

### Architecture & Design
- **[Modular Architecture](./MODULAR_ARCHITECTURE.md)** - Overview of the modular AppleScript structure and benefits
- **[Theme-Aware Content](./THEME_AWARE_CONTENT.md)** - Guide to using Keynote's theme elements for better presentations
- **[Project Roadmap](./ROADMAP.md)** - Future development plans and feature timeline

### Getting Started
- **[README](../README.md)** - Project overview and quick start

## 🏗️ Architecture Overview

```
keynote-mcp/
├── docs/                           # 📖 Documentation
│   ├── README.md                   # This file
│   ├── MODULAR_ARCHITECTURE.md     # AppleScript modular structure
│   └── THEME_AWARE_CONTENT.md      # Theme element usage guide
├── src/
│   ├── applescript/               # 🍎 Modular AppleScript files
│   │   ├── keynote_base.applescript
│   │   ├── presentation.applescript
│   │   ├── slide.applescript
│   │   ├── text_content.applescript    # 🆕 Text operations
│   │   ├── media_content.applescript   # 🆕 Media operations
│   │   ├── shapes_tables.applescript   # 🆕 Shapes & tables
│   │   ├── formatting.applescript      # 🆕 Formatting
│   │   └── object_management.applescript # 🆕 Object manipulation
│   ├── tools/                     # 🐍 Python MCP tools
│   └── utils/                     # 🔧 Utilities
└── ...
```

## 🚀 Quick Navigation

### For Developers
1. Start with [Modular Architecture](./MODULAR_ARCHITECTURE.md) to understand the codebase structure
2. Read [Theme-Aware Content](./THEME_AWARE_CONTENT.md) for best practices
3. Check the main [README](../README.md) for API usage examples

### For Users
1. Follow the Quick Setup section in the main [README](../README.md)
2. See [Theme-Aware Content](./THEME_AWARE_CONTENT.md) for advanced usage
3. Refer to the main [README](../README.md) for basic operations

## 📝 Documentation Standards

All documentation in this project follows these standards:

- **Clear Structure**: Organized with headers and sections
- **Code Examples**: Practical examples for all features
- **Best Practices**: Recommended approaches highlighted
- **Error Handling**: Common issues and solutions documented
- **Cross-References**: Links between related documents

## 🔄 Recent Updates

- **Modular Architecture**: AppleScript files reorganized for better maintainability
- **Theme-Aware Functions**: New functions that use Keynote's default theme elements
- **Enhanced Documentation**: Comprehensive guides for architecture and usage

## 🤝 Contributing

When adding new documentation:

1. Place files in the appropriate subdirectory
2. Update this index with a brief description
3. Follow the existing documentation format
4. Include practical examples
5. Cross-reference related documents

## 📧 Support

For questions about the documentation or implementation:

- Review existing documentation thoroughly
- Follow the examples in the guides
