FROM python:3
RUN git clone https://github.com/Ignacio687/4-en-linea.git
WORKDIR /4-en-linea
RUN pip install -r requirements.txt
CMD ["coverage", "run", "-m", "unittest"]

# comandos para probar docker:
# docker build -t {nombre(arbitrario)}:{version(arbitrario)} .
# docker run -i --name {nombre(arbitrario)} {nombre imagen:version imagen}
# mostrar y eliminar instancias de docker:
# docker ps -a
# docker rm {conteiner.id}
# ver imagnes y elimnarlas:
# docker images
# docker image rm {id}