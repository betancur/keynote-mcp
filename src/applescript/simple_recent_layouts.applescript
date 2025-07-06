-- simple_recent_layouts.applescript
-- Get recent layout usage for guidance

-- Get information about recently used layouts
on getSimpleRecentLayouts(docName, lastNSlides)
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
                set slideInfo to "Slide " & i & ": " & slideLayout
                set end of recentLayouts to slideInfo
            on error
                set slideInfo to "Slide " & i & ": Unknown layout"
                set end of recentLayouts to slideInfo
            end try
        end repeat
        
        -- Return as formatted string
        set AppleScript's text item delimiters to "\n"
        set resultText to recentLayouts as string
        set AppleScript's text item delimiters to ""
        
        return resultText
    end tell
end getSimpleRecentLayouts