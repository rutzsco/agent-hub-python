# Azure Container Apps Deployment Setup

This document outlines the required GitHub repository configuration for deploying to Azure Container Apps.

## Required GitHub Repository Secrets

Configure the following secrets in your GitHub repository settings (`Settings` > `Secrets and variables` > `Actions`):

### Container Registry Secrets
- `DOCKER_USERNAME`: Username for your container registry (Azure Container Registry or Docker Hub)
- `DOCKER_PASSWORD`: Password/token for your container registry

### Azure Authentication
- `AZURE_CREDENTIALS`: Azure service principal credentials in JSON format

To create the Azure service principal credentials:

```bash
# Login to Azure
az login

# Create a service principal with contributor role
az ad sp create-for-rbac --name "github-actions-sp" --role contributor --scopes /subscriptions/{subscription-id} --sdk-auth
```

The output should be in this format:
```json
{
  "clientId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "clientSecret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "subscriptionId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "tenantId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

## Required GitHub Repository Variables

Configure the following variables in your GitHub repository settings (`Settings` > `Secrets and variables` > `Actions` > `Variables`):

### Container Registry Variables
- `CONTAINER_REGISTRY_URL`: URL of your container registry (e.g., `myregistry.azurecr.io` for ACR)
- `CONTAINER_REGISTRY_REPOSITORY_NAME`: Name of your container repository/image (e.g., `agent-hub-python`)

### Azure Container Apps Variables
- `AZURE_CONTAINER_APP_NAME`: Name of your Azure Container App
- `AZURE_RESOURCE_GROUP`: Azure resource group containing your Container App
- `AZURE_CONTAINER_REGISTRY_NAME`: Name of your Azure Container Registry (if using ACR)

## Azure Resources Setup

### 1. Create Azure Container Registry (Optional)
```bash
# Create resource group
az group create --name myResourceGroup --location eastus

# Create Azure Container Registry
az acr create --resource-group myResourceGroup --name myregistry --sku Basic
```

### 2. Create Azure Container App Environment
```bash
# Create Container App Environment
az containerapp env create --name myContainerAppEnv --resource-group myResourceGroup --location eastus
```

### 3. Create Azure Container App
```bash
# Create Container App
az containerapp create \
  --name agent-hub-python \
  --resource-group myResourceGroup \
  --environment myContainerAppEnv \
  --image myregistry.azurecr.io/agent-hub-python:latest \
  --target-port 8000 \
  --ingress external \
  --min-replicas 1 \
  --max-replicas 3
```

## Workflow Behavior

- **Pull Requests**: Builds and validates the Docker image but does not push or deploy
- **Push to Main**: Builds, pushes the Docker image, and deploys to Azure Container Apps
- **Image Tags**: 
  - Latest commit SHA (short format)
  - `latest` tag (only for main branch pushes)

## Troubleshooting

### Common Issues

1. **Authentication Errors**: Ensure `AZURE_CREDENTIALS` secret is properly formatted JSON
2. **Registry Access**: Verify `DOCKER_USERNAME` and `DOCKER_PASSWORD` have push permissions
3. **Container App Not Found**: Check `AZURE_CONTAINER_APP_NAME` and `AZURE_RESOURCE_GROUP` variables
4. **Image Pull Errors**: Ensure the Container App has access to pull from your registry

### Useful Commands

```bash
# Check Container App status
az containerapp show --name agent-hub-python --resource-group myResourceGroup

# View Container App logs
az containerapp logs show --name agent-hub-python --resource-group myResourceGroup

# Update Container App with new image
az containerapp update --name agent-hub-python --resource-group myResourceGroup --image myregistry.azurecr.io/agent-hub-python:latest
```
