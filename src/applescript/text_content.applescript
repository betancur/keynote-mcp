-- text_content.applescript
-- Text content management script

-- Add text box
on addTextBox(docName, slideNumber, textContent, xPos, yPos, textWidth, textHeight)
    tell application "Keynote"
        activate
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        tell targetDoc
            tell slide slideNumber
                -- Create text box
                set newTextBox to make new text item with properties {object text:textContent}
                
                -- Set position and size if specified
                if xPos is not 0 or yPos is not 0 then
                    set position of newTextBox to {xPos, yPos}
                end if
                
                if textWidth is not 0 or textHeight is not 0 then
                    set size of newTextBox to {textWidth, textHeight}
                end if
            end tell
        end tell
        
        return true
    end tell
end addTextBox

-- Add title (uses default title item when available)
on addTitle(docName, slideNumber, titleText, xPos, yPos, fontSize, fontName)
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
                    -- Try to use default title item first
                    set the object text of the default title item to titleText
                    
                    -- Apply custom formatting if specified
                    if fontSize is not 0 or fontName is not "" then
                        tell default title item
                            if fontSize is not 0 then
                                set size of object text to fontSize
                            end if
                            
                            if fontName is not "" then
                                set font of object text to fontName
                            end if
                        end tell
                    end if
                    
                    return true
                    
                on error
                    -- Fallback: Create new title text box if no default title item
                    set newTitle to make new text item with properties {object text:titleText}
                    
                    -- Set position if specified
                    if xPos is not 0 or yPos is not 0 then
                        set position of newTitle to {xPos, yPos}
                    else
                        -- Use default title position
                        set position of newTitle to {100, 100}
                    end if
                    
                    -- Set font style
                    tell newTitle
                        if fontSize is not 0 then
                            set size of object text to fontSize
                        else
                            set size of object text to 36  -- Default title size
                        end if
                        
                        if fontName is not "" then
                            set font of object text to fontName
                        end if
                        
                        -- Set to bold
                        set font style of object text to bold
                    end tell
                    
                    return true
                end try
            end tell
        end tell
    end tell
end addTitle

-- Add subtitle (uses default body item when available)
on addSubtitle(docName, slideNumber, subtitleText, xPos, yPos, fontSize, fontName)
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
                    -- Try to use default body item first
                    set the object text of the default body item to subtitleText
                    
                    -- Apply custom formatting if specified
                    if fontSize is not 0 or fontName is not "" then
                        tell default body item
                            if fontSize is not 0 then
                                set size of object text to fontSize
                            end if
                            
                            if fontName is not "" then
                                set font of object text to fontName
                            end if
                        end tell
                    end if
                    
                    return true
                    
                on error
                    -- Fallback: Create new subtitle text box if no default body item
                    set newSubtitle to make new text item with properties {object text:subtitleText}
                    
                    -- Set position if specified
                    if xPos is not 0 or yPos is not 0 then
                        set position of newSubtitle to {xPos, yPos}
                    else
                        -- Use default subtitle position
                        set position of newSubtitle to {100, 200}
                    end if
                    
                    -- Set font style
                    tell newSubtitle
                        if fontSize is not 0 then
                            set size of object text to fontSize
                        else
                            set size of object text to 24  -- Default subtitle size
                        end if
                        
                        if fontName is not "" then
                            set font of object text to fontName
                        end if
                    end tell
                    
                    return true
                end try
            end tell
        end tell
    end tell
end addSubtitle

-- Add bullet list (uses default body item when available)
on addBulletList(docName, slideNumber, listItems, xPos, yPos, fontSize, fontName)
    tell application "Keynote"
        activate
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        tell targetDoc
            tell slide slideNumber
                -- Build list text
                set listText to ""
                repeat with i from 1 to count of listItems
                    set listText to listText & "• " & (item i of listItems)
                    if i < count of listItems then
                        set listText to listText & return
                    end if
                end repeat
                
                try
                    -- Try to use default body item first
                    set the object text of the default body item to listText
                    
                    -- Apply custom formatting if specified
                    if fontSize is not 0 or fontName is not "" then
                        tell default body item
                            if fontSize is not 0 then
                                set size of object text to fontSize
                            end if
                            
                            if fontName is not "" then
                                set font of object text to fontName
                            end if
                        end tell
                    end if
                    
                    return true
                    
                on error
                    -- Fallback: Create new list text box if no default body item
                    set newList to make new text item with properties {object text:listText}
                    
                    -- Set position
                    if xPos is not 0 or yPos is not 0 then
                        set position of newList to {xPos, yPos}
                    else
                        set position of newList to {100, 250}
                    end if
                    
                    -- Set font style
                    tell newList
                        if fontSize is not 0 then
                            set size of object text to fontSize
                        else
                            set size of object text to 18  -- Default list size
                        end if
                        
                        if fontName is not "" then
                            set font of object text to fontName
                        end if
                    end tell
                    
                    return true
                end try
            end tell
        end tell
    end tell
end addBulletList

-- Add numbered list
on addNumberedList(docName, slideNumber, listItems, xPos, yPos, fontSize, fontName)
    tell application "Keynote"
        activate
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        tell targetDoc
            tell slide slideNumber
                -- Build numbered list text
                set listText to ""
                repeat with i from 1 to count of listItems
                    set listText to listText & (i as string) & ". " & (item i of listItems)
                    if i < count of listItems then
                        set listText to listText & return
                    end if
                end repeat
                
                -- Create numbered list text box
                set newList to make new text item with properties {object text:listText}
                
                -- Set position
                if xPos is not 0 or yPos is not 0 then
                    set position of newList to {xPos, yPos}
                end if
                
                -- Set font style
                tell newList
                    if fontSize is not 0 then
                        set size of object text to fontSize
                    else
                        set size of object text to 18  -- Default list size
                    end if
                    
                    if fontName is not "" then
                        set font of object text to fontName
                    end if
                end tell
            end tell
        end tell
        
        return true
    end tell
end addNumberedList

-- Add code block
on addCodeBlock(docName, slideNumber, codeText, xPos, yPos, fontSize, fontName)
    tell application "Keynote"
        activate
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        tell targetDoc
            tell slide slideNumber
                -- Create code block text box
                set newCodeBlock to make new text item with properties {object text:codeText}
                
                -- Set position
                if xPos is not 0 or yPos is not 0 then
                    set position of newCodeBlock to {xPos, yPos}
                end if
                
                -- Set font style (monospace font)
                tell newCodeBlock
                    if fontSize is not 0 then
                        set size of object text to fontSize
                    else
                        set size of object text to 14  -- Default code font size
                    end if
                    
                    if fontName is not "" then
                        set font of object text to fontName
                    else
                        set font of object text to "Monaco"  -- Default monospace font
                    end if
                end tell
            end tell
        end tell
        
        return true
    end tell
end addCodeBlock

-- Add quote text
on addQuote(docName, slideNumber, quoteText, xPos, yPos, fontSize, fontName)
    tell application "Keynote"
        activate
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        tell targetDoc
            tell slide slideNumber
                -- Add quotes to quote text
                set formattedQuote to """ & quoteText & """
                
                -- Create quote text box
                set newQuote to make new text item with properties {object text:formattedQuote}
                
                -- Set position
                if xPos is not 0 or yPos is not 0 then
                    set position of newQuote to {xPos, yPos}
                end if
                
                -- Set font style (italic)
                tell newQuote
                    if fontSize is not 0 then
                        set size of object text to fontSize
                    else
                        set size of object text to 20  -- Default quote font size
                    end if
                    
                    if fontName is not "" then
                        set font of object text to fontName
                    end if
                    
                    -- Set to italic
                    set font style of object text to italic
                end tell
            end tell
        end tell
        
        return true
    end tell
end addQuote

-- Edit text box content
on editTextBox(docName, slideNumber, textIndex, newContent)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set targetSlide to slide slideNumber of targetDoc
        
        try
            set object text of text item textIndex of targetSlide to newContent
            return true
        on error
            return false
        end try
    end tell
end editTextBox

-- Set slide content using default theme elements (recommended approach)
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
