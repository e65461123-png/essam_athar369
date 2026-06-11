from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# كود يمثل نموذج البيانات القادمة من الواجهة
class VideoRequest(BaseModel):
    url: str

# 1. إرجاع صفحة الـ HTML عند فتح الرابط الرئيسي للموقع
@app.get("/", response_class=HTMLResponse)
async def get_home():
    # هنا نضع كود الـ HTML المطور الخاص بك كاملاً ليقرأه السيرفر مباشرة
    html_content = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Viral AI - صانع المحتوى الفيروسي</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght=400;700&display=swap" rel="stylesheet">
        <style> body { font-family: 'Tajawal', sans-serif; } </style>
    </head>
    <body class="bg-slate-900 text-white min-h-screen flex flex-col justify-between">
        <header class="p-4 border-b border-slate-800 flex justify-between items-center">
            <div class="text-2xl font-bold text-indigo-500 tracking-wider">Viral <span class="text-white">AI</span></div>
            <span class="bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 text-xs px-2.5 py-1 rounded-full font-bold">الإصدار 1.0</span>
        </header>

        <main class="max-w-4xl mx-auto px-4 py-10 text-center flex-grow flex flex-col justify-center items-center">
            <h1 class="text-3xl md:text-5xl font-extrabold mb-4 bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent leading-tight">
                حوّل فيديوهاتك الطويلة إلى مقاطع قصيرة فيروسية!
            </h1>
            <p class="text-slate-400 text-sm md:text-base mb-8 max-w-xl leading-relaxed">
                ضع رابط الفيديو، ودع الذكاء الاصطناعي يتولى استخراج أفضل اللقطات، كتابة النصوص الجذابة، وإعداد المقاطع لـ TikTok و Shorts فوراً.
            </p>

            <div class="w-full max-w-xl bg-slate-800/50 p-2 rounded-2xl border border-slate-700 shadow-2xl flex flex-col gap-2">
                <input type="url" id="videoUrl" placeholder="أدخل رابط فيديو اليوتيوب هنا..." class="bg-transparent text-white placeholder-slate-500 px-4 py-3.5 rounded-xl flex-grow focus:outline-none text-left text-sm" dir="ltr">
                <button onclick="startProcessing()" class="bg-indigo-600 hover:bg-indigo-500 active:scale-95 transition-all text-white font-bold px-6 py-3.5 rounded-xl text-sm">اصنع السحر ⚡</button>
            </div>

            <div id="loadingStatus" class="hidden mt-6 flex items-center gap-3 text-indigo-400 text-sm bg-slate-800/30 px-4 py-2 rounded-full border border-indigo-500/10">
                <svg class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                <span>الذكاء الاصطناعي يستخرج اللقطات الفيروسية...</span>
            </div>

            <div id="resultArea" class="hidden w-full max-w-xl mt-8 bg-slate-800/80 border border-slate-700 rounded-2xl p-5 text-right shadow-2xl">
                <h3 class="text-lg font-bold text-emerald-400 mb-4">✨ تم تحليل الفيديو بنجاح!</h3>
                <div class="bg-slate-900/90 p-3.5 rounded-xl border border-slate-700/50 mb-3.5">
                    <p class="text-[11px] text-indigo-400 font-bold mb-1">توقيت اللقطة الأكثر حماساً:</p>
                    <p id="suggestedTime" class="text-base font-mono text-white font-bold">02:15 - 03:00</p>
                </div>
                <div class="bg-slate-900/90 p-3.5 rounded-xl border border-slate-700/50 mb-3.5">
                    <p class="text-[11px] text-purple-400 font-bold mb-1">العنوان المقترح:</p>
                    <p id="suggestedTitle" class="text-sm text-white font-bold leading-relaxed"></p>
                </div>
                <div class="bg-slate-900/90 p-3.5 rounded-xl border border-slate-700/50">
                    <p class="text-[11px] text-pink-400 font-bold mb-1">النص والهاشتاغات (الوصف):</p>
                    <p id="suggestedTags" class="text-xs text-slate-300 leading-relaxed whitespace-pre-line"></p>
                </div>
            </div>
        </main>

        <footer class="p-4 border-t border-slate-800 text-center text-xs text-slate-500">&copy; 2026 Viral AI. جميع الحقوق محفوظة لملياردير المستقبل.</footer>

        <script>
            async function startProcessing() {
                const urlInput = document.getElementById('videoUrl').value;
                if (!urlInput) { alert('من فضلك ضع رابط فيديو صحيح أولاً!'); return; }
                document.getElementById('resultArea').classList.add('hidden');
                document.getElementById('loadingStatus').classList.remove('hidden');

                try {
                    const response = await fetch('/api/analyze', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ url: urlInput })
                    });
                    const data = await response.json();
                    if (data.success) {
                        document.getElementById('loadingStatus').classList.add('hidden');
                        const resultArea = document.getElementById('resultArea');
                        resultArea.classList.remove('hidden');
                        document.getElementById('suggestedTime').innerText = data.time_frame;
                        document.getElementById('suggestedTitle').innerText = data.title;
                        document.getElementById('suggestedTags').innerText = data.tags;
                        resultArea.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                } catch (error) {
                    alert('حدث خطأ أثناء الاتصال بالسيرفر!');
                    document.getElementById('loadingStatus').classList.add('hidden');
                }
            }
        </script>
    </body>
    </html>
    """
    return html_content

# 2. استقبال الرابط ومعالجته ديناميكياً كما فعلت أنت
@app.post("/api/analyze")
async def analyze_video(data: VideoRequest):
    video_url = data.url
    if "shorts" in video_url.lower():
        title = "❌ خطأ مالي فادح يدمر ميزانيتك دون أن تشعر!"
        tags = "هذا المقطع القصير يشرح لك الأسباب بالتفصيل.\n\n#مال #استثمار #وعي_مالي #ادخار #Viral"
        time_frame = "00:05 - 00:35"
    else:
        title = "🔥 الاستراتيجية السرية التي حققت ملايين الدولارات في أشهر!"
        tags = "استراتيجية مجربة لتنمية أعمالك بسرعة الصاروخ.\n\n#تجارة_إلكترونية #بزنس #مشاريع #نجاح #Fyp"
        time_frame = "04:20 - 05:10"

    return {
        "success": True,
        "time_frame": time_frame,
        "title": title,
        "tags": tags
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
