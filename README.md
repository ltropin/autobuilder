- Dart: v2.10.0 (beta)
- Flutter: v1.22.0 (beta)
- Python 3.8.5

### Automative building

1. Install pipenv
```bash
sudo pip install pipenv
```
> If you don't have ***pip*** run this command:
```bash
sudo easy_install pip
```
> Note! It's pip working with ***python 2***

2. Creating VENV for current project. Run this command:
```bash
pipenv shell --python=3.8
```
> Note! If you already created venv then you should use this command:
```bash
pipenv shell
```

3. Installing requirements
```bash
pip install -r requirements.txt
```

4. Configure settings in ***automated_building/config.py***.

5. Run script:
```bash
python build.py
```

### Features
- [ ] For android
