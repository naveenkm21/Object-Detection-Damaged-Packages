"""
Script 6: Generate comprehensive research metrics and visualizations
"""

from ultralytics import YOLO
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from pathlib import Path
import json
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ResearchAnalyzer:
    def __init__(self):
        self.research_dir = Path('research_output')
        self.research_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.model_family = 'yolov8m'
        self.model_label = 'YOLOv8m'
        # Keep validation lightweight on Windows to avoid multiprocessing paging-file crashes.
        self.val_base_kwargs = {
            'data': 'dataset/data.yaml',
            'iou': 0.6,
            'workers': 0,
            'verbose': False,
            'plots': False
        }
        
    def load_model(self, model_path=None):
        """Load the best YOLOv8m model by default."""
        if model_path is None:
            # Prefer trained YOLOv8m runs in results/, then fallback to root yolov8m.pt.
            model_files = list(Path('results').glob(f'{self.model_family}*/weights/best.pt'))
            if model_files:
                model_path = max(model_files, key=lambda x: x.stat().st_mtime)
            elif Path(f'{self.model_family}.pt').exists():
                model_path = Path(f'{self.model_family}.pt')
            else:
                logger.error("No YOLOv8m model found in results/*/weights/best.pt or yolov8m.pt")
                return None
        
        logger.info(f"Loading model: {model_path}")
        return YOLO(str(model_path))
    
    def threshold_analysis(self, model):
        """Analyze model performance at different confidence thresholds"""
        logger.info("Running threshold analysis...")
        
        thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        results = []
        
        for conf in thresholds:
            metrics = model.val(conf=conf, **self.val_base_kwargs)
            
            f1 = 2 * (metrics.box.mp * metrics.box.mr) / (metrics.box.mp + metrics.box.mr + 1e-10)
            
            results.append({
                'threshold': conf,
                'mAP50': metrics.box.map50,
                'mAP50-95': metrics.box.map,
                'precision': metrics.box.mp,
                'recall': metrics.box.mr,
                'f1': f1
            })
        
        df = pd.DataFrame(results)
        
        # Find best threshold
        best_idx = df['f1'].idxmax()
        best_threshold = df.iloc[best_idx]
        
        # Plot
        plt.figure(figsize=(12, 8))
        plt.plot(df['threshold'], df['precision'], 'b-', label='Precision', linewidth=2)
        plt.plot(df['threshold'], df['recall'], 'g-', label='Recall', linewidth=2)
        plt.plot(df['threshold'], df['f1'], 'r-', label='F1-Score', linewidth=2)
        plt.plot(df['threshold'], df['mAP50'], 'y--', label='mAP50', linewidth=2)
        
        plt.axvline(x=best_threshold['threshold'], color='k', linestyle='--', alpha=0.5)
        plt.scatter([best_threshold['threshold']], [best_threshold['f1']], 
                   color='red', s=100, zorder=5)
        
        plt.xlabel('Confidence Threshold')
        plt.ylabel('Score')
        plt.title('Performance at Different Confidence Thresholds')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig(self.research_dir / f'threshold_analysis_{self.timestamp}.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()
        
        # Save results
        df.to_csv(self.research_dir / f'threshold_results_{self.timestamp}.csv', index=False)
        
        logger.info(f"\n📊 Best threshold: {best_threshold['threshold']:.2f}")
        logger.info(f"   F1-Score: {best_threshold['f1']:.4f}")
        logger.info(f"   mAP50: {best_threshold['mAP50']:.4f}")
        
        return df
    
    def confusion_matrix_analysis(self, model):
        """Analyze confusion matrix"""
        logger.info("Running confusion matrix analysis...")
        
        # Run validation to get predictions
        results = model.val(**self.val_base_kwargs)
        
        # Load confusion matrix image if available
        conf_files = list(Path('results').glob('**/confusion_matrix.png'))
        
        if conf_files:
            img = plt.imread(conf_files[0])
            plt.figure(figsize=(10, 8))
            plt.imshow(img)
            plt.axis('off')
            plt.title('Confusion Matrix')
            plt.savefig(self.research_dir / f'confusion_matrix_{self.timestamp}.png', 
                       dpi=300, bbox_inches='tight')
            plt.show()
    
    def per_class_metrics(self, model):
        """Detailed per-class analysis"""
        logger.info("Calculating per-class metrics...")
        
        # Get detailed metrics
        metrics = model.val(**self.val_base_kwargs)
        box_metrics = metrics.box

        # Ultralytics v8 exposes class-wise precision/recall/F1 as arrays and AP via methods.
        p = np.asarray(getattr(box_metrics, 'p', []), dtype=float)
        r = np.asarray(getattr(box_metrics, 'r', []), dtype=float)
        f1 = np.asarray(getattr(box_metrics, 'f1', []), dtype=float)
        ap50_attr = getattr(box_metrics, 'ap50', np.array([]))
        ap_attr = getattr(box_metrics, 'ap', np.array([]))
        ap50 = np.asarray(ap50_attr() if callable(ap50_attr) else ap50_attr, dtype=float)
        ap5095 = np.asarray(ap_attr() if callable(ap_attr) else ap_attr, dtype=float)

        if f1.size == 0 and p.size and r.size:
            f1 = 2 * (p * r) / (p + r + 1e-10)
        
        class_metrics = []
        for i, class_name in enumerate(model.names.values()):
            class_metrics.append({
                'class': class_name,
                'precision': float(p[i]) if i < p.size else 0.0,
                'recall': float(r[i]) if i < r.size else 0.0,
                'f1': float(f1[i]) if i < f1.size else 0.0,
                'ap50': float(ap50[i]) if i < ap50.size else 0.0,
                'map50-95': float(ap5095[i]) if i < ap5095.size else 0.0,
                'num_classes': int(getattr(box_metrics, 'nc', 0))
            })
        
        df = pd.DataFrame(class_metrics)
        
        # Plot
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        # Precision
        axes[0].bar(df['class'], df['precision'], color='skyblue')
        axes[0].set_title('Precision per Class')
        axes[0].set_ylim(0, 1)
        axes[0].set_ylabel('Precision')
        
        # Recall
        axes[1].bar(df['class'], df['recall'], color='lightgreen')
        axes[1].set_title('Recall per Class')
        axes[1].set_ylim(0, 1)
        axes[1].set_ylabel('Recall')
        
        # F1
        axes[2].bar(df['class'], df['f1'], color='salmon')
        axes[2].set_title('F1-Score per Class')
        axes[2].set_ylim(0, 1)
        axes[2].set_ylabel('F1-Score')
        
        plt.tight_layout()
        plt.savefig(self.research_dir / f'per_class_metrics_{self.timestamp}.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()
        
        df.to_csv(self.research_dir / f'per_class_metrics_{self.timestamp}.csv', index=False)
        
        return df
    
    def generate_research_report(self, model, threshold_df, class_df):
        """Generate complete research report"""
        
        # Get overall metrics
        metrics = model.val(**self.val_base_kwargs)
        
        report = f"""
===============================================================================
        RESEARCH REPORT: DAMAGED PARCEL DETECTION USING {self.model_label}
===============================================================================

EXPERIMENT INFORMATION
===============================================================================
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Model: {self.model_label}
Classes: {list(model.names.values())}

OVERALL PERFORMANCE
===============================================================================
• mAP@0.5: {metrics.box.map50:.4f}
• mAP@0.5:0.95: {metrics.box.map:.4f}
• Precision: {metrics.box.mp:.4f}
• Recall: {metrics.box.mr:.4f}
• F1-Score: {2 * (metrics.box.mp * metrics.box.mr) / (metrics.box.mp + metrics.box.mr + 1e-10):.4f}

THRESHOLD ANALYSIS
===============================================================================
"""
        
        # Add best threshold info
        best_thresh = threshold_df.loc[threshold_df['f1'].idxmax()]
        report += f"""
Optimal Confidence Threshold: {best_thresh['threshold']:.2f}
• Precision at optimal threshold: {best_thresh['precision']:.4f}
• Recall at optimal threshold: {best_thresh['recall']:.4f}
• F1-Score at optimal threshold: {best_thresh['f1']:.4f}
• mAP50 at optimal threshold: {best_thresh['mAP50']:.4f}

PER-CLASS PERFORMANCE
===============================================================================
"""
        
        for _, row in class_df.iterrows():
            report += f"""
{row['class']}:
  • Precision: {row['precision']:.4f}
  • Recall: {row['recall']:.4f}
  • F1-Score: {row['f1']:.4f}
"""
        
        report += f"""
===============================================================================
                        CONCLUSION
===============================================================================
The {self.model_label} model demonstrates {'excellent' if metrics.box.map50 > 0.9 else 
                                           'good' if metrics.box.map50 > 0.8 else
                                           'satisfactory' if metrics.box.map50 > 0.7 else
                                           'moderate'} performance in detecting damaged parcels,
with an overall mAP50 of {metrics.box.map50:.1%}.

Best results are achieved at a confidence threshold of {best_thresh['threshold']:.2f},
balancing precision and recall with an F1-score of {best_thresh['f1']:.4f}.

===============================================================================
Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
===============================================================================
"""
        
        # Save report
        report_path = self.research_dir / f'research_report_{self.timestamp}.txt'
        with open(report_path, 'w') as f:
            f.write(report)
        
        print(report)
        logger.info(f"Report saved to: {report_path}")
        
        return report

if __name__ == "__main__":
    analyzer = ResearchAnalyzer()
    
    # Load model
    model_path = input("Enter model path (press Enter for latest YOLOv8m): ").strip()
    model = analyzer.load_model(model_path if model_path else None)
    
    if model:
        # Run analyses
        threshold_df = analyzer.threshold_analysis(model)
        class_df = analyzer.per_class_metrics(model)
        analyzer.confusion_matrix_analysis(model)
        
        # Generate report
        report = analyzer.generate_research_report(model, threshold_df, class_df)
        
        print("\n✅ Research analysis complete!")
        print(f"📁 All outputs saved in: {analyzer.research_dir}")