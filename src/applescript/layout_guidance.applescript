-- layout_guidance.applescript
-- Provides detailed layout information and recommendations for Claude Desktop

-- Get detailed layout information with use cases and recommendations
on getDetailedLayoutInfo(docName)
    tell application "Keynote"
        activate
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        -- Get available master slides
        set masterSlideNames to name of every master slide of targetDoc
        
        -- Create detailed information for each layout
        set layoutInfo to {}
        
        repeat with masterName in masterSlideNames
            set masterNameStr to masterName as string
            
            -- Analyze layout and provide guidance
            set layoutDescription to ""
            set useCases to ""
            set bestFor to ""
            
            if masterNameStr contains "Title" and not (masterNameStr contains "Bullets") and not (masterNameStr contains "Photo") then
                set layoutDescription to "Clean title-focused layout"
                set useCases to "Section breaks, chapter introductions, main titles"
                set bestFor to "Opening slides, section dividers, emphasis slides"
                
            else if masterNameStr contains "Title" and masterNameStr contains "Bullets" then
                set layoutDescription to "Title with bullet points layout"
                set useCases to "Content slides with structured information"
                set bestFor to "Feature lists, process steps, key points"
                
            else if masterNameStr contains "Title" and masterNameStr contains "Photo" then
                set layoutDescription to "Title with large image area"
                set useCases to "Image-focused content with descriptive title"
                set bestFor to "Product showcases, before/after, hero images"
                
            else if masterNameStr contains "Photo" and masterNameStr contains "3 Up" then
                set layoutDescription to "Multiple image gallery layout"
                set useCases to "Multiple related images or comparisons"
                set bestFor to "Product catalogs, team photos, step-by-step visuals"
                
            else if masterNameStr contains "Photo" and not (masterNameStr contains "3 Up") then
                set layoutDescription to "Single large image layout"
                set useCases to "Impact images, photography, visual storytelling"
                set bestFor to "Emotional impact, visual breaks, photography"
                
            else if masterNameStr contains "Quote" then
                set layoutDescription to "Quote or testimonial layout"
                set useCases to "Customer testimonials, inspirational quotes"
                set bestFor to "Social proof, motivation, key messages"
                
            else if masterNameStr contains "Bullets" and not (masterNameStr contains "Title") then
                set layoutDescription to "Bullet points without title"
                set useCases to "Dense information, detailed lists"
                set bestFor to "Detailed explanations, specifications"
                
            else if masterNameStr contains "Blank" then
                set layoutDescription to "Completely customizable blank layout"
                set useCases to "Custom designs, complex layouts, creative content"
                set bestFor to "Infographics, custom designs, creative layouts"
                
            else if masterNameStr contains "Statement" or masterNameStr contains "Big Fact" then
                set layoutDescription to "Large text for impact statements"
                set useCases to "Statistics, key facts, important announcements"
                set bestFor to "Wow moments, key statistics, important facts"
                
            else if masterNameStr contains "Agenda" then
                set layoutDescription to "Structured agenda or outline layout"
                set useCases to "Presentation outlines, agendas, roadmaps"
                set bestFor to "Overview slides, agenda, table of contents"
                
            else if masterNameStr contains "Section" then
                set layoutDescription to "Section divider layout"
                set useCases to "Separating presentation sections"
                set bestFor to "Chapter breaks, topic transitions"
                
            else
                set layoutDescription to "Specialized layout"
                set useCases to "Specific content needs"
                set bestFor to "Various applications"
            end if
            
            -- Combine all information (ensure no empty strings)
            if layoutDescription is "" then set layoutDescription to "Standard layout"
            if useCases is "" then set useCases to "General purpose"
            if bestFor is "" then set bestFor to "Various uses"
            
            set layoutDetails to masterNameStr & "|" & layoutDescription & "|" & useCases & "|" & bestFor
            set end of layoutInfo to layoutDetails
        end repeat
        
        -- Return as formatted string
        set AppleScript's text item delimiters to "||"
        set result to layoutInfo as string
        set AppleScript's text item delimiters to ""
        
        return result
    end tell
end getDetailedLayoutInfo

-- Get layout recommendations based on slide position and content context
on getContextualLayoutSuggestions(docName, slidePosition, contentType, contentDescription, presentationTheme)
    tell application "Keynote"
        activate
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        -- Get total slide count for context
        set totalSlides to count of slides of targetDoc
        set masterSlideNames to name of every master slide of targetDoc
        
        -- Determine slide context
        set slideContext to ""
        if slidePosition ≤ 2 then
            set slideContext to "opening"
        else if slidePosition ≥ (totalSlides - 1) then
            set slideContext to "closing"
        else
            set slideContext to "content"
        end if
        
        -- Create contextual recommendations
        set recommendations to {}
        
        -- Primary recommendation based on content type and context
        if slideContext is "opening" then
            if contentType is "title" then
                repeat with masterName in masterSlideNames
                    set masterNameStr to masterName as string
                    if masterNameStr contains "Title" and not (masterNameStr contains "Bullets") then
                        set end of recommendations to masterNameStr & " (Perfect for opening title)"
                        exit repeat
                    end if
                end repeat
            else if contentType is "image" then
                repeat with masterName in masterSlideNames
                    set masterNameStr to masterName as string
                    if masterNameStr contains "Title" and masterNameStr contains "Photo" then
                        set end of recommendations to masterNameStr & " (Great opening visual)"
                        exit repeat
                    end if
                end repeat
            end if
            
        else if slideContext is "closing" then
            repeat with masterName in masterSlideNames
                set masterNameStr to masterName as string
                if masterNameStr contains "Statement" or masterNameStr contains "Quote" then
                    set end of recommendations to masterNameStr & " (Powerful closing)"
                    exit repeat
                end if
            end repeat
            
        else -- content slides
            if contentType is "image" then
                repeat with masterName in masterSlideNames
                    set masterNameStr to masterName as string
                    if masterNameStr contains "Photo" then
                        if masterNameStr contains "3 Up" and (contentDescription contains "multiple" or contentDescription contains "several" or contentDescription contains "gallery") then
                            set end of recommendations to masterNameStr & " (Multiple images detected)"
                            exit repeat
                        else if not (masterNameStr contains "3 Up") then
                            set end of recommendations to masterNameStr & " (Single impactful image)"
                            exit repeat
                        end if
                    end if
                end repeat
                
            else if contentType is "text" or contentType is "content" then
                repeat with masterName in masterSlideNames
                    set masterNameStr to masterName as string
                    if masterNameStr contains "Bullets" then
                        set end of recommendations to masterNameStr & " (Structured content)"
                        exit repeat
                    end if
                end repeat
                
            else if contentType is "quote" then
                repeat with masterName in masterSlideNames
                    set masterNameStr to masterName as string
                    if masterNameStr contains "Quote" then
                        set end of recommendations to masterNameStr & " (Designed for quotes)"
                        exit repeat
                    end if
                end repeat
            end if
        end if
        
        -- Add alternative suggestions
        set end of recommendations to "Consider variety: avoid repeating the same layout"
        set end of recommendations to "Mix text and visual layouts for better flow"
        set end of recommendations to "Use section breaks every 3-4 slides"
        
        -- Return recommendations
        set AppleScript's text item delimiters to "|"
        set result to recommendations as string
        set AppleScript's text item delimiters to ""
        
        return result
    end tell
end getContextualLayoutSuggestions

-- Get information about recently used layouts to help avoid repetition
on getRecentLayoutUsage(docName, lastNSlides)
    tell application "Keynote"
        activate
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set totalSlides to count of slides of targetDoc
        set recentLayouts to {}
        
        -- Check last N slides for their layouts
        set startSlide to totalSlides - lastNSlides + 1
        if startSlide < 1 then set startSlide to 1
        
        repeat with i from startSlide to totalSlides
            try
                set slideLayout to name of base slide of slide i of targetDoc
                set end of recentLayouts to slideLayout
            on error
                set end of recentLayouts to "Unknown"
            end try
        end repeat
        
        -- Return as formatted string
        set AppleScript's text item delimiters to "|"
        set result to recentLayouts as string
        set AppleScript's text item delimiters to ""
        
        return result
    end tell
end getRecentLayoutUsage