function StartSession {
	param(
		[Parameter(Mandatory=$true)]
		$ID,
		[Parameter(Mandatory=$true)]
		$Port
	)
	Start-Process -WindowStyle hidden -FilePath 'powershell.exe' -ArgumentList ('aws ssm start-session --target '+$ID+' --document-name AWS-StartPortForwardingSession --parameters localPortNumber='+$Port+',portNumber=3389')
}

$ec2 = Get-SSMInstanceInformation
$win_temp = @()
$win_temp_2 = @()
$lin_temp = @()
$lin_temp_2 = @()
$port = @()
$win_port_num = 55600
$lin_port_num = 55700
foreach($i in $ec2){
	if($i.PlatformType -eq 'Windows'){
		$win_temp += $i.ComputerName
		$win_temp_2 += $i.InstanceId
		$port += [string]$win_port_num
		$win_port_num += 1
	}
	if($i.PlatformType -eq 'Linux'){
		$lin_temp += $i.ComputerName
		$lin_temp_2 += $i.InstanceId
		$port += [string]$lin_port_num
		$lin_port_num += 1
	}
}
$os = Read-Host 'Which OS would you like to connect ?
[1] Windows   [2] Linux   
'
if($os -eq '1'){
	if($win_temp -ne ''){
		Write-Host 'Windows instances you can connect:'
		for($i=0;$i -le ($win_temp.Count-1);$i++){
			Write-Host ($i+1)'.'($win_temp[$i])'('($win_temp_2[$i])') (port:'$port[$i]')'
		}
		$id_num = Read-Host 'Which EC2 would you like to connect (If more than one, please separate by comma)
'
		$id_num = $id_num -split ","
		$RDP = Read-Host 'Would you like to use Windows Remote Desktop Connection? 
[Y] Yes   [N] No   (default is [Y])
'
		foreach($i in $id_num){
			StartSession -ID ($win_temp_2[$i-1]) -Port ($port[$i-1])
			Start-Sleep -Seconds 5
			$port_temp = $port[$i-1]
			if(($RDP -eq '') -or ($RDP -like 'Y')){mstsc /v:localhost:$port_temp}
			Write-Host 'The Session of'($win_temp_2[$i-1])'is already created
ServerName:'($win_temp[$i-1])'
Port:'($port[$i-1])'
'
		}
		Read-Host 'Please press Enter to end sessions
'
		$session = Get-Process -Name 'session-manager-plugin'
		foreach($i in $session){Stop-Process -Id $i.Id}
	}
	else{
		Write-Host 'There is no instances to connect.'
		Read-Host 'Please press Enter to exit'
	}
}
elseif($os -eq '2'){
	if($lin_temp -ne ''){
		$mode = Read-Host 'Which mode would you like to use? 
[1] Command line   [2] GUI   '
		Write-Host 'Linux instances you can connect:'
		for($i=0;$i -le ($lin_temp.Count-1);$i++){
			Write-Host ($i+1)'.'($lin_temp[$i])'('($lin_temp_2[$i])') (port:'$port[$i]')'
		}
		if($mode -eq '1'){
			$id_num = Read-Host 'Which EC2 would you like to connect (Only one instance at a time)'
			Set-Clipboard -Value $lin_temp_2[($id_num-1)]
			Write-Host 'The instance id has been pasted to clipboard already.'
			Read-Host 'Please press Enter to exit'
		}
		elseif($mode -eq '2'){
			$id_num = Read-Host 'Which EC2 would you like to connect (If more than one, please separate by comma)'
			$id_num = $id_num -split ","
			foreach($i in $id_num){
				StartSession -ID ($lin_temp_2[$i-1]) -Port ($port[$i-1])
				Start-Sleep -Seconds 5
				$port_temp = $port[$i-1]
				mstsc C:\aws_ec2\ssm.rdp /v:localhost:$port_temp
			}
			Read-Host 'Please press Enter to end sessions'
			$session = Get-Process -Name 'session-manager-plugin'
			foreach($i in $session){Stop-Process -Id $i.Id}
		}
	}
	else{
		Write-Host 'There is no instances to connect.'
		Read-Host 'Please press Enter to exit'
	}
}
else{
	Write-Host 'There is no instances to connect.'
	Read-Host 'Please press Enter to exit'
}