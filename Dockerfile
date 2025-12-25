# Multi-stage build
FROM python:3.11-slim as builder

WORKDIR /build

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
        && rm -rf /var/lib/apt/lists/*

        # Copy requirements and install Python dependencies
        COPY requirements.txt .
        RUN pip install --user --no-cache-dir -r requirements.txt

        # Final stage
        FROM python:3.11-slim

        WORKDIR /app

        # Copy Python dependencies from builder
        COPY --from=builder /root/.local /root/.local

        # Set environment variables
        ENV PATH=/root/.local/bin:$PATH \
            PYTHONUNBUFFERED=1 \
                PYTHONDONTWRITEBYTECODE=1 \
                    ANTHROPIC_API_KEY=""

                    # Copy application files
                    COPY . .

                    # Health check
                    HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
                        CMD python -c "import anthropic; print('OK')" || exit 1

                        # Default command
                        CMD ["python", "app.py"]
