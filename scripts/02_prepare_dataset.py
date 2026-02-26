"""
Script 2: Prepare and verify dataset
Run this to ensure your dataset is properly formatted
"""

import os
import yaml
import shutil
from pathlib import Path
import random
from tqdm import tqdm
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DatasetPreparator:
    def __init__(self, dataset_path="./dataset"):
        self.dataset_path = Path(dataset_path)
        self.yaml_path = self.dataset_path / "data.yaml"
        
    def verify_structure(self):
        """Verify and fix dataset structure"""
        logger.info("Verifying dataset structure...")
        
        # Check if images and labels are in correct folders
        for split in ['train', 'valid']:
            split_path = self.dataset_path / split
            
            # Check if images are directly in split folder
            images_direct = [f for f in split_path.glob('*') if f.suffix.lower() in ['.jpg', '.jpeg', '.png']]
            
            if images_direct and not (split_path / 'images').exists():
                logger.info(f"Moving {len(images_direct)} images to {split}/images/")
                (split_path / 'images').mkdir(exist_ok=True)
                for img in images_direct:
                    shutil.move(str(img), str(split_path / 'images' / img.name))
            
            # Check for labels
            labels_path = split_path / 'labels'
            if not labels_path.exists():
                logger.warning(f"Labels folder not found in {split}. Creating empty folder.")
                labels_path.mkdir(exist_ok=True)
        
        logger.info("Dataset structure verified!")
    
    def check_class_distribution(self):
        """Check distribution of classes"""
        logger.info("\nChecking class distribution...")
        
        with open(self.yaml_path, 'r') as f:
            data = yaml.safe_load(f)
        class_names = data['names']
        
        class_counts = {i: 0 for i in range(len(class_names))}
        
        for split in ['train', 'valid']:
            labels_path = self.dataset_path / split / 'labels'
            if labels_path.exists():
                label_files = list(labels_path.glob('*.txt'))
                for lbl_file in tqdm(label_files, desc=f"Processing {split}"):
                    with open(lbl_file, 'r') as f:
                        for line in f:
                            if line.strip():
                                class_id = int(line.strip().split()[0])
                                if class_id in class_counts:
                                    class_counts[class_id] += 1
        
        logger.info("\nClass distribution:")
        for class_id, count in class_counts.items():
            logger.info(f"  {class_names[class_id]}: {count} instances")
        
        return class_counts
    
    def create_dataset_summary(self):
        """Create a summary of the dataset"""
        summary = {
            'total_images': 0,
            'total_labels': 0,
            'splits': {}
        }
        
        for split in ['train', 'valid', 'test']:
            split_path = self.dataset_path / split / 'images'
            if split_path.exists():
                images = list(split_path.glob('*'))
                summary['splits'][split] = {
                    'images': len(images),
                    'image_paths': [str(img) for img in images[:5]]  # First 5 as sample
                }
                summary['total_images'] += len(images)
        
        # Save summary
        import json
        with open('results/dataset_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"\nDataset Summary saved to results/dataset_summary.json")
        return summary

if __name__ == "__main__":
    preparator = DatasetPreparator()
    preparator.verify_structure()
    class_counts = preparator.check_class_distribution()
    summary = preparator.create_dataset_summary()
    
    logger.info("\n✅ Dataset preparation complete!")