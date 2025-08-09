FROM node:24-alpine


WORKDIR /app

COPY package*.json .


RUN  npm install     
RUN npm install -g serve
COPY . . 
EXPOSE 3000  
RUN npm run build

CMD [ "serve" ,"-s", "dist" ]