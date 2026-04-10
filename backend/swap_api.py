import os

directory = r'C:\Users\HP\projects\Fullstack project\frontend\src'
count = 0
for root, _, files in os.walk(directory):
    for file in files:
        if file.endswith('.jsx'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            if 'http://localhost:8000' in content:
                new_content = content.replace('http://localhost:8000', 'https://biometric-hostel-system.onrender.com')
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                count += 1
print(f'Swapped in {count} files.')
