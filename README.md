# Nginx App With CICD

This is a simple web application served by an Nginx server.

## How to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/[repo]/nginx-app.git
   cd simple-nginx-app-cicd
2. Rebuild and Restart
    After confirming the Dockerfile and nginx.conf, rebuild the image and run the container:
    ```bash
    docker build -t simple-nginx-app-cicd .
    docker run -d -p 8080:80 simple-nginx-app-cicd
3.  Access application

    [http://localhost:8080](http://localhost:8080)
    