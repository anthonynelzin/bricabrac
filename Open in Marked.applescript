tell application "iA Writer"
	set theDocument to file of document of window 1
end tell
tell application "Marked"
	open theDocument
	activate
end tell