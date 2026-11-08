# n8n with native Python (CranL)

This folder builds a custom n8n 2.46.6 image with Python 3 installed in the same container.

## Build locally

```sh
docker build -t n8n-python:2.46.6 ./n8n-python
```

## Publish

The GitHub Actions workflow at `.github/workflows/n8n-python-image.yml` builds and pushes the image to GHCR on changes to this folder or by manual dispatch.

Image:
`ghcr.io/roplizeramr-blip/n8n-python:2.46.6`

The GHCR package must be made public before CranL can pull it without registry credentials.

## CranL environment

Keep the existing persistent volume at `/home/node/.n8n` and set:

- `N8N_NATIVE_PYTHON_RUNNER=true`
- `N8N_RUNNERS_MODE=internal`

Internal mode is intended for isolated instances, not production with untrusted workflow editors. For production, use n8n's external task-runner architecture.
