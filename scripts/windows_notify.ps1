$title=$args[0]
$text=$args[1]

[void] [System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms")

$objNotifyIcon = New-Object System.Windows.Forms.NotifyIcon

$objNotifyIcon.Icon = [System.Drawing.SystemIcons]::Information
$objNotifyIcon.BalloonTipIcon = "Warning" 
$objNotifyIcon.BalloonTipTitle = $title
$objNotifyIcon.BalloonTipText = $text
$objNotifyIcon.Visible = $True 
$objNotifyIcon.ShowBalloonTip(10000)