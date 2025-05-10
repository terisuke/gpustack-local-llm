set -e


echo "Setting up Docker buildx for multi-architecture builds..."

if ! docker buildx inspect mybuilder &>/dev/null; then
  docker buildx create --name mybuilder --use
fi

docker buildx inspect --bootstrap

echo "Building multi-architecture images for ARM64 and AMD64..."

docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --tag gpustack-local-llm:latest \
  --file Dockerfile \
  --push \
  .

echo "Multi-architecture build complete!"
echo "To use the image locally, pull it with: docker pull gpustack-local-llm:latest"
echo "To verify the supported architectures: docker buildx imagetools inspect gpustack-local-llm:latest"
