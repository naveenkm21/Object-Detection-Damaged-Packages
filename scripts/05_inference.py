"""
Script 5: Run inference on images/videos
"""

from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
from pathlib import Path
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class InferenceEngine:
    def __init__(self):
        self.output_dir = Path('results/inference')
        self.output_dir.mkdir(exist_ok=True)
        
    def load_model(self, model_path=None):
        """Load YOLO model"""
        if model_path is None:
            # Find latest model
            model_files = list(Path('results').rglob('*/weights/best.pt'))
            if not model_files:
                logger.error("No trained model found!")
                return None
            
            model_path = max(model_files, key=lambda x: x.stat().st_mtime)
        
        logger.info(f"Loading model: {model_path}")
        return YOLO(str(model_path))
    
    def inference_image(self, model, image_path, conf=0.25):
        """Run inference on single image"""
        image_path = Path(image_path)
        
        if not image_path.exists():
            logger.error(f"Image not found: {image_path}")
            return
        
        logger.info(f"Processing: {image_path.name}")
        
        # Run inference
        results = model(str(image_path), conf=conf)
        
        # Display results
        for r in results:
            # Plot detections
            im_array = r.plot()
            
            # Convert BGR to RGB
            im_rgb = cv2.cvtColor(im_array, cv2.COLOR_BGR2RGB)
            
            # Display
            plt.figure(figsize=(12, 8))
            plt.imshow(im_rgb)
            plt.title(f'Detections (conf={conf})')
            plt.axis('off')
            plt.show()
            
            # Print detections
            if len(r.boxes) > 0:
                print(f"\n📦 Found {len(r.boxes)} objects:")
                for i, box in enumerate(r.boxes):
                    cls = int(box.cls[0])
                    conf = float(box.conf[0])
                    print(f"   {i+1}. {model.names[cls]}: {conf:.2f}")
            else:
                print("\n❌ No objects detected")
            
            # Save result
            output_path = self.output_dir / f"detected_{image_path.name}"
            cv2.imwrite(str(output_path), im_array)
            logger.info(f"Saved to: {output_path}")
    
    def inference_video(self, model, video_path, conf=0.25):
        """Run inference on video"""
        video_path = Path(video_path)
        
        if not video_path.exists():
            logger.error(f"Video not found: {video_path}")
            return
        
        cap = cv2.VideoCapture(str(video_path))
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Output video
        output_path = self.output_dir / f"detected_{video_path.name}"
        out = cv2.VideoWriter(str(output_path), 
                              cv2.VideoWriter_fourcc(*'mp4v'), 
                              fps, (width, height))
        
        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Run inference
            results = model(frame, conf=conf)
            
            # Plot detections
            annotated_frame = results[0].plot()
            
            # Write frame
            out.write(annotated_frame)
            
            frame_count += 1
            if frame_count % 30 == 0:
                logger.info(f"Processed {frame_count} frames")
        
        cap.release()
        out.release()
        logger.info(f"Video saved to: {output_path}")
    
    def batch_inference(self, model, input_folder, conf=0.25):
        """Process all images in a folder"""
        input_folder = Path(input_folder)
        
        if not input_folder.exists():
            logger.error(f"Folder not found: {input_folder}")
            return
        
        # Get all images
        images = []
        for ext in ['*.jpg', '*.jpeg', '*.png']:
            images.extend(input_folder.glob(ext))
        
        logger.info(f"Found {len(images)} images to process")
        
        for img_path in images:
            self.inference_image(model, img_path, conf)

if __name__ == "__main__":
    engine = InferenceEngine()
    
    print("\n" + "="*60)
    print("INFERENCE OPTIONS")
    print("="*60)
    print("1. Single image")
    print("2. Video file")
    print("3. Batch process folder")
    
    choice = input("\nChoose (1-3): ").strip()
    
    # Load model
    model_path = input("Enter model path (press Enter for latest): ").strip()
    model = engine.load_model(model_path if model_path else None)
    
    if not model:
        exit()
    
    conf = float(input("Confidence threshold [0.25]: ").strip() or "0.25")
    
    if choice == "1":
        img_path = input("Enter image path: ").strip()
        engine.inference_image(model, img_path, conf)
    
    elif choice == "2":
        video_path = input("Enter video path: ").strip()
        engine.inference_video(model, video_path, conf)
    
    elif choice == "3":
        folder = input("Enter folder path: ").strip()
        engine.batch_inference(model, folder, conf)