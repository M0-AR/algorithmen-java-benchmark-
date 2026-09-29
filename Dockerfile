FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY benchmarks/ benchmarks/
COPY scripts/ scripts/
COPY tests/ tests/
CMD ["python3", "scripts/run_benchmarks.py"]
