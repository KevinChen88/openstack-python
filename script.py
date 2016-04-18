#Script - download and configure devstack to deploy openstack
#Requires user to fill out local.conf file manually
#Must be run as stack user


try:
    import git
    import os
    import ConfigParser 
    import subprocess
except:
    print 'Error: missing necessary modules. exiting...'
    exit()

def main():
    config=config_files('config.ini')
    commit_id=config_files('commit_ids.ini')
    install_dir=config.get('default','install_directory')  
    git_devstack(install_dir,commit_id)
    deploy_openstack(install_dir)

def config_files(config_filename):
    #Function - Parse config files and return object
    print 'parsing %s ...' %config_filename
    config=ConfigParser.RawConfigParser()
    config.read(config_filename)
    return config
    
def git_devstack(install_dir,commit_id):
    #Function - Git clone devstack and components
    #Switch to user's target directory
    git_dir=install_dir+'/devstack'
    os.chdir(install_dir)
    #Loop thru commit_id list and git clone/checkout    
    for i in commit_id.sections():
        git_url=commit_id.get(i,'url')
        git_branch=commit_id.get(i,'branch')
        git_tag=commit_id.get(i,'tag')                
        if i != 'devstack':
            new_dir=install_dir+'/devstack'
            git_dir=new_dir+'/'+i
            os.chdir(new_dir)
        print 'cloning into %s ...' %i
        git_newrepo=git.Repo.clone_from(git_url, i, branch=git_branch)
        git.Git(git_dir).checkout(git_tag)
    
def deploy_openstack(install_dir):
    #Function - Call devstack's stack.sh script to deploy openstack
    os.chdir(install_dir)
    subprocess.call("./stack.sh")


if __name__ == "__main__":
    main()
