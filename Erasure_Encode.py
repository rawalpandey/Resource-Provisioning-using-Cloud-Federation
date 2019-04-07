
from pyeclib.ec_iface import ECDriver
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('k', type=int)
parser.add_argument('m', type=int)
parser.add_argument('ec_type')
parser.add_argument('file_dir')
parser.add_argument('filename')
parser.add_argument('fragment_dir')

args = parser.parse_args()

print("k = %d, m = %d" % (args.k, args.m))
print("ec_type = %s" % args.ec_type)
print("filename = %s" % args.filename)

ec_driver = ECDriver(k=args.k, m=args.m, ec_type=args.ec_type)

# read
with open(("%s/%s" % (args.file_dir, args.filename)), "rb") as fp:
    whole_file_str = fp.read()

# encode
fragments = ec_driver.encode(whole_file_str)

# store
i = 0
for fragment in fragments:
    with open("%s/%s.%d" % (args.fragment_dir, args.filename, i), "wb") as fp:
        fp.write(fragment)
    i += 1
