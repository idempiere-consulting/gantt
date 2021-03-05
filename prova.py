import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
""" parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator') """
""" parser.add_argument('sum', dest='accumulate', action='store_const',
                    const=sum, default='sdcsdc',
                    help='sum the integers (default: find the max)')
 """
parser.add_argument('config_file',nargs='?',help='filename of configuration',default='dcdc')
parser.add_argument('mapping_file',nargs='?',help='filename of mapping',default='123')
args = parser.parse_args()
print(args)