tell application "System Events" to tell process "Xcode"
    click menu item "location" of menu 1 of menu item "Simulate Location" of menu 1 of menu bar item "Debug" of menu bar 1
    if exists (sheet 1 of window 1) then
        click (button "OK" of sheet 1 of window 1)
    end if
end tell