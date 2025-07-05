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
                
                -- Set position and size
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

-- Add title
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
                -- Create title text box
                set newTitle to make new text item with properties {object text:titleText}
                
                -- Set position
                if xPos is not 0 or yPos is not 0 then
                    set position of newTitle to {xPos, yPos}
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
            end tell
        end tell
        
        return true
    end tell
end addTitle

-- Add subtitle
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
                -- Create subtitle text box
                set newSubtitle to make new text item with properties {object text:subtitleText}
                
                -- Set position
                if xPos is not 0 or yPos is not 0 then
                    set position of newSubtitle to {xPos, yPos}
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
            end tell
        end tell
        
        return true
    end tell
end addSubtitle

-- Add bullet list
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
                
                -- Create list text box
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
