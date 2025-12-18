from flask import Flask, session, redirect, url_for, request

app = Flask(__name__)
app.secret_key = "segredo_super_confidencial"  # chave para sessão funcionar


# =====================
# Rota de Login
# =====================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        session["username"] = username
        return redirect(url_for("user"))
    
    # formulário simples direto em HTML
    return """
        <h2>Login</h2>
        <form method="post">
            Usuário: <input type="text" name="username">
            <input type="submit" value="Entrar">
        </form>
    """


# =====================
# Rota do Usuário
# =====================
@app.route("/user")
def user():
    if "username" not in session:
        return redirect(url_for("login"))
    return f"""
        <h2>Olá, {session['username']}!</h2>
        <p><a href='/admin'>Ir para área ADMIN</a></p>
        <p><a href='/logout'>Logout</a></p>
    """


# =====================
# Rota do ADMIN (Erro proposital!)
# =====================
@app.route("/admin")
def admin():
    # ❌ Aqui está o erro: não há verificação se o usuário é realmente admin!
    return """
        <h2>Área ADMIN</h2>
        <p>🔑 Conteúdo super secreto de administrador!</p>
        <p><a href='/user'>Voltar</a></p>
    """


# =====================
# Rota de Logout
# =====================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# =====================
# Rodar o App
# =====================
if __name__ == "__main__":
    app.run(debug=True)
