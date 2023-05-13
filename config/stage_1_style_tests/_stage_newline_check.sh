set -ex

echo -e '\n'

echo "Check newline at the end of the file"

source venv/bin/activate
export PYTHONPATH=$(pwd):$PYTHONPATH

python config/stage_1_style_tests/newline_check.py
