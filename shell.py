import time, os, sys, shutil
from stat import *
from os import stat
from pwd import *
#os.system("clear")
sys.stderr.write("\x1b[2J\x1b[H")

pcuser = os.getlogin()

def isgroupreadable(filepath):
	st = os.stat(filepath)
	return bool(st.st_mode & S_IRGRP)

def recurse(file, tab):
#print tab,
	thisfile=file.split("/")[-1]
	print ("|\t"*(tab-1))+"#-------------------------- %s/ --------------------------#" %thisfile
	if(isgroupreadable(file)==False):
		print ("\t"*(tab-1))+"                        (PERMISSION DENIED)" 
		return
	for i in os.walk(file):
		if(len(i[2])==0):
			print ("\t"*(tab-1))+"                        (EMPTY FOLDER)" 
			return
		for tmpfile in i[2]:
		 	if(tmpfile[0]!='.'):
				print ("|\t"*tab)+"|"
				print ("|\t"*tab)+"#--"+tmpfile 
		for directory in i[1]:
			tmpdir=i[0]+"/"+directory
			print ("|\t"*tab)+"|"
			recurse(tmpdir, tab+1)
		break


while True:
	try:	
		comm=raw_input("$ ")
		if(comm.split()[0]=="mkdir"):
			for i in comm.split():
				if(i!="mkdir"):
					os.mkdir(i)

		elif(comm=="clear"):
		  	sys.stderr.write("\x1b[2J\x1b[H")

		elif(comm.strip()=="whoami"):
		  	print pcuser

		elif(comm.split()[0]=="ls"):
			tmp=comm.split()
			if(len(tmp)==1):
				for i in os.listdir("."):
				      	if(i[0]!='.'):
						print i,
				print 			

			elif(tmp[1]=='-a'):
					
				if(len(tmp)==2):
					print ". ..",
					for i in os.listdir("."):
						print i+" ",
				else:
				 	if(tmp[2][0]=='~'):
						tmp[2]="/home/"+pcuser+tmp[2][1:]
					try:
						tmpx=os.listdir(tmp[2])
				 	except OSError as e:
						print "ls: %s" %e
						continue
					print ". ..",
				 	for i in os.listdir(tmp[2]):
						print i,
					print 
			elif(tmp[1]=="-l"):
			   	if(len(tmp)==2):
					tmpfile="."
				else:
					try:
						tmpfile=tmp[2]

				 		if(tmpfile[0]=='~'):
							tmpfile="/home/"+pcuser+tmpfile[1:]+"/"
						else:
						 	tmpfile=os.path.realpath(".")+"/"+tmpfile
				 		tmpx=os.listdir(tmpfile)
					except OSError as e:
						print "ls: %s" %e
				tmpdict={'0':'---','1':"--x",'2':"-w-",'3':"-wx",'4':"r--",'5':"r-x",'6':"rw-",'7':"rwx"}
				for i in os.listdir(tmpfile):
					if(i[0]=='.'):
						continue
					i=tmpfile+"/"+i
					per=oct(os.stat(i)[ST_MODE])[-3:]
	       	       	 		count=0
					decide=os.path.isdir(i)
					tmpstr=""
					for j in per:
#print tmpdict[j],	
						if(count==0):
							if(os.path.islink(i)):
								tmpstr+='l'
							elif(decide):
								tmpstr+='d'
							else:
							 	tmpstr+='-'
							tmpstr+=tmpdict[j]
						else:
							tmpstr+=tmpdict[j]
						count+=1
					try:
						t=time.ctime(os.path.getmtime(i))[4:-8].split()
						print "%s %3d %-4s %-4s %10d %3s %2s %2s %s" %(tmpstr, os.stat(i)[3], getpwuid(stat(i).st_gid).pw_name,getpwuid(stat(i).st_uid).pw_name, os.stat(i).st_size, t[0], t[1], t[2], i.split("/")[-1])
					except OSError as e:
						print "ls: %s" %e
			else:
				if(len(comm.split())==2 and (comm.split()[1]!='-a' and comm.split()[1]!='-l' and comm.split()[1]!='-la')):
					file=tmp[1]
					
					if(file[0]=="~"):
						file="/home/"+pcuser+file[1:]
					try:
						for i in os.listdir(file):
                                                	if(i[0]!='.'):	
								print i,
						print
					except OSError as e:
					   	print "ls: %s" %e
	
		elif(comm.strip()=="pwd"):
			tmp=os.path.realpath(".")
			print tmp

		elif(comm[:2]=="cd"):
			tmp=comm.split()
			if(len(tmp)==1):
				os.chdir("/home/"+pcuser)
				continue
			if(tmp[1][0]=='~'):
				tmp[1]='/home/'+pcuser+tmp[1][1:]
			try:
			    	if(os.path.isdir(tmp[1])):
		       		 	os.chdir(tmp[1])
		     		else:
					print "Input file is not a directory"
		     	except OSError as e:
				print "cd: %s" %e 
		elif(comm.split()[0]=='mv'):
			try:
				l=comm.split()
				if(len(l)!=3):
					print "Please Check The command"
					continue
				shutil.move(comm.split()[1], comm.split()[2])
			except IOError as e:
				print "mv: %s" %e
		elif(comm.split()[0]=='cp'):
			try:
				shutil.copy(comm.split()[1], comm.split()[2])
			except IOError as e:
				print "cp: %s" %e
		elif(comm.split()[0]=='rm'):
			try:
				l=comm.split()
				flag=0
				if((len(l)==2 and (l[1]=='-r' or l[1]=='rf')) or len(l)==1):
					print "Please give an input file for the command"
				for i in l:
					if(i=='-r' or i=='-rf'):
						flag=1
					if(i!='rm' and i!='-r' and i!='-rf'):
						if(os.path.isdir(i) and flag):
							shutil.rmtree(i)
						elif(os.path.isdir(i) and flag==0):
						 	print "%s is a directory add -r for removing" %(i)
						elif(os.path.isdir(i)==False):
							os.remove(i)

			except OSError as e:
				print "rm: %s" %e
#	elif(comm.split()[0]=='')
		elif comm.split()[0]=="dirstr":
			tmparr=comm.split()
			if(len(tmparr)==1):
				recurse(".", 1)	
			else:
				if(tmparr[1][0]=="~"):
					tmparr[1]="/home/"+pcuser+tmparr[1][1:]
				if(os.path.isdir(tmparr[1])):
					recurse(tmparr[1], 1)
				elif(os.path.isfile(tmparr[1])):
					print "Input is a file and not a directory"
				else:
			 		print "File does not exist"
		else:
			print "Command not Implemented"
	except EOFError:
	      	print "\n"
		sys.exit()
	except KeyboardInterrupt:
	      	print "\n"
		sys.exit()
