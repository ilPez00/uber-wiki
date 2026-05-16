#!/bin/bash

# Configuration
MODEL_DIR="/home/gio/ai/models"
MODEL_FILE="gemma-4-26B-A4B-it-ultra-uncensored-heretic-Q2_K.gguf"
DOWNLOAD_URL="https://huggingface.co/mradermacher/gemma-4-26B-A4B-it-ultra-uncensored-heretic-i1-GGUF/resolve/main/gemma-4-26B-A4B-it-ultra-uncensored-heretic.i1-Q2_K.gguf?download=true"
LOG_FILE="$MODEL_DIR/download.log"

mkdir -p "$MODEL_DIR"
cd "$MODEL_DIR" || exit 1

echo "--- $(date) ---" | tee -a "$LOG_FILE"
echo "Checking download status for $MODEL_FILE..." | tee -a "$LOG_FILE"

# Check if already running
if pgrep -x "wget" > /dev/null; then
    echo "wget is already running. Monitoring progress..."
else
    echo "Starting/Resuming download..."
    nohup wget -c "$DOWNLOAD_URL" -O "$MODEL_FILE" >> "$LOG_FILE" 2>&1 &
    echo "Download started in background (PID: $!)."
fi

# Show progress
sleep 2
tail -n 10 "$LOG_FILE"

# Integrity check (size based, can be expanded to sha256)
EXPECTED_SIZE_GB=10.5
ACTUAL_SIZE=$(ls -l "$MODEL_FILE" | awk '{print $5}')
ACTUAL_SIZE_GB=$(echo "scale=2; $ACTUAL_SIZE / 1024 / 1024 / 1024" | bc)

echo "Current size: $ACTUAL_SIZE_GB GB / ~$EXPECTED_SIZE_GB GB" | tee -a "$LOG_FILE"

if (( $(echo "$ACTUAL_SIZE_GB >= $EXPECTED_SIZE_GB" | bc -l) )); then
    echo "Download appears complete based on size." | tee -a "$LOG_FILE"
else
    echo "Download in progress. Check $LOG_FILE for details."
fi
