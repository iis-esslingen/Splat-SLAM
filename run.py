# Copyright 2024 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
import torch
import argparse
import os

from thirdparty.glorie_slam import config
from src.slam import SLAM
from src.utils.datasets import get_dataset
from time import gmtime, strftime
from colorama import Fore,Style

import random
def setup_seed(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)
    torch.backends.cudnn.deterministic = True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('config', type=str, help='Path to config file.')
    parser.add_argument('--input_dir', type=str, help='Path to input directory.')
    parser.add_argument('--output_dir', type=str, help='Path to output directory.')
    parser.add_argument("--only_tracking", action="store_true", help="Only tracking is triggered")
    args = parser.parse_args()

    torch.multiprocessing.set_start_method('spawn')

    cfg = config.load_config(
        args.config, './configs/splat_slam.yaml'
    )
    setup_seed(cfg['setup_seed'])

    if args.only_tracking:
        cfg['only_tracking'] = True
        cfg['mono_prior']['predict_online'] = True

    if args.output_dir:
        cfg['data']['output'] = args.output_dir
    if args.input_dir:
        cfg['data']['input_folder'] = args.input_dir

    start_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    start_info = "-"*30+Fore.LIGHTRED_EX+\
                 f"\nStart Splat-SLAM at {start_time},\n"+Style.RESET_ALL+ \
                 f"   scene: {cfg['dataset']}-{cfg['scene']},\n" \
                 f"   only_tracking: {cfg['only_tracking']},\n" \
                 f"   output: {cfg['data']['output']}\n"+ \
                 "-"*30
    print(start_info)
    
    if not os.path.exists(cfg['data']['output']):
        os.makedirs(cfg['data']['output'])

    config.save_config(cfg, f"{cfg['data']['output']}/cfg.yaml")

    dataset = get_dataset(cfg)

    slam = SLAM(cfg,dataset)
    slam.run()

    end_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print("-"*30+Fore.LIGHTRED_EX+f"\nSplat-SLAM finishes!\n"+Style.RESET_ALL+f"{end_time}\n"+"-"*30)

