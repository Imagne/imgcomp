import argparse
import os

from comparator import *
from imgcomparing import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("ref", help="Reference image image")
    parser.add_argument("tar", help="Target image image")
    parser.add_argument("--diff", help="Compare images with raw difference", action="store_true")
    parser.add_argument("--patch", help="Compare images with patch difference", action="store_true")
    parser.add_argument("--bgs", help="Compare images with background subtraction", action="store_true")
    parser.add_argument("--flow", help="Compare images with optical flow", action="store_true")
    parser.add_argument("--dl", help="Use deep learning technique for image matching", action="store_true")
    args = parser.parse_args()
    
    ref_name = os.path.splitext(args.ref)[0]
    tar_name = os.path.splitext(args.tar)[0]
    dest = f'{ref_name}_{tar_name}.jpg'
    
    if args.dl:
        dest = f'{ref_name}_{tar_name}_dl.jpg'
        with open('images/pairs.txt','w') as f:
            f.write(f'{args.ref} {args.tar}')

    match_method = ImageMatcherSG() if args.dl \
        else ImageMatcher()

    cmp_method = BGSubCMP() if args.bgs \
        else OptFlowCMP() if args.flow \
        else RawDiffCMP() if args.diff \
        else PatchDiffCMP()

    comparator = Comparator(match_method, cmp_method)
    comparator.compare(os.path.join('images/',args.ref),\
                       os.path.join('images/',args.tar),\
                       os.path.join('comparisons/',dest))
