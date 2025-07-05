-- formatting.applescript
-- Text and object formatting script

-- Set text style
on setTextStyle(docName, slideNumber, textIndex, fontSize, fontColor, fontName, isBold, isItalic)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set targetSlide to slide slideNumber of targetDoc
        
        try
            set targetText to text item textIndex of targetSlide
            
            -- Set font size
            if fontSize is not 0 then
                set size of targetText to fontSize
            end if
            
            -- Set font name
            if fontName is not "" then
                set font of targetText to fontName
            end if
            
            -- Set bold and italic (simplified version)
            -- Note: Font style setting may need adjustment based on specific Keynote version
            
            return true
        on error
            return false
        end try
    end tell
end setTextStyle
