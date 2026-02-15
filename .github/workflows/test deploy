# .github/workflows/deploy.yml
name: Bot CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build_and_test:
    runs-on: ubuntu-latest
    outputs:
      image-tag: ${{ steps.build.outputs.tag }}

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Cache pip
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r dev-requirements.txt || true

      - name: Lint
        run: |
          flake8 bot tests
          black --check .
          isort --check-only .

      - name: Test
        env:
          BOT_TOKEN: ${{ secrets.BOT_TOKEN }}
          TEST_MODE: 1
        run: |
          pytest tests

      - name: Build Docker image
        id: build
        run: |
          IMAGE=ghcr.io/${{ github.repository_owner }}/mybot
          TAG=${{ github.sha }}
          docker build -t $IMAGE:$TAG -f docker/Dockerfile .
          echo "::set-output name=tag::$TAG"

      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Push Docker image
        run: |
          IMAGE=ghcr.io/${{ github.repository_owner }}/mybot
          TAG=${{ steps.build.outputs.tag }}
          docker push $IMAGE:$TAG

  deploy:
    needs: build_and_test
    runs-on: ubuntu-latest
    environment: Production
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Deploy to Kubernetes
        env:
          KUBECONFIG: ${{ secrets.KUBECONFIG_BASE64 }}
        run: |
          echo "$KUBECONFIG" | base64 -d > ~/.kube/config
          kubectl set image deployment/mybot-deploy mybot=ghcr.io/${{ github.repository_owner }}/mybot:${{ needs.build_and_test.outputs.image-tag }}
          kubectl rollout status deployment/mybot-deploy

      # Если используете Docker‑Compose на VPS:
      # - name: Deploy via SSH
      #   uses: appleboy/ssh-action@v0.1.10
      #   with:
      #     host: ${{ secrets.SSH_HOST }}
      #     username: ${{ secrets.SSH_USER }}
      #     key: ${{ secrets.SSH_KEY }}
      #     script: |
      #       cd /opt/mybot
      #       git pull
      #       docker-compose down
      #       docker-compose up -d
