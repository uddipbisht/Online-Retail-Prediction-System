# -*- coding: utf-8 -*-
"""
train_models.py - Standalone script to download data and train all ML models.

Run this ONCE before starting the Flask API or Streamlit app.

Usage:
    python train_models.py
"""
import os
import sys
import urllib.request
import zipfile

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")

sys.path.insert(0, BACKEND_DIR)

from data_processor import load_data, clean_data, engineer_features
from ml_model import train_revenue_model, train_segment_model


def download_dataset():
    """Download UCI Online Retail dataset if not present."""
    excel_path = os.path.join(DATA_DIR, "Online Retail.xlsx")
    if os.path.exists(excel_path):
        print("[OK] Dataset already exists: %s" % excel_path)
        return excel_path

    print("[*] Downloading Online Retail dataset from UCI ML Repository...")
    zip_path = os.path.join(DATA_DIR, "online_retail.zip")
    url = "https://archive.ics.uci.edu/static/public/352/online+retail.zip"

    try:
        urllib.request.urlretrieve(url, zip_path)
        print("[OK] Download complete. Extracting...")
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(DATA_DIR)
        os.remove(zip_path)
        print("[OK] Extracted to %s" % DATA_DIR)
    except Exception as e:
        print("[FAIL] Download failed: %s" % e)
        print(
            "\nPlease manually download the dataset from:\n"
            "  https://archive.ics.uci.edu/dataset/352/online+retail\n"
            "and place 'Online Retail.xlsx' in: %s" % DATA_DIR
        )
        sys.exit(1)

    return excel_path


def main():
    print("=" * 60)
    print("  Online Retail Prediction - Model Training Pipeline")
    print("=" * 60)

    # Step 1: Download data
    data_path = download_dataset()

    # Step 2: Load & clean
    print("\n[1] Loading and cleaning data...")
    df_raw = load_data(data_path)
    print("    Raw rows    : %s" % f"{len(df_raw):,}")
    df_clean = clean_data(df_raw)
    print("    Clean rows  : %s" % f"{len(df_clean):,}")

    # Step 3: Feature engineering
    print("\n[2] Engineering RFM features...")
    features = engineer_features(df_clean)
    print("    Customers   : %s" % f"{len(features):,}")

    # Step 4: Train models
    print("\n[3] Training Revenue Prediction Model (Random Forest)...")
    _, _, rev_metrics = train_revenue_model(features)
    print("    MAE         = %s" % rev_metrics["mae"])
    print("    RMSE        = %s" % rev_metrics["rmse"])
    print("    R2          = %s" % rev_metrics["r2"])

    print("\n[4] Training Customer Segmentation Model (Gradient Boosting)...")
    _, _, _, seg_metrics = train_segment_model(features)
    print("    Accuracy    = %s" % seg_metrics["accuracy"])

    print("\n" + "=" * 60)
    print("[DONE] Training complete! Models saved to /models/")
    print("\nNext steps:")
    print("  1. Start the Flask API   : python backend/app.py")
    print("  2. Start the Streamlit UI: streamlit run frontend/streamlit_app.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
