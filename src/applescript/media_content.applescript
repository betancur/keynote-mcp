-- media_content.applescript
-- Media content management script

-- Add image
on addImage(docName, slideNumber, imagePath, xPos, yPos, imageWidth, imageHeight)
    tell application "Keynote"
        activate
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        tell targetDoc
            tell slide slideNumber
                -- Add image
                set imageFile to POSIX file imagePath
                set newImage to make new image with properties {file:imageFile}
                
                -- Set position and size
                if xPos is not 0 or yPos is not 0 then
                    set position of newImage to {xPos, yPos}
                end if
                
                if imageWidth is not 0 or imageHeight is not 0 then
                    set size of newImage to {imageWidth, imageHeight}
                end if
            end tell
        end tell
        
        return true
    end tell
end addImage
