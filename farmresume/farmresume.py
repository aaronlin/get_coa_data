import requests

farmgood = requests.get('http://data.coa.gov.tw/Service/OpenData/Resume/ResumeData_Plus.aspx').json()

file = open('./farmgood.csv','w+')
OnPfile = open('./OnP.csv','w+')
cfile = open('./certificate.csv','w+')

file.write('PID,PName,FName,Place,PackDate,Info,OID,OName,CName,ValidDate,OnP,Certificate\n')
OnPfile.write('PID,Date,Type,Detail,Memo\n')
cfile.write('PID,Certificate\n')

nb = len(farmgood)

for i in range(nb):
	OURL = 'http://data.coa.gov.tw:80/Service/OpenData/Resume/OperationDetail_Plus.aspx?Tracecode='
	#RURL = 'http://data.coa.gov.tw:80/Service/OpenData/Resume/ResumeDetail_Plus.aspx?Tracecode='
	PURL = 'http://data.coa.gov.tw:80/Service/OpenData/Resume/ProcessDetail_Plus.aspx?Tracecode='
	CURL = 'http://data.coa.gov.tw:80/Service/OpenData/Resume/CertificateDetail_Plus.aspx?Tracecode='
	PID = farmgood[i]['Tracecode']
	PName = farmgood[i]['ProductName']
	FName = farmgood[i]['FarmerName']
	Place = farmgood[i]['Place']
	PackDate = farmgood[i]['PackDate']
	Info = farmgood[i]['StoreInfo']
	OID = farmgood[i]['OrgID']
	OName = farmgood[i]['Producer']
	CName = farmgood[i]['CertificationName']
	ValidDate = farmgood[i]['ValidDate']
	OnP = "NULL"
	Certificate = "0"
	OURL += PID
	#RURL += PID
	PURL += PID
	CURL += PID
	operation = requests.get(OURL).json()
	#detail = requests.get(RURL).json()
	process = requests.get(PURL).json()
	certificate = requests.get(CURL).json()
	for j in range(len(operation)):
		OnP = operation[j]['OperationDate']
		ODate = operation[j]['OperationDate']
		OType = operation[j]['OperationType']
		Operation = operation[j]['Operation']
		OMemo = operation[j]['OperationMemo']
		operation_string = PID+','+ODate+','+OType+','+Operation+','+OMemo
		OnPfile.write(operation_string.encode('utf8'))
		OnPfile.write('\n')
	for j in range(len(process)):
		OnP = process[j]['ProcessDate']
		PDate = process[j]['ProcessDate']
		PType = process[j]['ProcessItem']
		Process = process[j]['ProcessArea']
		PMemo = process[j]['ProcessMemo']
		process_string = PID+','+PDate+','+PType+','+Process+','+PMemo
		OnPfile.write(process_string.encode('utf8'))
		OnPfile.write('\n')	
	output_string = PID+','+PName+','+FName+','+Place+','+PackDate+','+Info+','+OID+','+OName+','+CName+','+ValidDate+','+OnP+','+Certificate
	#if len(detail):
	#	print 'Detail Resume: '+RURL
	for j in range(len(certificate)):
		Certificate = "1"
		certificate_string = PID+','+certificate[j]['Certificate']
		cfile.write(certificate_string.encode('utf8'))
		cfile.write('\n')
	file.write(output_string.encode('utf8'))
	file.write('\n')
	print str(i+1)+'/'+str(nb)
