#!/bin/bash

python3 -m celery -A core beat -l info
