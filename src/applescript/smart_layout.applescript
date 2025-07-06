-- smart_layout.applescript
-- Intelligent slide layout selection based on content type

-- Get available master slides for a presentation
on getAvailableMasterSlides(docName)
    tell application "Keynote"
        activate
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        -- Get list of master slide names
        set masterSlideNames to name of every master slide of targetDoc
        
        -- Return as JSON-like string for easier parsing
        set AppleScript's text item delimiters to "\", \""
        set masterSlideList to "\"" & (masterSlideNames as string) & "\""
        set AppleScript's text item delimiters to ""
        
        return "[" & masterSlideList & "]"
    end tell
end getAvailableMasterSlides

-- Suggest best layout based on content type and available masters
on suggestLayoutForContent(docName, contentType, contentDescription)
    tell application "Keynote"
        activate
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        -- Get available master slides
        set masterSlideNames to name of every master slide of targetDoc
        
        -- Define content type to layout mapping
        set suggestedLayout to ""
        
        -- Check content type and suggest appropriate layout
        if contentType is "image" or contentType is "photo" then
            -- For image content, prefer photo layouts
            repeat with masterName in masterSlideNames
                set masterNameStr to masterName as string
                if masterNameStr contains "Photo" then
                    set suggestedLayout to masterNameStr
                    exit repeat
                end if
            end repeat
            
            -- If no photo layout found, try image-related layouts
            if suggestedLayout is "" then
                repeat with masterName in masterSlideNames
                    set masterNameStr to masterName as string
                    if masterNameStr contains "Image" or masterNameStr contains "Picture" then
                        set suggestedLayout to masterNameStr
                        exit repeat
                    end if
                end repeat
            end if
            
        else if contentType is "text" or contentType is "content" then
            -- For text content, prefer content layouts
            repeat with masterName in masterSlideNames
                set masterNameStr to masterName as string
                if masterNameStr contains "Bullets" or masterNameStr contains "Content" then
                    set suggestedLayout to masterNameStr
                    exit repeat
                end if
            end repeat
            
        else if contentType is "title" then
            -- For title slides, prefer title layouts
            repeat with masterName in masterSlideNames
                set masterNameStr to masterName as string
                if masterNameStr contains "Title" and not (masterNameStr contains "Bullets") then
                    set suggestedLayout to masterNameStr
                    exit repeat
                end if
            end repeat
            
        else if contentType is "quote" then
            -- For quotes, prefer quote layouts
            repeat with masterName in masterSlideNames
                set masterNameStr to masterName as string
                if masterNameStr contains "Quote" then
                    set suggestedLayout to masterNameStr
                    exit repeat
                end if
            end repeat
            
        else if contentType is "comparison" or contentType is "split" then
            -- For comparison content, prefer layouts with multiple areas
            repeat with masterName in masterSlideNames
                set masterNameStr to masterName as string
                if masterNameStr contains "Two" or masterNameStr contains "Split" or masterNameStr contains "Comparison" then
                    set suggestedLayout to masterNameStr
                    exit repeat
                end if
            end repeat
            
        else if contentType is "gallery" or contentType is "multiple_images" then
            -- For multiple images, prefer gallery layouts
            repeat with masterName in masterSlideNames
                set masterNameStr to masterName as string
                if masterNameStr contains "3 Up" or masterNameStr contains "Gallery" or masterNameStr contains "Grid" then
                    set suggestedLayout to masterNameStr
                    exit repeat
                end if
            end repeat
            
        else if contentType is "blank" then
            -- For blank slides, prefer blank layouts
            repeat with masterName in masterSlideNames
                set masterNameStr to masterName as string
                if masterNameStr contains "Blank" then
                    set suggestedLayout to masterNameStr
                    exit repeat
                end if
            end repeat
        end if
        
        -- If no specific layout found, use a default content layout
        if suggestedLayout is "" then
            repeat with masterName in masterSlideNames
                set masterNameStr to masterName as string
                if masterNameStr contains "Title" and masterNameStr contains "Bullets" then
                    set suggestedLayout to masterNameStr
                    exit repeat
                end if
            end repeat
        end if
        
        -- Final fallback: use the second master slide (usually a content slide)
        if suggestedLayout is "" then
            if (count of masterSlideNames) > 1 then
                set suggestedLayout to item 2 of masterSlideNames
            else
                set suggestedLayout to item 1 of masterSlideNames
            end if
        end if
        
        return suggestedLayout
    end tell
end suggestLayoutForContent

-- Add slide with smart layout selection and presenter notes
on addSlideWithSmartLayout(docName, slidePosition, contentType, contentDescription)
    tell application "Keynote"
        activate
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        -- Get suggested layout
        set suggestedLayout to my suggestLayoutForContent(docName, contentType, contentDescription)
        
        -- Create new slide
        if slidePosition is 0 then
            set newSlide to make new slide at end of slides of targetDoc
        else
            set newSlide to make new slide at slide slidePosition of targetDoc
        end if
        
        -- Apply the suggested layout
        try
            set base slide of newSlide to master slide suggestedLayout of targetDoc
            set layoutApplied to true
        on error
            set layoutApplied to false
        end try
        
        -- Set presenter notes for image/photo content types
        if (contentType is "image" or contentType is "photo" or contentType is "gallery" or contentType is "multiple_images") and contentDescription is not "" then
            try
                set presenterNotesText to "Image suggestion: " & contentDescription
                set presenter notes of newSlide to presenterNotesText
            on error errorMsg
                -- Ignore errors setting presenter notes, but log for debugging
                log "Could not set presenter notes: " & errorMsg
            end try
        end if
        
        -- Return slide number and layout info
        set slideNumber to slide number of newSlide
        
        if layoutApplied then
            return slideNumber & "|" & suggestedLayout
        else
            return slideNumber & "|default"
        end if
    end tell
end addSlideWithSmartLayout

-- Get layout recommendations for content
on getLayoutRecommendations(docName, contentType, contentDescription)
    tell application "Keynote"
        activate
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        -- Get available master slides
        set masterSlideNames to name of every master slide of targetDoc
        
        -- Simplified: just return the primary recommendation plus two others
        set recommendations to {}
        
        -- Get primary recommendation using existing function
        set primaryLayout to my suggestLayoutForContent(docName, contentType, contentDescription)
        if primaryLayout is not "" then
            set end of recommendations to primaryLayout
        end if
        
        -- Add two more different layouts
        set addedCount to 0
        repeat with masterName in masterSlideNames
            set masterNameStr to masterName as string
            if masterNameStr is not primaryLayout and addedCount < 2 then
                set end of recommendations to masterNameStr
                set addedCount to addedCount + 1
            end if
        end repeat
        
        -- Return as formatted string
        set AppleScript's text item delimiters to "|"
        set resultString to recommendations as string
        set AppleScript's text item delimiters to ""
        
        return resultString
    end tell
end getLayoutRecommendations