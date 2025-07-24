for f in crab_*; do
  echo "--------------------------------------------"
  echo "Crab resubmit: $f"
  crab resubmit $f --numcores=16 --maxjobruntime=2750 --sitewhitelist=T1_FR_CCIN2P3
  echo "--------------------------------------------"
done