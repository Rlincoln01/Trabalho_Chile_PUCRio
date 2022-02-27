# Load existing image
FROM python:latest

# Install all packages used in the assignment
RUN pip install pandas
RUN pip install statsmodels
RUN pip install matplotlib
RUN pip install datetime
RUN pip install tqdm
RUN pip install bs4
RUN pip install requests
RUN pip install regex

# Copy the necessary files from the folder into the image
COPY /Codes/data_scraping_twitter.py ./
COPY /Codes/political_participation_index.py ./
COPY /Codes/plots.py ./
COPY /Codes/models.py ./

# Run each of the scripts in the correct order
CMD ["python","-u","./data_scraping_twitter.py"]
CMD ["python","-u","./political_participation_index.py"] 
CMD ["python","-u","./plots.py"]
CMD ["python","-u","./models.py"]