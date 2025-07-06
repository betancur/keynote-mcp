-- presentation_simple.applescript
-- Simple presentation management (avoiding complex syntax)

-- Create new presentation
on createNewPresentation(presentationName, themeName)
    tell application "Keynote"
        activate
        
        -- Create new document with specific theme if provided
        if themeName is not "" then
            try
                -- Try to create with specific theme
                set newDoc to make new document with properties {document theme:(theme themeName)}
            on error
                -- If theme doesn't work, create default document
                set newDoc to make new document
                log "Theme " & themeName & " not found, using default theme"
            end try
        else
            -- Create default document
            set newDoc to make new document
        end if
        
        -- If name is specified, save to desktop
        if presentationName is not "" then
            try
                set desktopPath to (path to desktop as string) & presentationName & ".key"
                save newDoc in file desktopPath
            on error
                log "Could not save presentation with name: " & presentationName
            end try
        end if
        
        return name of newDoc
    end tell
end createNewPresentation

-- Get available themes
on getAvailableThemes()
    tell application "Keynote"
        set themeList to {}
        try
            repeat with currentTheme in themes
                set end of themeList to name of currentTheme
            end repeat
        on error
            -- If themes can't be enumerated, return empty list
            set themeList to {}
        end try
        return themeList
    end tell
end getAvailableThemes

-- Open presentation
on openPresentation(filePath)
    tell application "Keynote"
        try
            set targetFile to POSIX file filePath
            open targetFile
            return name of front document
        on error
            return "Error: Could not open file at " & filePath
        end try
    end tell
end openPresentation

-- Save presentation
on savePresentation(docName)
    tell application "Keynote"
        try
            if docName is "" then
                save front document
                return name of front document
            else
                save document docName
                return docName
            end if
        on error
            return "Error: Could not save presentation"
        end try
    end tell
end savePresentation

-- Close presentation
on closePresentation(docName, shouldSave)
    tell application "Keynote"
        try
            if docName is "" then
                set targetDoc to front document
            else
                set targetDoc to document docName
            end if
            
            if shouldSave then
                save targetDoc
            end if
            
            close targetDoc
            return true
        on error
            return false
        end try
    end tell
end closePresentation

-- List open presentations
on listPresentations()
    tell application "Keynote"
        set docList to {}
        try
            repeat with doc in documents
                set end of docList to name of doc
            end repeat
        on error
            set docList to {}
        end try
        return docList
    end tell
end listPresentations

-- Get presentation info
on getPresentationInfo(docName)
    tell application "Keynote"
        try
            if docName is "" then
                set targetDoc to front document
            else
                set targetDoc to document docName
            end if
            
            set docInfo to {}
            set end of docInfo to name of targetDoc
            set end of docInfo to count of slides of targetDoc
            
            try
                set end of docInfo to name of document theme of targetDoc
            on error
                set end of docInfo to "Unknown Theme"
            end try
            
            return docInfo
        on error
            return {"Error", 0, "Unknown"}
        end try
    end tell
end getPresentationInfo