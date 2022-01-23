import os
def backupexists(filepath):
    exists = os.path.isfile(filepath)
    return exists
        

def backup_check(savefilepath,backupexists):
    counter=1
    backupfilepath = savefilepath+"-BAK-"+str(counter)
    exists = backupexists(backupfilepath)
    backupfilepath = savefilepath+"-BAK-"+str(counter)
    while exists:
        counter = counter+1
        backupfilepath = savefilepath+"-BAK-"+str(counter)
        exists = backupexists(backupfilepath)
        if exists != True:
            f = open(backupfilepath, "x")
            break
    return backupfilepath
        
def backup(savefilepath,backupfile):
    with open(savefilepath,'r') as file:
        backupdata=file.read()
    with open(backupfile,'w') as backupfile:
        backupfile.write(backupdata)