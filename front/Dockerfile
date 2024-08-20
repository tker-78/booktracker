FROM --platform=$BUILDPLATFORM node:20-alpine AS development

RUN mkdir /project
WORKDIR /project

COPY . .

RUN npm install -g @vue/cli
RUN npm install
ENV HOST=0.0.0.0
CMD ["npm", "run", "dev"]