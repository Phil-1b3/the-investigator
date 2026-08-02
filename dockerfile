FROM python:3.12-slim          
# start from a small official Python image
WORKDIR /app                   
# work inside /app in the container
COPY requirements.txt .        
# copy deps list FIRST (caching trick, see below)
RUN pip install -r requirements.txt
COPY agent.py .                
# then copy the code
COPY evidence/ ./evidence/     
# and the sample logs
CMD ["python", "agent.py"]     
# what runs when the container starts