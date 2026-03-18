# Use a specific, slim base image
FROM python:3.10-slim

# Create a non-root user and group
RUN addgroup --system app && adduser --system --ingroup app app

# Set the working directory
WORKDIR /home/app

# Copy dependency file and install as the new user
COPY --chown=app:app requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY --chown=app:app . .

# Switch to the non-root user
USER app

# Expose the port Streamlit will run on
EXPOSE 8000

# Command to run the app
CMD ["streamlit", "run", "app.py", "--server.port=8000", "--server.address=0.0.0.0"]