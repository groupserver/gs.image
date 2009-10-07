version='1.0'
release=False


import commands
def get_version():
    version_string = version
    if not release:
        status,output = commands.getstatusoutput("hg tip --template '{node|short}'")
        if status != 0:
            version_string += '-dev'
        else:
            version_string += '-%s' % output
    
    return version_string
       
    
