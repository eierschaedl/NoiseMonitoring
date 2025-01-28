import soundata

# Initialize and validate UrbanSound8K dataset
dataset = soundata.initialize('urbansound8k')
#dataset.download()
dataset.validate()

# Select a random clip
example_clip = dataset.choice_clip()

# Print available attributes and methods of the tags object
print(dir(example_clip.tags))