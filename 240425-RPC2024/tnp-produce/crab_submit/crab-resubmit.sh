for f in crab_muRPCTnPFlatTableProducer_cfg*; do
  echo "--------------------------------------------"
  echo "Resubmit -> $f"
  crab resubmit $f --siteblacklist=T2_DE_DESY
done