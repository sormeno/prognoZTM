FROM python:3

RUN apt-get update && apt-get install -y --no-install-recommends \
    unixodbc-dev \
    unixodbc \
    libpq-dev 
	
RUN git clone https://github.com/sormeno/prognoZTM.git
RUN pip install -r ./prognoZTM/configs/requirements.txt
COPY libs/lib_credentials/access.json /prognoZTM/libs/lib_credentials

# We need wget to set up the PPA and xvfb to have a virtual screen and unzip to install the Chromedriver
RUN apt-get install -y wget xvfb unzip
# Set up the Chrome PPA
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
# Update the package list and install chrome
RUN apt-get update -y
RUN apt-get install -y google-chrome-stable
# Set up Chromedriver Environment variables
ENV CHROMEDRIVER_VERSION 87.0.4280.88
ENV CHROMEDRIVER_DIR /chromedriver
RUN mkdir $CHROMEDRIVER_DIR
# Download and install Chromedriver
RUN wget -q --continue -P $CHROMEDRIVER_DIR "http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
RUN unzip $CHROMEDRIVER_DIR/chromedriver* -d $CHROMEDRIVER_DIR
# Put Chromedriver into the PATH
ENV PATH $CHROMEDRIVER_DIR:$PATH

RUN mkdir MySQL_ODBC && mkdir -p prognoZTM/utils/badfiles
ENV MYSQL_ODBC_VERSION mysql-connector-odbc-8.0.21-linux-glibc2.12-x86-64bit
RUN wget -q --continue -P MySQL_ODBC "https://downloads.mysql.com/archives/get/p/10/file/$MYSQL_ODBC_VERSION.tar.gz"
RUN gunzip /MySQL_ODBC/$MYSQL_ODBC_VERSION.tar.gz && tar xvf /MySQL_ODBC/$MYSQL_ODBC_VERSION.tar -C MySQL_ODBC
RUN cp MySQL_ODBC/$MYSQL_ODBC_VERSION/bin/* /usr/local/bin && cp MySQL_ODBC/$MYSQL_ODBC_VERSION/lib/* /usr/local/lib
RUN myodbc-installer -a -d -n "MySQL ODBC 8.0" -t "Driver=/usr/local/lib/libmyodbc8a.so"

RUN chmod +x ./prognoZTM/app.py