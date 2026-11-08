FROM n8nio/n8n:2.46.6

USER root

# n8n 2.46.6 uses Alpine; install native Python 3 for the native Python Code runner.
RUN apk add --no-cache python3 \
    && python3 --version \
    && chown -R node:node /home/node/.n8n

ENV N8N_NATIVE_PYTHON_RUNNER=true

USER node
