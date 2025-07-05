-- content.applescript
-- DEPRECATED: This file is maintained for backward compatibility only
-- Use the modular files directly: text_content.applescript, media_content.applescript, etc.
-- 
-- This file will be removed in a future version.

-- Load modular scripts
property textContentScript : load script POSIX file ((path to me as text) & "::text_content.applescript")
property mediaContentScript : load script POSIX file ((path to me as text) & "::media_content.applescript")
property shapesTablesScript : load script POSIX file ((path to me as text) & "::shapes_tables.applescript")
property formattingScript : load script POSIX file ((path to me as text) & "::formatting.applescript")
property objectManagementScript : load script POSIX file ((path to me as text) & "::object_management.applescript")

-- Text content functions (redirect to modular files)
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

-- Media content functions
on addImage(docName, slideNumber, imagePath, xPos, yPos, imageWidth, imageHeight)
    return mediaContentScript's addImage(docName, slideNumber, imagePath, xPos, yPos, imageWidth, imageHeight)
end addImage

-- Shapes and tables functions
on addShape(docName, slideNumber, shapeType, xPos, yPos, shapeWidth, shapeHeight)
    return shapesTablesScript's addShape(docName, slideNumber, shapeType, xPos, yPos, shapeWidth, shapeHeight)
end addShape

on addTable(docName, slideNumber, rowCount, columnCount, xPos, yPos)
    return shapesTablesScript's addTable(docName, slideNumber, rowCount, columnCount, xPos, yPos)
end addTable

on setTableCell(docName, slideNumber, tableIndex, rowIndex, columnIndex, cellContent)
    return shapesTablesScript's setTableCell(docName, slideNumber, tableIndex, rowIndex, columnIndex, cellContent)
end setTableCell

-- Formatting functions
on setTextStyle(docName, slideNumber, textIndex, fontSize, fontColor, fontName, isBold, isItalic)
    return formattingScript's setTextStyle(docName, slideNumber, textIndex, fontSize, fontColor, fontName, isBold, isItalic)
end setTextStyle

-- Object management functions
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
