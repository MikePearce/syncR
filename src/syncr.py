import os.path
#!/usr/bin/python

# @desc     This script will sync a local directory with a remote directory
#           written specifically to work on OSX to keep a local music dir in sync
#           with a remote one as TimeMachine isn't enough
# @author   Mike Pearce <mike@mikepearce.net>
# @since    18/05/2010

# Grab some libraries
import sys, os, glob, subprocess

# Setup some stuff
excludes        = ''
excludes_file   = './excludesFile.txt'
do_exact        = ''

#-------------------
def show_usage():
#-------------------
    """Print the program usage to the screen"""
    
    sys.stdout.write("\nUsage: syncR [source] [destination] [deleteDestFiles] ")

#-------------------
def show_error(error="Undefined Error!"):
#-------------------
    """Writes an error to stderr"""
    sys.stderr.write(error)
    show_usage()
    sys.exit(1)

#-------------------
def file_dir_exists(file_or_dir):
#-------------------
    """Checks to see if the file, or dir eists"""
    if True == os.path.isdir(file_or_dir):
        return True

    if True == os.path.isfile(file_or_dir):
        return True

    return False

#-------------------
# Now, onto the main event!
#-------------------
if __name__ == "__main__":
    os.system('clear')
    
    # Check to make sure we have all the required arguments
    try:
        (scriptName, source, destination, exact) = sys.argv
    except ValueError:
            show_usage()
            sys.exit(1)

    # Now check the source and destination exists
    if False == file_dir_exists(source):
        show_error("That source is not a valid path\n")
    
    # Ok, now we have a source, let's check a destination
    if False == file_dir_exists(destination):
        show_error("That destination is not a valid path\n")
    
    #Check and see if there is an exclude file
    # If so, set the exclude-from switch and print the excludes
    if True == file_dir_exists(excludes_file):
        excludes = "--exclude-from '%s'" % excludes_file
        f = open(excludes_file)
        sys.stdout.write("Excluding...\n%s\n" %(f.read(),))
        f.close()
        
    # Do we want to delete remote stuff?
    if 1 == exact:
        do_exact = '--delete'
    
    #Build teh command
    command = "rsync -aE %s %s '%s' '%s'" % (do_exact, excludes, source, destination)
    
    # Now do the rysnc
    try:
        sys.stdout.write("Beginning Rsync\n")
        os.system(command)
    except OsError:
        show_error("There was an error performing the rsync")

    sys.stdout.write("Rsync Complete!\n")
    sys.exit(0)
