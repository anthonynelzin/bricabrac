-- Anthony Nelzin, 2012. CeCILL Free Software License (http://www.cecill.info/licences/Licence_CeCILL_V2-en.html)

display dialog "What word would you like to define?" default answer "" with title "Add a Markdown referenced link to Wikipedia" with icon note

set theReference to (text returned of result) as text
set theAnchor to "[" & theReference & "][" & theReference & "]"
set theLink to "[" & theReference & "]: http://en.wikipedia.org/wiki/" & theReference & " '" & theReference & " - Wikipedia, the free encyclopedia'"

tell application "iA Writer"
	activate
	tell application "System Events"
		set the clipboard to theAnchor
		keystroke "v" using {command down}
		delay 0.5
		set the clipboard to theLink
		keystroke (ASCII character 31) using {command down}
		delay 0.2
		key code 36 using {option down}
		delay 0.5
		keystroke "v" using {command down}
	end tell
end tell