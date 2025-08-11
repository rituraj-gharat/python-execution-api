#!/bin/bash

# Google Cloud Run Deployment Script
# Make sure you have gcloud CLI installed and configured

set -e

# Configuration
PROJECT_ID=$(gcloud config get-value project)
SERVICE_NAME="python-executor"
REGION="us-central1"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "🚀 Deploying Python Code Execution Service to Google Cloud Run"
echo "Project ID: $PROJECT_ID"
echo "Service Name: $SERVICE_NAME"
echo "Region: $REGION"
echo "Image: $IMAGE_NAME"
echo ""

# Build and push the Docker image
echo "📦 Building and pushing Docker image..."
gcloud builds submit --tag $IMAGE_NAME

# Deploy to Cloud Run
echo "☁️ Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image $IMAGE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi \
  --cpu 1 \
  --timeout 300 \
  --max-instances 10

# Get the service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format='value(status.url)')

echo ""
echo "✅ Deployment successful!"
echo "Service URL: $SERVICE_URL"
echo ""
echo "🧪 Test the service:"
echo "curl -X POST $SERVICE_URL/execute \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{\"script\": \"def main():\\n    return {\\\"message\\\": \\\"Hello from Cloud Run!\\\"}\"}'"
echo ""
echo "🏥 Health check:"
echo "curl $SERVICE_URL/health" 