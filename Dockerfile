FROM python:3
RUN git clone https://github.com/Ignacio687/4-en-linea.git
WORKDIR /4-en-linea
RUN pip install -r requirements.txt
CMD ["python3", "-m", "unittest"]

# comando para probar docker
# docker build -t {nombre(arbitrario)}:{version(arbitrario)} .
# docker run -i --name {nombre(arbitrario)} {nombre imagen:version imagen}