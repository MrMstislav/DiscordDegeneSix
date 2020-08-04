FROM gorialis/discord.py:3.6
WORKDIR /src
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "DegeneSix.py"]