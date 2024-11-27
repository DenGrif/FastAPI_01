from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Эта строчка нужна, чтобы мы могли подключиться к базе данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
# Эта строчка отключает сигнализацию об изменении объектов внутри базы данных
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Создание объекта, через который мы будем работать с базой данных
db = SQLAlchemy(app)

class User(db.Model):
    # В скобках указываем модель, чтобы в дальнейшем создать именно базу данных
    id = db.Column(db.Integer, primary_key=True)
    # В скобках описываем поля таблицы
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self): # Этот метод определяет, как объект модели будет выглядеть в виде строки
        return f'<User {self.username}>'

with app.app_context(): # Функция создаёт контекст приложения, который нужен для работы с базой данных
    db.create_all() # Создание всей таблицы, которые определены в классе User

# Получаем записи из таблицы
@app.route('/add_user') # С помощью декоратора создаём маршрут, который будет вызывать функцию
def add_user(): # Функция будет создавать объект класса User
    new_user = User(username='new_username')
    db.session.add(new_user) # Добавляем в сессию
    db.session.commit() #  Сохраняем изменения в базу данных
    return 'User added' # Вывод сообщения о том, что юзер добавлен в базу данных

@app.route('/users')
def get_users():
    users = User.query.all() # Получаем всех юзеров из базы данных и сохраняем в переменную users
    return str(users)
if __name__ == '__main__':
    app.run(debug=True)