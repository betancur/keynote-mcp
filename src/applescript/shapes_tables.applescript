-- shapes_tables.applescript  
-- Shapes and tables management script

-- Add shape
on addShape(docName, slideNumber, shapeType, xPos, yPos, shapeWidth, shapeHeight)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set targetSlide to slide slideNumber of targetDoc
        
        -- Create shape
        set newShape to make new shape at end of shapes of targetSlide
        
        -- Set shape type (simplified version)
        -- Note: Actual shape type setting may need adjustment based on specific Keynote version
        
        -- Set position and size
        if xPos is not 0 or yPos is not 0 then
            set position of newShape to {xPos, yPos}
        end if
        
        if shapeWidth is not 0 or shapeHeight is not 0 then
            set size of newShape to {shapeWidth, shapeHeight}
        end if
        
        return true
    end tell
end addShape

-- Add table
on addTable(docName, slideNumber, rowCount, columnCount, xPos, yPos)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set targetSlide to slide slideNumber of targetDoc
        
        -- Create table
        set newTable to make new table at end of tables of targetSlide
        set row count of newTable to rowCount
        set column count of newTable to columnCount
        
        -- Set position
        if xPos is not 0 or yPos is not 0 then
            set position of newTable to {xPos, yPos}
        end if
        
        return true
    end tell
end addTable

-- Set table cell content
on setTableCell(docName, slideNumber, tableIndex, rowIndex, columnIndex, cellContent)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set targetSlide to slide slideNumber of targetDoc
        
        try
            set targetTable to table tableIndex of targetSlide
            set value of cell columnIndex of row rowIndex of targetTable to cellContent
            return true
        on error
            return false
        end try
    end tell
end setTableCell
