#!/usr/bin/env python3
import sys, os
import argparse
from pathlib import Path

sys.path.append("/users/hep/eigen1907/Workspace/Workspace-RPC/modules")
from NanoAODTnP.Analysis.NanoAOD import flatten_nanoaod

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-i', '--input-path', required=True, type=Path,
                        help='input NanoAOD file')
    parser.add_argument('-c', '--cert-path', required=True, type=Path,
                        help='Golden JSON file')
    parser.add_argument('-g', '--geom-path', required=True, type=Path,
                        help='csv file containing RPC roll information')
    parser.add_argument('-r', '--run-path', required=True, type=Path,
                        help='csv file contaning existing run list')
    parser.add_argument('-o', '--output-path', default='output.root',
                        type=Path, help='output file name')
    parser.add_argument('-n', '--name', default='rpcTnP', type=str,
                        help='branch prefix')
    parser.add_argument('--roll-blacklist-path', type=str,
                        help='blacklist roll file')
    parser.add_argument('--run-blacklist-path', type=str,
                        help='blacklist run file')
    parser.add_argument('--exclude-RE4', type=bool,
                        help='True: Exclude RE4, False(default): include RE4')
    args = parser.parse_args()

    flatten_nanoaod(
        input_path=args.input_path,
        cert_path=args.cert_path,
        geom_path=args.geom_path,
        run_path=args.run_path,
        output_path=args.output_path,
        name=args.name,
        roll_blacklist_path=args.roll_blacklist_path,
        run_blacklist_path=args.run_blacklist_path,
        exclude_RE4=args.exclude_RE4,
    )


if __name__ == "__main__":
    main()