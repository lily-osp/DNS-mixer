// DNS-Mixer Documentation JavaScript
// Interactive elements and dynamic content

class DNSMixerDocs {
    constructor() {
        this.init();
    }

    init() {
        this.setupSmoothScrolling();
        this.setupCodeCopyButtons();
        this.setupProgressAnimations();
        this.setupInteractiveDemos();
        this.setupMobileMenu();
        this.setupLazyLoading();
        this.setupScrollEffects();
    }

    // Smooth scrolling for anchor links
    setupSmoothScrolling() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    // Copy code blocks to clipboard
    setupCodeCopyButtons() {
        // Add copy buttons to all code blocks
        document.querySelectorAll('pre, .code-block').forEach(block => {
            if (!block.querySelector('.copy-btn')) {
                const copyBtn = document.createElement('button');
                copyBtn.className = 'copy-btn';
                copyBtn.innerHTML = '📋 Copy';
                copyBtn.title = 'Copy to clipboard';

                copyBtn.addEventListener('click', () => {
                    const text = block.textContent || block.innerText;
                    navigator.clipboard.writeText(text).then(() => {
                        copyBtn.innerHTML = '✅ Copied!';
                        copyBtn.classList.add('success');

                        setTimeout(() => {
                            copyBtn.innerHTML = '📋 Copy';
                            copyBtn.classList.remove('success');
                        }, 2000);
                    }).catch(err => {
                        console.error('Failed to copy: ', err);
                        copyBtn.innerHTML = '❌ Failed';
                        setTimeout(() => {
                            copyBtn.innerHTML = '📋 Copy';
                        }, 2000);
                    });
                });

                // Position the button
                block.style.position = 'relative';
                copyBtn.style.cssText = `
                    position: absolute;
                    top: 8px;
                    right: 8px;
                    padding: 4px 8px;
                    background: rgba(0,0,0,0.7);
                    color: white;
                    border: none;
                    border-radius: 4px;
                    font-size: 12px;
                    cursor: pointer;
                    opacity: 0;
                    transition: opacity 0.3s;
                `;

                block.appendChild(copyBtn);

                // Show/hide copy button on hover
                block.addEventListener('mouseenter', () => {
                    copyBtn.style.opacity = '1';
                });
                block.addEventListener('mouseleave', () => {
                    copyBtn.style.opacity = '0';
                });
            }
        });
    }

    // Animated progress bars for demonstrations
    setupProgressAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const progressBar = entry.target.querySelector('.progress-fill');
                    if (progressBar) {
                        // Simulate DNS resolution progress
                        this.animateProgress(progressBar, 0, 100, 2000);
                    }
                }
            });
        }, observerOptions);

        // Observe all progress bars
        document.querySelectorAll('.progress-bar').forEach(bar => {
            observer.observe(bar);
        });
    }

    animateProgress(element, start, end, duration) {
        const startTime = performance.now();
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const currentValue = start + (end - start) * this.easeOutCubic(progress);

            element.style.width = currentValue + '%';

            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        requestAnimationFrame(animate);
    }

    easeOutCubic(t) {
        return 1 - Math.pow(1 - t, 3);
    }

    // Interactive DNS resolution demo
    setupInteractiveDemos() {
        // DNS Resolution Simulator
        const dnsDemo = document.getElementById('dns-demo');
        if (dnsDemo) {
            const startBtn = dnsDemo.querySelector('.start-demo');
            const statusDiv = dnsDemo.querySelector('.demo-status');
            const progressBar = dnsDemo.querySelector('.progress-bar .progress-fill');

            if (startBtn && statusDiv && progressBar) {
                startBtn.addEventListener('click', () => {
                    this.runDNSResolutionDemo(statusDiv, progressBar, startBtn);
                });
            }
        }

        // OLED Display Simulator
        const oledDemo = document.getElementById('oled-demo');
        if (oledDemo) {
            const startBtn = oledDemo.querySelector('.start-demo');
            const displayDiv = oledDemo.querySelector('.oled-display');

            if (startBtn && displayDiv) {
                startBtn.addEventListener('click', () => {
                    this.runOLEDDemo(displayDiv, startBtn);
                });
            }
        }
    }

    async runDNSResolutionDemo(statusDiv, progressBar, startBtn) {
        const providers = [
            'Quad9 (9.9.9.9)',
            'Cloudflare (1.1.1.1)',
            'Google (8.8.8.8)',
            'AdGuard (94.140.14.14)'
        ];

        startBtn.disabled = true;
        startBtn.textContent = 'Testing...';

        statusDiv.innerHTML = '<div class="fade-in">Starting DNS resolution test...</div>';

        for (let i = 0; i < providers.length; i++) {
            const provider = providers[i];
            const delay = 800 + Math.random() * 400; // 800-1200ms

            statusDiv.innerHTML = `
                <div class="fade-in">
                    <strong>Testing ${provider}</strong><br>
                    <span class="text-secondary">Attempting DNS resolution...</span>
                </div>
            `;

            await this.sleep(delay);

            // Simulate occasional failure for realism
            const success = Math.random() > 0.2 || i === providers.length - 1;

            if (success) {
                statusDiv.innerHTML = `
                    <div class="fade-in">
                        <span class="badge badge-success">SUCCESS</span>
                        <strong>${provider}</strong><br>
                        <span class="text-secondary">DNS resolution successful!</span>
                    </div>
                `;
                this.animateProgress(progressBar, 0, 100, 500);
                break;
            } else {
                statusDiv.innerHTML = `
                    <div class="fade-in">
                        <span class="badge badge-warning">FAILED</span>
                        <strong>${provider}</strong><br>
                        <span class="text-secondary">Connection timeout, trying next provider...</span>
                    </div>
                `;
                await this.sleep(300);
            }
        }

        setTimeout(() => {
            startBtn.disabled = false;
            startBtn.textContent = 'Run Demo';
            statusDiv.innerHTML = '<div class="text-secondary">Click "Run Demo" to simulate DNS resolution</div>';
            progressBar.style.width = '0%';
        }, 2000);
    }

    async runOLEDDemo(displayDiv, startBtn) {
        const messages = [
            { text: 'DNS-mixer Ready', duration: 1500 },
            { text: 'WiFi Connected!', duration: 1200 },
            { text: 'Processing DNS...', duration: 1000 },
            { text: 'IP:192.168.1.100', duration: 1400 },
            { text: 'Total: 1,247', duration: 1100 },
            { text: 'Success: 1,245', duration: 1300 },
            { text: 'Failed: 2', duration: 1200 }
        ];

        startBtn.disabled = true;
        startBtn.textContent = 'Running...';

        displayDiv.style.backgroundColor = '#2d3748';
        displayDiv.style.color = '#e2e8f0';
        displayDiv.style.fontFamily = 'monospace';
        displayDiv.style.padding = '1rem';
        displayDiv.style.borderRadius = '4px';
        displayDiv.style.minHeight = '80px';
        displayDiv.style.display = 'flex';
        displayDiv.style.alignItems = 'center';
        displayDiv.style.justifyContent = 'center';
        displayDiv.style.fontSize = '14px';
        displayDiv.style.fontWeight = 'bold';

        for (const message of messages) {
            displayDiv.textContent = message.text;
            displayDiv.classList.add('fade-in');
            await this.sleep(message.duration);
            displayDiv.classList.remove('fade-in');
        }

        displayDiv.textContent = 'DNS-mixer Ready';
        startBtn.disabled = false;
        startBtn.textContent = 'Run Demo';
    }

    // Mobile menu toggle
    setupMobileMenu() {
        // Create mobile menu button if it doesn't exist
        const header = document.querySelector('.header .container');
        const nav = document.querySelector('.nav-links');

        if (header && nav && window.innerWidth <= 768) {
            const mobileBtn = document.createElement('button');
            mobileBtn.className = 'mobile-menu-btn';
            mobileBtn.innerHTML = '☰';
            mobileBtn.style.cssText = `
                display: none;
                background: none;
                border: none;
                color: white;
                font-size: 1.5rem;
                cursor: pointer;
                padding: 0.5rem;
            `;

            // Show mobile button on small screens
            if (window.innerWidth <= 768) {
                mobileBtn.style.display = 'block';
                nav.style.display = 'none';

                mobileBtn.addEventListener('click', () => {
                    nav.style.display = nav.style.display === 'none' ? 'flex' : 'none';
                });
            }

            header.appendChild(mobileBtn);

            // Handle window resize
            window.addEventListener('resize', () => {
                if (window.innerWidth > 768) {
                    mobileBtn.style.display = 'none';
                    nav.style.display = 'flex';
                } else {
                    mobileBtn.style.display = 'block';
                    nav.style.display = 'none';
                }
            });
        }
    }

    // Lazy loading for images
    setupLazyLoading() {
        const images = document.querySelectorAll('img[data-src]');

        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        images.forEach(img => imageObserver.observe(img));
    }

    // Scroll effects and animations
    setupScrollEffects() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                }
            });
        }, observerOptions);

        // Observe elements that should animate in
        document.querySelectorAll('.card, .feature-item, .table').forEach(el => {
            observer.observe(el);
        });
    }

    // Utility function for delays
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    // Error handling
    handleError(error, context) {
        console.error(`Error in ${context}:`, error);
        // Could send error reports or show user-friendly messages
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new DNSMixerDocs();
});

// Handle browser back/forward buttons
window.addEventListener('popstate', (event) => {
    // Handle navigation state changes if needed
});

// Performance monitoring
if ('performance' in window && 'timing' in performance) {
    window.addEventListener('load', () => {
        const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
        console.log(`Page loaded in ${loadTime}ms`);
    });
}

// Service worker for offline functionality (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // navigator.serviceWorker.register('/sw.js');
    });
}
