for f in crab_*; do
  echo "--------------------------------------------"
  echo "Kill -> $f"
  crab kill $f
  rm -rf $f
done