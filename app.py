HOME_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Wallet Dashboard</title>

<style>
body{
    margin:0;
    font-family: 'Segoe UI', sans-serif;
    background: radial-gradient(circle at top, #0f172a, #020617);
    color:white;
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
}

/* خلفية متحركة خفيفة */
body::before{
    content:"";
    position:absolute;
    width:100%;
    height:100%;
    background: linear-gradient(45deg, #1e293b, #0f172a, #1e3a8a);
    opacity:0.4;
    filter: blur(60px);
    z-index:-1;
}

.card{
    width:380px;
    padding:25px;
    border-radius:20px;
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    box-shadow: 0 0 30px rgba(0,0,0,0.6);
    border: 1px solid rgba(255,255,255,0.1);
    text-align:center;
}

h2{
    color:#38bdf8;
    margin-bottom:5px;
}

.balance{
    font-size:24px;
    color:#22c55e;
    margin:15px 0;
}

input{
    width:90%;
    padding:12px;
    margin-top:10px;
    border:none;
    border-radius:10px;
    outline:none;
    font-size:15px;
}

.btn{
    width:45%;
    padding:12px;
    margin-top:10px;
    border:none;
    border-radius:10px;
    font-weight:bold;
    cursor:pointer;
    transition:0.3s;
}

.deposit{
    background:#22c55e;
    color:white;
}

.withdraw{
    background:#ef4444;
    color:white;
}

.btn:hover{
    transform: scale(1.05);
}

a{
    display:block;
    margin-top:15px;
    color:#facc15;
    text-decoration:none;
}

.badge{
    font-size:12px;
    opacity:0.7;
}
</style>
</head>

<body>

<div class="card">

    <div class="badge">💳 Secure Wallet System</div>

    <h2>مرحباً {{ user }}</h2>

    <div class="balance">
        💰 USD {{ balance }}
    </div>

    <form method="POST" action="/update_balance">
        <input name="amount" type="number" step="0.01" placeholder="أدخل المبلغ" required>

        <div>
            <button class="btn deposit" name="action" value="deposit">إيداع</button>
            <button class="btn withdraw" name="action" value="withdraw">سحب</button>
        </div>
    </form>

    <a href="/logout">Logout</a>

</div>

</body>
</html>
"""
