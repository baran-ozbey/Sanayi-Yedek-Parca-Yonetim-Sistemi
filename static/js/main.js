/**
 * main.js — Sanayi Yedek Parça Yönetim Sistemi
 * JavaScript işlevleri: Modal yönetimi, sidebar toggle, yardımcı fonksiyonlar
 */

// ============================================================
// SIDEBAR TOGGLE
// ============================================================
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const main = document.getElementById('mainContent');
    sidebar.classList.toggle('collapsed');
    main.classList.toggle('expanded');
}

// Mobil: overlay tıklanınca sidebar kapat
document.addEventListener('click', function(e) {
    const sidebar = document.getElementById('sidebar');
    const toggle = document.getElementById('menuToggle');
    if (window.innerWidth <= 768 && !sidebar.contains(e.target) && !toggle.contains(e.target)) {
        sidebar.classList.add('collapsed');
    }
});

// ============================================================
// MODAL YÖNETİMİ
// ============================================================
function openModal(title, content) {
    const modal = document.getElementById('modal');
    const overlay = document.getElementById('modalOverlay');
    const modalTitle = document.getElementById('modalTitle');
    const modalBody = document.getElementById('modalBody');

    modalTitle.textContent = title;
    modalBody.innerHTML = '';

    if (typeof content === 'string') {
        modalBody.innerHTML = content;
    } else {
        modalBody.appendChild(content);
    }

    modal.classList.add('active');
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    const modal = document.getElementById('modal');
    const overlay = document.getElementById('modalOverlay');
    modal.classList.remove('active');
    overlay.classList.remove('active');
    document.body.style.overflow = '';
}

// ESC tuşu ile modal kapat
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closeModal();
});

// ============================================================
// YARDIMCI FONKSİYONLAR
// ============================================================

// Sayı formatlama (Türkçe)
function formatNumber(num) {
    return new Intl.NumberFormat('tr-TR').format(num);
}

// Para formatlama
function formatCurrency(num) {
    return new Intl.NumberFormat('tr-TR', { style: 'currency', currency: 'TRY' }).format(num);
}
