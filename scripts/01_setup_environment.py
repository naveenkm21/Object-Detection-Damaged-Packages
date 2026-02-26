"""
Script 1: Check and verify setup
Run this first to ensure everything is configured correctly
"""

import os
import sys
import torch
import yaml
import cv2
import numpy as np
from pathlib import Path
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'setup_check_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def check_system():
    """Check system and Python environment"""
    logger.info("="*60)
    logger.info("SYSTEM CHECK")
    logger.info("="*60)
    
    # Python version
    logger.info(f"Python version: {sys.version}")
    
    # PyTorch
    logger.info(f"PyTorch version: {torch.__version__}")
    logger.info(f"CUDA available: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        logger.info(f"CUDA version: {torch.version.cuda}")
        logger.info(f"GPU: {torch.cuda.get_device_name(0)}")
        logger.info(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
    else:
        logger.warning("Running on CPU - training will be slow")
    
    # Check important packages
    packages = {
        'ultralytics': None,
        'cv2': cv2.__version__,
        'numpy': np.__version__,
        'yaml': yaml.__version__ if hasattr(yaml, '__version__') else 'installed'
    }
    
    for pkg, ver in packages.items():
        logger.info(f"{pkg}: {ver}")

def check_dataset():
    """Check dataset structure"""
    logger.info("\n" + "="*60)
    logger.info("DATASET CHECK")
    logger.info("="*60)
    
    dataset_path = Path("./dataset")
    if not dataset_path.exists():
        logger.error("Dataset folder not found! Please place your dataset in ./dataset")
        return False
    
    # Check data.yaml
    yaml_path = dataset_path / "data.yaml"
    if not yaml_path.exists():
        logger.error("data.yaml not found in dataset folder!")
        return False
    
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
    
    logger.info(f"Classes: {data.get('names', 'Not specified')}")
    logger.info(f"Number of classes: {data.get('nc', 'Not specified')}")
    
    # Check each split
    splits = ['train', 'valid', 'test']
    all_good = True
    
    for split in splits:
        split_path = dataset_path / split / 'images'
        if split_path.exists():
            images = list(split_path.glob('*.jpg')) + list(split_path.glob('*.png')) + \
                    list(split_path.glob('*.jpeg')) + list(split_path.glob('*.JPG'))
            logger.info(f"{split}: {len(images)} images")
            
            if len(images) == 0:
                logger.warning(f"No images found in {split} folder")
        else:
            if split == 'test':  # test is optional
                logger.info(f"{split}: Optional - not found")
            else:
                logger.error(f"{split} folder not found!")
                all_good = False
    
    return all_good

def check_directories():
    """Check if all required directories exist"""
    dirs = ['models', 'results', 'results/logs', 'results/plots', 'results/reports']
    
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
        logger.info(f"Directory checked: {d}")

if __name__ == "__main__":
    logger.info("Starting setup verification...")
    
    check_system()
    dataset_ok = check_dataset()
    check_directories()
    
    logger.info("\n" + "="*60)
    if dataset_ok:
        logger.info("✅ Setup verification complete! Ready to train.")
    else:
        logger.warning("⚠️ Dataset issues found. Please fix before training.")
    logger.info("="*60)