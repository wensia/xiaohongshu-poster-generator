/**
 * Poster Utils - 海报导出工具库
 *
 * 功能：将 HTML 海报导出为高清 PNG 图片
 * 技术：DOM → Canvas → PNG（无需 Playwright）
 *
 * 使用方式：
 * 1. 在 HTML 中引入此文件
 * 2. 调用 window.PosterUtils.exportPoster() 或 downloadPosters()
 */

(function() {
    'use strict';

    // 默认配置
    const DEFAULT_CONFIG = {
        scale: 2,           // 缩放倍数（2x = 2160x2880）
        format: 'png',      // 输出格式
        quality: 1.0,       // 图片质量（仅对 jpeg 有效）
        selector: '.poster' // 海报容器选择器
    };

    // 海报规格（小红书 3:4 比例）
    const POSTER_SIZE = {
        width: 1080,
        height: 1440
    };

    /**
     * 等待所有图片和字体加载完成
     */
    async function waitForResources() {
        // 等待所有图片加载
        const images = document.querySelectorAll('img');
        const imagePromises = Array.from(images).map(img => {
            if (img.complete) return Promise.resolve();
            return new Promise((resolve, reject) => {
                img.onload = resolve;
                img.onerror = resolve; // 即使失败也继续
            });
        });

        // 等待字体加载
        if (document.fonts && document.fonts.ready) {
            await document.fonts.ready;
        }

        await Promise.all(imagePromises);

        // 额外等待渲染稳定
        await new Promise(resolve => setTimeout(resolve, 100));
    }

    /**
     * HTML 元素 → Canvas
     * 使用 html2canvas 库（需要外部引入）
     */
    async function elementToCanvas(element, scale = 2) {
        if (typeof html2canvas === 'undefined') {
            throw new Error('html2canvas library is required. Please include it: <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>');
        }

        await waitForResources();

        const canvas = await html2canvas(element, {
            scale: scale,
            useCORS: true,
            allowTaint: true,
            backgroundColor: null,
            width: POSTER_SIZE.width,
            height: POSTER_SIZE.height,
            logging: false
        });

        return canvas;
    }

    /**
     * Canvas → Blob
     */
    function canvasToBlob(canvas, format = 'png', quality = 1.0) {
        return new Promise((resolve, reject) => {
            const mimeType = format === 'jpeg' ? 'image/jpeg' : 'image/png';
            canvas.toBlob(
                blob => blob ? resolve(blob) : reject(new Error('Failed to create blob')),
                mimeType,
                quality
            );
        });
    }

    /**
     * 下载单个文件
     */
    function downloadBlob(blob, filename) {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    /**
     * 导出单张海报
     *
     * @param {Object} options - 配置选项
     * @param {HTMLElement} options.element - 要导出的元素（默认使用 .poster）
     * @param {string} options.filename - 输出文件名
     * @param {number} options.scale - 缩放倍数
     * @param {string} options.format - 输出格式（png/jpeg）
     * @returns {Promise<Blob>} - 图片 Blob
     */
    async function exportPoster(options = {}) {
        const config = { ...DEFAULT_CONFIG, ...options };
        const element = config.element || document.querySelector(config.selector);

        if (!element) {
            throw new Error(`Element not found: ${config.selector}`);
        }

        const canvas = await elementToCanvas(element, config.scale);
        const blob = await canvasToBlob(canvas, config.format, config.quality);

        if (config.filename) {
            downloadBlob(blob, config.filename);
        }

        return blob;
    }

    /**
     * 批量导出海报并打包为 ZIP
     *
     * @param {Array} posters - 海报配置数组 [{id, name, element?}, ...]
     * @param {string} zipFilename - ZIP 文件名
     * @param {Object} callbacks - 回调函数 {onStart, onProgress, onEnd, onError}
     */
    async function downloadPosters(posters, zipFilename, callbacks = {}) {
        const { onStart, onProgress, onEnd, onError } = callbacks;

        // 检查依赖
        if (typeof JSZip === 'undefined') {
            const error = new Error('JSZip library is required. Please include it: <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>');
            if (onError) onError(error);
            throw error;
        }

        if (typeof saveAs === 'undefined' && typeof FileSaver === 'undefined') {
            const error = new Error('FileSaver library is required. Please include it: <script src="https://cdnjs.cloudflare.com/ajax/libs/FileSaver.js/2.0.5/FileSaver.min.js"></script>');
            if (onError) onError(error);
            throw error;
        }

        try {
            if (onStart) onStart();

            const zip = new JSZip();
            let processed = 0;

            for (const poster of posters) {
                const element = poster.element || document.getElementById(poster.id);

                if (!element) {
                    console.warn(`Poster element not found: ${poster.id}`);
                    continue;
                }

                const blob = await exportPoster({
                    element: element,
                    scale: poster.scale || DEFAULT_CONFIG.scale,
                    format: poster.format || DEFAULT_CONFIG.format
                });

                const filename = `${poster.name || poster.id}.png`;
                zip.file(filename, blob);

                processed++;
                if (onProgress) onProgress(processed, posters.length);
            }

            const content = await zip.generateAsync({ type: 'blob' });

            // 使用 FileSaver 或 saveAs
            const save = typeof saveAs !== 'undefined' ? saveAs : FileSaver.saveAs;
            save(content, zipFilename);

            if (onEnd) onEnd();

        } catch (error) {
            console.error('Export failed:', error);
            if (onError) onError(error);
            throw error;
        }
    }

    /**
     * 创建导出按钮并添加到页面
     *
     * @param {Object} options - 按钮配置
     */
    function createExportButton(options = {}) {
        const {
            text = '导出图片',
            loadingText = '导出中...',
            position = 'bottom-right',
            className = '',
            onClick = null
        } = options;

        const button = document.createElement('button');
        button.textContent = text;
        button.className = `poster-export-btn ${className}`;

        // 默认样式
        const style = document.createElement('style');
        style.textContent = `
            .poster-export-btn {
                position: fixed;
                ${position.includes('bottom') ? 'bottom: 20px;' : 'top: 20px;'}
                ${position.includes('right') ? 'right: 20px;' : 'left: 20px;'}
                padding: 12px 24px;
                background: #C4653A;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 500;
                cursor: pointer;
                z-index: 9999;
                transition: all 0.3s ease;
                box-shadow: 0 4px 12px rgba(196, 101, 58, 0.3);
            }
            .poster-export-btn:hover {
                background: #A85432;
                transform: translateY(-2px);
                box-shadow: 0 6px 16px rgba(196, 101, 58, 0.4);
            }
            .poster-export-btn:disabled {
                background: #999;
                cursor: not-allowed;
                transform: none;
                box-shadow: none;
            }
        `;
        document.head.appendChild(style);

        button.addEventListener('click', async () => {
            if (button.disabled) return;

            button.disabled = true;
            button.textContent = loadingText;

            try {
                if (onClick) {
                    await onClick();
                } else {
                    // 默认行为：导出当前页面的 .poster 元素
                    const filename = document.title.replace(/[^a-zA-Z0-9\u4e00-\u9fa5]/g, '_') + '.png';
                    await exportPoster({ filename });
                }
            } catch (error) {
                alert('导出失败: ' + error.message);
            } finally {
                button.disabled = false;
                button.textContent = text;
            }
        });

        document.body.appendChild(button);
        return button;
    }

    // 暴露到全局
    window.PosterUtils = {
        exportPoster,
        downloadPosters,
        createExportButton,
        elementToCanvas,
        canvasToBlob,
        downloadBlob,
        waitForResources,
        POSTER_SIZE,
        DEFAULT_CONFIG
    };

    // 兼容 CommonJS
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = window.PosterUtils;
    }

})();
