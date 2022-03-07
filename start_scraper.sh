until python3 main.py; do
    echo "The script crashed with exit code $?.  Restarting.." >&2
    sleep 1
done