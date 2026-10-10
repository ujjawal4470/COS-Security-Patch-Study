#!/bin/bash
# Setup script for creating a COS VM on Google Cloud
# This script creates a Container-Optimized OS VM instance for security study
set -euo pipefail

echo "=== GCP COS VM Setup ==="

if ! command -v gcloud &> /dev/null; then
    echo "Error: gcloud CLI is not installed or not in PATH."
    exit 1
fi

PROJECT_ID=${1:-$(gcloud config get-value project 2>/dev/null || echo "")}
ZONE=${2:-us-central1-a}
INSTANCE_NAME=${3:-cos-study-vm}

if [ -z "$PROJECT_ID" ]; then
    echo "Usage: $0 [PROJECT_ID] [ZONE] [INSTANCE_NAME]"
    echo "No project ID provided or configured."
    exit 1
fi

echo "Configuration:"
echo "  Project: $PROJECT_ID"
echo "  Zone: $ZONE"
echo "  Instance: $INSTANCE_NAME"
echo "  Machine Type: e2-medium (Estimated cost: ~$25/month)"
echo "  Image: cos-101-lts"
echo ""
read -p "Do you want to proceed with creating this VM? (y/n): " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "Operation cancelled."
    exit 0
fi

echo "Creating instance $INSTANCE_NAME..."
gcloud compute instances create "$INSTANCE_NAME" \
    --project="$PROJECT_ID" \
    --zone="$ZONE" \
    --machine-type=e2-medium \
    --image-family=cos-101-lts \
    --image-project=cos-cloud \
    --boot-disk-size=20GB \
    --tags=cos-study

echo "=== Setup Complete ==="
echo "You can now connect via:"
echo "gcloud compute ssh $INSTANCE_NAME --project=$PROJECT_ID --zone=$ZONE"
