# Use official lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Install system libraries (remove if OpenCV headless is enough)
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgtk2.0-dev \
    pkg-config \
    ffmpeg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python libraries in one step to reduce layers
RUN pip install --upgrade pip && \
    pip install -r yolov5/requirements.txt && \
    pip install opencv-python-headless filterpy scikit-image

# Ensure ai.py has execute permissions
RUN chmod +x ai.py

# Run the application
CMD ["python", "ai.py"]
