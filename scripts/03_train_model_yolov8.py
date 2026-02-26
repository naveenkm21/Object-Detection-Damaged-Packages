"""
Script 3: Train YOLOv8 Model (More Stable)
"""

import os
import torch
import yaml
from ultralytics import YOLO
from pathlib import Path
import logging
from datetime import datetime
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class YOLOv8Trainer:
    def __init__(self):
        self.base_dir = Path.cwd()
        self.models_dir = self.base_dir / 'models'
        self.results_dir = self.base_dir / 'results'
        self.checkpoint_file = self.models_dir / 'training_state.json'
        
        # Create directories
        self.models_dir.mkdir(exist_ok=True)
        self.results_dir.mkdir(exist_ok=True)
        
    def get_user_config(self):
        """Get configuration from user"""
        print("\n" + "="*60)
        print("YOLOv8 TRAINING CONFIGURATION")
        print("="*60)
        
        print("\nModel sizes:")
        print("1. Nano (n) - Fastest")
        print("2. Small (s) - Recommended for research")
        print("3. Medium (m) - Better accuracy")
        print("4. Large (l) - High accuracy")
        print("5. XLarge (x) - Maximum accuracy")
        
        size_choice = input("\nChoose model size (1-5) [default=2]: ").strip() or "2"
        size_map = {'1': 'n', '2': 's', '3': 'm', '4': 'l', '5': 'x'}
        model_size = size_map.get(size_choice, 's')
        
        epochs = input("Number of epochs [default=50]: ").strip() or "50"
        epochs = int(epochs)
        
        batch_size = input("Batch size [default=16] (reduce if OOM): ").strip() or "16"
        batch_size = int(batch_size)
        
        imgsz = input("Image size [default=640]: ").strip() or "640"
        imgsz = int(imgsz)
        
        resume = input("\nResume previous training? (y/n) [default=n]: ").strip().lower() == 'y'
        
        config = {
            'model_size': model_size,
            'epochs': epochs,
            'batch_size': batch_size,
            'imgsz': imgsz,
            'resume': resume,
            'experiment_name': f"yolov8{model_size}_{datetime.now().strftime('%Y%m%d_%H%M')}"
        }
        
        return config
    
    def train(self):
        """Main training function"""
        config = self.get_user_config()
        
        logger.info(f"Starting fresh training with YOLOv8-{config['model_size']}")
        
        # YOLOv8 will automatically download the weights if not present
        model = YOLO(f"yolov8{config['model_size']}.pt")
        
        # Training arguments
        train_args = {
            'data': 'dataset/data.yaml',
            'epochs': config['epochs'],
            'imgsz': config['imgsz'],
            'batch': config['batch_size'],
            'device': 0 if torch.cuda.is_available() else 'cpu',
            'workers': 4,
            'patience': 20,
            'save': True,
            'project': str(self.results_dir),
            'name': config['experiment_name'],
            'exist_ok': True,
            'pretrained': True,
            'optimizer': 'AdamW',
            'lr0': 0.001,
            'lrf': 0.01,
            'momentum': 0.937,
            'weight_decay': 0.0005,
            'warmup_epochs': 3,
            'warmup_momentum': 0.8,
            'box': 7.5,
            'cls': 0.5,
            'dfl': 1.5,
            'seed': 42,
            'verbose': True,
        }
        
        logger.info("\n" + "="*60)
        logger.info("STARTING TRAINING")
        logger.info("="*60)
        logger.info(f"Configuration: {json.dumps(config, indent=2)}")
        
        try:
            # Train
            results = model.train(**train_args)
            
            logger.info("\n✅ Training completed successfully!")
            logger.info(f"Best model saved at: {self.results_dir / config['experiment_name'] / 'weights' / 'best.pt'}")
            
            return model, results
            
        except KeyboardInterrupt:
            logger.info("\n⚠️ Training interrupted by user")
            
        except Exception as e:
            logger.error(f"Training failed: {e}")
            raise

if __name__ == "__main__":
    trainer = YOLOv8Trainer()
    trainer.train()