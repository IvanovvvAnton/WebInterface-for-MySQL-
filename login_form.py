@app.route('/auth', methods=['POST'])
def auth():
    username = request.form['username']
    password = request.form['password']

    if username != USERNAME and password != PASSWORD:
        log_to_login("Авторизация", f"Неудачная попытка входа: {username} | Неверный логин и пароль")
        return render_template('login.html', error="Неверные данные!")

    if username != USERNAME:
        log_to_login("Авторизация", f"Неудачная попытка входа: {username} | Неверный логин")
        return render_template('login.html', error="Неверные данные!")

    if password != PASSWORD:
        log_to_login("Авторизация", f"Неудачная попытка входа: {username} | Неверный пароль")
        return render_template('login.html', error="Неверные данные!")

    session['username'] = username
    log_to_login("Авторизация", f"Успешный вход в систему: {username}")
    return redirect(url_for('admin_dashboard'))
