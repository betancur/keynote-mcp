-- slide.applescript
-- Slide operations script

-- Add new slide
on addSlide(docName, slidePosition, layoutType)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        if slidePosition is 0 then
            set newSlide to make new slide at end of slides of targetDoc
        else
            set newSlide to make new slide at slide slidePosition of targetDoc
        end if
        
        -- If no layout is specified, try to use a layout with title and content
        if layoutType is "" then
            try
                -- Try to use the second master slide (typically title and bullets)
                set masterSlides to master slides of targetDoc
                if (count of masterSlides) > 1 then
                    set base slide of newSlide to master slide 2 of targetDoc
                else
                    -- If only one master slide, use it
                    set base slide of newSlide to master slide 1 of targetDoc
                end if
            on error
                -- If that fails, leave with default layout
                log "Could not set master slide layout, using default"
            end try
        else
            try
                set base slide of newSlide to master slide layoutType of targetDoc
            on error
                -- If layout doesn't exist, try using a layout with content
                try
                    set masterSlides to master slides of targetDoc
                    if (count of masterSlides) > 1 then
                        set base slide of newSlide to master slide 2 of targetDoc
                        log "Layout " & layoutType & " not found, using second master slide"
                    else
                        set base slide of newSlide to master slide 1 of targetDoc
                        log "Layout " & layoutType & " not found, using first master slide"
                    end if
                on error
                    log "Could not set any master slide layout"
                end try
            end try
        end if
        
        return slide number of newSlide
    end tell
end addSlide

-- Delete slide
on deleteSlide(docName, slideNumber)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        delete slide slideNumber of targetDoc
    end tell
end deleteSlide

-- Copy slide
on duplicateSlide(docName, slideNumber, newPosition)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set sourceSlide to slide slideNumber of targetDoc
        set newSlide to duplicate sourceSlide
        
        if newPosition is not 0 then
            move newSlide to slide newPosition of targetDoc
        end if
        
        return slide number of newSlide
    end tell
end duplicateSlide

-- Move slide
on moveSlide(docName, fromPosition, toPosition)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set sourceSlide to slide fromPosition of targetDoc
        move sourceSlide to slide toPosition of targetDoc
    end tell
end moveSlide

-- Get slide count
on getSlideCount(docName)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        return count of slides of targetDoc
    end tell
end getSlideCount

-- Select slide
on selectSlide(docName, slideNumber)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set current slide of targetDoc to slide slideNumber of targetDoc
    end tell
end selectSlide

-- Get current slide number
on getCurrentSlideNumber(docName)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        return slide number of current slide of targetDoc
    end tell
end getCurrentSlideNumber

-- Set slide layout
on setSlideLayout(docName, slideNumber, layoutType)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        try
            set master slide of slide slideNumber of targetDoc to master slide layoutType of targetDoc
            return true
        on error
            return false
        end try
    end tell
end setSlideLayout

-- Get available layouts list
on getAvailableLayouts(docName)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set layoutList to {}
        repeat with masterSlide in master slides of targetDoc
            set end of layoutList to name of masterSlide
        end repeat
        return layoutList
    end tell
end getAvailableLayouts

-- Get slide information
on getSlideInfo(docName, slideNumber)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set targetSlide to slide slideNumber of targetDoc
        set slideInfo to {}
        
        set end of slideInfo to slide number of targetSlide
        
        try
            set end of slideInfo to name of master slide of targetSlide
        on error
            set end of slideInfo to "Unknown Layout"
        end try
        
        try
            set end of slideInfo to count of text items of targetSlide
        on error
            set end of slideInfo to 0
        end try
        
        return slideInfo
    end tell
end getSlideInfo

-- Go to slide
on goToSlide(docName, slideNumber)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set current slide of targetDoc to slide slideNumber of targetDoc
        show slide slideNumber of targetDoc
    end tell
end goToSlide

-- Get slide title
on getSlideTitle(docName, slideNumber)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set targetSlide to slide slideNumber of targetDoc
        
        try
            -- Try to get title text box content
            repeat with textItem in text items of targetSlide
                if object text of textItem contains "Title" or object text of textItem contains "标题" then
                    return object text of textItem
                end if
            end repeat
            
            -- If no title found, return first text item
            if (count of text items of targetSlide) > 0 then
                return object text of text item 1 of targetSlide
            else
                return ""
            end if
        on error
            return ""
        end try
    end tell
end getSlideTitle

-- Set slide title
on setSlideTitle(docName, slideNumber, titleText)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set targetSlide to slide slideNumber of targetDoc
        
        try
            -- Try to find title text box and set content
            repeat with textItem in text items of targetSlide
                if object text of textItem contains "Title" or object text of textItem contains "标题" then
                    set object text of textItem to titleText
                    return true
                end if
            end repeat
            
            -- If no title found, set first text item
            if (count of text items of targetSlide) > 0 then
                set object text of text item 1 of targetSlide to titleText
                return true
            else
                return false
            end if
        on error
            return false
        end try
    end tell
end setSlideTitle 