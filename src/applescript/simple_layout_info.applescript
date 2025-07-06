-- simple_layout_info.applescript
-- Simplified layout information for debugging

-- Get basic layout information
on getSimpleLayoutInfo(docName)
    tell application "Keynote"
        activate
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        -- Get available master slides
        set masterSlideNames to name of every master slide of targetDoc
        
        -- Create simple information for each layout
        set layoutInfo to {}
        
        repeat with masterName in masterSlideNames
            set masterNameStr to masterName as string
            
            -- Simple description based on name
            if masterNameStr contains "Title" and not (masterNameStr contains "Bullets") and not (masterNameStr contains "Photo") then
                set layoutDesc to "Title-focused layout - Use for: Section breaks, main titles, opening slides"
            else if masterNameStr contains "Title" and masterNameStr contains "Bullets" then
                set layoutDesc to "Title with bullet points - Use for: Feature lists, key points, structured content"
            else if masterNameStr contains "Title" and masterNameStr contains "Photo" then
                set layoutDesc to "Title with image - Use for: Product showcases, visual content with description"
            else if masterNameStr contains "Photo" and masterNameStr contains "3 Up" then
                set layoutDesc to "Multiple images - Use for: Product galleries, comparisons, multiple visuals"
            else if masterNameStr contains "Photo" then
                set layoutDesc to "Single large image - Use for: Impact photos, hero images, visual storytelling"
            else if masterNameStr contains "Quote" then
                set layoutDesc to "Quote layout - Use for: Testimonials, key messages, inspirational content"
            else if masterNameStr contains "Blank" then
                set layoutDesc to "Blank canvas - Use for: Custom designs, infographics, creative layouts"
            else if masterNameStr contains "Statement" or masterNameStr contains "Big Fact" then
                set layoutDesc to "Big statement - Use for: Key statistics, important facts, wow moments"
            else
                set layoutDesc to "Specialized layout - Use for: Specific content needs"
            end if
            
            set layoutDetails to masterNameStr & " → " & layoutDesc
            set end of layoutInfo to layoutDetails
        end repeat
        
        -- Return as simple list
        set AppleScript's text item delimiters to "\n"
        set result to layoutInfo as string
        set AppleScript's text item delimiters to ""
        
        return result
    end tell
end getSimpleLayoutInfo