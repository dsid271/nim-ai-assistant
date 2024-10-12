FROM nvcr.io/nvidia/tritonserver:21.08-py3

WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose ports for the API and Prometheus metrics
EXPOSE 8000 9090

# Run the application
CMD ["python", "src/main.py"]
