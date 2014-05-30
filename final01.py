import sys

def main(argc, argv):
	if argc < 2 or argv[1][-2:] != '.v':
		sys.exit('Usage: main.py <CtoS Verilog file> [ii]')
	#Open input cdfg file
	try:
		cdfg_fp = open(argv[1], 'r')
	except IOError:
		sys.exit('Input file missing')

	file_data = cdfg_fp.readlines()
	cdfg_fp.close()

	if argc >= 3:
		ii = int(argv[2])
	else:
		ii = 1

	PRINT = False
	if argc == 4 and argv[3] == '-v':
		PRINT = True
	
	conlist=[]#constant identity list
	con_namelist=[]#constant name list
	outlist=[]
	inputlist=[]
	
	i = 0
	address=0
	while i <= len(file_data)-1:
		line = file_data[i]
#		list=[]
#		list.append(line)
#		if ";" not in line:
#			i=i+1
#			line=file_data[i]
#			list.append(line)
#			line=''.join(list).replace("\n","")
		contain=line.split()
		k=0
		for k in range(0, len(contain)):
			if "'" not in contain[k]:
				k=k+1
				sflag=0
			elif "'" in contain[k]:
				cap=contain[k].replace(";","").replace("}","").replace(")","").replace(":","").replace("/n","")
				sflag=1
				break
		if sflag==1:
			if (cap not in conlist) and ("state_" not in line) and ("joins_" not in line) and ("//" not in line) and (len(line.split("<="))!=2):
				conlist.append(cap)
				con_namelist.append(cap.replace("'",""))
				print ("constant("+cap.replace("'","")+") {")
				print ("\tbitwidth "+ cap.split("'")[0]+";")
				if "'sb" in line or "'sh" in line:
					print ("\tsigned 1;")
					cap=cap.split("'")[1]
					cap=cap.replace("s","").replace("\n","")
					if "h" in cap:#Hex to dec conversion
						valconv=cap.split("h")[1]
						valfin=int(valconv, 16)
						#print (valfin)
					elif "b" in cap:#binary to dec conversion
						valconv=cap.split("b")[1]
						valfin=int(valconv, 2)
						#print (valfin)
					print ("\tvalue "+ str(valfin)+";")					
				elif "'b" in line or "'h" in line:
					print ("\tsigned 0;")
					if "'h" in cap:
						valconv=cap.split("'h")[1]
						valfin=int(valconv, 16)
					elif "'b" in cap:#binary to dec conversion
						valconv=cap.split("'b")[1]
						valfin=int(valconv, 2)					
					print ("\tvalue "+ str(valfin) +";")
				print ("\tbank 0;")
				print ("\taddress "+str(address)+";")
				print ("}")
				address+=1
		if '$end-module' in line:
			break
		i+=1	

	i = 0
	while i <= len(file_data)-1:
		line = file_data[i]
		#list=[]
		#list.append(line)
		line=file_data[i]
		if 'read_' in line:
			#print (line)
			if len(line.split())==3 and '=' in line:
				in_name = line.split()[0] #Strip input var name
				inputlist.append(line.split()[0])
				print ("input("+in_name+") {")
				print ("\tbitwidth 32;")
				if 'signed' in line:
					print ("\tsigned 1;")
				else:
					print ("\tsigned 0;")
				print ("}")
				i+=1
				continue

		if '<=' in line and '_ln' in line:
			out_name = line.split()[2][:-1] #Strip input var name
			outlist.append(out_name)
			print ("output("+out_name+") {")
			print ("\tbitwidth 32;")
			if 'signed' in line:
				print ("\tsigned 1;")
			else:
				print ("\tsigned 0;")
			print ("}")
			i+=1
			continue
		if '$end-module' in line:
			break
		i+=1

	i = 0
	while i <= len(file_data)-1:
		line = file_data[i]
		#list=[]
		#list.append(line)
		line=file_data[i]
		if ('reg [' or 'reg signed [' in line) and ('read_' not in line):
			if 'reg [' in line and len(line.split())==3 and (line.split()[2][:-1] not in outlist):
				#print (line)
				var_name = line.split()[2][:-1] #Strip input var name
				bw0=line.split()[1]
				bw1=bw0.split(":")[0][1:]
				bw2=bw0.split(":")[1][:-1]
				bwint=int(bw1)+int(bw2)+1
				print ("variable("+var_name+")"+" {")
				print ("\tbitwidth "+ str(bwint)+";")
				print ("\tsigned 0;")
				print ("\tvalue 0;")
				print ("}")
				i+=1
				continue
			elif 'reg signed [' in line:
				var_name = line.split()[3][:-1] #Strip input var name
				bw0=line.split()[2]
				bw1=bw0.split(":")[0][1:]
				bw2=bw0.split(":")[1][:-1]
				bwint=int(bw1)+int(bw2)+1
				print ("variable("+var_name+"){")
				print ("tbitwidth "+ str(bwint)+";")
				print ("signed 1;")
				print ("}")
				i+=1
				continue
		if '$end-module' in line:
			break
		i+=1
#constant creation


#op capture below
	op_cnt=0
	
	i = 0
	while i <= len(file_data)-1:
		line = file_data[i]
#		list=[]
#		list.append(line)
#		if ";" not in line:
#			i=i+1
#			line=file_data[i]
#			list.append(line)
#			line=''.join(list).replace("\n","")
#input process
#		if ("read_" in line.split("=")[0]) and (('=') in line.split(" ")) and (('+') not in line.split(" ")) and (('-') not in line.split(" ")) and (('*') not in line.split(" ")):
#			op_cnt+=1
#			op_name = line.split()[0][:4]
#			operand1 = line.split()[2][:-1]
#			wrto = line.split()[0][:]
#			print ("operation (" + repr(op_cnt) +") {")
#			print ("function "+ op_name)
#			print ("read " + operand1)
#			print ("write "+ wrto)
#			print ("}")
#			i+=1
#			continue			
#add op process	without concatenation
		if ("add_" in line.split("=")[0]) and (("+") in line) and ("{" not in line):
			op_cnt+=1
			op_name = line.split()[0][0:3]
			operand1 = line.split()[2][:].replace("'","")
			operand2 = line.split()[4][:-1].replace("'","")
			wrto = line.split()[0][:]
			print ("operation(op" + repr(op_cnt) +")  {")
			print ("\tfunction "+ op_name+";")
			print ("\tread " + operand1 + "," + operand2+";")
			print ("\twrite "+ wrto+";")
			print ("}")
			i+=1
			continue
		elif ("add_" in line.split("=")[0]) and (("+") in line) and ("{" in line):
			op_cnt+=1
			op_name = line.split()[0][0:3]
			operand1 = line.split("=")[1].split("+")[0].replace(" ","").replace("'","")			
			operand2 = line.split("=")[1].split("+")[1].replace(" ","").replace("'","")
			wrto=line.split("=")[0].replace(" ","")
			print ("operation(op" + repr(op_cnt) +")  {")
			print ("\tfunction "+ op_name+";")
			print ("\tread " + operand1 + "," + operand2+";")
			print ("\twrite "+ wrto+";")
			print ("}")
			i+=1
			continue
		if '$end-module' in line:
			break
		i+=1
	i = 0
	while i <= len(file_data)-1:
		line = file_data[i]
#		list=[]
#		list.append(line)
#		if ";" not in line:
#			i=i+1
#			line=file_data[i]
#			list.append(line)
#			line=''.join(list).replace("\n","")

#sub op process	without concatenation	
		if ("sub_" in line.split("=")[0]) and (("-") in line) and ("{" not in line):
			op_cnt+=1
			op_name = line.split()[0][0:3]
			operand1 = line.split()[2][:].replace("'","")
			operand2 = line.split()[4][:-1].replace("'","")
			wrto = line.split()[0][:]
			print ("operation(op" + repr(op_cnt) +")  {")
			print ("\tfunction "+ op_name+";")
			print ("\tread " + operand1 + "," + operand2+";")
			print ("\twrite "+ wrto+";")
			print ("}")
			i+=1
			continue
		elif("sub_" in line.split("=")[0]) and (("-") in line) and ("{" in line):
			op_cnt+=1
			op_name = line.split()[0][0:3]
			operand1 = line.split("=")[1].split("-")[0].replace(" ","").replace("'","")		
			operand2 = line.split("=")[1].split("-")[1].replace(" ","").replace("'","")
			wrto=line.split("=")[0].replace(" ","")
			print ("operation(op" + repr(op_cnt) +")  {")
			print ("\tfunction "+ op_name+";")
			print ("\tread " + operand1 + "," + operand2+";")
			print ("\twrite "+ wrto+";")
			print ("}")
			i+=1
			continue		
		if '$end-module' in line:
			break
		i+=1
	i = 0
	while i <= len(file_data)-1:
		line = file_data[i]
#		list=[]
#		list.append(line)
#		if ";" not in line:
#			i=i+1
#			line=file_data[i]
#			list.append(line)
#			line=''.join(list).replace("\n","")
#multiply op process without concatenation
		if ("mul_" in line.split("=")[0]) and (('*') in line) and ('{' not in line):
			op_cnt+=1
			op_name = line.split()[0][0:3]
			operand1 = line.split()[2][:].replace("'","")
			operand2 = line.split()[4][:-1].replace("'","")
			wrto = line.split()[0][:]
			print ("operation(op" + repr(op_cnt) +")  {")
			print ("\tfunction "+ op_name+";")
			print ("\tread " + operand1 + "," + operand2+";")
			print ("\twrite "+ wrto+";")
			print ("}")
			i+=1
			continue
		if '$end-module' in line:
			break
		i+=1

#negate op
	i = 0
	while i <= len(file_data)-1:
		line = file_data[i]
		list=[]
		list.append(line)
		if ";" not in line:
			i=i+1
			line=file_data[i]
			list.append(line)
			line=''.join(list).replace("\n","")
		if  ("negate_" in line.split("=")[0]) and ("=") in line:
			if("{" not in line) :
				e=line.split()
				op_cnt+=1
				op_name = line.split()[0][0:6]
				e2=line.split("-")
				operand1=e2[1].split()[0][:-1]
				wrto = line.split()[0][:]
				print ("operation(op" + repr(op_cnt) +")  {")
				print ("\tfunction "+ "uminus;")
				print ("\tread " + operand1+";")
				print ("\twrite "+ wrto+";")
				print ("}")
				i+=1
				continue
			elif ("{" in line):
				e=line.split("=")
				op_cnt+=1
				operand1 = e[1]
				operand1 = operand1.replace("-","").replace(";","").replace("\n","")
				wrto = e[0].strip()
				print ("operation(op" + repr(op_cnt) +")  {")
				print ("\tfunction "+ "uminus;")
				print ("\tread " + operand1+";")
				print ("\twrite "+ wrto+";")
				print ("}")
				i+=1
				continue
		if '$end-module' in line:
			
			break
		i+=1
	print ("sink(dut_end) {")
	print ("\ttargets "+ outlist[0]+";")
	print ("}")

	print ("source(dut_start) {")
	
	if len(con_namelist)>0:
		print ("\ttargets "+con_namelist[0]+",")
		for conl in range (1, len(con_namelist)):
			print ("\t"+con_namelist[conl]+",")
		for inpl in range (0, (len(inputlist)-1)):
			print ("\t"+inputlist[inpl]+",")
		print ("\t"+inputlist[len(inputlist)-1]+";")
	elif len(con_namelist)==0:
		print("\ttargets "+inputlist[0]+",")
		for inpl in range (1, (len(inputlist)-1)):
			print ("\t"+inputlist[inpl]+",")
		print ("\t"+inputlist[len(inputlist)-1]+";")
				
	print ("}")
	
	#main call
if __name__ == "__main__":
	main(len(sys.argv),sys.argv)
