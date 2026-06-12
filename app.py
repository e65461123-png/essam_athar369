HTML_CONTENT = """
<!DOCTYPE html>
<html lang="ar">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Viral AI</title>

<style>
body{
    margin:0;
    font-family:Arial,sans-serif;
    background:linear-gradient(135deg,#0f172a,#1e293b,#2563eb);
    min-height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
}

.card{
    width:90%;
    max-width:500px;
    background:white;
    padding:30px;
    border-radius:20px;
    box-shadow:0 10px 30px rgba(0,0,0,.3);
    text-align:center;
}

h1{
    color:#2563eb;
}

input{
    width:100%;
    padding:15px;
    margin-top:15px;
    border:1px solid #ddd;
    border-radius:10px;
    font-size:16px;
}

button{
    width:100%;
    padding:15px;
    margin-top:15px;
    border:none;
    border-radius:10px;
    background:#2563eb;
    color:white;
    font-size:18px;
    cursor:pointer;
}

button:hover{
    background:#1d4ed8;
}

#result{
    margin-top:20px;
    text-align:right;
    direction:rtl;
    padding:15px;
    background:#f3f4f6;
    border-radius:10px;
}
</style>
</head>

<body>

<div class="card">
<h1>🚀 Viral AI</h1>

<p>أدخل رابط الفيديو لتحليل أفضل مقطع</p>

<input type="text" id="url" placeholder="ضع رابط الفيديو هنا">

<button onclick="analyze()">تحليل الفيديو</button>

<div id="result"></div>
</div>

<script>
async function analyze(){

let url=document.getElementById("url").value;

document.getElementById("result").innerHTML=
"⏳ جاري التحليل...";

try{

const response=await fetch("/api/analyze",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
url:url
})
});

const data=await response.json();

document.getElementById("result").innerHTML=
`
<h3>✅ تم التحليل</h3>
<p><b>الفترة:</b> ${data.time_frame}</p>
<p><b>العنوان:</b> ${data.title}</p>
<p><b>الهاشتاجات:</b> ${data.tags}</p>
`;

}catch(e){

document.getElementById("result").innerHTML=
"❌ حدث خطأ أثناء التحليل";

}
}
</script>

</body>
</html>
"""
