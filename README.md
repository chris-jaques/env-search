# env-search
Searches all functions and aliases in your [env](https://github.com/chris-jaques/env) for a keyword or phrase

## Example Usage
```
docker run -v ~/env:/root/env siege4/env-search search $SEARCH_STRING
```

## Debugging
```
docker-compose run debug $SEARCH_STRING
```