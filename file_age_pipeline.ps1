# Define the path where you want to save the CSV file
$csvPath = "C:\file_age_report.csv"

# Get the current date and time
$currentDate = Get-Date

# Prepare to write to the CSV file directly
$csvFile = New-Object System.IO.StreamWriter($csvPath)
$csvFile.WriteLine("FileName,CreationDate,CreationAgeDays,LastAccessDate,LastAccessAgeDays,LastWriteDate,LastWriteAgeDays,FileAgeDays")

# Use Get-ChildItem in a pipeline to process files one at a time
$counter = 0
$files = Get-ChildItem -Path C:\ -Recurse -File -ErrorAction SilentlyContinue

$totalFiles = $files.Count

$files | ForEach-Object {
    $file = $_
    $creationAge = $currentDate - $file.CreationTime
    $lastAccessAge = $currentDate - $file.LastAccessTime
    $lastWriteAge = $currentDate - $file.LastWriteTime

    # Write each file's information directly to the CSV file
    $csvFile.WriteLine("$($file.FullName),$($file.CreationTime),$([math]::Round($creationAge.Days, 2)),$($file.LastAccessTime),$([math]::Round($lastAccessAge.Days, 2)),$($file.LastWriteTime),$([math]::Round($lastWriteAge.Days, 2)),$([math]::Round([math]::Max($creationAge.Days, [math]::Max($lastAccessAge.Days, $lastWriteAge.Days)), 2))")

    # Update progress bar
    $counter++
    Write-Progress -PercentComplete (($counter / $totalFiles) * 100) `
                    -CurrentOperation "Processing file $counter of $totalFiles" `
                    -Status "Processing Files" `
                    -Activity "File Processing"
}

# Close the CSV file
$csvFile.Close()

Write-Output "File age report based on various timestamps has been saved to $csvPath"
