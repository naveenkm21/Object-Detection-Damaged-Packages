"""
Optimized YOLOv8 Training for Better Accuracy - FIXED VERSION
"""

from ultralytics import YOLO
import torch
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_model_safely(model_name):
    """Load YOLO model with PyTorch 2.6+ compatibility"""
    try:
        # Try direct loading first
        return YOLO(model_name)
    except Exception as e:
        print(f"Direct loading failed: {e}")
        print("Attempting alternative loading method...")
        
        # If fails, load with weights_only=False
        import torch
        import os
        
        # Download the model file if it doesn't exist
        if not os.path.exists(model_name):
            from ultralytics.utils.downloads import download
            url = f"https://github.com/ultralytics/assets/releases/download/v8.1.0/{model_name}"
            download(url, model_name)
        
        # Load with weights_only=False
        checkpoint = torch.load(model_name, map_location='cpu', weights_only=False)
        
        # Now try loading again
        return YOLO(model_name)

# Configuration for BETTER ACCURACY
config = {
    'model_size': 'm',        # Medium model (better than small)
    'epochs': 150,             # More epochs
    'batch_size': 12,          # Slightly reduced for stability
    'imgsz': 640,              # Keep same
    'optimizer': 'AdamW',      # Best optimizer
    'lr0': 0.0005,             # Lower learning rate for fine-tuning
    'lrf': 0.001,              # Final learning rate factor
    'momentum': 0.937,         
    'weight_decay': 0.0005,    
    'warmup_epochs': 5,        # More warmup
    'box': 7.5,                
    'cls': 0.5,                
    'dfl': 1.5,                
    'hsv_h': 0.015,            # Augmentation - hue
    'hsv_s': 0.7,              # Augmentation - saturation
    'hsv_v': 0.4,              # Augmentation - value
    'degrees': 10.0,           # Rotation augmentation
    'translate': 0.1,          # Translation augmentation
    'scale': 0.5,              # Scaling augmentation
    'shear': 2.0,              # Shear augmentation
    'perspective': 0.0005,     # Perspective augmentation
    'flipud': 0.5,             # Vertical flip
    'fliplr': 0.5,             # Horizontal flip
    'mosaic': 1.0,             # Mosaic augmentation
    'mixup': 0.2,              # Mixup augmentation
    'copy_paste': 0.2,         # Copy-paste augmentation
}

print("="*60)
print("🚀 OPTIMIZED TRAINING FOR BETTER ACCURACY")
print("="*60)
print(f"\n📋 Configuration:")
print(f"   Model: YOLOv8-{config['model_size']}")
print(f"   Epochs: {config['epochs']}")
print(f"   Batch Size: {config['batch_size']}")
print(f"   Image Size: {config['imgsz']}")
print(f"   Optimizer: {config['optimizer']}")
print(f"   Initial LR: {config['lr0']}")

confirm = input("\nStart optimized training? (y/n): ").lower()
if confirm != 'y':
    print("Training cancelled")
    exit()

# Load model safely
model_name = f"yolov8{config['model_size']}.pt"
print(f"\n📦 Loading model: {model_name}")
model = load_model_safely(model_name)
print("✅ Model loaded successfully!")

# Create experiment name
exp_name = f"yolov8{config['model_size']}_optimized_{datetime.now().strftime('%Y%m%d_%H%M')}"

# Train with optimized parameters
results = model.train(
    data='dataset/data.yaml',
    epochs=config['epochs'],
    imgsz=config['imgsz'],
    batch=config['batch_size'],
    device=0 if torch.cuda.is_available() else 'cpu',
    workers=4,
    patience=30,              # More patience
    save=True,
    project='results',
    name=exp_name,
    exist_ok=True,
    pretrained=True,
    optimizer=config['optimizer'],
    lr0=config['lr0'],
    lrf=config['lrf'],
    momentum=config['momentum'],
    weight_decay=config['weight_decay'],
    warmup_epochs=config['warmup_epochs'],
    warmup_momentum=0.8,
    warmup_bias_lr=0.1,
    box=config['box'],
    cls=config['cls'],
    dfl=config['dfl'],
    # Augmentations
    hsv_h=config['hsv_h'],
    hsv_s=config['hsv_s'],
    hsv_v=config['hsv_v'],
    degrees=config['degrees'],
    translate=config['translate'],
    scale=config['scale'],
    shear=config['shear'],
    perspective=config['perspective'],
    flipud=config['flipud'],
    fliplr=config['fliplr'],
    mosaic=config['mosaic'],
    mixup=config['mixup'],
    copy_paste=config['copy_paste'],
    seed=42,
    verbose=True,
)

print("\n✅ Optimized training complete!")
print(f"📁 Results saved in: results/{exp_name}")