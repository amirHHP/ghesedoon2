---
title: "پرداخت با موفقیت انجام شد"
description: "اشتراک نسخه انگلیسی قصه دون با موفقیت برای شما فعال شد."
date: 2026-09-22
draft: false
---

<div class="payment-result-container success" dir="rtl">
<div class="result-icon-wrapper success-icon">
<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
<polyline points="22 4 12 14.01 9 11.01"></polyline>
</svg>
</div>

<h1 class="result-title">پرداخت با موفقیت انجام شد!</h1>
<p class="result-subtitle">از همراهی شما سپاسگزاریم. دسترسی شما به نسخه انگلیسی و صوت قصه‌ها فعال شد.</p>

<div class="result-box">
<div class="result-status-badge">✨ وضعیت: اشتراک فعال</div>
<p class="result-info">
دسترسی نامحدود به <strong>بیش از ۲۰۰ داستان صوتی و متنی انگلیسی</strong> روی این مرورگر به صورت خودکار فعال شد. اکنون می‌توانید از داستان‌ها برای یادگیری و تقویت زبان انگلیسی لذت ببرید.
</p>
<div class="result-sync-note">
<span class="sync-icon">💡</span>
<span><strong>استفاده در دستگاه‌های دیگر:</strong> برای باز کردن قصه‌ها در گوشی یا سیستم‌های دیگر، کافیست در صفحه داستان‌های انگلیسی روی «فعال‌سازی با کد دسترسی» کلیک کرده و شماره پیگیری یا شماره تماس پرداخت خود را وارد کنید.</span>
</div>
</div>

<div class="result-actions">
<a href="/en/posts/" class="btn-result-primary">
<span>ورود به آرشیو داستان‌های انگلیسی</span>
<span class="btn-arrow">←</span>
</a>
<a href="/" class="btn-result-secondary">
<span>بازگشت به صفحه اصلی قصه دون</span>
</a>
</div>
</div>

<script>
(function() {
    try {
        localStorage.setItem('ghesedoon_en_access', 'granted');
        var params = new URLSearchParams(window.location.search);
        var ref = params.get('track_id') || params.get('Authority') || params.get('id') || params.get('ref') || 'GHESEDOON-VIP';
        localStorage.setItem('ghesedoon_license_code', ref);
    } catch (e) {
        console.error('Storage access error', e);
    }
})();
</script>
