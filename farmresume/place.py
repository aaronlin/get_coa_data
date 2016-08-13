import requests

url_template = 'http://data.coa.gov.tw/Service/OpenData/Resume/ResumeData_Plus.aspx?$top=1000&$skip='
place_count={}

for j in range(10):
	url = url_template+str(int(j*1000))
	print url
	farmgood = requests.get(url).json()
	nb = len(farmgood)
	for i in range(nb):
		p = farmgood[i]['Place'][0:3]
		d = farmgood[i]['PackDate']
		if p not in place_count:
			place_count.update({p:1})
		else:
			place_count[p]+=1
		#print str(i+1)+"/"+str(nb)
print d
print place_count
'''
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
	'''
	#print str(i+1)+'/'+str(nb)
