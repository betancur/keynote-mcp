-- Zen Analysis AppleScript Functions
-- Functions to analyze presentations for Presentation Zen principles

-- Function to get all text content from all slides
on getSlideTextContent(docName)
    tell application "Keynote"
        try
            if docName is not equal to "" then
                set targetDoc to document docName
            else
                set targetDoc to front document
            end if
            
            set slideTextList to {}
            set slideCount to count of slides of targetDoc
            
            repeat with slideNum from 1 to slideCount
                set currentSlide to slide slideNum of targetDoc
                set slideText to ""
                
                -- Get text from all text items on the slide
                repeat with textItem in (text items of currentSlide)
                    set slideText to slideText & (object text of textItem) & " "
                end repeat
                
                -- Clean up the text
                set slideText to my cleanText(slideText)
                
                -- Add to list with slide number
                set end of slideTextList to {slideNumber:slideNum, textContent:slideText}
            end repeat
            
            return my listToJSON(slideTextList)
            
        on error errorMsg number errorNum
            return "{\"error\":\"" & errorMsg & "\",\"errorNumber\":" & errorNum & "}"
        end try
    end tell
end getSlideTextContent

-- Function to count words in a specific slide
on countWordsInSlide(slideNum, docName)
    tell application "Keynote"
        try
            if docName is not equal to "" then
                set targetDoc to document docName
            else
                set targetDoc to front document
            end if
            
            set targetSlide to slide slideNum of targetDoc
            set slideText to ""
            
            -- Get text from all text items on the slide
            repeat with textItem in (text items of targetSlide)
                set slideText to slideText & (object text of textItem) & " "
            end repeat
            
            -- Clean and count words
            set slideText to my cleanText(slideText)
            set wordCount to my countWords(slideText)
            
            return "{\"slideNumber\":" & slideNum & ",\"wordCount\":" & wordCount & ",\"text\":\"" & slideText & "\"}"
            
        on error errorMsg number errorNum
            return "{\"error\":\"" & errorMsg & "\",\"errorNumber\":" & errorNum & "}"
        end try
    end tell
end countWordsInSlide

-- Function to analyze text density across all slides
on analyzeTextDensity(docName)
    tell application "Keynote"
        try
            if docName is not equal to "" then
                set targetDoc to document docName
            else
                set targetDoc to front document
            end if
            
            set slideCount to count of slides of targetDoc
            set totalWords to 0
            set textHeavySlides to {}
            set zenCompliantSlides to {}
            
            repeat with slideNum from 1 to slideCount
                set currentSlide to slide slideNum of targetDoc
                set slideText to ""
                
                -- Get text from all text items on the slide
                repeat with textItem in (text items of currentSlide)
                    set slideText to slideText & (object text of textItem) & " "
                end repeat
                
                -- Clean and count words
                set slideText to my cleanText(slideText)
                set wordCount to my countWords(slideText)
                set totalWords to totalWords + wordCount
                
                -- Categorize slides based on word count
                if wordCount > 6 then
                    set end of textHeavySlides to {slideNumber:slideNum, wordCount:wordCount, text:slideText}
                else
                    set end of zenCompliantSlides to {slideNumber:slideNum, wordCount:wordCount}
                end if
            end repeat
            
            set avgWords to totalWords / slideCount
            
            return "{\"totalSlides\":" & slideCount & ",\"totalWords\":" & totalWords & ",\"averageWords\":" & avgWords & ",\"textHeavySlides\":" & my listToJSON(textHeavySlides) & ",\"zenCompliantSlides\":" & my listToJSON(zenCompliantSlides) & "}"
            
        on error errorMsg number errorNum
            return "{\"error\":\"" & errorMsg & "\",\"errorNumber\":" & errorNum & "}"
        end try
    end tell
end analyzeTextDensity

-- Function to check font sizes for back row visibility
on checkFontSizes(docName)
    tell application "Keynote"
        try
            if docName is not equal to "" then
                set targetDoc to document docName
            else
                set targetDoc to front document
            end if
            
            set slideCount to count of slides of targetDoc
            set fontSizeAnalysis to {}
            
            repeat with slideNum from 1 to slideCount
                set currentSlide to slide slideNum of targetDoc
                set slideFontInfo to {}
                
                -- Analyze text items on the slide
                repeat with textItem in (text items of currentSlide)
                    try
                        set fontSize to size of font of textItem
                        set fontName to name of font of textItem
                        set end of slideFontInfo to {fontSize:fontSize, fontName:fontName}
                    on error
                        -- Skip if font info not accessible
                    end try
                end repeat
                
                if (count of slideFontInfo) > 0 then
                    set end of fontSizeAnalysis to {slideNumber:slideNum, fonts:slideFontInfo}
                end if
            end repeat
            
            return my listToJSON(fontSizeAnalysis)
            
        on error errorMsg number errorNum
            return "{\"error\":\"" & errorMsg & "\",\"errorNumber\":" & errorNum & "}"
        end try
    end tell
end checkFontSizes

-- Function to count visual elements vs text elements
on analyzeVisualBalance(docName)
    tell application "Keynote"
        try
            if docName is not equal to "" then
                set targetDoc to document docName
            else
                set targetDoc to front document
            end if
            
            set slideCount to count of slides of targetDoc
            set visualAnalysis to {}
            
            repeat with slideNum from 1 to slideCount
                set currentSlide to slide slideNum of targetDoc
                
                set textItemCount to count of text items of currentSlide
                set imageItemCount to count of images of currentSlide
                set shapeItemCount to count of shapes of currentSlide
                set totalVisualItems to imageItemCount + shapeItemCount
                
                -- Calculate visual to text ratio
                set visualToTextRatio to 0
                if textItemCount > 0 then
                    set visualToTextRatio to totalVisualItems / textItemCount
                end if
                
                set end of visualAnalysis to {slideNumber:slideNum, textItems:textItemCount, imageItems:imageItemCount, shapeItems:shapeItemCount, visualToTextRatio:visualToTextRatio}
            end repeat
            
            return my listToJSON(visualAnalysis)
            
        on error errorMsg number errorNum
            return "{\"error\":\"" & errorMsg & "\",\"errorNumber\":" & errorNum & "}"
        end try
    end tell
end analyzeVisualBalance

-- Utility function to clean text
on cleanText(inputText)
    set inputText to my replaceText(inputText, "\n", " ")
    set inputText to my replaceText(inputText, "\r", " ")
    set inputText to my replaceText(inputText, "\t", " ")
    -- Remove extra spaces
    repeat while inputText contains "  "
        set inputText to my replaceText(inputText, "  ", " ")
    end repeat
    return inputText
end cleanText

-- Utility function to count words
on countWords(inputText)
    set inputText to my cleanText(inputText)
    if inputText is "" then return 0
    set wordList to my split(inputText, " ")
    return count of wordList
end countWords

-- Utility function to replace text
on replaceText(inputText, searchText, replaceText)
    set text item delimiters to searchText
    set textItems to text items of inputText
    set text item delimiters to replaceText
    set outputText to textItems as string
    set text item delimiters to ""
    return outputText
end replaceText

-- Utility function to split text
on split(inputText, delimiter)
    set text item delimiters to delimiter
    set textItems to text items of inputText
    set text item delimiters to ""
    return textItems
end split

-- Utility function to convert list to JSON (simplified)
on listToJSON(inputList)
    set jsonString to "["
    repeat with i from 1 to count of inputList
        set currentItem to item i of inputList
        if class of currentItem is record then
            set jsonString to jsonString & my recordToJSON(currentItem)
        else
            set jsonString to jsonString & "\"" & currentItem & "\""
        end if
        if i < count of inputList then
            set jsonString to jsonString & ","
        end if
    end repeat
    set jsonString to jsonString & "]"
    return jsonString
end listToJSON

-- Utility function to convert record to JSON (simplified)
on recordToJSON(inputRecord)
    set jsonString to "{"
    set recordProperties to properties of inputRecord
    set propertyNames to {}
    
    -- Extract property names (simplified approach)
    try
        if slideNumber of inputRecord is not missing value then
            set jsonString to jsonString & "\"slideNumber\":" & (slideNumber of inputRecord) & ","
        end if
    on error
    end try
    
    try
        if textContent of inputRecord is not missing value then
            set jsonString to jsonString & "\"textContent\":\"" & (textContent of inputRecord) & "\","
        end if
    on error
    end try
    
    try
        if wordCount of inputRecord is not missing value then
            set jsonString to jsonString & "\"wordCount\":" & (wordCount of inputRecord) & ","
        end if
    on error
    end try
    
    try
        if text of inputRecord is not missing value then
            set jsonString to jsonString & "\"text\":\"" & (text of inputRecord) & "\","
        end if
    on error
    end try
    
    -- Remove trailing comma
    if jsonString ends with "," then
        set jsonString to text 1 thru -2 of jsonString
    end if
    
    set jsonString to jsonString & "}"
    return jsonString
end recordToJSON