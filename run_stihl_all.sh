#!/bin/bash

dates=("2023-09-15" "2024-01-13" "2024-04-11" "2024-05-29_1" "2024-05-29_2" "2024-05-29_3" "2024-05-29_4")

for date in "${dates[@]}"; do
    echo "Processing date: $date"

    trials=("0")

    for trial in "${trials[@]}"; do
        echo "  Trial: $trial"
        python run.py configs/Stihl/d435i.yaml --input_dir /media/mobile-robots/data_recording_r/2024-04-11/tum/d435i --output_dir output/short_only_tracking/$date/$trial --only_tracking
    done
done

echo "All dates processed."