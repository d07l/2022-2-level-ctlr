set -x

source venv/bin/activate

export PYTHONPATH=$(pwd):$PYTHONPATH
python config/skip_check.py --pr_name "$1" --pr_author "$2" --lab_path "lab_5_scrapper"
if [ $? -eq 0 ]; then
  echo 'skip check due to special conditions...' && exit 0
fi

python config/config_param_changer.py --config_path="lab_5_scrapper/scrapper_config.json"

echo "Changed config params"

python lab_5_scrapper/scrapper.py

if [[ $? -ne 0 ]]; then
  echo "Check failed for common files."
  exit 1
else
  echo "Check passed for common files."
fi

echo "Collected dataset"

ls -la tmp/articles
