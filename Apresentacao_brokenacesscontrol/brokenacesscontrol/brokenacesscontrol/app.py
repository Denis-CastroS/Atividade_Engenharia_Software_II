from flask import Flask, session, redirect, url_for, request

app = Flask(__name__)
app.secret_key = "segredo_super_confidencial"  # só para demo!


# Credenciais de demo:
# admin -> senha 12345  (role "admin")
# julho -> senha 3535   (role "user")
ADMIN_USER = "admin"
ADMIN_PASS = "12345"
JULIO_PASS = "3535"


# =====================
# Rota de Login (com senha)
# =====================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = (request.form.get("password") or "").strip()

        # simples checagem de credenciais só para demo
        if username == ADMIN_USER and password == ADMIN_PASS:
            session["username"] = username
            session["role"] = "admin"
            return redirect(url_for("user", username=username))
        elif username.lower() == "julho" and password == JULIO_PASS:
            session["username"] = "julho"
            session["role"] = "user"
            return redirect(url_for("user", username="julho"))
        else:
            # credenciais inválidas
            return """
                <h3>Credenciais inválidas.</h3>
                <p><a href="/login">Voltar ao login</a></p>
            """, 401

    # GET: mostra o formulário com campo senha
    return """
        <h2>Login</h2>
        <form method="post">
            Usuário: <input type="text" name="username" ><br><br>
            Senha: <input type="password" name="password" ><br><br>
            <input type="submit" value="Entrar">
        </form>
        <p>Credenciais de demonstração — admin/12345 ; julho/3535</p>
        <p>Para demonstrar a falha: mesmo logado como <b>julho</b>, abra <code>/login/admin</code> na barra de endereço e verá o painel ADMIN (vulnerabilidade).</p>
    """


@app.route("/user/<username>")
def user(username):
    
    if "username" not in session:
        return redirect(url_for("login"))

    current = session.get("username", "desconhecido")
    role = session.get("role", "unknown")
    return f"""
        <h2>Olá, {username}!</h2>
        <p>Você está logado como: <b>{current}</b> (role = {role})</p>
        <ul>
            <li><a href="/login/admin">Ir para ADMIN</a></li>
            <li><a href="/logout">Logout</a></li>
        </ul>
        
    """


# =====================
# admin: aqui rola o idor
# =====================
@app.route("/login/admin")
def admin_vulnerable():
    """
    PONTO CRÍTICO: rota deliberadamente vulnerável para a demo.
    Não verifica session['role'] nem session['username'] — qualquer um que acessar
    esta URL verá o painel de admin.
    """
    return """
        
        <h3>Conteúdo exclusivo do admin (simulado):</h3>
        <ul>
            <li>📊 Relatórios financeiros sensíveis</li>
            <li>👥 Lista completa de usuários cadastrados</li>
            <li>🔑 Chaves e tokens (simulados)</li>
            <li>⚙️ Configurações críticas do sistema</li>
        </ul>
        
        <p><a href="/logout">Logout</a></p>
    """


# =====================
# Logout
# =====================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# =====================
# Rodar o App
# =====================
if __name__ == "__main__":
    app.run(debug=True, port=5001)
