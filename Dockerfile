# Use an official Python runtime as a parent image
FROM python

# Set the working directory
WORKDIR /fady@fady-G5-5587:~/Desktop/twitter-bot

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run twitter_bot.py when the container launches
CMD ["python", "./twitter_bot.py"]
