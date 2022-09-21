function SelectDB($param){
    $temp = aws s3 ls s3://$bucketname/$folder/
    $temp = $temp.replace('/',' ')
    $num = 1
    $db = @()
    Write-Host 'Your Database:'
    $len = $temp.Count
    for($i=0;$i -le $len-2;$i+=1){
        $db_name = ($temp[$i].Trim() -split ' ')[-1]
        $db += $db_name
        Write-Host $num'.' $db_name
        $num += 1
    }
    $db_num = Read-Host 'Please enter the number of database you would like to choose (Only one at a time):
'
    return $db[($db_num-1)]
}

function SelectFile($param){
    $file = @()
    $temp = aws s3 ls s3://$bucketname/$folder/$path/
    $len = $temp.Count
    for($i=0;$i -le $len-1;$i++){
        $k = $temp[$i] -split ' '
        $file_date = $k[0].replace('-','')
        if($file_date -eq $param){
            $file += $k[-1]
        }
    }
    return $file
}

function Download($param){
    Write-Host "Your SQL Database backup file:"
    $num = 1
    foreach($i in $param[0]){
        Write-Host $num"." $i
        $num += 1
    }
    $file_selected = Read-Host 'Please enter the number of files you would like to download (Only one at a time)
'
    if($param[0].Count -gt 1){
        $s3_path = $bucketname+'/'+$folder+'/'+$path+'/'+($param[0][($file_selected-1)])
        $file_path = $param[1]+'\'+($param[0][($file_selected-1)])
        aws s3 cp s3://$s3_path $file_path
    }else{
        $s3_path = $bucketname+'/'+$folder+'/'+$path+'/'+$param[0]
        $file_path = $param[1]+'\'+$param[0]
        aws s3 cp s3://$s3_path $file_path
    }

}

if (-not (Test-Path -Path C:\Temp\DB_Restore)){New-Item -ItemType directory -Path C:\Temp\DB_Restore}
$bucketname = '<s3 bucket name>'
$folder = '<s3 folder name>'
$local_path = Read-Host 'Please enter the local path to put your files
(default: C:\Temp\DB_Restore)
'
if(-not $local_path){$local_path = 'C:\Temp\DB_Restore'}
while(-not (Test-Path -Path $local_path)){
    Write-Host ($local_path+' does not exist.')
    $local_path = Read-Host 'Please enter the local path to put your files again
(default: C:\Temp\DB_Restore)
'
    if(-not $local_path){$local_path = 'C:\Temp\DB_Restore'}
}

$path = SelectDB($bucketname)
$date = Read-Host 'Please enter the date you would like to show (format: yyyymmdd)
'

$file = SelectFile($date)
while(-not $file){
    Write-Host ('There is no file on '+$date+'.')
    $date = Read-Host 'Please enter the date you would like to show again (format: yyyymmdd)
'
    $file = SelectFile($date)
}
Download($file,$local_path)
Read-Host 'Please press Enter to exit'