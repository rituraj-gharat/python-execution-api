FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    build-essential \
    git \
    libprotobuf-dev \
    libnl-route-3-dev \
    libtool \
    autoconf \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install nsjail from source with specific version
RUN git clone --depth 1 --branch 3.0 https://github.com/google/nsjail.git /tmp/nsjail \
    && cd /tmp/nsjail \
    && make \
    && cp nsjail /usr/local/bin/ \
    && chmod +x /usr/local/bin/nsjail \
    && rm -rf /tmp/nsjail

# Clean up build dependencies
RUN apt-get remove -y git build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install common data science libraries
RUN pip install --no-cache-dir \
    pandas==2.0.3 \
    numpy==1.24.3 \
    matplotlib==3.7.2 \
    scipy==1.11.1

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app && \
    chown -R appuser:appuser /app

# Copy application files
COPY app.py /app/
COPY nsjail.cfg /etc/nsjail.cfg

# Set working directory
WORKDIR /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8080

# Run the application
CMD ["python", "app.py"]
