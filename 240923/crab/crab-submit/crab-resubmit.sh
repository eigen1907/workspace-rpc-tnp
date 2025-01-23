for f in crab_*; do
  echo "--------------------------------------------"
  echo "Resubmit -> $f"
  crab resubmit $f --numcores=8 --maxjobruntime=2750
done