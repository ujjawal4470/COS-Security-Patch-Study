#!/bin/bash
# Configure firewall rules for the COS study VM
set -euo pipefail

PROJECT_ID=${1:-$(gcloud config get-value project 2>/dev/null || echo "")}

if [ -z "$PROJECT_ID" ]; then
    echo "Usage: $0 [PROJECT_ID]"
    exit 1
fi

echo "Fetching your public IP..."
USER_IP=$(curl -s ifconfig.me)
if [ -z "$USER_IP" ]; then
    echo "Failed to determine public IP."
    exit 1
fi

echo "Your IP is $USER_IP"
echo "Creating restricted firewall rules for tag 'cos-study'..."

read -p "Proceed with creating firewall rules? (y/n): " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "Operation cancelled."
    exit 0
fi

gcloud compute firewall-rules create allow-ssh-cos-study \
    --project="$PROJECT_ID" \
    --direction=INGRESS \
    --priority=1000 \
    --network=default \
    --action=ALLOW \
    --rules=tcp:22 \
    --source-ranges="${USER_IP}/32" \
    --target-tags=cos-study

gcloud compute firewall-rules create allow-https-cos-study \
    --project="$PROJECT_ID" \
    --direction=INGRESS \
    --priority=1000 \
    --network=default \
    --action=ALLOW \
    --rules=tcp:443 \
    --source-ranges="${USER_IP}/32" \
    --target-tags=cos-study

echo "Firewall rules applied to tag: cos-study"
