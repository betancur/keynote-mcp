-- slide_content_simple.applescript
-- Simple slide content management (non-modular version)

-- Set slide content using default theme elements
on setSlideContent(docName, slideNumber, titleText, bodyText)
    tell application "Keynote"
        activate
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        tell targetDoc
            tell slide slideNumber
                try
                    -- Set title using default title item
                    if titleText is not "" then
                        set titleItem to default title item
                        set object text of titleItem to titleText
                    end if
                on error
                    -- No default title item available
                end try
                
                try
                    -- Set body using default body item
                    if bodyText is not "" then
                        set bodyItem to default body item
                        set object text of bodyItem to bodyText
                    end if
                on error
                    -- No default body item available
                end try
                
                return true
            end tell
        end tell
    end tell
end setSlideContent

-- Get available default elements in a slide
on getSlideDefaultElements(docName, slideNumber)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        tell targetDoc
            tell slide slideNumber
                set availableElements to {}
                
                try
                    set titleExists to (default title item exists)
                    if titleExists then
                        set end of availableElements to "title"
                    end if
                on error
                    -- No title item
                end try
                
                try
                    set bodyExists to (default body item exists)
                    if bodyExists then
                        set end of availableElements to "body"
                    end if
                on error
                    -- No body item
                end try
                
                return availableElements
            end tell
        end tell
    end tell
end getSlideDefaultElements