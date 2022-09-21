#!/bin/bash
bucketname="<s3 bucket name>"
folder="<s3 folder name>"
read -p "Please enter the local path to put your files
(default: /hana/db_backup/restores):
" local_path

temp=$(aws s3 ls s3://$bucketname/$folder/)
temp=(`echo $temp | tr '/' ' '`)
num=1
db=()
echo "Your Database:"
for ((i=1;i<=${#temp[@]};i+=2)); do db+=(${temp[$i]}); echo $num'.' ${temp[$i]}; num=$(($num+1)); done
read -p "Please enter the number of database you would like to choose (Only one at a time):
" db_num

read -p "Please enter the date you would like to show (format: yyyymmdd):
" date

temp=$(aws s3 ls s3://$bucketname/$folder/${db[$(($db_num-1))]}/)
temp=(`echo $temp | tr '/' ' '`)
file=()
for ((i=1;i<=${#temp[@]};i+=2)); do file+=(`echo ${temp[$i]} | grep $date`); done
num=1
echo "Your export file:"
for ((i=0;i<${#file[@]};i++)); do echo $num'.' ${file[$i]}; num=$(($num+1)); done
read -p "Please enter the number of file you would like to download (Only one at a time):
" file_num
if test $local_path; then aws s3 sync s3://$bucketname/$folder/${db[$(($db_num-1))]}/${file[$(($file_num-1))]} $local_path/.; else aws s3 sync s3://$bucketname/$folder/${db[$(($db_num-1))]}/${file[$(($file_num-1))]} /hana/shared/backup_service/restores/.; fi
