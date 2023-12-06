# brainimaging-workflow

```
docker system prune && docker build --tag brainimage --file Dockerfile .
```

```
docker run --env-file=.env brainimage python src/utils/preprocessing.py
```

```
docker run --rm -it --entrypoint bash brainimage
```

run a file:

```
docker system prune && 
docker build --tag brainimage --file Dockerfile . && 
docker run -v ./static_volume:/app/static_volume -w /app brainimage python src/utils/preprocessing.py
```

jupyter notebook:

```
docker system prune && 
docker build --tag brainimage --file Dockerfile . && 
docker run -v ./src/notebooks:/app/src/notebooks -p 8888:8888 brainimage
```

```
docker-compose up --build
```