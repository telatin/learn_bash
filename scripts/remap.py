#!/usr/bin/env python3

"""
Extract the reads from a BAM file and map them against a new reference
Requires:
    - Python3
    - samtools
    - minimap2
"""

import argparse
import tempfile
import os, sys, re
import subprocess

def checkversion(cmd, grep_kw="."):
    """
    Check if a command is available and return its version
    """
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        print("ERROR: {} not found".format(cmd[0]), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print("ERROR: {} not found.\n{}".format(cmd[0], e), file=sys.stderr)
        sys.exit(1)

    try:
        version = re.search(grep_kw, output.decode("utf-8")).group(0)
        return version
    except Exception as e:
        print("ERROR: Version unparsable: {}".format(e), file=sys.stderr)
        sys.exit(1)

def execute(cmd):
    """
    Execute a command passed as a list of arguments.
    """
    command_str = " ".join(cmd)
    try:
        print("% {}".format(command_str), file=sys.stderr)
        retcode = subprocess.call(cmd)
        if retcode == 0:
            print("\tDone ✅", file=sys.stderr)
        elif retcode < 0:
            print("\tChild was terminated by signal", -retcode, file=sys.stderr)
        else:
            print("\tChild returned", retcode, file=sys.stderr)
    except OSError as e:
        print("ERROR: Execution failed:", e, file=sys.stderr)
        sys.exit(1)
    print("----------------------------------------", file=sys.stderr)

if __name__ == "__main__":
    args = argparse.ArgumentParser("Extract reads to a single file")
    args.add_argument("bam", help="Input BAM file")
    args.add_argument("-o", "--output", help="Output BAM file", required=True)
    args.add_argument("-r", "--reference", help="New reference FASTA file", required=True)
    args.add_argument("-n", "--seqname", help="Extract only reads from this target")
    args.add_argument("-s", "--singletons", help="Map singletons", action="store_true")
    args.add_argument("-t", "--threads", help="Number of threads", type=int, default=1)
    args.add_argument("--keep", help="Keep temporary files", action="store_true")
    args = args.parse_args()

    # Check dependencies
    samtools_version = checkversion(["samtools", "--version"], r"\d+\.\d+\.\d+")
    minimap2_version = checkversion(["minimap2", "--version"], r".+")

    print("samtools version: {}".format(samtools_version), file=sys.stderr)
    print("minimap2 version: {}".format(minimap2_version), file=sys.stderr)

    # Prepare paths
    tmpdir = tempfile.mkdtemp(prefix="remaptmp_", dir=os.getcwd())
    print("Temp dir: %s" % tmpdir, file=sys.stderr)
    forfile = os.path.join(tmpdir, "read_R1.fq")
    revfile = os.path.join(tmpdir, "read_R2.fq")
    tmpfile = os.path.join(tmpdir, "tmp.fq")
    sngfile = os.path.join(tmpdir, "sing.fq")
    bamfile = os.path.join(tmpdir, "original.bam")
    

    # Extract the reference sequences matching the target
    # or simply copy the bam to the temp dir for easier access
    if args.seqname is not None:
        get_bam_cmd = ["samtools", "view", "-o", bamfile, args.bam, args.seqname]
    else:
        get_bam_cmd = ["cp", args.bam, bamfile]
    
    execute(get_bam_cmd)

    # Get reads from the original BAM using samtools
    if not args.singletons:
        get_fastq_cmd = ["samtools", "fastq", "-1", forfile, "-2", revfile, "--threads", str(args.threads), bamfile]
        execute(get_fastq_cmd)
    else:
        get_fastq_cmd = ["samtools", "fastq", "-o", forfile, "--threads", str(args.threads), bamfile]
        execute(get_fastq_cmd)
      

    # Map them
    
    if not args.singletons:
        align_cmd    = ["minimap2", "-x", "sr", "-a" ,"-t", str(args.threads), args.reference, forfile, revfile]
    else:
        align_cmd    = ["minimap2", "-x", "sr", "-a" ,"-t", str(args.threads), args.reference, forfile]
    samtools_cmd = ["samtools", "view", "-bS"]
    sort_cmd     = ["samtools", "sort", "-o", args.output, "-"]

    # Compose the pipe using subprocess
    print("% {}".format(align_cmd), file=sys.stderr)
    p1 = subprocess.Popen(align_cmd, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(samtools_cmd, stdin=p1.stdout, stdout=subprocess.PIPE)
    p3 = subprocess.Popen(sort_cmd, stdin=p2.stdout, stdout=None)

    # Wait until the pipes have completed
    output, err = p3.communicate()


    # Remove temporary dir and its contents
    if not args.keep:
        import shutil
        shutil.rmtree(tmpdir)


    
