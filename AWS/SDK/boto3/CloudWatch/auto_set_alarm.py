import boto3

a = open('alarm_info.csv','r',encoding="utf-8")
temp = a.readlines()
a.close()

cloudwatch = boto3.client('cloudwatch')

#EC2
for i in range(1,len(temp)):
	info = temp[i].strip().split(',')
	alarm_name = info[0]
	alarm_description = info[1]
	metric = info[2]
	namespace = info[3]
	statistic = info[4]
	threshold = float(info[5])
	greaterless = info[6]
	period = int(info[7])
	sns = info[9]
	dim = info[8].split(' ')
	dimension = []
	for k in dim:
		k = k.split(':')
		dimension.append({'Name':k[0],'Value':k[1]})

	cloudwatch.put_metric_alarm(
		AlarmName=alarm_name,
		ComparisonOperator=greaterless,
		EvaluationPeriods=period,
		MetricName=metric,
		Namespace=namespace,
		Period=300,
		Statistic=statistic,
		Threshold=threshold,
		ActionsEnabled=True,
		AlarmActions=[sns],
		AlarmDescription=alarm_description,
		Dimensions=dimension,
		TreatMissingData='ignore'
		)

	print(info[0]+'\tFinish\n')
