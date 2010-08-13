#!/usr/bin/python

# @desc     This script will sync a local directory with a remote directory
#           written specifically to work on OSX to keep a local music dir in sync
#           with a remote one as TimeMachine isn't enough
# @author   Mike Pearce <mike@mikepearce.net>
# @since    18/05/2010

# Grab some libraries
import sys, os, glob, commands
from optparse import OptionParser

# Setup some stuff
parser = OptionParser(description = "\This is just a wrapper for rsync.  \
Huzzah. Time machine on my Mac is great but it only backs stuff up. \
This does MORE MUCH MORE! \
\
So, the only thing to be wary of is that rsync (and syncR) will delete remote \
files if you tell it to. What this means is that, if you've deleted a local \
file and then run rsync, it will also delete the remote file as well (if you \
tell it to. syncR WILL NOT delete files by default. Add the -x switch if you \
want to delete remote files.",
version = "%prog 0.9a",
usage = 'Usage: %prog -s[SOURCE] -d[DEST] -e[EXCLUDES_FILE] -x[REMOTE_DELETE]')

# Local
parser.add_option(
    "-s",
    "--src",
    action  = "store",
    dest    = "source",
    help    = "The location to sync files FROM.",
    default = os.path.abspath("./")+"/"
)

# Remote
parser.add_option(
    "-d",
    "--dest",
    action  = "store",
    dest    = "destination",
    default = False,
    help    = "The location to sync files TO."
)

# Delete on sync?
parser.add_option(
    "-e",
    "--excludes-file",
    action  = "store",
    dest    = "excludes_file",
    default = './excludesFile.txt',
    help    = "Location of file containing list of excludes, each on a new line."
)

# Delete on sync?
parser.add_option(
    "-x",
    "--delete",
    action  = "store_true",
    dest    = "deleteDestFiles",
    default = False,
    help    = "Add this flag if you want to delete destination files."
)

# Noisy?
parser.add_option(
    "-v",
    "--verbose",
    action  = "store_true",
    dest    = "verbose",
    default = True
)

# Grab all the options and/or args
(options, args) = parser.parse_args()


#-------------------
def show_error(error="Undefined Error!"):
#-------------------
    """Writes an error to stderr"""
    sys.stderr.write(error)
    parser.print_usage()
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

    # Clear the screen for fun
    os.system('clear')

    # Check we have everything we need
    if False == options.destination:
        parser.error("You must enter a destination to sync with!")
    
    # Now check the source and destination exists
    if False == file_dir_exists(options.source):
        show_error("That source is not a valid path\n")
    
    # Ok, now we have a source, let's check a destination
    if False == file_dir_exists(options.destination):
        show_error("That destination is not a valid path\n")
    
    #Check and see if there is an exclude file
    # If so, set the exclude-from switch and print the excludes
    if True == file_dir_exists(options.excludes_file):
        excludes = "--exclude-from '%s'" % options.excludes_file
        f = open(options.excludes_file)
        sys.stdout.write("Excluding...\n%s\n" %(f.read(),))
        f.close()
    else:
        sys.stdout.write("No excludes file found...")
        
    # Do we want to delete remote stuff?
    if True == options.deleteDestFiles:
        do_exact = '--delete'
    else:
        do_exact = ''
    
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
