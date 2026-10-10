# GCP Deployment & Configuration

## Prerequisites
- Google Cloud Platform account
- Active billing account
- A newly created GCP Project

## Creating the Target COS VM
You can use the provided script or manual steps.
**Via Script:**
```bash
./scripts/setup-gcp-vm.sh my-project-id us-central1-a cos-target-1
```

## Firewall Configuration
Apply strict rules allowing access only from your IP:
```bash
./scripts/configure-firewall.sh my-project-id
```

## Service Account Setup
1. Create a service account in GCP IAM.
2. Grant `Compute Viewer` and `Compute OS Login` roles.
3. Download the JSON key.
4. Set `GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json` in your backend environment.

## Connecting the Dashboard
In the UI, navigate to "Settings" or "VM Connection", enter the instance name, zone, and project ID. Click "Connect". The backend will verify SSH connectivity.

## Running Security Scans
Navigate to the "Assessment" page in the dashboard and click "Run Scan". Scans invoke the internal `gcloud compute ssh` commands.

## Cost Management
- Stop the VM when not in use: `gcloud compute instances stop cos-target-1 --zone=us-central1-a`
- e2-medium costs roughly $25/month if left running 24/7.

## Cleanup
To delete all resources and prevent further billing:
```bash
gcloud compute instances delete cos-target-1 --zone=us-central1-a
gcloud compute firewall-rules delete allow-ssh-cos-study allow-https-cos-study
```
