-- object_management.applescript
-- Object positioning, resizing and deletion script

-- Set object position
on positionObject(docName, slideNumber, objectType, objectIndex, xPos, yPos)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set targetSlide to slide slideNumber of targetDoc
        
        try
            if objectType is "text" then
                set position of text item objectIndex of targetSlide to {xPos, yPos}
            else if objectType is "image" then
                set position of image objectIndex of targetSlide to {xPos, yPos}
            else if objectType is "shape" then
                set position of shape objectIndex of targetSlide to {xPos, yPos}
            else if objectType is "table" then
                set position of table objectIndex of targetSlide to {xPos, yPos}
            end if
            
            return true
        on error
            return false
        end try
    end tell
end positionObject

-- Resize object
on resizeObject(docName, slideNumber, objectType, objectIndex, newWidth, newHeight)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set targetSlide to slide slideNumber of targetDoc
        
        try
            if objectType is "text" then
                set size of text item objectIndex of targetSlide to {newWidth, newHeight}
            else if objectType is "image" then
                set size of image objectIndex of targetSlide to {newWidth, newHeight}
            else if objectType is "shape" then
                set size of shape objectIndex of targetSlide to {newWidth, newHeight}
            else if objectType is "table" then
                set size of table objectIndex of targetSlide to {newWidth, newHeight}
            end if
            
            return true
        on error
            return false
        end try
    end tell
end resizeObject

-- Delete object
on deleteObject(docName, slideNumber, objectType, objectIndex)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set targetSlide to slide slideNumber of targetDoc
        
        try
            if objectType is "text" then
                delete text item objectIndex of targetSlide
            else if objectType is "image" then
                delete image objectIndex of targetSlide
            else if objectType is "shape" then
                delete shape objectIndex of targetSlide
            else if objectType is "table" then
                delete table objectIndex of targetSlide
            end if
            
            return true
        on error
            return false
        end try
    end tell
end deleteObject

-- Get slide content statistics
on getSlideContentStats(docName, slideNumber)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set targetSlide to slide slideNumber of targetDoc
        
        set stats to {}
        
        try
            set end of stats to count of text items of targetSlide
        on error
            set end of stats to 0
        end try
        
        try
            set end of stats to count of images of targetSlide
        on error
            set end of stats to 0
        end try
        
        try
            set end of stats to count of shapes of targetSlide
        on error
            set end of stats to 0
        end try
        
        try
            set end of stats to count of tables of targetSlide
        on error
            set end of stats to 0
        end try
        
        return stats
    end tell
end getSlideContentStats
