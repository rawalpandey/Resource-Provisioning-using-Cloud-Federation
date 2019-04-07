
from pyeclib.ec_iface import ECDriver
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('k', type=int)
parser.add_argument('m', type=int)
parser.add_argument('ec_type')
parser.add_argument('fragments', metavar='fragment', nargs='+')
parser.add_argument('filename')

args = parser.parse_args()

print("k = %d, m = %d" % (args.k, args.m))
print("ec_type = %s" % args.ec_type)
print("fragments = %s" % args.fragments)
print("filename = %s" % args.filename)

ec_driver = ECDriver(k=args.k, m=args.m, ec_type=args.ec_type)

fragment_list = []

# read fragments
for fragment in args.fragments:
    with open(("%s" % fragment), "rb") as fp:
        fragment_list.append(fp.read())
print fragment_list

# decode
decoded_file = ec_driver.decode(fragment_list)

# write
with open("%s.decoded" % args.filename, "wb") as fp:
    fp.write(decoded_file)
