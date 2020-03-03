.PHONY: acquisition

preprocess:
	python3.6 preprocessImage.py -in ${input} -out ${output}