document.addEventListener('DOMContentLoaded', () => {
    // Current Path Highlighting
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // Form submission animation
    const form = document.getElementById('analyze-form');
    if (form) {
        form.addEventListener('submit', (e) => {
            const btn = document.getElementById('analyze-btn');
            const btnText = btn.querySelector('.btn-text');
            const btnIcon = btn.querySelector('.btn-icon');
            const spinner = btn.querySelector('.spinner');
            const textarea = document.getElementById('statement-input');
            
            if (textarea.value.trim() === '') {
                e.preventDefault();
                textarea.style.borderColor = 'var(--fake-color)';
                setTimeout(() => {
                    textarea.style.borderColor = '';
                }, 2000);
                return;
            }
            
            btn.style.pointerEvents = 'none';
            btn.style.opacity = '0.9';
            btnText.textContent = 'Analyzing...';
            btnIcon.style.display = 'none';
            spinner.style.display = 'block';
        });
    }

    // Auto-resize textarea
    const textarea = document.getElementById('statement-input');
    if (textarea) {
        textarea.addEventListener('input', function() {
            this.style.height = '140px';
            if (this.scrollHeight > 140) {
                this.style.height = (this.scrollHeight) + 'px';
            }
        });
    }

    // Initialize initial animation widths (if any progress bars)
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const targetWidth = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.width = targetWidth;
        }, 100);
    });
});
