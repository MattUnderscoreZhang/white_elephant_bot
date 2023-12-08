#!/usr/bin/env make

default:
	@echo "Please specify a target to make."

serve:
	@echo "Serving with Hypercorn..."
	hypercorn main:app --reload
