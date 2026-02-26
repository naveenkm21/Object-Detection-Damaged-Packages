"""
Script 4: Evaluate trained model
Run this after training to get comprehensive metrics
"""

from ultralytics import YOLO
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path
import logging
import json
from datetime import datetime
import torch

# Simple fix - just use weights_only=False
print("✅ Using simple weights_only=False approach")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ModelEvaluator:
    def __init__(self):
        self.results_dir = Path('results')
        self.models_dir = Path('models')
        self.reports_dir = Path('results/reports')
        self.reports_dir.mkdir(exist_ok=True)
        
    def find_latest_model(self):
        """Find the latest trained model"""
        experiment_dirs = list(self.results_dir.glob('yolov8*'))
        
        if not experiment_dirs:
            logger.error("No trained models found in results directory!")
            return None, None
        
        latest_exp = max(experiment_dirs, key=lambda x: x.stat().st_mtime)
        model_path = latest_exp / 'weights' / 'best.pt'
        
        if model_path.exists():
            logger.info(f"Found latest model: {model_path}")
            return model_path, latest_exp.name
        
        return None, None
    
    def load_model_safely(self, model_path):
        """Load YOLO model with PyTorch 2.6+ compatibility - SIMPLE FIX"""
        
        logger.info("Loading with weights_only=False...")
        
        # First load the checkpoint with weights_only=False
        checkpoint = torch.load(
            str(model_path), 
            map_location='cpu', 
            weights_only=False  # This bypasses the security check
        )
        logger.info("✅ Checkpoint loaded successfully")
        
        # Now load the model - it will work because checkpoint is in memory
        model = YOLO(str(model_path))
        logger.info("✅ Model loaded successfully")
        
        return model
    
    def evaluate(self, model_path=None):
        """Evaluate model and generate reports"""
        
        if model_path is None:
            model_path, exp_name = self.find_latest_model()
            if model_path is None:
                print("\n❌ No model found automatically.")
                manual_path = input("Enter model path manually: ").strip()
                if manual_path:
                    model_path = Path(manual_path)
                    exp_name = model_path.parent.parent.name
                else:
                    return
        else:
            model_path = Path(model_path)
            exp_name = model_path.parent.parent.name
        
        if not model_path or not model_path.exists():
            logger.error(f"Model not found: {model_path}")
            return
        
        logger.info(f"Loading model from: {model_path}")
        
        try:
            model = self.load_model_safely(model_path)
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return
        
        device = 0 if torch.cuda.is_available() else 'cpu'
        logger.info(f"Using device: {device}")
        
        logger.info("Running validation...")
        try:
            metrics = model.val(
                data='dataset/data.yaml',
                split='val',
                imgsz=640,
                batch=16,
                conf=0.25,
                iou=0.6,
                device=device
            )
        except Exception as e:
            logger.error(f"Validation failed: {e}")
            return
        
        # Collect metrics
        eval_results = {
            'experiment': exp_name,
            'timestamp': datetime.now().isoformat(),
            'model_path': str(model_path),
            'mAP50': float(metrics.box.map50),
            'mAP50-95': float(metrics.box.map),
            'precision': float(metrics.box.mp),
            'recall': float(metrics.box.mr),
            'f1_score': float(2 * (metrics.box.mp * metrics.box.mr) / 
                              (metrics.box.mp + metrics.box.mr + 1e-10)),
            'per_class': {}
        }
        
        # Per-class metrics
        for i, class_name in enumerate(model.names.values()):
            eval_results['per_class'][class_name] = {
                'precision': float(metrics.box.ap_class[i]) if i < len(metrics.box.ap_class) else 0,
                'recall': float(metrics.box.ap_class[i]) if i < len(metrics.box.ap_class) else 0
            }
        
        # Save results
        report_file = self.reports_dir / f'evaluation_{exp_name}_{datetime.now().strftime("%Y%m%d_%H%M")}.json'
        with open(report_file, 'w') as f:
            json.dump(eval_results, f, indent=2)
        
        # Print summary
        print("\n" + "="*70)
        print("📊 EVALUATION RESULTS")
        print("="*70)
        print(f"\n📁 Model: {exp_name}")
        print(f"📁 Location: {model_path}")
        print(f"\n🎯 Overall Metrics:")
        print(f"   • mAP50: {eval_results['mAP50']:.4f} ({eval_results['mAP50']*100:.1f}%)")
        print(f"   • mAP50-95: {eval_results['mAP50-95']:.4f} ({eval_results['mAP50-95']*100:.1f}%)")
        print(f"   • Precision: {eval_results['precision']:.4f} ({eval_results['precision']*100:.1f}%)")
        print(f"   • Recall: {eval_results['recall']:.4f} ({eval_results['recall']*100:.1f}%)")
        print(f"   • F1-Score: {eval_results['f1_score']:.4f}")
        
        print(f"\n📊 Per-Class Performance:")
        print("-" * 60)
        print(f"{'Class':<15} {'Precision':<12} {'Recall':<12} {'F1-Score':<12}")
        print("-" * 60)
        
        for class_name, metrics in eval_results['per_class'].items():
            f1 = 2 * (metrics['precision'] * metrics['recall']) / (metrics['precision'] + metrics['recall'] + 1e-10)
            print(f"{class_name:<15} {metrics['precision']:.4f}     {metrics['recall']:.4f}     {f1:.4f}")
        
        print("-" * 60)
        print(f"\n✅ Report saved to: {report_file}")
        
        return eval_results
    
    def compare_experiments(self):
        """Compare multiple experiments"""
        report_files = list(self.reports_dir.glob('evaluation_*.json'))
        
        if len(report_files) == 0:
            logger.info("No evaluation reports found")
            return
        
        comparisons = []
        for report_file in report_files:
            with open(report_file, 'r') as f:
                comparisons.append(json.load(f))
        
        # Create comparison dataframe
        df = pd.DataFrame([{
            'Experiment': c['experiment'],
            'mAP50': c['mAP50'],
            'mAP50-95': c['mAP50-95'],
            'Precision': c['precision'],
            'Recall': c['recall'],
            'F1-Score': c['f1_score']
        } for c in comparisons])
        
        # Sort by mAP50
        df = df.sort_values('mAP50', ascending=False)
        
        print("\n" + "="*70)
        print("📊 EXPERIMENT COMPARISON")
        print("="*70)
        print(df.to_string(index=False))
        
        # Save comparison
        comparison_file = self.reports_dir / 'experiment_comparison.csv'
        df.to_csv(comparison_file, index=False)
        print(f"\n✅ Comparison saved to: {comparison_file}")
        
        return df

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🔍 YOLOv8 MODEL EVALUATION")
    print("="*70)
    
    print(f"\n📦 PyTorch version: {torch.__version__}")
    
    evaluator = ModelEvaluator()
    
    print("\nOptions:")
    print("1. Evaluate latest model")
    print("2. Compare all experiments")
    print("3. Specify model path")
    
    choice = input("\nChoose (1-3) [default=1]: ").strip() or "1"
    
    if choice == "1":
        evaluator.evaluate()
    elif choice == "2":
        evaluator.compare_experiments()
    elif choice == "3":
        path = input("Enter model path: ").strip()
        evaluator.evaluate(path)