#!/bin/bash
gcloud functions deploy alertas-findings-scc \
  --gen2 \
  --runtime=python312 \
  --region=us-east4 \
  --project=mgmt-movti-interno \
  --trigger-topic=topic-findings-scc \
  --source=./api  \
  --entry-point=receber_mensagem \
  --service-account=sa-apis-alertas-movti@mgmt-movti-interno.iam.gserviceaccount.com