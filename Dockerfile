FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install nsjail
RUN wget -O /tmp/nsjail.deb https://github.com/google/nsjail/releases/download/3.0/nsjail_3.0_amd64.deb \
    && dpkg -i /tmp/nsjail.deb \
    && rm /tmp/nsjail.deb

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