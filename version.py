version='1.0'
release=False


import commands, os
def get_version():
    version_string = ''
    if not release:
        status,output = commands.getstatusoutput("hg tip --template '{node|short}'")
        if status != 0:
            if os.path.exists('gs.image.egg-info/PKG-INFO'):
                for line in file('gs.image.egg-info/PKG-INFO'):
                    if line.find('Version: ') == 0:
                        version_string = line.strip().split('Version: ')[1].strip()
            if not version_string:
                version_string = '%s-dev' % version
        else:
            version_string += '%s-%s' % (version, output)
    
    return version_string
       
    
