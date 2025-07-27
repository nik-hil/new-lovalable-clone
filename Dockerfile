FROM node:18-slim

# Set working directory
WORKDIR /app

# Install Python and system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Vue CLI globally
RUN npm install -g @vue/cli @vue/cli-service

# Copy package.json for Node.js dependencies (we'll create this)
COPY package*.json ./
RUN npm install || echo "No package.json found, will install later"

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt --break-system-packages

# Copy application code
COPY . .

# Create output directory
RUN mkdir -p output

# Set environment variables
ENV PYTHONPATH=/app/src
ENV FLASK_APP=src/server.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

# Expose ports
EXPOSE 5001 8080 3000

# Start both Flask and Vue dev servers
CMD ["sh", "-c", "python3 src/server.py & (cd frontend && npm run serve 2>/dev/null || echo 'Vue frontend not ready yet') & wait"]
