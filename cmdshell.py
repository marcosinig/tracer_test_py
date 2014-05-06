#!/usr/local/bin/python2.7
# encoding: utf-8
'''
cmdshell -- shortdesc

cmdshell is a description

It defines classes_and_methods

@author:     user_name

@copyright:  2014 organization_name. All rights reserved.

@license:    license

@contact:    user_email
@deffield    updated: Updated
'''

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2014-05-02'
__updated__ = '2014-05-02'

DEBUG = 1 

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s


USAGE
''' #% (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        
        parser.add_argument("-o", "--output", dest="ouput", action="store_true", help="Specify output direcotry")
        #add or statement
        group = parser.add_mutually_exclusive_group(required=True)        
        group.add_argument("-c", "--COM", dest="com", action="store_true", help="specify com port")
        group.add_argument("-f", "--path_file", dest="path_file", help="specify file to parse" )
        
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        
        #parser.add_argument(dest="paths", help="paths to folder(s) with source file(s) [default: %(default)s]", metavar="path", nargs='+')

        # Process arguments
        args = parser.parse_args()
        ouput = args.ouput
        path_file = args.path_file
        verbose = args.verbose
        com = args.com
        #recurse = args.recurse
        #inpat = args.include
        #expat = args.exclude

        if verbose > 0:
            print "Verbose mode on:" 
            print "Output directory " + ouput
            print "Uart com " + com
            print "fila path " + path_file

            
        print "OKKKKKKKKKKKKKKKKKK"

        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        if DEBUG :
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
        sys.argv.append("-v")
        sys.argv.append("-r")

    sys.exit(main())