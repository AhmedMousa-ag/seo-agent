docker build -t seo-agent .
docker stop seo-agent && docker rm seo-agent
docker run --name seo-agent -d -p 8500:8000 --restart always seo-agent