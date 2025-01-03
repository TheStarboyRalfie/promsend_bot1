import os

for file in os.listdir('/promsend_bot/executors/'):
    if file.endswith('_executor.py'):
        os.system(f'python /promsend_bot/executors/{file}')
# os.path.abspath(file)
