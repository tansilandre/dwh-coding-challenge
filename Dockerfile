FROM python:3.9.12

RUN pip3 install pandas
COPY ./ ./

# CMD ["python", "main.py"]
CMD [ "python3","solution/main.py" ]
