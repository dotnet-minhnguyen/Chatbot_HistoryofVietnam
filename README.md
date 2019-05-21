## Chatbot - Learning History of Vietnam

Usage :

**Consonle**

```
    $ python input.py
```
**Local**

- Download [ngrok](https://ngrok.com/download)

- Install virtualenv via pip:
```
    $ pip install virtualenv
```
- Edit file app.py:
```
    if __name__ == '__main__':
      app.run(debug = True, port = 5000)
```

- Run
```
    $ virtualenv myvenv
```
```
    $ myvenv\Scripts\activate
```
```
    $ pip install flask requests pymessenger
```
```
    $ ngrok.exe http 5000
```
```
    $ python app.py
```

**Deloy with Heroku sever**

- Install [Heroku](https://devcenter.heroku.com/articles/heroku-cli), or :
```
    $ npm install -g heroku
```
```
    $ heroku login
```
```
    $ heroku create
    $ cd your-project
    $ git init
    $ heroku git:remote -a name_herokuapp
```
```
    $ git add .
    $ git commit -am "something like this"
    $ git push heroku master
```



Training data :

### 1. Training Characters

```
    $ python handleCharacters.py
```

### 2. Training Conversation
```
    $ python handleCommunication.py
```
### 3. Training Info-Characters
```
    $ python handleInfoCharacters.py
```
### 4. Training Type-Question
```
    $ python handlleTypeQuestions.py
```
