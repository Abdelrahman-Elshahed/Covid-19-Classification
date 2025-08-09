# Multi-stage build for Next.js + FastAPI
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy package files and install dependencies (including dev dependencies for build)
COPY frontend_nextjs/package*.json ./
RUN npm ci

# Copy all frontend files
COPY frontend_nextjs/ ./

# Build the frontend
RUN npm run build

# Production stage
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY pyproject.toml ./

# ✅ Install PyTorch (CPU-only) BEFORE installing the rest of the project
RUN pip install --upgrade pip && \
    pip install torch==2.5.1+cpu --index-url https://download.pytorch.org/whl/cpu && \
    pip install -e .
# Copy backend code
COPY covid_predictor_api/ ./covid_predictor_api/
COPY RagModule/ ./RagModule/
COPY models/ ./models/
COPY data/ ./data/

# Copy environment files for Azure OpenAI
COPY .env.docker ./RagModule/.env
COPY .env.docker ./.env

# Copy built frontend from builder stage (Next.js static export)
COPY --from=frontend-builder /app/frontend/out ./frontend_nextjs/out
COPY --from=frontend-builder /app/frontend/package*.json ./frontend_nextjs/

# Copy Next.js config files explicitly
COPY frontend_nextjs/next.config.mjs ./frontend_nextjs/next.config.mjs
COPY frontend_nextjs/jsconfig.json ./frontend_nextjs/jsconfig.json

# Back to app directory
WORKDIR /app

# Create startup script - ONLY START BACKEND (it will serve frontend)
RUN echo '#!/bin/bash\n\
export PYTHONPATH="/app:/app/covid_predictor_api:$PYTHONPATH"\n\
export $(cat .env | grep -v "#" | xargs)\n\
PORT=${PORT:-8000}\n\
echo "🦠 COVID-19 Classification App Starting..."\n\
echo ""\n\
echo "📡 Application will be available at:"\n\
echo "   🌐 Frontend: http://localhost:$PORT"\n\
echo "   🔬 Prediction Tool: http://localhost:$PORT"\n\
echo "   💬 Research Chatbot: http://localhost:$PORT/chatbot"\n\
echo "   📚 API Documentation: http://localhost:$PORT/docs"\n\
echo "   🏥 Health Status: http://localhost:$PORT/health"\n\
echo ""\n\
echo "⚡ Starting server on 0.0.0.0:$PORT (accessible via localhost:$PORT)"\n\
echo ""\n\
cd /app/covid_predictor_api && python -m uvicorn main:app --host 0.0.0.0 --port $PORT' > /app/start.sh && chmod +x /app/start.sh

# Only expose port 8000 (backend will serve frontend)
EXPOSE 8000

CMD ["/app/start.sh"]