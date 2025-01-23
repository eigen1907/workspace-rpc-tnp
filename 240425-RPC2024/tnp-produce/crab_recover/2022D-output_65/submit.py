import htcondor  # for submitting jobs, querying HTCondor daemons, etc.
import classad   # for interacting with ClassAds, HTCondor's internal data format
from pathlib import Path

cwd = Path.cwd()

proxy_path = '/u/user/sjws5411/tmp/x509up'
execute_path = cwd / "execute.sh"
lfns_path = cwd / "filelist.txt"
pfn = "root://cms-xrd-global.cern.ch/"

with open(lfns_path) as lfns_file:
    input_files = [pfn + lfn.strip() for lfn in lfns_file]

output_path = cwd / "condor" / "output"
if not output_path.exists():
    output_path.mkdir()

itemdata = [{
    "execute": str(execute_path),
    "cwd": str(cwd),
    "proxy": proxy_path,
    "inputFiles": input_files[idx],
    "outputFile": str(output_path / f"output_{idx}.root")
} for idx in range(len(input_files))]

cmsRun_job = htcondor.Submit({
    "executable": "/bin/bash",
    "arguments": "$(execute) $(cwd) $(proxy) $(inputFiles) $(outputFile)",
    "output": "condor/log/cmsRun-$(ProcId).out",
    "error": "condor/log/cmsRun-$(ProcId).err",
    "log": "condor/log/cmsRun.log",
    "should_transfer_files": "yes",
})

schedd = htcondor.Schedd()
submit_result = schedd.submit(cmsRun_job, itemdata = iter(itemdata))

print(submit_result.cluster())

