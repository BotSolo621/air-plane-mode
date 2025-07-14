# latest.ps1 - Test payload that pops up a text file saying "pwned"

$text = "You have been pwned! 💀"
$file = "$env:TEMP\pwned.txt"

# Write the message to a text file
Set-Content -Path $file -Value $text -Encoding UTF8

# Open the text file with default associated app (usually Notepad)
Start-Process -FilePath $file
