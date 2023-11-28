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

```
docker system prune && docker build --tag brainimage --file Dockerfile . && docker run -v ~/static_volume:/app/data -w /app brainimage python src/utils/preprocessing.py
```