FROM python:3.10.15-slim

WORKDIR /home

# install base tools
RUN apt-get update && apt-get install -y gnupg2 curl wget unzip ca-certificates
 
# download and install latest chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb;exit 0
RUN apt install -f -y

# config timezone
RUN ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# RUN apt-get update && apt-get install -y gnupg2 curl wget unzip ca-certificates

# RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
#     mkdir -p /opt/chromedriver-$CHROMEDRIVER_VERSION && \
#     curl -sS -o /tmp/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
#     unzip -qq /tmp/chromedriver_linux64.zip -d /opt/chromedriver-$CHROMEDRIVER_VERSION && \
#     rm /tmp/chromedriver_linux64.zip && \
#     chmod +x /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver && \
#     ln -fs /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver /usr/local/bin/chromedriver

#     RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
#     echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
#     apt-get -y update && \
#     apt-get -y install google-chrome-stable && \
#     rm -rf /var/lib/apt/lists/*

# RUN dpkg -i chrome.deb

# RUN apt-get update && apt-get install -y gnupg2 curl wget unzip ca-certificates

# COPY start.sh /usr/local/bin/start.sh

COPY . /app

# 暴露应用端口
EXPOSE 5000

# RUN chmod +x /usr/local/bin/start.sh

# 设置启动命令
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]