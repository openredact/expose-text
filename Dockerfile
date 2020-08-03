FROM python:3.7

# Run tests within Docker
# docker build -t expose-text .
# docker run expose-text

WORKDIR /app

# Install PDF depdencies (expose-text)
RUN apt-get update
RUN apt-get install -y cmake autoconf

# wkhtmltopdf
RUN wget --quiet https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.3/wkhtmltox-0.12.3_linux-generic-amd64.tar.xz && \
    tar vxf wkhtmltox-0.12.3_linux-generic-amd64.tar.xz && \
    cp wkhtmltox/bin/wk* /usr/local/bin/ && \
    rm -rf wkhtmltox

# Uninstall old version (latest version is not available over apt)
RUN apt-get purge -y poppler-utils

# Install new poppler-utils manually
RUN wget poppler.freedesktop.org/poppler-0.90.1.tar.xz
RUN tar -xvf poppler-0.90.1.tar.xz
RUN cd poppler-0.90.1 && mkdir build && cd build && cmake .. && make && ldconfig
RUN ln -s /usr/local/bin/pdftohtml /usr/bin/pdftohtml

# Install packages
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install pytest pytest-cov

COPY ./ /app/

CMD ["pytest", "--doctest-modules", "--cov-report", "term", "--cov", "expose_text", "-s"]

