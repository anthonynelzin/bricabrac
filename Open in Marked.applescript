-- Anthony Nelzin, 2012. CeCILL Free Software License (http://www.cecill.info/licences/Licence_CeCILL_V2-en.html)

tell application "iA Writer"
	set theDocument to file of document of window 1
end tell
tell application "Marked"
	open theDocument
	activate
end tell