-- content_main.applescript
-- Main content management script that orchestrates all content modules
-- This file serves as the main entry point for content operations

-- Load text content functions
property textContentScript : load script POSIX file ((path to me as text) & "::text_content.applescript")

-- Load media content functions  
property mediaContentScript : load script POSIX file ((path to me as text) & "::media_content.applescript")

-- Load shapes and tables functions
property shapesTablesScript : load script POSIX file ((path to me as text) & "::shapes_tables.applescript")

-- Load formatting functions
property formattingScript : load script POSIX file ((path to me as text) & "::formatting.applescript")

-- Load object management functions
property objectManagementScript : load script POSIX file ((path to me as text) & "::object_management.applescript")

-- Text content wrapper functions
on addTextBox(docName, slideNumber, textContent, xPos, yPos, textWidth, textHeight)
    return textContentScript's addTextBox(docName, slideNumber, textContent, xPos, yPos, textWidth, textHeight)
end addTextBox

on addTitle(docName, slideNumber, titleText, xPos, yPos, fontSize, fontName)
    return textContentScript's addTitle(docName, slideNumber, titleText, xPos, yPos, fontSize, fontName)
end addTitle

on addSubtitle(docName, slideNumber, subtitleText, xPos, yPos, fontSize, fontName)
    return textContentScript's addSubtitle(docName, slideNumber, subtitleText, xPos, yPos, fontSize, fontName)
end addSubtitle

on addBulletList(docName, slideNumber, listItems, xPos, yPos, fontSize, fontName)
    return textContentScript's addBulletList(docName, slideNumber, listItems, xPos, yPos, fontSize, fontName)
end addBulletList

on addNumberedList(docName, slideNumber, listItems, xPos, yPos, fontSize, fontName)
    return textContentScript's addNumberedList(docName, slideNumber, listItems, xPos, yPos, fontSize, fontName)
end addNumberedList

on addCodeBlock(docName, slideNumber, codeText, xPos, yPos, fontSize, fontName)
    return textContentScript's addCodeBlock(docName, slideNumber, codeText, xPos, yPos, fontSize, fontName)
end addCodeBlock

on addQuote(docName, slideNumber, quoteText, xPos, yPos, fontSize, fontName)
    return textContentScript's addQuote(docName, slideNumber, quoteText, xPos, yPos, fontSize, fontName)
end addQuote

on editTextBox(docName, slideNumber, textIndex, newContent)
    return textContentScript's editTextBox(docName, slideNumber, textIndex, newContent)
end editTextBox

-- Media content wrapper functions
on addImage(docName, slideNumber, imagePath, xPos, yPos, imageWidth, imageHeight)
    return mediaContentScript's addImage(docName, slideNumber, imagePath, xPos, yPos, imageWidth, imageHeight)
end addImage

-- Shapes and tables wrapper functions
on addShape(docName, slideNumber, shapeType, xPos, yPos, shapeWidth, shapeHeight)
    return shapesTablesScript's addShape(docName, slideNumber, shapeType, xPos, yPos, shapeWidth, shapeHeight)
end addShape

on addTable(docName, slideNumber, rowCount, columnCount, xPos, yPos)
    return shapesTablesScript's addTable(docName, slideNumber, rowCount, columnCount, xPos, yPos)
end addTable

on setTableCell(docName, slideNumber, tableIndex, rowIndex, columnIndex, cellContent)
    return shapesTablesScript's setTableCell(docName, slideNumber, tableIndex, rowIndex, columnIndex, cellContent)
end setTableCell

-- Formatting wrapper functions
on setTextStyle(docName, slideNumber, textIndex, fontSize, fontColor, fontName, isBold, isItalic)
    return formattingScript's setTextStyle(docName, slideNumber, textIndex, fontSize, fontColor, fontName, isBold, isItalic)
end setTextStyle

-- Object management wrapper functions
on positionObject(docName, slideNumber, objectType, objectIndex, xPos, yPos)
    return objectManagementScript's positionObject(docName, slideNumber, objectType, objectIndex, xPos, yPos)
end positionObject

on resizeObject(docName, slideNumber, objectType, objectIndex, newWidth, newHeight)
    return objectManagementScript's resizeObject(docName, slideNumber, objectType, objectIndex, newWidth, newHeight)
end resizeObject

on deleteObject(docName, slideNumber, objectType, objectIndex)
    return objectManagementScript's deleteObject(docName, slideNumber, objectType, objectIndex)
end deleteObject

on getSlideContentStats(docName, slideNumber)
    return objectManagementScript's getSlideContentStats(docName, slideNumber)
end getSlideContentStats
