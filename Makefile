USER_NAME ?= youcefamar
USER_EMAIL ?= youcefamar127@gmail.com

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:	
	black *.py 

train:
	python train.py

eval:
	echo "## Model Metrics" > report.md
	cat ./Results/metrics.txt >> report.md
	
	echo '\n## Confusion Matrix Plot' >> report.md
	echo '![Confusion Matrix](./Results/model_results.png)' >> report.md
	
	cml comment create report.md
		
update-branch:
	git config --global user.name "$(USER_NAME)"
	git config --global user.email "$(USER_EMAIL)"
	git add -A
	git diff-index --quiet HEAD || git commit -m "Update with new results"
	git push --force origin HEAD:update

hf-login: 
	pip install -U huggingface_hub
	git fetch origin update:update || true
	git checkout update || true
	@TOKEN=$${HF_TOKEN:-$(HF)}; \
	if [ -z "$$TOKEN" ]; then \
		echo "********************************************************************************"; \
		echo "ERROR: Hugging Face token secret 'HF' is missing or empty!"; \
		echo "Please add your Hugging Face WRITE token under GitHub Settings -> Secrets and variables -> Actions -> Repository secret named 'HF'."; \
		echo "********************************************************************************"; \
		exit 1; \
	else \
		hf auth login --token "$$TOKEN" ; \
	fi

push-hub: 
	hf upload youcefamar/drug-app ./App . --repo-type=space --commit-message="Sync App files"
	hf upload youcefamar/drug-app ./Model /Model --repo-type=space --commit-message="Sync Model"
	hf upload youcefamar/drug-app ./Results /Results --repo-type=space --commit-message="Sync Model"

deploy: hf-login push-hub

all: install format train eval update-branch deploy