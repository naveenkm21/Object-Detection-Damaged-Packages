"""
Script: Train YOLOv8 Optimized for Better Accuracy
This uses YOLOv8 which actually works with your setup
"""

import os
import torch
from ultralytics import YOLO
from pathlib import Path
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class YOLOv8OptimizedTrainer:
    def __init__(self):
        self.results_dir = Path('results')
        self.results_dir.mkdir(exist_ok=True)
        
    def get_user_config(self):
        """Get configuration from user"""
        print("\n" + "="*60)
        print("🚀 YOLOv8 OPTIMIZED TRAINING FOR BETTER ACCURACY")
        print("="*60)
        
        print("\nModel sizes (bigger = better accuracy but slower):")
        print("1. Nano (n) - Fastest, lowest accuracy")
        print("2. Small (s) - Good balance (your previous model)")
        print("3. Medium (m) - Better accuracy (RECOMMENDED)")
        print("4. Large (l) - High accuracy (needs more GPU)")
        print("5. XLarge (x) - Maximum accuracy (slowest)")
        
        size_choice = input("\nChoose model size (1-5) [default=3]: ").strip() or "3"
        size_map = {'1': 'n', '2': 's', '3': 'm', '4': 'l', '5': 'x'}
        model_size = size_map.get(size_choice, 'm')
        
        print("\n📊 Training strategies:")
        print("1. Quick (100 epochs) - 5-6 hours")
        print("2. Balanced (150 epochs) - 8-9 hours (RECOMMENDED)")
        print("3. Maximum (200 epochs) - 10-12 hours")
        
        strategy = input("\nChoose strategy (1-3) [default=2]: ").strip() or "2"
        
        if strategy == "1":
            epochs = 100
            lr = 0.001
        elif strategy == "2":
            epochs = 150
            lr = 0.0005
        else:
            epochs = 200
            lr = 0.0003
            
        batch_size = input(f"Batch size [default=12 for {model_size} model]: ").strip()
        if not batch_size:
            batch_size = 16 if model_size in ['n', 's'] else (12 if model_size == 'm' else 8)
        else:
            batch_size = int(batch_size)
            
        imgsz = input("Image size [default=640]: ").strip() or "640"
        imgsz = int(imgsz)
        
        config = {
            'model_size': model_size,
            'epochs': epochs,
            'batch_size': batch_size,
            'imgsz': imgsz,
            'lr': lr,
            'experiment_name': f"yolov8{model_size}_optimized_{datetime.now().strftime('%Y%m%d_%H%M')}"
        }
        
        return config
    
    def train(self):
        """Main training function"""
        config = self.get_user_config()
        
        print(f"\n📋 Training Configuration:")
        print(f"   Model: YOLOv8-{config['model_size']}")
        print(f"   Epochs: {config['epochs']}")
        print(f"   Batch Size: {config['batch_size']}")
        print(f"   Image Size: {config['imgsz']}")
        print(f"   Learning Rate: {config['lr']}")
        print(f"   Experiment: {config['experiment_name']}")
        
        confirm = input("\nStart training? (y/n): ").lower()
        if confirm != 'y':
            print("Training cancelled")
            return
        
        # Load model - YOLOv8 weights exist!
        logger.info(f"Loading YOLOv8-{config['model_size']}...")
        model = YOLO(f"yolov8{config['model_size']}.pt")
        
        # Optimized training arguments
        train_args = {
            'data': 'dataset/data.yaml',
            'epochs': config['epochs'],
            'imgsz': config['imgsz'],
            'batch': config['batch_size'],
            'device': 0 if torch.cuda.is_available() else 'cpu',
            'workers': 4,
            'patience': 30,
            'save': True,
            'project': str(self.results_dir),
            'name': config['experiment_name'],
            'exist_ok': True,
            'pretrained': True,
            'optimizer': 'AdamW',
            'lr0': config['lr'],
            'lrf': 0.001,
            'momentum': 0.937,
            'weight_decay': 0.0005,
            'warmup_epochs': 5,
            'warmup_momentum': 0.8,
            'warmup_bias_lr': 0.1,
            'box': 7.5,
            'cls': 0.5,
            'dfl': 1.5,
            # Enhanced augmentations for better accuracy
            'hsv_h': 0.02,
            'hsv_s': 0.8,
            'hsv_v': 0.5,
            'degrees': 15.0,
            'translate': 0.2,
            'scale': 0.7,
            'shear': 3.0,
            'perspective': 0.001,
            'flipud': 0.5,
            'fliplr': 0.5,
            'mosaic': 1.0,
            'mixup': 0.3,
            'copy_paste': 0.3,
            'seed': 42,
            'verbose': True,
        }
        
        logger.info("\n" + "="*60)
        logger.info("STARTING OPTIMIZED TRAINING")
        logger.info("="*60)
        
        try:
            # Train
            results = model.train(**train_args)
            
            logger.info("\n✅ Training completed successfully!")
            logger.info(f"Best model saved at: {self.results_dir / config['experiment_name'] / 'weights' / 'best.pt'}")
            
            # Show final metrics
            print("\n" + "="*60)
            print("📊 FINAL METRICS")
            print("="*60)
            print("\nRun this to evaluate:")
            print(f"python scripts/04_evaluate_model.py")
            print("\nOr specify the model path:")
            print(f"results/{config['experiment_name']}/weights/best.pt")
            
            return model, results
            
        except KeyboardInterrupt:
            logger.info("\n⚠️ Training interrupted by user")
            print("\nYou can resume later by running the script again with 'resume' option.")
            
        except Exception as e:
            logger.error(f"Training failed: {e}")
            raise

if __name__ == "__main__":
    trainer = YOLOv8OptimizedTrainer()
    trainer.train()