# Azure Container App Configuration Example

# This file contains example Azure CLI commands and configuration for setting up
# the Azure Container Apps infrastructure needed for the GitHub Actions deployment.

# 1. Set variables (replace with your actual values)
RESOURCE_GROUP="rg-agent-hub-python"
LOCATION="eastus"
CONTAINER_APP_ENV="env-agent-hub-python"
CONTAINER_APP_NAME="app-agent-hub-python"
ACR_NAME="acragenthubbpython"  # Must be globally unique
IMAGE_NAME="agent-hub-python"

# 2. Create resource group
az group create \
  --name $RESOURCE_GROUP \
  --location $LOCATION

# 3. Create Azure Container Registry (if not using Docker Hub)
az acr create \
  --resource-group $RESOURCE_GROUP \
  --name $ACR_NAME \
  --sku Basic \
  --admin-enabled true

# 4. Get ACR credentials (needed for GitHub secrets)
az acr credential show --name $ACR_NAME

# 5. Create Container Apps Environment
az containerapp env create \
  --name $CONTAINER_APP_ENV \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION

# 6. Create initial Container App with a placeholder image
az containerapp create \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment $CONTAINER_APP_ENV \
  --image mcr.microsoft.com/azuredocs/containerapps-helloworld:latest \
  --target-port 8000 \
  --ingress 'external' \
  --min-replicas 1 \
  --max-replicas 3 \
  --cpu 0.5 \
  --memory 1.0Gi

# 7. Get the Container App URL
az containerapp show \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query properties.configuration.ingress.fqdn \
  --output tsv

# Example GitHub Repository Variables to set:
echo "Set these GitHub Repository Variables:"
echo "CONTAINER_REGISTRY_URL: $ACR_NAME.azurecr.io"
echo "CONTAINER_REGISTRY_REPOSITORY_NAME: $IMAGE_NAME"
echo "AZURE_CONTAINER_APP_NAME: $CONTAINER_APP_NAME"
echo "AZURE_RESOURCE_GROUP: $RESOURCE_GROUP"
echo "AZURE_CONTAINER_REGISTRY_NAME: $ACR_NAME"
echo ""
echo "Set these GitHub Repository Secrets:"
echo "DOCKER_USERNAME: [ACR username from step 4]"
echo "DOCKER_PASSWORD: [ACR password from step 4]"
echo "AZURE_CREDENTIALS: [Service principal JSON from Azure setup]"
