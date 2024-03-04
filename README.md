# MyMidjourney Client

This is a simple Python based client for the APIs exposed by https://www.mymidjourney.ai/

## Pre-requisites

You will need to have a My Midjourney API, a [MyMidjourney Token](https://www.mymidjourney.ai/setup).

## Ddevelopment instructions

Please make sure to install [Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) first.

```bash
conda create -n mymidjourney_client python=3.12
conda activate mymidjourney_client
pip install poetry
poetry install
```

## Running unit tests

```bash
python -m unittest
```


## Fundamental Environment Variables

There are some expected environment variables which you can save in the .env file:

```
MY_MIDJOURNEY_BEARER_TOKEN=<My Midjourney token (optional)>
MY_MIDJOURNEY_TEMP_DIR=/development/playground/agents/mymidjourney-client/generated_images
```

## Running the command line client

This library contains a small command line client which allows to imagine images and to upscale them. You can run it with the follwoing command:

```
python ./mymidjourney_client/workflow.py
```