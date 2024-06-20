FROM ubuntu:latest
ENV TZ=Asia/Kolkata DEBIAN_FRONTEND=noninteractive PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y libcairo2-dev libpango1.0-dev libjpeg-dev libgif-dev curl python3 python3-distutils python3-pip python3-venv libsm6 libxext6 libgl1 libxrender1 libfontconfig1 libice6 python3-opencv
RUN curl -sL https://deb.nodesource.com/setup_18.x | bash
RUN apt-get install -y nodejs gcc g++ make
RUN echo "Node.js version is:" && node -v && echo "NPM version is:" && npm -v && echo "Python version is:" && python3 --version && echo "Python pip version is:" && pip --version

WORKDIR /simpplr
COPY . .

WORKDIR /simpplr/frontend

RUN export NODE_ENV=production
RUN npm install -g npm@latest
RUN npm install
RUN npm run build

RUN rm -r ../backend/backend/static
RUN mkdir ../backend/backend/static
RUN mv ./out/* ../backend/backend/static

WORKDIR ../backend
RUN pip install -r requirements.txt
RUN python -m backend setupDB

CMD ["python", "-m", "backend"]