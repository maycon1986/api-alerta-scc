#!/bin/bash
gcloud functions deploy alertas-findings-scc \
  --gen2 \
  --runtime=python312 \
  --region=us-east4 \
  --project=<projeto id> \
  --trigger-topic=topic-findings-scc \
  --source=./api  \
  --entry-point=receber_mensagem \
  --service-account=<service account>
