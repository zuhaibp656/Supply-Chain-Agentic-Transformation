FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    GOOGLE_CLOUD_PROJECT=zuhaibp-ai \
    GOOGLE_CLOUD_LOCATION=us-central1

WORKDIR /app

COPY enterprise_twin/requirements.txt /app/enterprise_twin/requirements.txt
RUN pip install --no-cache-dir -r /app/enterprise_twin/requirements.txt

# Copy portal HTML assets, canonical catalog, pre-seeded twins & Enterprise Twin Studio backend
COPY index.html periodic_table.html mind_map.html cost_analysis_presentation.html agent_testing_and_video_playbook.html supply_chain_101_interactive_academy.html /app/
COPY data/ /app/data/
COPY videos/ /app/videos/
COPY enterprise_twin/ /app/enterprise_twin/

EXPOSE 8080

CMD ["sh", "-c", "uvicorn enterprise_twin.server:app --host 0.0.0.0 --port ${PORT:-8080} --workers 1"]
